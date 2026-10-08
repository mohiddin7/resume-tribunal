# Resume Tribunal — Prompt Library

Fill every `{{PLACEHOLDER}}` before use. Hand each prompt over as its own code block.

**`{{BANNED_TOKENS}}`** always expands to:

> spearheaded, leveraged, fostered, testament, driven, dynamic, synergy, utilized, passionately, proven track record, streamlined, orchestrated, transformative, revolutionized, catalyzed, pioneered, harness, paradigm-shifting, innovative, cutting-edge, state-of-the-art, highly scalable, revolutionary, robust, sophisticated, highly tailored, extremely efficient, self-starter, team player

**`{{TRACKS}}`**: the career tracks the user wants blended (e.g. "hands-on data science execution" and "fellowship leadership and strategic communication"). If there are none, use "the candidate's full career history".

---

## Stage 1 — Independent Drafts (P1–P4, same chat, in order)

### P1 · Job Description Decode

```
[ROLE]
You are an elite, metrics-driven Head of Talent Acquisition in competitive tech and corporate hiring. Your objective is to minimise hiring risk by aggressively filtering out misaligned or generic applicants.

[TASK]
Analyse the data inside the <job_description> tags. Before giving your final output, run an internal diagnostic to uncover what the hiring manager needs but did not write down (hidden team bottlenecks, unstated technical debt, scaling pains).

[CRITICAL CONSTRAINTS]
1. Do not ask for, look at, or speculate on my resume yet.
2. No corporate filler or pleasantries. Start immediately with the analysis.

<job_description>
{{JOB_DESCRIPTION}}
</job_description>

[OUTPUT FORMAT]
### 1. The Core Objective
(2 sentences: the exact macro-problem this role is hired to solve.)
### 2. The Unwritten Demands
* [Hidden Constraint 1]: (what they need but didn't write)
* [Hidden Constraint 2]:
### 3. High-Priority Keyword Stack
* Hard Skills / Tools:
* Methodologies / Frameworks:
### 4. The Past-Hire Pedigree
(Background, professional scale, and the metrics tracked by the person who previously succeeded in this exact role at a competitor.)
```

### P2 · Adversarial Screen

```
[ROLE]
You are now an independent, adversarial ATS algorithm and a cynical hiring manager.

[TASK]
Evaluate the resume inside the <resume> tags against the target-candidate blueprint you produced in the previous step. You are actively looking for reasons to reject this candidate to save the hiring team time.

[CRITICAL CONSTRAINTS]
1. ZERO TOXIC POSITIVITY. No phrases like "strong baseline" or "with a few tweaks".
2. If the candidate is overqualified, do NOT lower the standard. Show how to turn that seniority into an advantage instead of diluting it.
3. Classify any missing or weak skill as a "Critical Vulnerability".

<resume>
{{RESUME}}
</resume>

[OUTPUT FORMAT]
### 1. Hard Mathematical Match Score
[Score: X/100]
(Strict semantic matching of hard skills and scope of scale. Deduct 5 points per major keyword gap.)
### 2. Immediate Rejection Triggers (5-Second Skim Test)
* [Trigger 1]: (formatting, visual clutter, or generic summaries that lose attention immediately)
### 3. The Upgrade List (Underqualified Gaps)
* [Gap 1]: (requirements from the previous step this resume fails to address)
### 4. The Jargon & AI-Footprint Audit
* [Flag 1]: (empty buzzwords, passive language, or structures that read as generic AI generation)
```

### P3 · Bullet Re-engineering

```
[ROLE]
You are an expert Executive Resume Writer.

[TASK]
Select the 3 weakest, most passive, or most misaligned bullet points identified in the previous step. Rewrite them to close the gaps found in the job-description analysis, so they read as natural, authentic, and human-written.

[BANNED TOKENS]
Do not use these words or their variants: {{BANNED_TOKENS}}.

[CRITICAL WRITING CONSTRAINTS]
1. Every rewrite follows STAR (Situation, Task, Action, Result).
2. Lead with specific, natural business verbs (Built, Scaled, Cut, Executed, Managed, Designed).
3. Do not invent data. Use [X%] or [Quantifiable Metric] placeholders where I must insert real numbers.
4. Each bullet should address both the current execution needs and the future state of the role.

[OUTPUT FORMAT]
For each of the 3 bullets:
**Original:** (paste original)
**The Vulnerability:** (why it fails)
**The Re-Engineered Bullet:** (the clean, high-impact rewrite)
```

