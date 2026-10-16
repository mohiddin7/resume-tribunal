#!/usr/bin/env python3
"""Turn a recorded example run into examples/<slug>/: run.json for the site's viewer, a transcript and a
README for GitHub, the resumes and inputs, and every prompt and reply the seats saw.

  export.py RUN SLUG --title "Growth analyst applying for a senior pricing analyst job" --fictional
  export.py RUN --check [--real-with-consent]   is the record complete? (the host runs this before finishing)
  export.py --self-test

RUN is the run folder: before.md, job.md and own-words.md (the inputs), and .tribunal/ with events.jsonl
(written by record.py), final.md and changes.json (the host's reasons for each changed line, optional).
Every email must be on a reserved example domain and every phone a 555-01xx number. A fictional candidate
(--fictional) may share no line with a real resume in research/real-resumes/; a real resume whose owner agreed to
publish it (--real-with-consent) must be de-identified first: invented name, example contact details, renamed
projects, consistently shifted dates. Standard library only.
"""
import argparse
import difflib
import json
import pathlib
import re
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills" / "resume-tribunal" / "scripts"))
from seats import labelled_id  # noqa: E402  the skill's own rule: "Req. ID: 1273383451" is not a phone
SEAT_NAMES = {"codex": ("Codex", "OpenAI"), "agy": ("Gemini", "Google"), "claude": ("Fresh Claude", "Anthropic"),
              "chatgpt": ("ChatGPT", "OpenAI"), "gemini": ("Gemini", "Google")}  # the last two: pasted by hand
MANUAL = {"chatgpt", "gemini"}
SOURCES = {"own words", "sign-off", "old resume", "linked page"}
MAX_WAIT = 300  # seconds of a candidate's wait drawn on the timeline
EMAIL_RE = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
SAFE_DOMAIN = re.compile(r"(?:^|\.)(?:example\.(?:com|org|net)|example|test|invalid)$", re.I)
PHONE_RE = re.compile(r"(?<![\w$])\+?(?:\d[\s().-]*){10,}(?!\w)")
SAFE_PHONE = re.compile(r"555[\s.-]*01\d\d")


# ---------- resumes ----------

def strip_md(s):
    return re.sub(r"\*\*|__|`", "", s)


def norm(s):
    s = strip_md(re.sub(r"^\s*(?:[-*•●○▪◦]|#+)\s*", "", s)).lower()
    s = re.sub(r"\s*[|,•·]\s*", " ", s)  # "University, 2014", "University | 2014" and "University • 2014" are one line
    return re.sub(r"\s+", " ", re.sub(r"[.;:]+$", "", s.strip()))


SECTIONS = re.compile(r"(?:(?:professional|work|relevant|teaching|other)\s+)?(?:summary|profile|objective|experience|employment|education|"
                      r"skills|technical skills|certifications?|licen[cs]es?|projects|awards|publications|volunteering|volunteer work|"
                      r"languages|interests|training|courses)", re.I)


def is_heading(s):
    if s.startswith("## ") or SECTIONS.fullmatch(s.strip().rstrip(":")):
        return True
    letters = re.sub(r"[^A-Za-z]", "", s)
    return len(letters) >= 3 and s.upper() == s and len(s) <= 40 and "|" not in s and len(s.split()) <= 5 and not re.search(r"\d", s)


