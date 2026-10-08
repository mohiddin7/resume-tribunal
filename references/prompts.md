# Resume Tribunal: Prompt Library (v2)

Eight prompts. Each one is self-contained: the inputs come first in XML tags and the task comes last. Before handing a prompt over, replace every `{{PLACEHOLDER}}`.

| Prompt | Stage | Run by |
|---|---|---|
| P1 Draft | 1 | Every seat, new chat |
| P2 Audit | 2 and 4 | Every seat, new chat |
| P3 Merge | 3 | Presiding, clean context |
| P4 Consensus Refactor | 4 | Presiding, clean context (audits come from Seats B and C) |
| P5 Role Research | 5 | Seats B and C, deep-research or web mode |
| P6 Handbook | 5 | Presiding |
| P7 Compile | 6 | Presiding |
| P8 Final Review | 6 | Seat B or C (never the presiding seat), new chat |

## Shared values

**`{{HOUSE_RULES}}`** always expands to the block below. Every writing prompt uses this one rule set, so the seats never get conflicting instructions.

```
<house_rules>
These rules exist because recruiters skim a resume in seconds and set aside resumes that read as unedited AI output or marketing copy.

1. Write in a grounded, specific, human voice. Prefer plain verbs such as Built, Cut, Shipped, Designed, Led, Ran, Migrated, Negotiated, Reduced, Launched.
2. Leave out these words and their variants. They are the most common tells of AI or marketing copy: {{BANNED_TOKENS}}.
3. Shape every bullet as action → method or tools → result against a baseline (for example "from 9% to 4%"). Put tools inside the bullet instead of only listing them in a skills block.
4. Each bullet fills either exactly one line or 1.5 to 1.7 lines. A second line holding only one to four words looks like an error, and three-line bullets don't get read.
5. Start each bullet with a different verb from the one before it.
6. Use only facts the candidate provided. Where a number, tool, or skill is unconfirmed, write a placeholder such as [X%], [p95 latency baseline], or [dbt, only if used], so the candidate can fill it in honestly.
7. Match the role's domain and seniority without copying distinctive phrases from the job description, so the resume reads as an earned career story rather than a mirror of the posting.
8. Write metrics as plain text (Recall@10, p95 latency, MAPE), not LaTeX, so they survive Word export and ATS parsing.
9. Use a single column, standard headings (Summary, Experience, Projects, Skills, Education), and one date style throughout, for example "2021 – Present". Parsers in common applicant tracking systems read this layout reliably.
</house_rules>
```

**`{{BANNED_TOKENS}}`:** spearheaded, leveraged, fostered, testament, driven, dynamic, synergy, utilized, passionately, proven track record, streamlined, orchestrated, transformative, revolutionized, catalyzed, pioneered, harness, paradigm-shifting, innovative, cutting-edge, state-of-the-art, highly scalable, revolutionary, robust, sophisticated, highly tailored, extremely efficient, self-starter, team player, results-oriented, detail-oriented, go-getter, delve, seamless

**`{{HANDBOOK}}`:** the Stage 5 handbook. If Stage 5 was skipped, use the `{{HOUSE_RULES}}` block instead.

**`{{TRACKS}}`:** the career threads to blend (for example "hands-on data science execution, and fellowship leadership and executive communication"). If the user doesn't name any, use "the candidate's full career history".

**`{{RESUME_SCHEMA}}`:**

```
# [Name]
[Email] | [Phone] | [LinkedIn] | [GitHub or Portfolio] | [City or Remote]

## Summary
3–4 sentences: the problems you solve, the scale you work at, and the impact you deliver.

## Experience
### [Company] — [City or Remote]
**[Title]** | [Start] – [End]
- 3–5 bullets per recent role, 1–3 for older roles

## Projects
### [Project]
- 2 bullets: the problem, what you built, the outcome

## Skills
**[Category]:** grouped tools and methods, without filler such as "Microsoft Office" or "communication skills"

## Education & Certifications
- **[Degree]**, [Institution], [Year]
```

---

## P1 · Draft