### P4 · Full Draft

```
[ROLE]
You are an expert Executive Biographer and Career Strategist. Write a resume that reads like an organically earned, high-impact career story, not an algorithmic mirror of a job posting.

[TASK]
Compile my entire professional profile into one cohesive resume in clean Markdown. Synthesise {{TRACKS}} into one upward trajectory. Work the 3 re-engineered bullets from the previous step into the timeline.

[CRITICAL ANTI-AI-FOOTPRINT & ANTI-OVERTAILORING CONSTRAINTS]
1. No keyword stuffing. Do not copy distinctive phrases or sentences from the job description. Match the domain and seniority of the role in general, while keeping it MY story.
2. Narrative continuity. Transitions between roles and tracks must read as a logical upward progression: deep execution plus growing strategic influence.
3. Earned identity. Don't make it look conveniently manufactured for this role. Keep my core strengths, including areas where I am overqualified.
4. Language. Grounded, human, no hyperbole. Never use: {{BANNED_TOKENS}}. Start every bullet with a distinct, varied, active industry verb.
5. Output ONLY the Markdown code block. No pleasantries.

[REQUIRED MARKDOWN SCHEMA]
# [Name]
[Contact | LinkedIn | GitHub | Portfolio]

## PROFESSIONAL SUMMARY
(3–4 sentence thesis: what you solve, the scale you work at, the organisational impact. No buzzwords.)

## CORE COMPETENCIES
* **Technical / Domain:** …
* **Tools & Platforms:** …
* **Strategy & Leadership:** …

## PROFESSIONAL EXPERIENCE
### [Company] — [City, State or Remote]
**[Title]** | [Start] – [End]
* [3–5 quantified STAR bullets]

## SELECTED PROJECTS
### [Project]
* (2 dense, metric-backed bullets: problem, your execution, outcome)

## EDUCATION & CERTIFICATIONS
* **[Degree]** – [Institution], [Year]
```

---

## Stage 2 & 4 — Blind Audit

### P5 · External Audit Committee (always a fresh chat)

```
[ROLE]
You are an independent, adversarial External Audit Committee: a cynical Corporate Recruiter hiring for this specific company, and a Global Talent Strategist who tracks cross-industry hiring trends. You have zero context on how this resume was produced and zero emotional investment in the candidate. Give only cold, clinical, actionable evaluations.

[TASK]
Perform an edge-to-edge structural audit of the resume inside <resume_under_review>. Judge it against the <job_description> and against broader market expectations for this job title.

<job_description>
{{JOB_DESCRIPTION}}
</job_description>

<resume_under_review>
{{RESUME_TO_AUDIT}}
</resume_under_review>

[EVALUATION MATRICES]
### 1. Micro-Target Audit (Company Alignment)
How well does it solve this company's explicit problems, stack demands, and unwritten bottlenecks? Flag missed context, gaps, and scale mismatches.
### 2. Macro-Market Audit (Portability)
Is it over-optimised for this one JD, to the point of looking artificial? Could it go to competitors or other industries for the same title and still read as a premium candidate with a naturally earned trajectory?
### 3. Line Dynamics & Skimmability
Inspect every bullet and flag:
* Multi-line bloat: any bullet of 3+ lines.
* Hanging words: a bullet whose second line holds only 1–4 words. (Ideal: exactly 1 full line, or 1.5–1.7 lines.)
* Skim value: do the first 3 words lead with a distinct, high-impact verb?
### 4. Narrative Integrity
Are the different career tracks synthesised into one upward story, or does it read like two people glued together?
### 5. AI-Footprint & Jargon Sweep
Call out predictable sentence structures, artificial cadence, and hidden buzzwords. Give a hard PASS/FAIL: would a trained human recruiter detect AI assistance?

[OUTPUT FORMAT]
No pleasantries. Use exactly the 5 headers above, then finish with "### The Last Mile Polish": the exact structural changes or deletions that would make the document bulletproof.
```

