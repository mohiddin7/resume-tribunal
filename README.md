<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
    <img src="docs/assets/logo-light.svg" alt="Resume Tribunal" width="236" height="40">
  </picture>
</h1>

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black.svg)](https://agentskills.io)

**Tailor your resume to any job. Nothing made up.**

Resume Tribunal is a free add-on for AI apps (an "Agent Skill"). New to this? You can run it in the Claude app, free or paid, and use ChatGPT or Gemini for the second check. One AI rewrites your resume for a specific job using only facts you gave it. An AI made by a different company then checks the draft without being told who wrote it, so nothing gets exaggerated and no AI grades its own work.

One role from the [worked example](examples/operations-analyst/), before and after:

```
Before   - Helped improve on-time delivery
         - Utilized Excel for various reports

After    - Helped raise Dayton terminal on-time delivery from 81 to 93 percent over about three
           months, after the team moved one carrier's Friday pickups to another carrier.
         - Cut the Monday report on late deliveries for the operations manager from half a day's
           work to about 40 minutes by building it with Excel pivot tables and Power Query.

Rejected "from 4 hours to 40 minutes". The candidate had said "half a day", so that is what it says.
Rejected "Raised ...". The team made the change, so it says "Helped raise".
```

**Use a coding agent?** Run this in a terminal, then say *"Tailor my resume to this job: \<link\>"*.

```bash
npx skills add mohiddin7/resume-tribunal
```

**Never used a terminal?** [Start here](#new-to-this-start-here). No commands, and on a paid Claude plan, no download.

[Website](https://mohiddin7.github.io/resume-tribunal/) · [How it was made](https://mohiddin7.github.io/resume-tribunal/blog/how-resume-tribunal-was-made.html) · [Resume skills compared](https://mohiddin7.github.io/resume-tribunal/blog/resume-skills-compared.html)

## How it works

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/how-it-works-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/how-it-works-light.svg">
    <img src="docs/assets/how-it-works.svg" width="560" alt="How Resume Tribunal works. Step 1, you share your resume, the job link and a few words about what you did. Step 2, your AI writes it from your facts only, and a different company's AI checks it without being told who wrote it. Step 3, you approve each change and download a resume where every line is true.">
  </picture>
</p>

The second AI can be reached in four ways. The skill picks the first one that works for you and tells you which.

| Way | What happens | Your effort |
|---|---|---|
| **Automatic**, in a terminal with other AI tools installed ([Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code), [Codex](https://www.npmjs.com/package/@openai/codex), [Antigravity CLI](https://antigravity.google)) | The other AIs run by themselves on accounts you are already signed in to. Each runs read-only in an empty folder, so it cannot see or change your files. | A few minutes |
| **Copy and paste**, anywhere | Your assistant hands you a block of text. You paste it into another AI app (ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat or Perplexity, none preferred) and paste the reply back. | 1 round for a quick review, about 5 for a full council |
| **One platform**, where an app can ask several companies' AIs at once | The drafts and reviews run in one place | A few minutes |
| **One company only**, if you prefer | New chats of your own assistant review blind | A few minutes, and a weaker check |

**Full council** is the default when the other AIs run automatically: three AIs each write a draft, critique each other blind, and the best parts are merged before the check. **Quick review** is the default when you would be copying and pasting: one writer and one checker. Full council makes about eight calls against two and takes 10 to 15 minutes. It sends and receives about five times as much text, spread across your plans: about 30,000 tokens against 6,000 in the worked example, before each model's own reasoning.

Why three? It is the smallest group in which two can outvote one that is wrong. Aircraft flight computers and industrial safety systems run three units with two-out-of-three voting for that reason, and banks and auditors organise risk control as three lines of defence. For AI writing this is a design choice by analogy, and the checks that follow do not rely on it. Each AI runs at a strength similar to your main assistant, so no reviewer is much weaker than the writer.

## Why a second AI

Hiring managers have grown wary of AI-written resumes. In a vendor survey of 1,000 U.S. hiring managers, 76% said AI-written resumes make it harder to understand what a candidate actually did ([Resume Genius, 2026](https://resumegenius.com/blog/job-hunting/hiring-insights-report)). The worry has a basis: in a test on 25 synthetic resumes, AI rewriting with no safeguards added 2.5 to 5.4 false details per resume, such as tools the candidate never used ([Indukuri and Agrawal](https://arxiv.org/abs/2607.01457), preprint). An invented number is one you cannot defend when an interviewer asks about it.

The assistant that wrote a line is badly placed to catch it.

- **AI goes easy on its own work.** On checks with a right answer, model judges were up to [50% more likely or more](https://arxiv.org/abs/2604.06996) to pass a failed item when the output was their own (preprint). Used as resume screeners, models favoured summaries they had written over the human originals, with a quality-adjusted bias of 67% to 82% ([Xu, Li and Jiang](https://arxiv.org/abs/2509.00462), preprint).
- **An outside reviewer does better.** Across 37 models on reasoning tasks, checking by a different model family [beat both self-checking and checking within the same family](https://arxiv.org/abs/2512.02304). Those were maths and logic tasks, so for writing this is evidence by analogy.
- **Names and order sway AI judges.** Telling a model who wrote a text [changes its verdict](https://www.science.org/doi/10.1126/sciadv.adz2924), and so does [the order of the options](https://arxiv.org/abs/2410.02736). So the reviewer sees no names, and drafts arrive shuffled.
- **AIs from different companies still share mistakes.** On one benchmark, two models that were both wrong [gave the same wrong answer 60% of the time](https://arxiv.org/abs/2506.07962). So the last two checks do not depend on a model: a script flags every number that is missing from your own material, and you confirm each changed line.

**What it does not promise.** No study shows that several AIs write a better resume than one strong assistant, and no tool can promise interviews or a result from screening software. You get independent review, and a resume you can defend line by line.

## Questions people ask

**Is Resume Tribunal actually free?**
Yes. Resume Tribunal costs nothing and there's no sign-up. It runs inside AI apps you may already use, like Claude and ChatGPT. Their free plans are enough for a quick review. The thorough version sends more messages, so it runs more smoothly on a paid plan.

**I'm not a tech person. Can I still use Resume Tribunal?**
Yes. You add Resume Tribunal to the Claude app once, using the steps above, and then you just chat. There are no commands to type.

**Why can't I just ask ChatGPT to fix my resume?**
You can, and ChatGPT is fine for a quick tidy-up. The catch is that an AI checking its own writing tends to approve it, made-up numbers included. Resume Tribunal has a second AI, from a different company, check the draft without knowing who wrote it. A script then compares every number to what you actually said.

**Will Resume Tribunal make stuff up on my resume?**
No. Every number, tool and job title has to come from you, and a script checks that. If something is missing, Resume Tribunal asks you instead of guessing. You approve each changed line before you get the file.

**Will my resume get past the ATS robots?**
Nobody can honestly promise that. ATS is the software employers use to collect applications, and most of it sorts candidates. It rarely rejects anyone on its own. Resume Tribunal keeps your layout simple enough for that software to read, and checks the PDF's text before you send it. After that, a person reads it.

**Can a recruiter tell that AI wrote my resume?**
Resume Tribunal removes the usual giveaways, like long dashes and words such as "spearheaded", and keeps your own wording. It can't make the resume your unaided work, though. If an employer asks about AI use, be honest.

**Who gets to see my resume?**
Not us. Resume Tribunal has no server. Before anything goes to a second AI, your name, email, phone number and links are swapped for stand-ins like `<<NAME>>`, and you're asked first. The AI apps you use see the rest under their own terms.

**How long does Resume Tribunal take?**
About 5 minutes for a quick review, and about 15 for the thorough version, which we call the full council. If you copy and paste between apps yourself, plan on 20.

**What do I get at the end?**
Your finished resume as a PDF or Word file when your app can make files, and always as text you can paste into Word or Google Docs. You also get a list of what the job asks for that your resume doesn't show yet, plus the interview questions your resume is likely to prompt.

**Does Resume Tribunal work with Word files, or on my phone?**
Word files are fine: attach your .docx as it is. Phones work too, but copying text between two apps is easier on a laptop.

**What's warmhop™?**
A link tracker for resumes, made by the same person who made Resume Tribunal. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it.

## What makes it different

- **Truth first.** Every claim comes from you. Unknown numbers become questions, never guesses, and you confirm every changed line before it ships.
- **Readable by screening software (ATS-safe).** One column, standard headings, plain selectable text, visible links: the layout that applicant tracking systems are documented to parse. The PDF is checked for page count and line breaks.
- **Speaks the job's language without copying it.** It uses the posting's names for skills, tools and the role where they are true of you, and keeps your own wording for the rest.
- **Reads like you.** A checker flags common AI writing habits (em dashes, "not X but Y", trailing "-ing" clauses, repeated three-item lists, copied phrases) and words you never use.
- **Few questions.** One setup round with defaults you can accept with a "yes", then your sign-off on the claims.

## A worked example

A fictional operations coordinator applying for an operations analyst job, in full council mode with three assistants from three companies. See [examples/operations-analyst](examples/operations-analyst/).

- Each AI caught something the others missed, such as a draft that credited the candidate alone for a decision the team made.
- More than twenty enlarged or invented phrases were rejected, such as "root-cause tracking framework adopted by leadership" for a spreadsheet one supervisor used.
- The result is one page at 10.5 pt, with the job's unmet requirements listed for the candidate instead of papered over.
- You can verify it: the folder includes the candidate's own words, and one command shows that every number and name in the resume traces back to them.

A fresh agent ran the skill from its files alone: 8 calls, about 12 minutes, no failures. It is one run on one invented candidate, so it shows how the process works, not how it performs across many resumes.

## New to this? Start here

No commands needed. Pick where you use AI; each takes about two minutes to set up.

**Claude Pro or Max (no download).** In Claude, open Customize, then Plugins. Click Add, then Add marketplace, then Add from a repository, and paste `mohiddin7/resume-tribunal`. Install Resume Tribunal from the list.

**Claude free plan.** [Download resume-tribunal.zip](https://github.com/mohiddin7/resume-tribunal/releases/latest/download/resume-tribunal.zip) and keep it zipped. In Claude, open Customize, then Skills. Click +, Create skill, Upload a skill, and choose the zip. If it asks, switch on code execution.

**A coding agent** (Claude Code, Codex, Cursor and others). Send it one message; it asks your permission, installs Resume Tribunal, and starts:

```
Install the Resume Tribunal skill (npx skills add mohiddin7/resume-tribunal), then tailor my resume to this job: [paste the job link]
```

**Then:** start a new chat, attach your resume, paste the job link, and say "Tailor my resume to this job." If no second AI is connected, Resume Tribunal gives you one block of text to paste into ChatGPT or Gemini, and you paste the reply back.

Checked October 2026 against Claude's help pages; menus change.

## Install

| Where | How |
|---|---|
| Most coding agents (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and others) | `npx skills add mohiddin7/resume-tribunal` |
| Claude Code, as a plugin | `claude plugin marketplace add mohiddin7/resume-tribunal`, then `claude plugin install resume-tribunal@resume-tribunal` |
| GitHub CLI | `gh skill install mohiddin7/resume-tribunal` |
| By hand | Copy `skills/resume-tribunal/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (most other agents) |
| Chat apps that accept skill uploads | See [Start here](#new-to-this-start-here) |

Optional: Python 3 enables the checker and automatic seats; `pip install reportlab pypdf` enables PDF output and its text check.

## Private chats for copy and paste

The review is only blind if the other assistant starts with no memory of you. Checked October 2026; menus change.

| App | Use |
|---|---|
| ChatGPT | Temporary Chat |
| Claude | Incognito chat |
| Gemini | Temporary chat |
| Perplexity | Incognito |

Keep these chats outside any project, and copy each reply before closing the chat. A private chat stops the app remembering you; the provider may still keep the text for a period.

## The scripts

None of the four makes a network call of its own. `seats.py` starts the AI tools you chose, and those connect to their own services.

```bash
python3 skills/resume-tribunal/scripts/check_resume.py resume.md --source my-notes.md --vocab job.md
python3 skills/resume-tribunal/scripts/make_pdf.py resume.md Resume.pdf
python3 skills/resume-tribunal/scripts/seats.py detect
```

- `check_resume.py` flags AI writing habits, ATS layout problems, hidden text, page length, and numbers that do not appear in your own material. Standard library only.
- `make_pdf.py` builds a one-column, text-based PDF with real links, reports every line whose second line holds only a few words, and reads the text back out of the PDF the way screening software would. Needs reportlab; the read-back uses pypdf if installed.
- `prompt.py` fills the review prompts from your working files, shuffles the drafts, and pulls the resume out of each reply. Standard library only.
- `seats.py` finds other AI command-line tools and runs each one read-only in an empty folder, with your existing login. It refuses to send a prompt that still holds an email address or phone number.

## Please read

- You are responsible for everything you submit. Check each employer's policy on AI use in applications. This skill edits out common AI phrasing; it does not make the resume your unaided work.
- This project runs no server and never receives your resume. The assistants you choose do, under their own terms. Your name and contact details are replaced with stand-ins before anything goes to another AI, and you are asked first. Leave out anything confidential to an employer, and turn off model training in each app.
- In a terminal, working files are kept in a `.tribunal/` folder. Delete it when you are done, and do not commit or sync it.
- The skill will not invent facts, add hidden text, or help with assessments or live interviews.
- Disclosure: when a resume has links, the skill ends with one optional tip for warmhop™, a resume link tracker made by this project's author. The tip says so when it is shown. Nothing is sent to warmhop™, and the skill works the same without it.
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
    ├── prompt.py            # fills the prompts, extracts replies
    └── seats.py             # runs other AI command-line tools
examples/operations-analyst/ # a full run on a fictional candidate
manual-prompts/              # the original hand-run prompts
docs/                        # website and blog; build.py regenerates it
```

## License

MIT
