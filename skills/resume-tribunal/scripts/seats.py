#!/usr/bin/env python3
"""Find and run other assistants' command-line tools, so the host can fill Seats B and C itself.

Usage:
  python3 seats.py detect [--exclude VENDOR]         # list usable seats as JSON
  python3 seats.py models SEAT                       # list a seat's models, where the tool can
  python3 seats.py run SEAT prompt.txt reply.md [--model NAME] [--effort LEVEL]
  python3 seats.py run custom --cmd "mytool --print" prompt.txt reply.md   # any tool that reads stdin
  python3 seats.py run custom --cmd "mytool -p 'Read {prompt_file}'" prompt.txt reply.md  # or a file
  python3 seats.py --self-test

Each seat runs with the user's existing login for that tool. This script sends the prompt
file to that tool and nothing else: no API keys, no other network calls. Standard library only.
The built-in seats run read-only in an empty folder. `run custom` runs
the command exactly as given, so keeping that tool read-only is up to whoever writes it.
"""
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

# name: (vendor, command). Every seat runs read-only with its tools off or sandboxed, because
# the prompt carries text from outside (a job posting) that could contain instructions.
# The prompt goes in on stdin, or as a private file in the seat's folder where {prompt_file}
# appears. It never goes on the command line, where other local users could see it.
# Earlier entries win when one company has two tools installed.
# MODEL_FLAGS: where --model and --effort go for each tool (inserted after the first N words).
MODEL_FLAGS = {
    "claude": (1, ["--model", "{m}"], ["--effort", "{e}"]),
    "codex": (2, ["-m", "{m}"], ["-c", "model_reasoning_effort={e}"]),
    "agy": (1, ["--model", "{m}"], ["--effort", "{e}"]),
}
LIST_MODELS = {"agy": ["agy", "models"]}
CODEX_MODELS = os.path.expanduser("~/.codex/models_cache.json")  # the models this account can use
SEATS = {
    # --safe-mode keeps the user's own memory, hooks, plugins and MCP servers out of the seat's context.
    "claude": ("anthropic", ["claude", "-p", "--safe-mode", "--tools", "", "--no-session-persistence"]),
    "codex": ("openai", ["codex", "exec", "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check", "-"]),
    "agy": ("google", ["agy", "--sandbox", "--mode", "plan", "--print-timeout", "10m",
                       "-p", "Open the file {prompt_file} in this folder with your file-reading tool. Run no shell "
                             "commands. Then reply to it exactly as it asks."]),
}


def detect(exclude):
    """One seat per vendor, so two tools from the same company never count as two opinions."""
    found, seen = [], set(exclude)
    for name, (vendor, cmd) in SEATS.items():
        if vendor not in seen and shutil.which(cmd[0]):
            found.append({"seat": name, "vendor": vendor})
            seen.add(vendor)
    return found


def blocked(reply):
    """True only for the tool's own one-line error, never for a reply that merely quotes it."""
    text = reply.strip()
    return text.startswith("jetski: no output produced") and "\n" not in text


def contact_details(prompt):
    """Emails, profile links and phone numbers that should have been swapped for stand-ins."""
    found = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+|linkedin\.com/in/[\w-]+", prompt)
    found += [m for m in re.findall(r"\+?\d[\d ().-]{5,}\d", prompt)
              if sum(c.isdigit() for c in m) >= (7 if re.search(r"\D", m) else 10)
              and not re.fullmatch(r"(?:19|20)\d\d\s*-\s*(?:19|20)\d\d", m)]
    return found