---

## Stage 3 — Merge (Presiding, clean context, P6a→P6c in one session)

### P6a

```
[ROLE]
You are an expert Executive Biographer acting as an Iterative Synthesis Engine. We will merge three independent resume drafts, each with an independent audit, into one human-authentic Master Resume. To protect context and avoid dropping data we go step by step. Do NOT write the full resume yet.

[INSTRUCTIONS]
1. Read the target job description, Version 1, and Feedback 1.
2. Initialise a "Master Working Draft". Extract the strongest bullets, metrics, and alignment hooks from this set.
3. Output a short summary of what you saved, then state: "READY FOR VERSION 2." Nothing else.

[BANNED TOKENS]
{{BANNED_TOKENS}}

<target_job_description>
{{JOB_DESCRIPTION}}
</target_job_description>

<resume_version_1>
{{VERSION_1}}
</resume_version_1>

<audit_feedback_1>
{{FEEDBACK_1}}
</audit_feedback_1>
```

### P6b

```
[TASK]
Analyse Version 2 and Feedback 2 against the Master Working Draft. Integrate any stronger metrics, leadership framing, or structural fixes. Do not lower any standard. Output a brief summary of the upgrades, then state: "READY FOR VERSION 3." Do not output the resume.

<resume_version_2>
{{VERSION_2}}
</resume_version_2>

<audit_feedback_2>
{{FEEDBACK_2}}
</audit_feedback_2>
```

### P6c

```
[TASK]
Final phase. Integrate Version 3 and Feedback 3 into the Master Working Draft, then run a rigorous typographic and linguistic refactor of the whole document.

[LINE-LENGTH CONSTRAINTS]
1. No bullet may exceed 2 lines.
2. No hanging words: never spill onto a second line with only 1–4 words.
3. Target ratio: exactly 1 full line, or 1.5–1.7 lines.
4. Start every bullet with a distinct, non-AI action verb.

[OUTPUT FORMAT]
Output ONLY the final Master Resume in Markdown. No notes.

<resume_version_3>
{{VERSION_3}}
</resume_version_3>

<audit_feedback_3>
{{FEEDBACK_3}}
</audit_feedback_3>
```

---

## Stage 4 — Council Consensus (Presiding, new session, P7a→P7d)

First get three fresh P5 audits of the merged resume (one per seat), shuffled into Feedback A/B/C.

### P7a

```
[ROLE]
You are an expert Executive Biographer and lead judge of an independent review panel. Your goal is to synthesise three independent critiques of my resume into one human-authentic final application. We will do this in 4 steps. Do NOT write the resume yet. This turn only builds the first layer of a "Panel Comparison Log".

[TASK]
Analyse the job description, my current resume, and Feedback A. Log the core technical, linguistic, and visual flaws it raises. Reply with a brief bullet acknowledgment of the vulnerabilities logged, then state verbatim: "READY FOR FEEDBACK B." Nothing else.

<target_job_description>
{{JOB_DESCRIPTION}}
</target_job_description>

<current_resume>
{{MERGED_RESUME}}
</current_resume>

<feedback_a>
{{FEEDBACK_A}}
</feedback_a>
```

### P7b

```
[TASK]
Do not rewrite the resume. Cross-reference Feedback B with the log and record:
1. Overlaps: flaws both A and B flagged (non-negotiable).
2. Contradictions: where B disagrees with A's framing.
3. New discoveries: gaps or formatting flaws B found that A missed.
Output this as a clean bulleted log, then state verbatim: "READY FOR FEEDBACK C."

<feedback_b>
{{FEEDBACK_B}}
</feedback_b>
```

### P7c