```
<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<candidate_resume>
{{RESUME}}
</candidate_resume>

{{HOUSE_RULES}}

<resume_schema>
{{RESUME_SCHEMA}}
</resume_schema>

You are a senior talent partner who has hired for this kind of role many times. Work in two parts.

Part 1: Diagnose. Be blunt and specific. The candidate gains more from an accurate critique than from encouragement.
- Core objective: in two sentences, the business problem this hire is meant to solve.
- Unwritten demands: what the hiring manager needs but did not write down (team bottlenecks, technical debt, scaling pressure).
- Keyword stack: the hard skills, tools, and methods that matter most.
- Benchmark hire: the background, scale, and metrics of someone who has succeeded in this role elsewhere.
- Screen result: a 0–100 match score with a one-line rationale based on hard-skill overlap and scope, the reasons a skimming recruiter would reject the resume, the requirements it misses, and any phrasing that reads as AI-generated. If the candidate is overqualified, show how to present that seniority as an asset.

Part 2: Rewrite. Write the complete resume following the house rules and the schema. Blend {{TRACKS}} into one upward trajectory. Rebuild the weakest bullets first.

Format: Part 1 as short headed sections. Part 2 as a single Markdown code block containing only the resume.
```

## P2 · Audit

```
<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<resume_under_review>
{{RESUME_TO_AUDIT}}
</resume_under_review>

You are an independent audit panel made up of a recruiter hiring for this exact role and a talent strategist who tracks hiring across the industry. You don't know how this resume was produced and have no stake in the candidate. Your critique is only useful if it is specific and unsentimental. Praise a line only where you can point to evidence.

Assess the resume in five areas:
1. Company fit: does it address this employer's explicit requirements, stack, and likely unwritten bottlenecks? Name the gaps and scale mismatches.
2. Market portability: would the same resume still read as a strong candidate at competitors, or is it so tuned to this posting that it looks artificial?
3. Skimmability: list every bullet that runs to 3 or more lines, has a second line of only one to four words, or doesn't open with a strong, distinct verb.
4. Narrative: do the career threads read as one coherent upward story, or as separate profiles stitched together?
5. AI footprint: point to predictable sentence patterns, artificial rhythm, and buzzwords. Give a verdict of PASS or FAIL on whether an experienced recruiter would suspect unedited AI writing.

Use exactly those five headings. Then add a final heading, "Last-mile fixes": an ordered list of the specific edits that would make the resume hold up, quoting each line you would change.
```

## P3 · Merge

```
<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<drafts>
<draft label="Version 1">{{VERSION_1}}</draft>
<draft label="Version 2">{{VERSION_2}}</draft>
<draft label="Version 3">{{VERSION_3}}</draft>
</drafts>

<audits>
<audit of="Version 1">{{FEEDBACK_1}}</audit>
<audit of="Version 2">{{FEEDBACK_2}}</audit>
<audit of="Version 3">{{FEEDBACK_3}}</audit>
</audits>

{{HOUSE_RULES}}

<resume_schema>
{{RESUME_SCHEMA}}
</resume_schema>

You are an executive resume editor merging three independent drafts into one master resume. The drafts are anonymous and their order is random. Judge every line on merit alone and give no draft priority because of its position.

For each section, keep the strongest bullets, metrics, and framing from any draft, and apply every audit point that holds up. Where the drafts conflict on a fact, keep the version that matches the original resume. If none of them does, use a placeholder.

Output:
1. Merge log: 5–10 bullets, each naming what you took from which version and which audit points you applied or rejected, with the reason.
2. The master resume, in one Markdown code block.
```

## P4 · Consensus Refactor

Include one `<feedback>` element per review received (two in a full tribunal, one in two-seat mode).

```
<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<current_resume>
{{MERGED_RESUME}}
</current_resume>

<reviews>
<feedback label="A">{{FEEDBACK_A}}</feedback>
<feedback label="B">{{FEEDBACK_B}}</feedback>
</reviews>

{{HOUSE_RULES}}

You are the lead editor on a panel that has received independent reviews of the same resume. The feedback labels are random.

First, build the consensus:
- Overlaps: issues raised by more than one reviewer. Fix all of them.
- Contradictions: where the reviewers disagree. Rule on each one and give your reason in one line.
- Unique finds: valid issues raised by only one reviewer.

Then write a master checklist in three groups: (1) technical, metric, and scope upgrades, (2) wording to cut or rewrite, (3) bullets that break the line-length rules.

Finally, rewrite the resume so that every checklist item is done.

Output: the consensus, then the checklist, then the final resume in one Markdown code block.
```

## P5 · Role Research