def parse_resume(text):
    """Lines of a resume as {k, tx}: k is name, contact, h2, role, bul or p. Markdown resumes follow make_pdf.py
    (a '### Company' line followed by '**Title** | dates' prints as 'Title | **Company** | dates'); plain-text
    resumes are read by shape: an all-caps line is a heading, a line with ' | ' ending in a year is a role."""
    raw = [l.rstrip() for l in text.splitlines() if l.strip()]
    markdown = bool(raw) and raw[0].startswith("# ")
    out, i = [], 0
    while i < len(raw):
        s = raw[i].strip()
        words = s.split()  # "PROFESSIONAL SUMMARY With 4+ years..." pasted from a PDF: the heading, then its text
        cut = max((k for k in range(1, min(5, len(words))) if " ".join(words[:k]).isupper()
                   and SECTIONS.fullmatch(" ".join(words[:k])) and len(" ".join(words[k:])) > 20), default=0)
        if out and cut:
            out.append({"k": "h2", "tx": " ".join(words[:cut])})
            s = " ".join(words[cut:])
        if not out:
            out.append({"k": "name", "tx": s.lstrip("# ").strip()})
        elif len(out) == 1 and ("|" in s or "@" in s) and not is_heading(s):
            out.append({"k": "contact", "tx": s})
        elif is_heading(s):
            out.append({"k": "h2", "tx": s[3:].strip() if s.startswith("#") else s.strip().rstrip(":")})  # printed in capitals anyway
        elif s.startswith("### "):
            nxt = raw[i + 1].strip() if i + 1 < len(raw) else ""
            if nxt.startswith("**") and " | " in nxt:
                title, dates = nxt.rsplit(" | ", 1)  # alt: the line as written, so changes.json may quote either
                out.append({"k": "role", "tx": f"{strip_md(title)} | **{s[4:]}** | {dates}", "alt": nxt})
                i += 1
            else:
                out.append({"k": "role", "tx": f"**{s[4:]}**"})
        elif re.match(r"[-*•●○▪◦]\s*", s) and not s.startswith("**"):
            out.append({"k": "bul", "tx": re.sub(r"^[-*•●○▪◦]\s*", "", s)})
        elif markdown and s.startswith("**") and " | " in s:
            out.append({"k": "role", "tx": s})  # a second title under the same company
        elif not markdown and " | " in s and re.search(r"(?:19|20)\d\d|present|current", s.split(" | ")[-1], re.I):
            prev = out[-1]
            if prev["k"] == "p" and len(prev["tx"]) < 80 and " | " not in prev["tx"] and not prev["tx"].endswith("."):
                title, dates = s.rsplit(" | ", 1)  # a company line above "Title | dates" prints as one line, as in make_pdf.py
                out[-1] = {"k": "role", "tx": f"{title} | **{prev['tx']}** | {dates}", "alt": s}
            else:
                out.append({"k": "role", "tx": s})
        else:
            out.append({"k": "p", "tx": s})
        i += 1
    return out


