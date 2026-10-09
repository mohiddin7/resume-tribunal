# Resume Tribunal

**A free, open skill that has three different AI assistants draft your tailored resume independently, critique each other blind, and hand you one merged resume in your own voice, plus the interview questions it will invite.** No app, no API keys, no account.

Resume Tribunal is an [Agent Skill](https://agentskills.io) (`SKILL.md`). Install it on the AI assistant you already use and say "tailor my resume to this job".

## What it does

1. **Setup.** You give the job description, your resume, and a few plain sentences about what you did in your recent roles. You answer every question here, once.
2. **Drafts.** Three assistants from three different companies each write a resume from your material.
3. **Blind critique.** Each assistant reviews the drafts it did not write, without knowing who wrote them. Every criticism has to quote the line it is about.
4. **Merge.** Your main assistant takes the strongest draft and brings in the best lines from the others.
5. **Review and voice.** A different assistant reviews the result, a script checks it for common AI-writing patterns, and the text is edited back toward your own wording. You confirm every claim is true.

You get a Markdown resume, a list of anything you still need to fill in, and three to five questions an interviewer is likely to ask about your claims.

## Why three assistants

A language model tends to be lenient toward its own writing. In a 2025 study of resume screening, models preferred resumes they had rewritten over human-written ones 67–82% of the time ([Xu, Li and Jiang](https://arxiv.org/abs/2509.00462)). So in this skill no draft is reviewed by the assistant that wrote it.

**What this does not prove:** no study shows that a multi-AI council writes a better resume than one strong assistant. The process gives you independent review and a resume you can defend line by line. It does not guarantee interviews.

## How much work is it for you

The skill uses the least manual route available:

| Where you run it | What happens |
|---|---|
| A platform that can run one prompt across several companies' models | The drafts and critiques run automatically |
| A terminal with other AI command-line tools installed | The skill runs them for you with your existing logins |
| Anything else | The skill gives you ready-made prompts to paste into two other assistants |

It asks before sending your resume anywhere.

## Install

**Most coding agents** (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and others):

```bash
npx skills add mohiddin7/resume-tribunal
```

**GitHub CLI:**

```bash
gh skill install mohiddin7/resume-tribunal
```

**By hand:** copy `skills/resume-tribunal/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (most other agents).

**Chat apps that accept skill uploads:** download `resume-tribunal.zip` from the latest release and upload it in the app's skills settings.

## Private chats for the other two assistants

The critique is only blind if the other assistants start with no memory of you. Checked October 2026; menus change.

| App | Use |
|---|---|
| ChatGPT | Temporary Chat |
| Claude | Incognito chat |
| Gemini | Temporary chat |
| Perplexity | Incognito |

Keep these chats outside any project or shared workspace, and copy each reply before you close the chat.

## The checker

`scripts/check_resume.py` reads the files you name, writes nothing, and makes no network calls. It needs only Python 3.

```bash
python3 skills/resume-tribunal/scripts/check_resume.py resume.md --source my-own-notes.md
```

It flags em dashes, "not X but Y" phrasing, trailing "-ing" clauses, repeated three-item lists, bullets that all look alike, stock openers, hidden text, mixed date styles, numbers that do not appear in your own material, and words you never used.

## Please read

- You are responsible for everything you submit. Check each employer's policy on AI use in applications.
- This project runs no server and never receives your resume. The assistants you choose do, under their own terms. Remove personal identifiers and confidential employer figures, and turn off model training in each app.
- No tool can promise interviews, an ATS outcome, or how a reader or an AI detector will judge your text.
- The skill will not invent facts, add hidden text, or help with assessments or live interviews.
- This is general information, not career or legal advice.

## Files

```
skills/resume-tribunal/
├── SKILL.md                 # instructions for the assistant
├── references/prompts.md    # seven prompts
└── scripts/
    ├── check_resume.py      # resume checker
    └── seats.py             # finds and runs other AI command-line tools
```

## License

MIT