```
<target_role>
{{TARGET_ROLE}} ({{SENIORITY}})
</target_role>

Many applications for this role now arrive as near-identical, AI-tailored resumes, and screeners have grown skeptical of keyword-stuffed templates and of experience that looks like tutorial work. I need evidence on what makes a resume for this role credible.

Research practitioner communities (career and resume forums, domain communities, anonymous professional forums) and current job postings at respected employers. Cover:
1. Trust and screening: why reviewers doubt applicants for this role, the signs of an inflated resume, and how a recruiter, a hiring manager, and a senior practitioner each read a resume differently.
2. Clichés: this role's equivalent of "built a basic API wrapper", meaning the projects, tools, and claims that signal classroom-only experience.
3. Production signals: the decisions and trade-offs that prove real shipped work, and the metrics that matter for this role. Give formulas in LaTeX where the metric is quantitative, for example $F_1$, $MAPE$, $Recall@k$.
4. Skills section: how to group skills, and what counts as filler to leave out.
5. Language: the words that read as AI-generated or marketing copy, and the plain verbs senior practitioners use instead.
6. Layout: what gets through applicant tracking system parsers and a quick human scan (page budget, section order, date format, links).

Write a structured Markdown report. Keep the specifics and tie each claim to an observed hiring practice or a cited source.
```

## P6 · Handbook

```
<research source="A">
{{RESEARCH_A}}
</research>

<research source="B">
{{RESEARCH_B}}
</research>

You are a senior recruiter for {{TARGET_ROLE}} who also writes your team's screening guidelines. Synthesize the two research reports into one authoritative handbook. Merge what overlaps, resolve contradictions (and note how you resolved each), and drop anything you can't support. A downstream assistant will use this handbook as its rulebook for rewriting resumes, so make each rule concrete and testable.

Title: "The {{TARGET_ROLE}} Resume Handbook"

Sections:
1. The three gatekeepers: how the recruiter, the hiring manager, and the technical lead each read a resume.
2. Layout and ATS rules: single column, page budget, and section order by seniority.
3. Cliché blacklist: 3–6 statements that are clichés for this role, why each fails, and a credible rewrite of each.
4. Language: words to avoid and plain verbs to use instead.
5. Bullet formula: Task → Technique → Tools → Method → Metric, with one worked before/after example.
6. Metrics: what to measure for this role, the scale dimensions and costs involved, and their formulas (LaTeX is fine here, since the handbook is not a resume).
7. Interview defense: the questions screeners use to test whether claims are real.
8. Drafting system prompt: a copy-ready prompt that applies every rule above.

Write the handbook in the same plain, specific voice it prescribes. Output it as one Markdown document.
```

## P7 · Compile

```
<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<handbook>
{{HANDBOOK}}
</handbook>

<current_resume>
{{PANEL_RESUME}}
</current_resume>

{{HOUSE_RULES}}

Acting as a hiring panel for a {{SENIORITY}} {{TARGET_ROLE}} (a senior recruiter, the hiring manager, and a principal practitioner), compile a final resume that follows the handbook and the house rules.

Check every bullet three ways before you keep it:
1. Defensible: it describes real components, decisions, and trade-offs rather than tutorial-level patterns.
2. Handbook-compliant: it follows the bullet formula and ends with a metric anchored to a baseline, or with a placeholder.
3. Clean: it uses no avoided words.

Sources: start from the current resume. Choose the technical areas to emphasize yourself.

Before drafting, ask me for any raw work-history details that the current resume leaves out (responsibilities, outcomes, numbers), along with specific follow-up questions about my companies and roles. Then output the resume as `resume-v1`, and number later revisions v2, v3, and so on.
```

> **Tell the user:** a fuller answer gives a better result. Dictating is faster than typing. If the details are already in the resume, just say so, and answer the follow-up questions precisely.

## P8 · Final Review

Run this in Seat B or C, not the presiding seat, because models rate their own writing more highly.

```
<handbook>
{{HANDBOOK}}
</handbook>

<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<resume_under_review>
{{RESUME_V1}}
</resume_under_review>

You are a hiring director and the senior technical lead for {{TARGET_ROLE}}. Review this resume against the handbook as if the candidate will have to defend every line in a live interview. Be precise and direct. Flag any metric that has no baseline.

1. Scores from 0.0 to 10.0, with one line of justification each: ATS parseability and keyword coverage; quick-scan recruiter readability; hiring-manager business value (impact, scale, cost ownership); technical-lead scrutiny (reproducibility, trade-offs, rigor).
2. Credibility: lines that read as unedited AI output or inflation, metrics with no baseline, and claims too vague to believe.
3. Red flags: omissions that would lead to a quiet rejection at the technical screen, AI assistants listed as core skills, and inflated titles.
4. Line-by-line edits: for each bullet, give the issue and a rewrite that follows the handbook's bullet formula. Keep metrics in plain text.
5. Interview stress test: 3–5 hard questions a senior interviewer would ask about these claims. For each, explain what the question is really probing and how to answer it well.
6. The final resume, in one Markdown code block, ready to export to Word, Google Docs, or LaTeX.
```
