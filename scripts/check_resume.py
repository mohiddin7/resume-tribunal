#!/usr/bin/env python3
"""Mechanical lint for a Markdown resume: the rules a model shouldn't police itself.

Usage:  python3 scripts/check_resume.py resume.md [--line-chars 105]
        python3 scripts/check_resume.py - < resume.md
        python3 scripts/check_resume.py --self-test

Line length is estimated from characters per printed line (default 105, about
letter paper, 0.5in margins, 10.5pt font). Tune --line-chars to your template.
Unfilled [placeholders] are listed as TODOs for the candidate and do not fail
the check. Exit code: 0 = no issues, 1 = issues found.
"""
import re
import sys

BANNED = [
    "spearheaded", "leveraged", "fostered", "testament", "driven", "dynamic",
    "synergy", "utilized", "passionately", "proven track record", "streamlined",
    "orchestrated", "transformative", "revolutionized", "catalyzed", "pioneered",
    "harness", "paradigm-shifting", "innovative", "cutting-edge", "state-of-the-art",
    "highly scalable", "revolutionary", "robust", "sophisticated", "highly tailored",
    "extremely efficient", "self-starter", "team player", "results-oriented",
    "detail-oriented", "go-getter", "delve", "seamless", "seamlessly",
]
# Stems catch variants (leverage/leveraging, utilize/utilization, ...).
BANNED_RE = re.compile(
    r"\b(" + "|".join(re.escape(w[:-2] if w.endswith("ed") else w) for w in BANNED) + r")\w*",
    re.IGNORECASE,
)
# Any [bracketed text] that is not a Markdown link.
PLACEHOLDER_RE = re.compile(r"\[[^\]]+\](?!\()")
DATE_RANGE_RE = re.compile(r"\b(?:19|20)\d{2}\s*([-–—]|to)\s*(?:(?:19|20)\d{2}|present|current)\b", re.IGNORECASE)
MD_STRIP_RE = re.compile(r"[*_`]|\[([^\]]*)\]\([^)]*\)")


def plain(text):
    return MD_STRIP_RE.sub(lambda m: m.group(1) or "", text).strip()


def check(md, line_chars=105):
    issues = []
    prev_verb = None
    dashes = set()
    for n, raw in enumerate(md.splitlines(), 1):
        for m in BANNED_RE.finditer(raw):
            issues.append((n, "banned", f'"{m.group(0)}"'))
        for m in PLACEHOLDER_RE.finditer(raw):
            issues.append((n, "placeholder", m.group(0)))
        for m in DATE_RANGE_RE.finditer(raw):
            dashes.add(m.group(1).lower())

        bullet = re.match(r"\s*[-*•]\s+(.*)", raw)
        if not bullet:
            prev_verb = None
            continue
        text = plain(bullet.group(1))
        lines = len(text) / line_chars
        # House rule: exactly one line, or 1.5 to 1.7 lines.
        if lines > 2:
            issues.append((n, "too-long", f"~{lines:.1f} lines (max 2)"))
        elif lines > 1.7:
            issues.append((n, "over-1.7-lines", f"~{lines:.1f} lines, trim to 1.7 or less"))
        elif 1 < lines < 1.5:
            issues.append((n, "short-second-line", f"~{lines:.1f} lines, cut to 1 or extend to 1.5"))
        verb = text.split()[0].lower() if text.split() else None
        if verb and verb == prev_verb:
            issues.append((n, "repeat-verb", f'adjacent bullets both start with "{verb}"'))
        prev_verb = verb

    if len(dashes) > 1:
        issues.append((0, "date-dash", f"mixed date separators: {sorted(dashes)}"))
    return issues


def self_test():
    md = "\n".join([
        "## Experience",
        "**Analyst** | 2021 – Present",
        "- Leveraged SQL to build dashboards",                    # banned
        "- Built a churn model that cut losses by [X%]",          # placeholder
        "- Built " + "word " * 40,                                # repeat verb + hanging/long
        "**Junior** | 2019 - 2021",                               # mixed dash
        "- Cut reporting time " + "from days to hours " * 12,     # too long
    ])
    kinds = {k for _, k, _ in check(md)}
    expected = {"banned", "placeholder", "repeat-verb", "too-long", "date-dash"}
    assert expected <= kinds, f"missing: {expected - kinds}"
    short = check("- Cut " + "x" * 120)                           # ~1.2 lines
    assert short[0][1] == "short-second-line", short
    assert check("See [LinkedIn](https://x.com) and [Degree]")[0][2] == "[Degree]"
    assert check("- Cut cloud spend 30% by moving batch jobs to spot instances") == []
    assert check("- Spearheading the rollout")[0][1] == "banned"
    print("self-test passed")


def main(argv):
    if "--self-test" in argv:
        self_test()
        return 0
    if not argv or (argv[0].startswith("-") and argv[0] != "-"):
        print(__doc__)
        return 2
    line_chars = int(argv[argv.index("--line-chars") + 1]) if "--line-chars" in argv else 105
    md = sys.stdin.read() if argv[0] == "-" else open(argv[0], encoding="utf-8").read()
    found = check(md, line_chars)
    issues = [i for i in found if i[1] != "placeholder"]
    todos = [i for i in found if i[1] == "placeholder"]
    for n, kind, detail in issues:
        print(f"{'line ' + str(n) if n else 'document'}: {kind}: {detail}")
    for n, _, detail in todos:
        print(f"line {n}: TODO fill in {detail}")
    print(f"{len(issues)} issue(s), {len(todos)} placeholder(s) to fill")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
