# Resume Tribunal: a blind multi-AI resume council skill

**Resume Tribunal** is an open [Agent Skill](https://agentskills.io) (`SKILL.md`) that tailors, audits, and rewrites your resume or CV for a specific job description. Three independent AI assistants each draft and cross-examine the resume **blind**, and your main assistant judges and merges the results. You get a de-biased, ATS-ready resume that doesn't read as AI-written.

> Think of it as a manual "model council" for your resume: three independent seats, blind cross-audits, and one presiding judge.

## Why it works

- **Language models favor their own writing.** A 2025 hiring study tested 2,245 resumes. Models preferred resumes they had rewritten themselves **68–88%** of the time. Candidates whose resume came from the same model as the screener were shortlisted **23–60% more often** ([Laurito et al.](https://arxiv.org/abs/2509.00462)). One model drafting and grading your resume inherits that bias.
- **AI-written text is caught by people, not software.** No major ATS detects AI authorship. Recruiters reject *unedited* AI text: generic openings, metrics with no baseline, and words like "leveraged" and "spearheaded".
- **The tribunal handles both.** Drafts are anonymized and shuffled, every audit is blind, the final review goes to a different seat than the one that compiled the resume, and a script checks the mechanical rules.

## What you get

- A tailored Markdown resume (exports to Word, Google Docs, PDF, or LaTeX)
- Decoded "unwritten demands" from the job description
- Adversarial ATS scoring and rejection triggers
- AI-footprint and buzzword detection with a banned-token list
- Line-length rules (no 3-line bullets, no hanging words)
- A role-specific **Resume Handbook** built from deep research
- An **interview stress test** (a "grill list") with the questions a senior interviewer will use to test your claims
- `check_resume.py`, a dependency-free linter for banned words, bullet length, short second lines, repeated verbs, and placeholders you haven't filled in

## Install

The skill follows the open Agent Skills standard, so it works in any agent that reads `SKILL.md`.

**Any supported agent (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode, and others):**

```bash
npx skills add mohiddin7/resume-tribunal
```

**Manual install:** copy the `resume-tribunal/` folder into one of these directories:

| Agent | Path |
|---|---|
| Claude Code | `~/.claude/skills/resume-tribunal/` |
| Codex CLI, Gemini CLI, Copilot CLI (shared path) | `~/.agents/skills/resume-tribunal/` |
| Project-local (any agent) | `.agents/skills/resume-tribunal/` |

**Claude.ai / Claude Desktop:** zip the folder and upload it under *Settings → Capabilities → Skills*.

**Chat apps without skill support** (custom GPTs, Gems, Projects, Spaces): paste `SKILL.md` into the instructions field and upload `references/prompts.md` as a knowledge file.

## Use

Ask your assistant something like:

> "Tailor my resume to this job description with Resume Tribunal."

It will collect your job description and resume, then walk you through each stage. The assistant you installed the skill on presides. It gives you copy-ready prompts to paste into two other independent AI assistants (Seats B and C), and you paste their replies back. If you only have one or zero other assistants, it runs in two-seat or solo mode.

| Stage | What happens |
|---|---|
| 1. Independent drafts | Each seat decodes the JD, screens the resume adversarially, and drafts its own version |
| 2. Blind cross-audit | Each seat audits another seat's draft without knowing who wrote it |
| 3. Merge | The presiding seat merges the three drafts and three audits |
| 4. Council review | All seats audit the merged resume; the presiding seat builds a consensus checklist and refactors |
| 5. Role handbook | Deep research on what credible resumes look like for your role |
| 6. Compile and final review | The presiding seat compiles a resume that follows the handbook; a *different* seat reviews it and writes the interview stress test |

## Files

```
resume-tribunal/
├── SKILL.md                # agent instructions and the blind-seat protocol
├── references/
│   └── prompts.md          # 8 prompt templates plus the shared house rules
└── scripts/
    └── check_resume.py     # resume linter (Python 3, standard library only)
```

Lint any Markdown resume yourself:

```bash
python3 scripts/check_resume.py my-resume.md --line-chars 105
```

## License

MIT

---

*Keywords: AI resume skill, multi-model resume review, model council resume, ATS resume optimizer, CV tailoring, job description analysis, anti-AI-detection resume, resume handbook, interview preparation, Agent Skills, SKILL.md, Claude skill, Codex skill, Gemini CLI skill.*