def similar(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def find(lines, text):
    """The line matching text exactly (ignoring markdown, bullets, case and end punctuation), or containing it."""
    n = norm(text)
    for l in lines:
        if n in (norm(l["tx"]), norm(l.get("alt", ""))):
            return l
    hits = [l for l in lines if len(n) >= 25 and (n in norm(l["tx"]) or norm(l["tx"]) in n)]
    return hits[0] if len(hits) == 1 else None


def compare(before, after, changes):
    """Give paired lines one id and mark each line kept, rw (reworded), cut or new, with the host's reasons."""
    content = lambda doc: [l for l in doc if l["k"] in ("contact", "role", "bul", "p")]
    b, a = content(before), content(after)
    pairs, problems = [], []
    heads = {norm(l["tx"]) for l in before + after if l["k"] in ("h2", "name")}
    for c in changes:
        if any(norm(c.get(k) or "") in heads for k in ("old", "new") if c.get(k)):
            continue  # a heading or the name: no facts to explain
        lo = find(b, c["old"]) if c.get("old") else None
        ln = find(a, c["new"]) if c.get("new") else None
        if c.get("old") and not lo:
            problems.append(f"changes.json: old line not in the old resume: {c['old'][:70]}")
        if c.get("new") and not ln:
            problems.append(f"changes.json: new line not in the new resume: {c['new'][:70]}")
        if c.get("source") and c["source"] not in SOURCES:
            problems.append(f"changes.json: source is one of {', '.join(sorted(SOURCES))}, not {c['source']!r}")
        for l in (lo, ln):
            if l and c.get("why"):
                l["why"] = c["why"]
        if ln and c.get("source"):
            ln["from"] = c["source"]
        if lo and ln:
            pairs.append((lo, ln))
        elif lo:
            lo["s"] = "cut"
        elif ln:
            ln["s"] = "new"
    taken = {id(x) for p in pairs for x in p} | {id(l) for l in b + a if l.get("s")}
    for l in b:  # identical lines, then close rewrites, best match first
        if id(l) in taken:
            continue
        twin = next((m for m in a if id(m) not in taken and norm(m["tx"]) == norm(l["tx"])), None)
        if twin:
            pairs.append((l, twin)); taken |= {id(l), id(twin)}
    scored = sorted(((similar(l["tx"], m["tx"]), j, k) for j, l in enumerate(b) if id(l) not in taken
                     for k, m in enumerate(a) if id(m) not in taken and m["k"] == l["k"]), reverse=True)
    for r, j, k in scored:
        if r < 0.6 or id(b[j]) in taken or id(a[k]) in taken:
            continue
        pairs.append((b[j], a[k])); taken |= {id(b[j]), id(a[k])}
    for n, (lo, ln) in enumerate(pairs, 1):
        lo["id"] = ln["id"] = f"L{n}"
        if norm(lo["tx"]) != norm(ln["tx"]):
            lo["s"] = ln["s"] = "rw"
    for prefix, doc, mark in (("B", b, "cut"), ("A", a, "new")):
        for n, l in enumerate(doc, 1):
            if "id" not in l:
                l["id"], l["s"] = f"{prefix}{n}", mark
    return problems


# ---------- privacy ----------

HOME_RE = re.compile(r"(?:/home/|/Users/|[A-Za-z]:\\Users\\)[\w.-]+")


def unsafe(text, where):
    """Contact details that could belong to a real person, and paths that name the computer's user."""
    bad = [f"{where}: email {m.group(0)}" for m in EMAIL_RE.finditer(text) if not SAFE_DOMAIN.search(m.group(1))]
    bad += [f"{where}: local path {m.group(0)}" for m in HOME_RE.finditer(text)]
    bad += [f"{where}: phone {m.group(0).strip()}" for m in PHONE_RE.finditer(text)
            if not SAFE_PHONE.search(m.group(0)) and not labelled_id(text[max(0, m.start() - 40):m.start()])]
    return bad


def from_real_resume(text, folder):
    if not folder.is_dir():
        return []
    mine = {norm(l) for l in text.splitlines() if len(l.strip()) >= 40}
    return [f.name for f in sorted(folder.glob("*.md")) if mine & {norm(l) for l in f.read_text(errors="ignore").splitlines()}]


# ---------- the run ----------

def build(run, slug, title, extra_facts=(), candidate=None, real=ROOT / "research" / "real-resumes", note="", consented=False):
    tri = run / ".tribunal"
    events = [json.loads(l) for l in (tri / "events.jsonl").read_text().splitlines() if l.strip()]
    if not events:
        raise SystemExit("events.jsonl is empty")
    before_md, final_md = (run / "before.md").read_text(), (tri / "final.md").read_text()
    if "<<" in final_md:
        raise SystemExit("final.md still holds stand-ins; restore it first")
    problems = [p for name, t in (("before.md", before_md), ("final.md", final_md)) for p in unsafe(t, name)]
    if not EMAIL_RE.search(before_md):
        problems.append("before.md has no email: a fictional candidate carries one on an example domain")
    copied = [] if consented else from_real_resume(before_md, real)
    if copied:
        problems.append(f"before.md shares lines with real resumes ({', '.join(copied)})")
    before, after = parse_resume(before_md), parse_resume(final_md)
    changes_path = tri / "changes.json"
    changes = json.loads(changes_path.read_text()).get("changes", []) if changes_path.exists() else []
    problems += compare(before, after, changes)
    cand = candidate or before[0]["tx"].split()[0].title()

    t0 = events[0]["t"]
    models = {e["who"]: e["text"] for e in events if e["kind"] == "model"}
    events = [e for e in events if e["kind"] != "model"]
    seats = [s for s in dict.fromkeys(e["seat"] for e in events if e["kind"] == "ask")]
    numbered = [s for s in seats if s != "claude"]
    reach = "Manual" if MANUAL & set(seats) else "Auto"
    who = {"user": {"n": cand, "s": cand[0], "role": "the candidate"},
           "host": {"n": "Host", "s": "H", "role": ", ".join(x for x in ("AI 1", models.get("host", "")) if x)}}
    for s in seats:
        name, company = SEAT_NAMES[s]
        parts = (f"AI {numbered.index(s) + 2}", company, models.get(s, "")) if s in numbered else (company, models.get(s, ""), "a fresh session")
        who[s] = {"n": name, "s": name[0], "role": ", ".join(x for x in parts if x)}
    if any(e["kind"] == "check" for e in events):
        who["check"] = {"n": "Checker", "s": "✓", "role": "check_resume.py"}

    # A candidate who takes longer than MAX_WAIT to answer a stop is drawn as MAX_WAIT on the timeline, and the
    # answer says how long they really took; the AIs' own times are never shortened.
    times, cut, waiting, prev = [], 0, False, t0
    for e in events:
        gap, waited = e["t"] - prev, 0
        if e["kind"] == "user" and waiting and gap > MAX_WAIT:
            cut += gap - MAX_WAIT
            waited = gap
        times.append((e["t"] - t0 - cut, waited))
        waiting = (waiting or bool(e.get("stop"))) and e["kind"] != "user"
        prev = e["t"]

    # The host shows the user where the working files are; on the page that path is relative to the run folder.
    local = lambda text: text.replace(str(run.resolve()) + "/", "").replace(str(run.resolve()), ".")
    files, out_events, outstanding, asked = {}, [], {}, {}
    for e, (t, waited) in zip(events, times):
        o = {"t": t, "kind": e["kind"], "text": local(e.get("text", ""))}
        if waited:
            o["waited"] = waited
        if e["kind"] == "ask":
            o.update(who="host", to=e["seat"]); asked[e["seat"]] = t
        elif e["kind"] == "reply":
            o.update(who=e["seat"])
            if e["seat"] in asked:
                o["d"] = t - asked.pop(e["seat"])
        elif e["kind"] == "user":
            o["who"] = "user"
        elif e["kind"] == "check":
            o["who"] = "check"
        else:
            o["who"] = "host"
        if e["kind"] == "step":
            o["step"] = e["step"]
        for k in ("stop", "label"):
            if e.get(k):
                o[k] = e[k]
        if e.get("file"):
            src = (tri / e["file"]) if (tri / e["file"]).exists() else (run / e["file"])  # older records named .tribunal/p4.txt
            if not src.exists():
                problems.append(f"events.jsonl names a file that is not in .tribunal: {e['file']}")
            else:
                name = src.name if src.suffix == ".txt" else src.name + ".txt"
                files[name] = src
                o["files"] = [name]
        o["links"] = links(o["text"], before, after)
        problems += unsafe(o["text"], f"event at {t} s")
        out_events.append(o)
    if asked:
        problems.append(f"no reply recorded for: {', '.join(asked)}")
    for name, src in files.items():
        problems += unsafe(src.read_text(errors="ignore"), name)
    if problems:
        raise SystemExit("not exported:\n  " + "\n  ".join(problems))

    end = out_events[-1]["t"]
    steps = [{"n": e["step"], "name": e["text"].split(".")[0][:40], "t": e["t"]} for e in out_events if e["kind"] == "step"]
    council = len(seats) > 1 or "claude" in seats
    def real_answer(e):  # a seat that only sent back an error (no file, or a few words such as a quota message) does not count
        f = e.get("file") and ((tri / e["file"]) if (tri / e["file"]).exists() else (run / e["file"]))
        return bool(f) and f.exists() and len(f.read_text(errors="ignore").split()) >= 100
    answered = [s for s in seats if any(e["kind"] == "reply" and e.get("seat") == s and real_answer(e) for e in events)]
    companies = {"Anthropic"} | {SEAT_NAMES[s][1] for s in answered}
    who_fact = "Real resume, shared with consent" if consented else "Fictional candidate"
    reach_fact = "Manual mode: pasted into other AI apps" if reach == "Manual" else "Auto mode: the other AIs ran by themselves"
    facts = [who_fact, reach_fact, f"{len(answered) + 1} AIs from {len(companies)} companies", f"{round(end / 60)} minutes", *extra_facts]
    return {
        "slug": slug, "title": title, "mode": "Full council" if council else "Quick review", "reach": reach, "facts": facts, "note": note,
        "candidate": cand, "end": end, "who": who, "steps": steps, "events": out_events,
        "lanes": lanes(out_events, who, cand), "before": before, "after": after,
    }, files


def links(text, before, after):
    """Resume lines a message talks about: the quoted phrases and the figures ($2.4M, 18%, 10+) it shares with them."""
    marks = [m for m in re.findall(r"[\"“]([^\"”]{4,80})[\"”]", text)]
    marks += re.findall(r"\$\d[\d.,]*[MKk]?|\d[\d.,]*%|\d+\+", text)
    found = []
    for l in before + after:
        if "id" in l and l["id"] not in found and any(m.lower() in strip_md(l["tx"]).lower() for m in marks):
            found.append(l["id"])
    return found[:4]


def lanes(events, who, cand):
    """Bars for the timeline: [who, start, end, label, is a wait for the candidate, what the chat shows meanwhile]."""
    out, open_asks = [], {}
    for i, e in enumerate(events):
        nxt = events[i + 1]["t"] if i + 1 < len(events) else e["t"]
        if e["kind"] == "ask":
            open_asks[e["to"]] = e
        if e["kind"] == "reply" and e["who"] in open_asks:
            a = open_asks.pop(e["who"])
            label = a.get("label", "")
            busy = f"{who[e['who']]['n']} is working" + (f" on the {label.lower()}" if label else "")
            out.append([e["who"], a["t"], e["t"], label, 0, busy])
        if e["kind"] == "check":
            out.append(["check", e["t"], e["t"], "", 0, ""])
        if e["kind"] == "say" and e.get("stop"):
            reply = next((x for x in events[i + 1:] if x["kind"] == "user"), None)
            if reply:
                out.append(["user", e["t"], reply["t"], e["stop"], 1, f"Waiting for {cand}"])
            continue
        if open_asks or nxt <= e["t"]:
            continue  # the host is waiting on a seat, or nothing took time
        label = e.get("label", "")  # the step band already names each step
        busy = "The host is working"  # what it is doing is already in the chat, as its note
        if out and out[-1][0] == "host" and out[-1][2] == e["t"] and not label:
            out[-1][2] = nxt
        else:
            out.append(["host", e["t"], nxt, label, 0, busy])
    return out


# ---------- output ----------

def clock(s):
    return f"{s // 60:02d}:{s % 60:02d}"


def transcript(r):
    names = {k: v["n"] for k, v in r["who"].items()}
    out = [f"# {r['title']}", "", " · ".join(r["facts"]), "",
           "Every message of the run in order. Times are minutes and seconds from the start. "
           "Prompts and replies are in [files/](files/).", ""]
    for e in r["events"]:
        if e["kind"] == "step":
            out += [f"## Step {e['step']}: {e['text']}", ""]
            continue
        head = names[e["who"]] + (f" to {names[e['to']]}" if e.get("to") else "")
        tags = ", ".join(x for x in (e.get("stop"), f"took {e['d']} s" if "d" in e else "",
                                     f"answered after {round(e['waited'] / 60)} min" if "waited" in e else "",
                                     "working" if e["kind"] == "note" else "") if x)
        out.append(f"**{clock(e['t'])} {head}**" + (f" ({tags})" if tags else ""))
        out.append("")
        out += ["> " + l if l else ">" for l in e["text"].splitlines()]
        out += ["", *(f"[{f}](files/{f})" for f in e.get("files", [])), ""] if e.get("files") else [""]
    return "\n".join(out).rstrip() + "\n"


def readme(r, files):
    rows = [("[before.md](before.md)", "The resume the candidate started with"),
            ("[job.md](job.md)", "The job posting"), ("[own-words.md](own-words.md)", "What the candidate wrote about their work"),
            ("[after.md](after.md)", "The resume the run produced"), ("[transcript.md](transcript.md)", "Every message, in order"),
            ("[files/](files/)", f"The {len(files)} prompts and replies the other AIs saw, names hidden"),
            ("[run.json](run.json)", "Everything above, for the website's viewer")]
    return "\n".join([f"# {r['title']}", "", " · ".join(r["facts"]), "",
                      "A recorded run of Resume Tribunal on a fictional candidate. "
                      + (r["note"] or "Nothing here was edited by hand: [tools/](../tools/) recorded the run and exported this folder."), "",
                      "| File | What it is |", "|---|---|", *(f"| {a} | {b} |" for a, b in rows), ""])


def export(run, slug, title, out_root, extra_facts=(), candidate=None, replace=False, real=ROOT / "research" / "real-resumes", note="", consented=False):
    r, files = build(run, slug, title, extra_facts, candidate, real, note, consented)
    out = out_root / slug
    if out.exists():
        if not replace:
            raise SystemExit(f"{out} exists; pass --replace to export over it")
        shutil.rmtree(out)
    (out / "files").mkdir(parents=True)
    for name, src in files.items():
        shutil.copyfile(src, out / "files" / name)
    shutil.copyfile(run / "before.md", out / "before.md")
    shutil.copyfile(run / ".tribunal" / "final.md", out / "after.md")
    for name in ("job.md", "own-words.md"):
        if (run / name).exists():
            shutil.copyfile(run / name, out / name)
    for l in r["before"] + r["after"]:
        l.pop("alt", None)
    (out / "run.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")
    (out / "transcript.md").write_text(transcript(r))
    (out / "README.md").write_text(readme(r, files))
    return out, r


# ---------- self-test ----------

def self_test():
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import record
    with tempfile.TemporaryDirectory() as d:
        record.main([d, "step", "2", "Draft"])
        record.main([d, "say", "--stop", "Stop 1", "Go ahead?"])
        pathlib.Path(d, "p1.txt").write_text("prompt")
        record.main([d, "ask", "codex", "--file", str(pathlib.Path(d, "p1.txt")), "--label", "Draft", "Write it."])
        logged = [json.loads(l) for l in pathlib.Path(d, "events.jsonl").read_text().splitlines()]
        assert [e["kind"] for e in logged] == ["step", "say", "ask"] and logged[0]["step"] == 2
        assert logged[1]["stop"] == "Stop 1" and logged[1]["text"] == "Go ahead?"
        assert logged[2]["seat"] == "codex" and logged[2]["file"] == "p1.txt" and logged[2]["text"] == "Write it."
        for bad in ([d, "ask", "gpt", "x"], [d, "step", "x", "Draft"], [d, "note"]):
            try:
                record.main(bad)
                raise AssertionError(f"record.py should refuse {bad[1:]}")
            except SystemExit as e:
                assert e.code != 0
    with tempfile.TemporaryDirectory() as d:
        run = pathlib.Path(d) / "run"
        tri = run / ".tribunal"
        tri.mkdir(parents=True)
        (run / "before.md").write_text("JO DOE\nAnytown | jo@example.com | (412) 555-0147\n\nEXPERIENCE\nShop\n"
                                       "Analyst | 2020 - Present\n- Increased conversion by 18%\n- Managed $2.4M budget\n- Built reports in Excel\n")
        (run / "job.md").write_text("Analyst job\n")
        (tri / "final.md").write_text("# Jo Doe\nAnytown | jo@example.com | (412) 555-0147\n\n## Experience\n"
                                      "### Shop\n**Analyst** | 2020 - Present\n- Conversion rose from 2.1% to 2.5%\n"
                                      "- Built the weekly reports in Excel\n- Wrote SQL most days\n")
        (tri / "changes.json").write_text(json.dumps({"changes": [
            {"old": "Increased conversion by 18%", "new": "Conversion rose from 2.1% to 2.5%", "why": "Her numbers.", "source": "own words"},
            {"old": "Managed $2.4M budget", "why": "Not hers."}, {"old": "EXPERIENCE", "new": "## Experience", "why": "Heading."}]}))
        (tri / "p1.txt").write_text("Write a resume for <<NAME>>.")
        (tri / "r.md").write_text("Draft. " * 120)
        ev = [(100, {"kind": "model", "who": "host", "text": "Claude Opus 5.5"}),
              (100, {"kind": "step", "step": 1, "text": "Setup"}),
              (110, {"kind": "say", "stop": "Stop 1", "text": "Go ahead?"}),
              (130, {"kind": "user", "text": "Yes."}),
              (131, {"kind": "note", "text": "Writing its own draft", "label": "Own draft"}),
              (140, {"kind": "ask", "seat": "codex", "label": "Draft", "file": "p1.txt", "text": "Write it."}),
              (150, {"kind": "check", "text": "0 errors"}),
              (200, {"kind": "reply", "seat": "codex", "file": "r.md", "text": "It kept the \"Managed $2.4M budget\" line."}),
              (220, {"kind": "say", "stop": "Stop 2", "text": f"Here it is, at {run.resolve()}/.tribunal/resume.md. True?"}),
              (220 + 4000, {"kind": "user", "text": "All true."}),
              (230 + 4000, {"kind": "say", "text": "Done."})]
        (tri / "events.jsonl").write_text("".join(json.dumps({"t": t, **e}) + "\n" for t, e in ev))
        out, r = export(run, "jo", "Jo", pathlib.Path(d) / "examples", real=pathlib.Path(d) / "none")
        b = {norm(l["tx"]): l for l in r["before"]}
        a = {norm(l["tx"]): l for l in r["after"]}
        assert b["managed $2.4m budget"]["s"] == "cut" and b["managed $2.4m budget"]["why"] == "Not hers."
        assert b["increased conversion by 18%"]["id"] == a["conversion rose from 2.1% to 2.5%"]["id"]
        assert a["conversion rose from 2.1% to 2.5%"]["from"] == "own words"
        assert a["built the weekly reports in excel"]["s"] == "rw", "a close rewrite pairs by similarity"
        assert a["wrote sql most days"]["s"] == "new"
        assert find(parse_resume((tri / "final.md").read_text()), "**Analyst** | 2020 - Present")["k"] == "role", "a role quoted as written in final.md"
        assert a["analyst shop 2020 - present"]["k"] == "role" and "**Shop**" in a["analyst shop 2020 - present"]["tx"], "### Company + **Title** | dates merge"
        assert [l["k"] for l in r["before"][:3]] == ["name", "contact", "h2"]
        assert [l["k"] for l in parse_resume("Jo\njo@example.com\nEducation\nBA, 2014\nSkills:\nExcel")] == ["name", "contact", "h2", "p", "h2", "p"]
        pdf = parse_resume("Jo\njo@example.com\nPROFESSIONAL SUMMARY With 4+ years of backend work in Java.\n● Built the claims API")
        assert [(l["k"], l["tx"][:12]) for l in pdf[2:]] == [("h2", "PROFESSIONAL"), ("p", "With 4+ year"), ("bul", "Built the cl")]
        assert b["analyst shop 2020 - present"].get("s") is None, "a plain company line + role matches the markdown role"
        assert r["who"]["codex"]["role"].startswith("AI 2, OpenAI") and r["who"]["host"]["role"] == "AI 1, Claude Opus 5.5"
        reply = next(e for e in r["events"] if e["kind"] == "reply")
        assert reply["d"] == 60 and reply["files"] == ["r.md.txt"] and b["managed $2.4m budget"]["id"] in reply["links"]
        L = r["lanes"]
        assert ["codex", 40, 100, "Draft", 0, "Codex is working on the draft"] in L
        assert ["user", 10, 30, "Stop 1", 1, "Waiting for Jo"] in L
        assert not any(l[0] == "host" and 40 <= l[1] < 100 for l in L), "the host waits while the seat works, even after a check"
        assert ["check", 50, 50, "", 0, ""] in L
        assert any(e["text"] == "Here it is, at .tribunal/resume.md. True?" for e in r["events"]), "the run folder's path is shown relative"
        late = next(e for e in r["events"] if e["text"] == "All true.")
        assert late["waited"] == 4000 and late["t"] == 120 + MAX_WAIT, "a long wait is drawn short and labelled"
        assert r["end"] == 130 + MAX_WAIT and ["user", 120, 120 + MAX_WAIT, "Stop 2", 1, "Waiting for Jo"] in r["lanes"]
        assert (out / "files" / "p1.txt").exists() and "**00:10 Host** (Stop 1)" in (out / "transcript.md").read_text()
        try:
            export(run, "jo", "Jo", pathlib.Path(d) / "examples", real=pathlib.Path(d) / "none")
            raise AssertionError("an existing folder needs --replace")
        except SystemExit:
            pass
        (run / "before.md").write_text((run / "before.md").read_text().replace("jo@example.com", "jo.doe@gmail.com"))
        try:
            build(run, "jo", "Jo", real=pathlib.Path(d) / "none")
            raise AssertionError("a real-looking email must stop the export")
        except SystemExit as e:
            assert "jo.doe@gmail.com" in str(e)
        (run / "before.md").write_text((run / "before.md").read_text().replace("jo.doe@gmail.com", "jo@example.com").replace("555-0147", "867-5309"))
        try:
            build(run, "jo", "Jo", real=pathlib.Path(d) / "none")
            raise AssertionError("a real-looking phone must stop the export")
        except SystemExit as e:
            assert "867-5309" in str(e)
        assert unsafe("saved to /home/jo/run/final.md", "x") == ["x: local path /home/jo"]
        assert unsafe("Req. ID: 1273383451", "x") == [] and unsafe("Phone No. 1273383451", "x") != []
        real = pathlib.Path(d) / "real"
        real.mkdir()
        (run / "before.md").write_text((run / "before.md").read_text().replace("867-5309", "555-0147"))
        (real / "resume-01.md").write_text("- Increased conversion by 18% through data-driven segmentation work\n")
        (run / "before.md").write_text((run / "before.md").read_text() + "- Increased conversion by 18% through data-driven segmentation work\n")
        try:
            build(run, "jo", "Jo", real=real)
            raise AssertionError("a line from a real resume must stop the export")
        except SystemExit as e:
            assert "resume-01.md" in str(e)
        r2, _ = build(run, "jo", "Jo", real=real, consented=True)
        assert r2["facts"][0] == "Real resume, shared with consent" and r2["reach"] == "Auto"
    print("export.py self-test passed")


def main():
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
    if len(sys.argv) in (3, 4) and sys.argv[2] == "--check":  # the host checks its record before finishing
        build(pathlib.Path(sys.argv[1]), "check", "check", consented=sys.argv[3:] == ["--real-with-consent"])
        return print("the record is complete: export.py can turn it into an example")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("slug")
    ap.add_argument("--title", required=True)
    kind = ap.add_mutually_exclusive_group(required=True)
    kind.add_argument("--fictional", action="store_true", help="confirm the candidate is invented")
    kind.add_argument("--real-with-consent", action="store_true",
                      help="a real resume whose owner agreed to publish it, already de-identified (invented name, example contact details)")
    ap.add_argument("--fact", action="append", default=[], help="an extra fact for the page, such as 'Real public job posting'")
    ap.add_argument("--candidate", help="the candidate's first name, if not the first word of the resume")
    ap.add_argument("--replace", action="store_true", help="export over an existing example")
    ap.add_argument("--note", default="", help="how the run was recorded, if not by record.py from the start; shown on the page and in the README")
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "examples")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a.slug):
        sys.exit("the slug is lower-case words joined by hyphens")
    out, r = export(a.run, a.slug, a.title, a.out, a.fact, a.candidate, a.replace, note=a.note, consented=a.real_with_consent)
    print(f"exported {out}: {len(r['events'])} events, {len(r['lanes'])} timeline bars")


if __name__ == "__main__":
    main()
