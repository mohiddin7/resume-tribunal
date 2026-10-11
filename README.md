# Resume Tribunal

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black.svg)](https://agentskills.io)

**Tailor your resume to a job, with a second AI checking the first.**

Resume Tribunal is a free add-on for AI apps (an "Agent Skill"). New to this? You'll run it in the free Claude app, and use ChatGPT or Gemini for the second check. One AI rewrites your resume for a specific job using only facts you gave it. An AI made by a different company then checks the draft without being told who wrote it, so nothing gets exaggerated and no AI grades its own work.

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

**Never used a terminal?** [Start here](#new-to-this-start-here). No commands needed.

[Website](https://mohiddin7.github.io/resume-tribunal/) · [How it was made](https://mohiddin7.github.io/resume-tribunal/blog/how-resume-tribunal-was-made.html) · [Resume skills compared](https://mohiddin7.github.io/resume-tribunal/blog/resume-skills-compared.html)

## How it works

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/how-it-works-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/how-it-works-light.svg">
    <img src="docs/assets/how-it-works.svg" width="620" alt="How Resume Tribunal works. You give your resume, the job posting and a few sentences in your own words. Your assistant writes a draft from your facts only. An AI from a different company checks it without being told who wrote it. A script flags AI writing habits, layout problems and numbers you never gave. You approve every changed line. You get a resume you can defend.">
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

**Do I need to know how to code?**
No. If you use the Claude app, you upload the skill once and then chat as usual. The steps are in [Start here](#new-to-this-start-here). The terminal route is quicker, but you can skip it.

**Is it free?**
The skill is. It runs on the AI apps you already use, and free plans work. Free plans have daily limits, and a long run can reach them, so the thorough version goes more smoothly on a paid plan.

**Why not just ask ChatGPT to fix my resume?**
You can, and for a quick tidy-up that's fine. The trouble starts when the same AI writes your resume and then tells you it's good. It tends to like its own work, and it will happily turn "half a day" into "4 hours". A second AI from another company catches more of that, and a script checks every number against what you actually said.

**Will it make things up?**
It's designed not to, and it checks. Every number, tool and job title has to come from you. If something's missing, it asks. Before you get the final file, you say yes or no to each changed line, and anything you don't confirm comes out.

**Will this get me past the ATS?**
No one can promise that. ATS is the software many employers use to collect and sort applications. This skill avoids the things known to confuse it: columns, tables, text in headers, images, hidden text. Then it checks that the PDF's text reads back correctly. In the end a person usually reads your resume, and it's written for them.

**Can recruiters tell an AI helped?**
Maybe. It removes the habits people spot most, like long dashes and words such as "spearheaded". It won't make the resume your unaided work, though. If an employer asks about AI use, tell the truth.

**Is my resume safe?**
This project never sees it. Your name, email, phone number and links are swapped for stand-in text such as <<NAME>> before anything goes to a second AI, and you're asked before anything is sent. The AI companies you use do see the text, under their own terms, so leave out anything confidential.

**How long does it take?**
About 5 minutes for a quick review when the other AI runs by itself, and about 15 for a full council. If you're copying and pasting by hand, allow 20 minutes or so.

**What's a "full council"?**
Three AIs from three companies each write a draft. Then they point out problems in each other's drafts without knowing who wrote which. The best parts are merged and checked again. It uses about five times as much AI time as a quick review.

**What's warmhop™?**
A resume link tracker made by the same person who made this skill. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it.

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

You do not need to be a programmer or run any commands. You need the Claude app, which is free: get it at [claude.ai](https://claude.ai) or from your phone's app store. Skills need one setting called "code execution" switched on, an on/off switch in the app's settings (checked October 2026).

1. [Download resume-tribunal.zip](https://github.com/mohiddin7/resume-tribunal/releases/latest/download/resume-tribunal.zip). Keep it zipped.
2. In the Claude app, open Customize, then Skills. Click "+", then "Create skill", then "Upload a skill", and choose the zip.
3. Start a new chat. Attach your resume, paste the job link, and type: "Tailor my resume to this job."
4. Answer its questions, or say "yes" to the suggestions.
5. When it shows you a block of text, paste it into a different company's AI app, such as ChatGPT or Gemini, in a private or temporary chat. Copy the reply and paste it back.
6. Confirm that every changed line is true.

Allow about 20 minutes. Your name and contact details are hidden before anything goes to the second AI, and you are asked before anything is sent.

- **Word files?** Yes. Attach your .docx resume as it is, or paste the text.
- **On a phone?** It works, but copying text between two apps is fiddly. A laptop is easier.
- **What do I get?** The finished resume as text you can paste into Word or Google Docs. When the app can make files, you also get a PDF or Word file.

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
