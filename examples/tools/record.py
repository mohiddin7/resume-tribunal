#!/usr/bin/env python3
"""Log one event of an example run to .tribunal/events.jsonl, with the time. The host of an example run calls
this as it works; export.py turns the log into the page and folder for the example.

  record.py DIR step 2 "Three drafts"                      a workflow step starts
  record.py DIR say --stop "Stop 1" - < message.txt        a message shown to the candidate, word for word
  record.py DIR user "Full council, please."               the candidate's reply, word for word
  record.py DIR note "Writing my own draft"                what the host is doing (not shown to the candidate)
  record.py DIR ask codex --label Draft --file p1.txt "Write a resume for this job from these files only."
  record.py DIR reply codex --file p1_reply_codex.md "Here's my draft. It kept the $2.4M budget line."
  record.py DIR check "0 errors, 6 warnings"               a check_resume.py result
  record.py DIR model host "Claude Opus 5.5"               which model a participant ran (once each)

DIR is the .tribunal folder. TEXT "-" reads the text from standard input. Standard library only.
"""
import argparse
import json
import os
import sys
import time

KINDS = ("step", "say", "user", "note", "ask", "reply", "check", "model")
SEATS = ("codex", "agy", "claude")


def event(a):
    # step, ask, reply and model take a first argument (step number, seat, participant); the rest take only text
    first, text = (a.arg, a.text) if a.kind in ("step", "ask", "reply", "model") else (None, a.arg)
    text = sys.stdin.read().strip() if text == "-" else (text or "").strip()
    e = {"t": int(time.time()), "kind": a.kind}
    if a.kind == "step":
        if not (first or "").isdigit():
            sys.exit("step: give the step number, then its name")
        e.update(step=int(first), text=text)
    elif a.kind in ("ask", "reply"):
        if first not in SEATS:
            sys.exit(f"{a.kind}: the seat is one of {', '.join(SEATS)}, not {first!r}")
        e.update(seat=first, text=text)
    elif a.kind == "model":
        e.update(who=first, text=text)
    else:
        e["text"] = text
    if not e["text"]:
        sys.exit(f"{a.kind}: give the text, or - to read it from standard input")
    for k in ("stop", "label", "file"):
        if getattr(a, k):
            e[k] = getattr(a, k)
    if a.file:  # stored relative to DIR, whether given as p4.txt, .tribunal/p4.txt or a full path
        full = os.path.abspath(a.file if os.path.exists(a.file) else os.path.join(a.dir, a.file))
        e["file"] = os.path.relpath(full, os.path.abspath(a.dir))
        if e["file"].startswith(".."):
            sys.exit(f"--file must be inside {a.dir}: {a.file}")
    return e


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("kind", choices=KINDS)
    ap.add_argument("arg", nargs="?", help="the step number, the seat, or the start of the text")
    ap.add_argument("text", nargs="?")
    ap.add_argument("--stop", help='for say: the stop it waits at, such as "Stop 2"')
    ap.add_argument("--label", help="for ask and note: a word or two for the timeline bar, such as Draft")
    ap.add_argument("--file", help="for ask and reply: the prompt or reply file inside DIR")
    a = ap.parse_intermixed_args(argv)  # options may come before or after the text
    e = event(a)
    with open(f"{a.dir.rstrip('/')}/events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