def run(cmd, prompt_path, reply_path, timeout, allow_contact=False):
    with open(prompt_path, encoding="utf-8") as f:
        prompt = f.read()
    found = contact_details(prompt)
    if found and not allow_contact:
        sys.exit(f"not sent: the prompt still holds contact details ({', '.join(found[:3])}). Replace them with "
                 "stand-ins, or pass --allow-contact if the user agreed to send them.")
    # Fail early if the reply cannot be saved, and clear any earlier reply so a failed run leaves nothing stale.
    open(reply_path, "w", encoding="utf-8").close()
    # These tools are agents that can read files. Run each one in an empty folder so it
    # cannot see the other drafts, the label log or anything else in the project.
    uses_file = any("{prompt_file}" in part for part in cmd)
    with tempfile.TemporaryDirectory() as empty:  # created readable by this user only
        if uses_file:
            fd = os.open(os.path.join(empty, "prompt.md"), os.O_WRONLY | os.O_CREAT, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(prompt)
        cmd = [part.replace("{prompt_file}", "prompt.md") for part in cmd]
        stdin = None if uses_file else prompt
        for attempt in (1, 2):  # a read-only seat sometimes reaches for a blocked tool; one retry clears it
            try:
                r = subprocess.run(cmd, input=stdin, capture_output=True, text=True, encoding="utf-8",
                                   timeout=timeout, cwd=empty)
            except (OSError, subprocess.TimeoutExpired) as e:
                sys.exit(f"seat failed: {e}")
            if r.returncode == 0 and r.stdout.strip() and not blocked(r.stdout):
                break
    if r.returncode != 0 or not r.stdout.strip() or blocked(r.stdout):
        sys.exit(f"seat failed (exit {r.returncode}): {(r.stderr.strip() or r.stdout.strip())[:500] or 'empty reply'}")
    with open(reply_path, "w", encoding="utf-8") as f:
        f.write(r.stdout)
    print(f"saved {len(r.stdout)} characters to {reply_path}")


def with_model(seat, cmd, model, effort):
    at, mflag, eflag = MODEL_FLAGS[seat]
    extra = ([f.format(m=model) for f in mflag] if model else []) + \
            ([f.format(e=effort) for f in eflag] if effort else [])
    return cmd[:at] + extra + cmd[at:]


def self_test():
    assert blocked("jetski: no output produced\n") and not blocked("# Resume\njetski: no output produced")
    assert with_model("codex", SEATS["codex"][1], "m1", "high")[:6] == ["codex", "exec", "-m", "m1", "-c", "model_reasoning_effort=high"]
    assert with_model("claude", SEATS["claude"][1], None, None) == SEATS["claude"][1]
    assert all(d["vendor"] != "openai" for d in detect(["openai"]))
    assert contact_details("Mail sam@example.com or call +1 (555) 010-2030") == ["sam@example.com", "+1 (555) 010-2030"]
    assert contact_details("<<EMAIL>> | <<PHONE>> | Jan 2019 - Mar 2021 | 2019 - 2021 | cut 1200 to 300 | 5000000") == []
    assert contact_details("call 555-0117") == ["555-0117"]
    assert contact_details("call 5551234567") == ["5551234567"]
    print("self-test passed")


def main():
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="action", required=True)
    d = sub.add_parser("detect")
    d.add_argument("--exclude", action="append", default=[], type=str.lower,
                   choices=sorted({v for v, _ in SEATS.values()}), help="the host's own vendor")
    m = sub.add_parser("models")
    m.add_argument("seat", choices=sorted(SEATS))
    r = sub.add_parser("run")
    r.add_argument("seat", choices=sorted(SEATS) + ["custom"], help="a seat name, or custom with --cmd")
    r.add_argument("--cmd", help="custom command that reads the prompt on stdin")
    r.add_argument("prompt")
    r.add_argument("reply")
    r.add_argument("--timeout", type=int, default=540, help="seconds; kept under a ten-minute shell limit")
    r.add_argument("--model", help="the seat company's own model, matched to the host's tier")
    r.add_argument("--effort", help="reasoning effort, such as low, medium or high")
    r.add_argument("--allow-contact", action="store_true", help="send even if the prompt holds an email, phone or profile link")
    a = p.parse_args()
    if a.action == "detect":
        print(json.dumps(detect(a.exclude)))
    elif a.action == "models" and a.seat == "codex" and os.path.exists(CODEX_MODELS):
        for m in json.load(open(CODEX_MODELS, encoding="utf-8")).get("models", []):
            if m.get("visibility") == "list":
                print(f"{m['slug']}\t{m.get('description', '')}")
    elif a.action == "models":
        if a.seat not in LIST_MODELS:
            sys.exit(f"{a.seat} cannot list its models here; use the names in its documentation")
        r = subprocess.run(LIST_MODELS[a.seat], capture_output=True, text=True, encoding="utf-8")
        print(r.stdout or r.stderr)
    elif a.seat == "custom":
        if not a.cmd:
            p.error("custom needs --cmd")
        run(shlex.split(a.cmd), a.prompt, a.reply, a.timeout, a.allow_contact)
    else:
        run(with_model(a.seat, SEATS[a.seat][1], a.model, a.effort), a.prompt, a.reply, a.timeout, a.allow_contact)


if __name__ == "__main__":
    main()