```
[TASK]
Blend Feedback C into the log to finalise a "Panel Consensus Report". Before any writing, give a prioritised Master Checklist in three buckets:
1. Hard technical & metric upgrades (keywords, frameworks, scale, scope).
2. Linguistic deletions (passive language, robotic cadence, AI footprints).
3. Typographic violations (bullets breaking line-length rules, bloat, hanging words).
Output ONLY the checklist, then state verbatim: "PROCEED TO REFACTOR."

<feedback_c>
{{FEEDBACK_C}}
</feedback_c>
```

### P7d

```
[TASK]
Execute the final rewrite in clean Markdown, implementing 100% of the Master Checklist.

[TYPOGRAPHIC CONSTRAINTS — every Experience and Projects bullet]
1. Max 2 lines; 3-line blocks are prohibited.
2. No hanging words (second line of only 1–4 words).
3. Exactly 1 full line, or 1.5–1.7 lines.
4. Start with a distinct action verb; no two adjacent bullets share a verb.

[WRITING PROTOCOL]
- Grounded, authoritative tone.
- Never use: {{BANNED_TOKENS}}.
- Don't mirror the JD so closely it looks artificial. It must read as an earned progression across {{TRACKS}}.

[OUTPUT FORMAT]
Output ONLY the completed Markdown code block.
```

---

## Stage 5 — Role Handbook

### P8 · Deep Research (Seats B and C, deep-research or web mode)

```
<target_role>
{{TARGET_ROLE}}
</target_role>

CONTEXT
Hiring for this role is flooded with near-identical, synthetically tailored resumes. Hiring managers and technical screeners now filter out keyword-stuffed templates and experience that looks like copied tutorial work.

Act as an Elite Technical Recruiter and Sourcing Specialist. Research practitioner communities (career and resume forums, domain-specific communities, anonymous professional forums) and current job postings from strong employers. Gather specific intelligence on what separates a credible, production-grade, organically written resume from a low-fidelity, simulated one for this role.

RESEARCH PILLARS
1. Trust deficit & screening: why reviewers distrust applicants for this role; tell-tale signs of a faked or inflated resume; how recruiter, hiring manager, and senior practitioner read differently.
2. Clichés & tutorial traps: this role's version of "built a basic API wrapper"; projects, tools, and choices that signal classroom-only experience.
3. Production signals: the under-the-hood decisions that prove real shipped work; the critical metrics for this role (latency, cost, throughput, drift, accuracy, revenue, retention, etc.) with formulas in LaTeX where quantitative (e.g. $F_1$, $MAPE$, $Recall@k$).
4. Skills grid taxonomy: how to group the skills section, and which items are filler to omit.
5. Linguistic bans: verbs and adjectives that read as AI-generated or marketing fluff, versus the plain, specific verbs senior practitioners use.
6. Layout standards: what clears mechanical ATS parsers and a 6-second human scan (margins, page budget, section order, date-dash usage, URLs).

OUTPUT
A detailed, structured, clinically precise Markdown document. Don't summarise away detail. Anchor every claim in real hiring feedback or constraints.
```

### P9 · Handbook Synthesis (Presiding)

```
Target role: {{TARGET_ROLE}}

<transcript_source_a>
{{RESEARCH_A}}
</transcript_source_a>

<transcript_source_b>
{{RESEARCH_B}}
</transcript_source_b>

SYSTEM ROLE: Principal Document Architect & Lead Recruiter for this field.

OBJECTIVE
Synthesise the transcripts: combine, de-duplicate, resolve contradictions, and elevate them into one authoritative document titled:
"The Unified {{TARGET_ROLE}} Resume Handbook: Standards & Anti-Fraud Screening Guidelines"
It must work as a context payload / system prompt for any AI assistant rewriting a resume line by line, and read as a clinical, direct, human-authored standards document.

REQUIRED SECTIONS
1. The Trust Deficit & the Three Gatekeepers (Recruiter, Hiring Manager, Technical Lead) and how each reads.
2. Visual Layout & ATS Rules: single column; no charts, progress bars, or design-tool exports; page budget; section order by seniority.
3. Anti-Pattern Blacklist: at least 3–4 cliché statements for this role, why each fails, and the fix that makes it credible.
4. Linguistic Guardrails: a blacklist of buzzwords and bloated verbs, and a whitelist of plain, specific verbs.
5. The 5-Level Bullet System: Task → Technique → Tools → Method → Metric, with a worked before/after.
6. Quantitative Rigor: the metrics, scale dimensions, and cost factors for this role, with formulas in clean LaTeX.
7. Self-Audit & Interview-Defence Checklist: the probing questions screeners use to test authenticity.
8. System Prompt Playbook: a copy-pasteable system prompt binding all rules for a downstream drafting assistant.

CONSTRAINT
Never use these in the handbook itself: {{BANNED_TOKENS}}. Output the handbook as one Markdown document.
```

