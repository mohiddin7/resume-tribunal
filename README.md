<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
    <img src="docs/assets/logo-light.svg" alt="Resume Tribunal" width="236" height="40">
  </picture>
</h1>

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black.svg)](https://agentskills.io)

**Not getting shortlisted? Fix your resume for the job in 2 minutes of your time, without the AI making anything up.**

Resume Tribunal is a free add-on for AI apps (an "Agent Skill"). It works in any AI chat app, such as ChatGPT, Gemini or Claude, and in coding agents. One AI rewrites your resume for a specific job, using only facts you gave it. An AI from a different company then checks the draft for anything exaggerated or made up, without being told who wrote it.

One role from the [worked example](examples/operations-analyst/), before and after:

```
Before   - Helped improve on-time delivery
         - Utilized Excel for various reports

After    - Traced one carrier's late Dayton terminal loads to its Friday pickups in six months of
           Excel data; after the team moved them to another carrier, on-time delivery there went
           from 81% to 93% over about three months.
         - Built the Monday late-delivery report in pivot tables and Power Query; it took half a
           day, now about 40 minutes.

Rejected "driving the rerouting decision". The candidate wrote "we moved those loads".
Rejected dropping "simple" from "simple SQL queries". It is the candidate's own word.
```

**Use a coding agent?** Run this in a terminal, then say *"Tailor my resume to this job: \<link\>"*.

```bash
npx skills add mohiddin7/resume-tribunal
```

**Never used a terminal?** [Start here](#new-to-this-start-here): paste one message into any AI chat app.

[Website](https://warmhop.com/r/wLWYpGNJ?ref=readme-top&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal) · [How it was made](https://warmhop.com/r/9R3btCCB?ref=readme-top&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal) · [Resume skills compared](https://warmhop.com/r/nHiARynB?ref=readme-top&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal)

## How it works

You paste the job and your resume, then check the changes. That takes about 2 minutes of your time, and the AIs do the rest.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/how-it-works-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/how-it-works-light.svg">
    <img src="docs/assets/how-it-works.svg" width="620" alt="How Resume Tribunal works, in six steps: share the job and your resume; your AI rewrites it for the job; a second AI from a different company reads it like the hiring manager; a script checks the details; you approve the changes; your resume is ready to send.">
  </picture>
</p>

1. Drop in the job and your resume: paste the link into any AI chat.
2. Your AI rewrites it for the job, using only your facts.
3. A second AI, from a different company, checks it like a hiring manager, looking for anything made up.
4. A script checks the details: layout, AI phrases and numbers.
5. You check the changes and say yes to the ones you want.
6. It's ready to send, with the interview questions you're likely to get.

In a full council, up to three AIs from different companies each write a draft and critique the others' drafts before they are merged.

The second AI can be reached in four ways. The skill picks the first one that works for you and tells you which.

| Way | What happens | Your effort |
|---|---|---|
| **Automatic**, in a terminal with other AI tools installed ([Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code), [Codex](https://www.npmjs.com/package/@openai/codex), [Antigravity CLI](https://antigravity.google)) | The other AIs run by themselves on accounts you are already signed in to. Each runs read-only in an empty folder, so it starts with none of your files around it and cannot change any. | A few minutes |
| **Copy and paste**, anywhere | Your assistant hands you a block of text. You paste it into another AI app (ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat or Perplexity, none preferred) and paste the reply back. | 1 round for a quick review, about 5 for a full council |
| **One platform**, where an app can ask several companies' AIs at once | The drafts and reviews run in one place | A few minutes |
| **One company only**, if you prefer | New chats of your own assistant review blind | A few minutes, and a weaker check |

**Full council** is the default when two or more other AIs run automatically: three AIs each write a draft, critique each other blind, and the best parts are merged before the check. **Quick review** is the default when you would be copying and pasting: one writer and one checker. Full council makes about eight calls against two, and took 27 to 37 minutes in the [recorded example runs](https://warmhop.com/r/mQSvf2z3?ref=readme-modes&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal). It sends and receives about five times as much text, spread across your plans: about 30,000 tokens against 6,000 in the worked example, before each model's own reasoning.

Why three? Each draft gets read by two AIs that didn't write it, so no single model's habits decide the merge. That's a design choice, not proof of a better resume, and the checks after it don't depend on it. Each AI runs at a strength similar to your main assistant or above where its company offers one; where none does, the skill uses the strongest it has, says so, and defaults to a quick review.

## Why a second AI

Hiring managers have grown wary of AI-written resumes. In a vendor survey of 1,000 U.S. hiring managers, 76% said AI-written resumes make it harder to understand what a candidate actually did ([Resume Genius, 2026](https://resumegenius.com/blog/job-hunting/hiring-insights-report)). The worry has a basis: in a test on 25 synthetic resumes, AI rewriting with no safeguards added 2.5 to 5.4 false details per resume, such as tools the candidate never used ([Indukuri and Agrawal](https://arxiv.org/abs/2607.01457), preprint). An invented number is one you cannot defend when an interviewer asks about it.

- **AI goes easy on its own work.** On checks with a right answer, model judges could be [more than 50% more likely](https://arxiv.org/abs/2604.06996) to pass a failed item when the output was their own (preprint). Used as resume screeners, models favoured summaries they had written over the human originals, with a quality-adjusted bias of 67% to 82% ([Xu, Li and Jiang](https://arxiv.org/abs/2509.00462), preprint).
- **An outside reviewer does better.** Across 37 models on reasoning tasks, checking by a different model family [beat both self-checking and checking within the same family](https://arxiv.org/abs/2512.02304). Those were maths and logic tasks, so for writing this is evidence by analogy.
- **Names and order sway AI judges.** Telling a model who wrote a text [changes its verdict](https://www.science.org/doi/10.1126/sciadv.adz2924), and so does [the order of the options](https://arxiv.org/abs/2410.02736). So the reviewer sees no names, and drafts arrive shuffled.
- **AIs from different companies still share mistakes.** On one benchmark, two models that were both wrong [gave the same wrong answer 60% of the time](https://arxiv.org/abs/2506.07962). So the last two checks do not depend on a model: a script flags numbers and names it cannot find in your own material, and you confirm each changed line.

**What it does not promise.** No study shows that several AIs write a better resume than one strong assistant, and no tool can promise interviews or a result from screening software. What you get is a check by an AI that didn't write the draft, and the final say on every changed line.

## Questions people ask

**Is Resume Tribunal actually free?**
Yes. Resume Tribunal costs nothing and there's no sign-up. It runs inside AI apps you may already use, like Claude and ChatGPT. Their free plans are enough for a quick review. The thorough version sends more messages, so it runs more smoothly on a paid plan.

**I'm not a tech person. Can I still use Resume Tribunal?**
Yes. You paste one message into any AI chat app, like ChatGPT, Gemini or Claude, attach your resume, and answer a couple of questions. There are no commands to type.

**Why can't I just ask ChatGPT to fix my resume?**
You can, and ChatGPT is fine for a quick tidy-up. The catch is that an AI checking its own writing tends to approve it, made-up numbers included. Resume Tribunal has a second AI, from a different company, check the draft without knowing who wrote it. A script then flags any number it can't find in what you said.

**Will Resume Tribunal make stuff up on my resume?**
It is built not to. Every number, tool and job title has to come from you; a script flags any it cannot find in your words, and the second AI checks each line against them. If something is missing, Resume Tribunal asks you instead of guessing. You approve each changed line before you get the file.

**Will my resume get past the ATS robots?**
Nobody can honestly promise that. ATS is the software employers use to collect applications, and most of it sorts candidates. It rarely rejects anyone on its own. Resume Tribunal keeps your layout simple enough for that software to read, and checks the PDF's text before you send it. After that, a person reads it.

**Can a recruiter tell that AI wrote my resume?**
Resume Tribunal removes the usual giveaways, like long dashes and words such as "spearheaded", and keeps your own wording. It can't make the resume your unaided work, though. If an employer asks about AI use, be honest.

**Who gets to see my resume?**
Not us. Resume Tribunal has no server. Before anything goes to a second AI, your name, email, phone number and links are swapped for stand-ins like `<<NAME>>`, and you're asked first. The AI apps you use see the rest under their own terms.

**How long does Resume Tribunal take?**
About 2 minutes of your time for a quick review: you answer a few questions and approve the changes, and the AIs do the rest on their own. In the eight recorded example runs, a quick review took 6 to 37 minutes from start to finish, most under 15, and a full council 27 to 37. If you copy and paste between two apps yourself, add a few minutes.

**What do I get at the end?**
Your finished resume as a PDF or Word file when your app can make files, and always as text you can paste into Word or Google Docs. You also get a list of what the job asks for that your resume doesn't show yet, plus the interview questions your resume is likely to prompt.

**Does Resume Tribunal work with Word files, or on my phone?**
Word files are fine: attach your .docx as it is. Phones work too, but copying text between two apps is easier on a laptop.

**Something went wrong. Who do I tell?**
Email [tribunal@warmhop.com](mailto:tribunal@warmhop.com) with what happened and which AI app you used. Leave your resume out unless we ask. You can also open an issue on GitHub.

**What's warmhop™?**
A link tracker for resumes, made by the same person who made Resume Tribunal. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it.

## What makes it different

- Every claim comes from you. When a number is missing, it asks you, and you confirm each changed line before you get the file.
- The layout is one column with standard headings, plain selectable text and visible links, which applicant tracking systems (ATS) are documented to parse. The PDF is checked for page count and line breaks.
- It uses the posting's names for skills, tools and the role where they're true of you, and keeps your own wording for the rest.
- A checker flags common AI writing habits (em dashes, "not X but Y", trailing "-ing" clauses, repeated three-item lists, copied phrases) and words you never use.
- You answer one setup round, with defaults you can accept with a "yes", then sign off on the claims.

## A worked example

A fictional operations coordinator applying for an operations analyst job, in full council mode with three assistants from three companies. See [examples/operations-analyst](examples/operations-analyst/).

- Each AI caught something the others missed, such as "half a day" being the previous person's time, or "Carrier management" borrowed from the posting into a Skills list.
- Enlarged or invented phrases were rejected, such as "driving the rerouting decision" for a move the team made, and an example of what the candidate's SQL looks up, which they never gave.
- The result is one page at 10.5 pt, with the job's unmet requirements listed for the candidate instead of papered over.
- You can verify it: the folder includes the candidate's own words, and one command checks that the resume's numbers and names appear in them.

A fresh agent ran the skill from its files alone: 8 calls, about 19 minutes including the candidate's answers, no failures. It is one run on one invented candidate, so it shows how the process works, not how it performs across many resumes.

## New to this? Start here

Works with any AI app and any model. No commands, no account with us.

**In an AI chat app** (ChatGPT, Gemini, Claude, Perplexity, Grok, Copilot, DeepSeek, Le Chat): open a new chat, attach your resume, and paste this with your job link at the end.

```
Read https://tribunal.warmhop.com/resume-tribunal.md and follow it to tailor my resume to this job: [paste the job link]
```

A quick review takes about 2 minutes of your time. If your app can't open links, download [resume-tribunal.md](docs/resume-tribunal.md) and attach it too.

**In a coding agent** (Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, Grok Build, OpenCode): send this. It asks your permission, installs Resume Tribunal, and starts.

```
Install the Resume Tribunal skill (npx skills add mohiddin7/resume-tribunal), then tailor my resume to this job: [paste the job link]
```

**Save it as a skill** so you never paste the link again. Download [resume-tribunal.zip](https://warmhop.com/r/ank5M2Qe?ref=readme-install&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal) and upload it once:

- Gemini: Settings, Skills, Upload (personal accounts, 18 and over).
- Claude: Customize, Skills, +, Upload a skill. On Pro or Max, skip the download: Customize, Plugins, Add marketplace, `mohiddin7/resume-tribunal`.
- ChatGPT, Grok, Perplexity: look for Skills in your settings. Which plans have it varies.

Checked October 2026 against each app's help pages; menus change.

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
- Disclosure: when a resume has links, the skill ends with one optional tip for warmhop, a resume link tracker made by this project's author. The tip says so when it is shown. Nothing is sent to warmhop, and the skill works the same without it.
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

## Support

Found a problem, or need help? Email [tribunal@warmhop.com](mailto:tribunal@warmhop.com) or [open an issue](https://warmhop.com/r/sdT9x8DB?ref=readme-support&utm_source=readme&utm_medium=referral&utm_campaign=resume-tribunal). Please leave your resume out of the email unless we ask for it.

## License

MIT
