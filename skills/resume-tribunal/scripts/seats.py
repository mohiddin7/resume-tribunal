#!/usr/bin/env python3
"""Find and run other assistants' command-line tools, so the host can fill Seats B and C itself.

Usage:
  python3 seats.py detect [--exclude VENDOR]         # list usable seats as JSON
  python3 seats.py run SEAT prompt.txt reply.md      # send one prompt, save the reply
  python3 seats.py run --cmd "mytool --print" prompt.txt reply.md   # any other tool that reads stdin
  python3 seats.py run --cmd "mytool -p 'Read {prompt_file}'" prompt.txt reply.md  # or reads a file

Each seat runs with the user's existing login for that tool. This script sends the prompt
file to that tool and nothing else: no API keys, no other network calls. Standard library only.
Tested by the maintainers: codex. The others follow each tool's documented non-interactive
mode. If one fails, pass --cmd or fall back to manual mode.
"""
import argparse
import json
import os
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
SEATS = {
    "claude": ("anthropic", ["claude", "-p", "--tools", "", "--no-session-persistence"]),
    "codex": ("openai", ["codex", "exec", "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check", "-"]),
    "agy": ("google", ["agy", "--sandbox", "--mode", "plan", "--print-timeout", "10m",
                       "-p", "Read the file {prompt_file} in this folder and reply to it exactly as it asks."]),
    # Gemini CLI now needs a paid API key; personal Google logins moved to agy. -p is appended to stdin.
    "gemini": ("google", ["gemini", "--skip-trust", "--approval-mode", "plan", "-p", "Reply to the material above."]),
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
    # Fail early if the reply cannot be saved, before the seat is called.
    open(reply_path, "a", encoding="utf-8").close()
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
        try:
            r = subprocess.run(cmd, input=stdin, capture_output=True, text=True, encoding="utf-8",
                               timeout=timeout, cwd=empty)
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
    d.add_argument("--exclude", action="append", default=[], type=str.lower,
                   choices=sorted({v for v, _ in SEATS.values()}), help="the host's own vendor")
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