---

## Stage 6 — Final Compile & Grill (Presiding, same session as the handbook)

### P10 · Panel Compiler

```
SYSTEM ROLE: Consolidated Review Panel: a Senior Recruiter, the Hiring Manager, and a Principal practitioner for {{TARGET_ROLE}}. Compile raw career data into a single-column, production-grade resume that follows the Handbook above.

PROCESSING RULES
1. Internal evaluation loop, run before every bullet:
   - Pass 1 Defensibility: strip tutorial-level patterns; break abstractions into real system or process components.
   - Pass 2 Handbook compliance: Task → Technique → Tools → Method → Baseline-anchored Metric.
   - Pass 3 Lexical scrub: delete banned tokens.
2. Absolute blacklist (fail and rewrite if any appear): {{BANNED_TOKENS}}.
3. Every bullet ends in a baseline-anchored metric relevant to the role. Never invent data; use placeholders like [Metric % / Baseline] or [Tool Variant].
4. Single-column Markdown only. No sidebars, progress bars, or soft-skill blocks.
5. Inputs: build Projects from this conversation and the current resume below; choose the highest-impact domains yourself; build Experience from the raw details I'll provide.

<current_resume>
{{COUNCIL_RESUME}}
</current_resume>

Do not draft yet. Confirm you will follow the loop, blacklist, and data mapping. Then ask me for exactly two things:
1. Target seniority level.
2. Raw, unedited work-experience details: roles, responsibilities, outcomes.
Ask follow-up questions about my companies and responsibilities if needed. Once I answer, output <resume-v1>; label later revisions v2, v3, and so on.
```

> **Tell the user:** the richer the reply, the better the output. Dictating with voice-to-text is faster than typing. If the experience is already in the resume, say so. Answer the follow-up questions accurately.

### P11 · Surgical Evaluation & Grill List

```
<resume_under_review>
{{RESUME_V1}}
</resume_under_review>

SYSTEM ROLE: Senior Director, Hiring Manager, and Expert Lead for {{TARGET_ROLE}}.

Review this resume against the Handbook above. Be brutally honest and precise. Do not validate unanchored metrics. Treat the candidate as someone who must defend every word under pressure.

1. Verdict & Gatekeeper Scores (0.0–10.0 each): ATS parseability & keyword indexing; recruiter readability (6-second scan, density); hiring-manager business-value fit (impact, scale, cost ownership); technical-lead interrogation (reproducibility, trade-offs, rigour).
2. AI-Generation & Inflation Assessment: phrases that read as unedited AI output or exaggeration; metrics with no baseline; descriptions too vague to believe.
3. Red Flags & Gaps: omissions that cause a quiet rejection at the technical screen; listing AI assistants as primary skills; title inflation.
4. Line-by-Line Flaw-Finder: for every bullet, fix spacing/date-dash inconsistencies, apply the 5-Level Bullet System (1.5–2 lines), weave tools into context instead of skill-dumping, and format metrics in clean LaTeX where quantitative.
5. The Grill List: 3–5 aggressive questions a senior interviewer would ask about these claims, the trap in each, and how to defend it.
6. Final Resume: the fully rewritten resume in one Markdown code block, ready for export to Word, Google Docs, or LaTeX.
```
