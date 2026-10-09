#!/usr/bin/env python3
"""Find and run other assistants' command-line tools, so the host can fill Seats B and C itself.

Usage:
  python3 seats.py detect [--exclude VENDOR]         # list usable seats as JSON
  python3 seats.py run SEAT prompt.txt reply.md      # send one prompt, save the reply
  python3 seats.py run --cmd "mytool --print" prompt.txt reply.md   # any other tool that reads stdin

Each seat runs with the user's existing login for that tool. This script sends the prompt
file to that tool and nothing else: no API keys, no other network calls. Standard library only.
Only the first entry below has been tested by the maintainers; the others follow each tool's
documented non-interactive mode. If one fails, pass --cmd or fall back to manual mode.
"""
import argparse
import json
import shlex
import shutil
import subprocess
import sys

# name: (vendor, command that reads the prompt on stdin and prints the reply)
SEATS = {
    "claude": ("anthropic", ["claude", "-p"]),
    "codex": ("openai", ["codex", "exec", "-"]),
    "gemini": ("google", ["gemini", "-p", ""]),
}


def detect(exclude):
    """One seat per vendor, so two tools from the same company never count as two opinions."""
    found, seen = [], set(exclude)
    for name, (vendor, cmd) in SEATS.items():
        if vendor not in seen and shutil.which(cmd[0]):
            found.append({"seat": name, "vendor": vendor})
            seen.add(vendor)
    return found


def run(cmd, prompt_path, reply_path, timeout):
    with open(prompt_path, encoding="utf-8") as f:
        prompt = f.read()
    try:
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        sys.exit(f"seat failed: {e}")
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit(f"seat failed (exit {r.returncode}): {r.stderr.strip()[:500] or 'empty reply'}")
    with open(reply_path, "w", encoding="utf-8") as f:
        f.write(r.stdout)
    print(f"saved {len(r.stdout)} characters to {reply_path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="action", required=True)
    d = sub.add_parser("detect")
    d.add_argument("--exclude", action="append", default=[], help="the host's own vendor: anthropic, openai or google")
    r = sub.add_parser("run")
    r.add_argument("seat", nargs="?", choices=sorted(SEATS))
    r.add_argument("--cmd", help="custom command that reads the prompt on stdin")
    r.add_argument("prompt")
    r.add_argument("reply")
    r.add_argument("--timeout", type=int, default=600)
    a = p.parse_args()
    if a.action == "detect":
        print(json.dumps(detect(a.exclude)))
    elif a.cmd:
        run(shlex.split(a.cmd), a.prompt, a.reply, a.timeout)
    elif a.seat:
        run(SEATS[a.seat][1], a.prompt, a.reply, a.timeout)
    else:
        p.error("name a seat or pass --cmd")


if __name__ == "__main__":
    main()
