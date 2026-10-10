# Resume Tribunal

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black.svg)](https://agentskills.io)

**Tailor your resume to a job, with every draft reviewed blind by an AI from a different company.** You get one ATS-safe resume built from your own facts and wording, plus the interview questions its claims will invite. Free and open source. No API keys, no new subscription.

```bash
npx skills add mohiddin7/resume-tribunal
```

Then tell your assistant: *"Tailor my resume to this job: \<link\>"*.

> **Status:** version 1.0, in testing. The install command works once the repository is public.

## Why

AI models favour their own writing. In a 2025 study of resume screening, models preferred resumes they had rewritten over human-written ones 67–82% of the time ([Xu, Li and Jiang](https://arxiv.org/abs/2509.00462)). That study measured screening, so it supports this design by analogy: if one AI writes your resume and also judges it, its blind spots go unchecked.

Resume Tribunal splits the work. Your assistant drafts, and an assistant from another company reviews without knowing who wrote what. In full council mode, three assistants draft and critique each other.

**What it does not promise:** no study shows that a multi-AI council writes a better resume than one strong assistant, and no tool can promise interviews or an ATS result. What you get is independent review, and a resume you can defend line by line.

## How it works

```
       You give: the job, your resume, and a few sentences in your own words
                                       |
            QUICK REVIEW               |               FULL COUNCIL
   drafts -> 1 other AI reviews        |   3 AIs draft -> critique each other blind
                                       |   -> merge -> another AI reviews
                                       |
              checks -> you confirm every claim -> resume.md
                                       |
           final blind look -> PDF or Word file when you say it's final
```

| How you run it | What happens | Your effort |
|---|---|---|
| **Automatic**, in a terminal with other AI tools installed ([Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code), [Codex](https://www.npmjs.com/package/@openai/codex), [Antigravity CLI](https://antigravity.google)) | The other AIs run by themselves on your existing logins, each read-only in an empty folder | A few minutes |
| **Automatic**, on a platform that runs several companies' models | The drafts and reviews run in one place | A few minutes |
| **Manual**, anywhere else | You paste a prompt into another AI app (ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat or Perplexity, none preferred) and paste the reply back | 1 round for quick review, about 5 for full council |
| **Solo**, if you want only one company involved | Fresh copies of your assistant review blind | A few minutes, weaker review |

Each seat runs its own company's model at the same tier as your main assistant, so no reviewer is much weaker than the writer.

## What makes it different

- **Truth first.** Every claim comes from you. Unknown numbers become questions, never guesses, and you confirm every changed line before it ships.
- **ATS-safe.** One column, standard headings, plain selectable text, visible links. The PDF is checked for page count and line breaks.
- **Speaks the job's language without copying it.** It uses the posting's names for skills, tools and the role where they are true of you, and keeps your own wording for the rest.
- **Reads like you.** A checker flags common AI writing habits (em dashes, "not X but Y", trailing "-ing" clauses, repeated three-item lists, copied phrases) and words you never use.
- **Asks once.** One setup round with defaults, then only the final sign-off.

## Install

| Where | How |
|---|---|
| Most coding agents (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and others) | `npx skills add mohiddin7/resume-tribunal` |
| GitHub CLI | `gh skill install mohiddin7/resume-tribunal` |
| By hand | Copy `skills/resume-tribunal/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (most other agents) |
| Chat apps that accept skill uploads | Zip the `skills/resume-tribunal/` folder and upload it in the app's skills settings |

Optional: Python 3 enables the checker and automatic seats; `pip install reportlab` enables PDF output.

## Private chats for manual mode

The review is only blind if the other assistant starts with no memory of you. Checked October 2026; menus change.

| App | Use |
|---|---|
| ChatGPT | Temporary Chat |
| Claude | Incognito chat |
| Gemini | Temporary chat |
| Perplexity | Incognito |

Keep these chats outside any project, and copy each reply before closing the chat. A private chat stops the app remembering you; the provider may still keep the text for a period.

## The scripts

All three read only the files you name, make no network calls of their own, and write only their output.

```bash
python3 skills/resume-tribunal/scripts/check_resume.py resume.md --source my-notes.md --vocab job.md
python3 skills/resume-tribunal/scripts/make_pdf.py resume.md Resume.pdf
python3 skills/resume-tribunal/scripts/seats.py detect
```

- `check_resume.py` flags AI writing habits, ATS layout problems, hidden text, page length, and numbers that do not appear in your own material. Standard library only.
- `make_pdf.py` builds a one-column, text-based PDF with real links and reports every line whose second line holds only a few words. Needs reportlab.
- `seats.py` finds other AI command-line tools and runs each one read-only in an empty folder, with your existing login.

## Please read

- You are responsible for everything you submit. Check each employer's policy on AI use in applications. This skill edits out common AI phrasing; it does not make the resume your unaided work.
- This project runs no server and never receives your resume. The assistants you choose do, under their own terms. Leave out anything confidential to an employer, and turn off model training in each app.
- In a terminal, working files are kept in a `.tribunal/` folder. Delete it when you are done, and do not commit or sync it.
- The skill will not invent facts, add hidden text, or help with assessments or live interviews.
- This is general information, not career or legal advice.

## Layout

```
skills/resume-tribunal/
├── SKILL.md                 # instructions for the assistant
├── references/
│   ├── seats.md             # modes, model matching, manual cards
│   └── prompts.md           # the prompts and shared rules
└── scripts/
    ├── check_resume.py      # resume checker
    ├── make_pdf.py          # PDF builder
    └── seats.py             # runs other AI command-line tools
```

## License

MIT
