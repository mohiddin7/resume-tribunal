---
name: resume-tribunal
description: Use when a user wants to tailor, rewrite, audit, de-bias, or ATS-optimize a resume or CV against a job description, asks for a second opinion or multi-AI / model-council resume review, or wants a role-specific resume handbook, anti-AI-detection pass, or interview grill list built from their resume.
license: MIT
metadata:
  version: "1.0.0"
---

# Resume Tribunal

## Overview

One AI judging its own resume draft grades its own homework. Resume Tribunal seats **three independent AI assistants** that draft, cross-audit, and judge the resume **blind**: no seat knows the others exist, and inputs are anonymised, so no model's house style or self-preference wins by default.

- **Seat A (Presiding)** is you, the assistant this skill is installed on. You run Seat A's prompts yourself and do all judging and merging.
- **Seats B and C** are two other independent AI assistants the user opens in their own browser tabs. You hand the user copy-ready prompts for them and the user pastes the replies back.

All prompt templates live in [references/prompts.md](references/prompts.md). Load it at the start of Stage 1.

## The Blind-Seat Protocol (non-negotiable)

1. **Refer to the other assistants only as "Seat B" and "Seat C".** When you tell the user what to open, say: *"a separate AI assistant from a different company than this one, in a fresh chat"*, and Seats B and C must come from different companies from each other. Don't name, suggest, rank, or guess products or companies. If the user names them, keep calling them Seat B / Seat C.
2. **Every hand-off prompt is self-contained and blind.** It contains only the role, task, and inputs. It never mentions other seats, other AIs, a council, this skill, or that any input text was AI-written.
3. **Anonymise and shuffle.** Label drafts *Version 1/2/3* and audits *Feedback A/B/C*, in a random order that you write down in the run log. Seat A's own work must not always sit in the first slot.
4. **Judge in a clean context.** If you can start a subagent or fresh session, run judging prompts (P6, P7) there with only the labelled inputs. Otherwise state once: "Treating all three versions as anonymous; none gets priority."
5. **Never invent numbers, tools, or skills.** Missing metrics become placeholders like `[X%]` or `[p95 latency baseline]`. Unconfirmed tools or skills become `[dbt — only if used]`. The user fills them in.

## Intake (before Stage 1)

Collect these, asking for all missing ones in a single message:
- Target job description (cleaned text)
- Current resume, or raw career history
- Target role title and seniority
- Optional: career tracks to blend (e.g. "IC data scientist + fellowship leadership")
- How many other assistants the user can open: 2 (full tribunal), 1 (two-seat), or 0 (solo). With fewer than 2, warn once that the de-biasing is weaker, then continue.

If you have a filesystem, create `tribunal/` and save every input and output there (`jd.md`, `draft-A.md`, `audit-B.md`, `run-log.md`, …). Long runs outlive chat context.

## Stages

| # | Stage | Who runs it | Prompts | Keep |
|---|-------|-------------|---------|------|
| 1 | Independent drafts | Each seat, one chat each | P1→P4 in sequence | Each P4 resume |
| 2 | Blind cross-audit | Fresh chat; rotate A→B, B→C, C→A (each seat audits another seat's draft) | P5 | 3 audits |
| 3 | Merge | Presiding, clean context | P6a→P6b→P6c | Merged resume |
| 4 | Council review | P5 on merged resume in a fresh chat per seat, then Presiding runs P7a→P7d | P5, P7 | Council resume |
| 5 | Role handbook (recommended) | Seats B and C in deep-research/web mode run P8; Presiding runs P9 | P8, P9 | Handbook |
| 6 | Final compile and grill | Presiding: P10 (asks the user 2 questions), then P11 | P10, P11 | Final resume + grill list |

If Stage 5 was skipped, paste the P7d constraints in place of "the Handbook above" in P10 and P11.

Two-seat mode: drop Seat C, use two-way rotation, and leave the third slots out of P6/P7. Solo mode: run every prompt yourself, each stage in a fresh context where possible.

## Hand-off Card (use for every Seat B/C step)

```
### Seat B · Stage 1 · open a NEW chat
Send these one at a time and wait for each reply:
[P1 fully filled, in its own code block]
[P2 …] [P3 …] [P4 …]
Paste back only the final reply (the full resume) and label it "B-draft".
```

When Seats B and C get identical prompts (Stages 1 and 4), one card with two paste-back labels is fine. For Seat A, show short notes from P1–P3 and the full P4 draft.

Fill-in rule: replace every `{{…}}` before handing off. A hand-off that still contains `{{` is broken; fix it before sending.

After each card, tell the user exactly which label to paste back, then wait. Track progress in `run-log.md` (or a short checklist in chat).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Saying "paste this into <product>" | "Open a separate assistant from a different company, in a new chat" |
| Hand-off prompt says "another model wrote this" | Present inputs as plain text; P5 already states "zero context on how this was generated" |
| Seat A's draft always labelled Version 1 | Shuffle and log the mapping |
| Running P1–P4 for B and C yourself | Only the user can run Seats B/C; you run Seat A |
| Filling metric gaps with plausible numbers | Placeholders only; list them at the end for the user |
| Dumping the whole workflow at once | One stage at a time; finish each stage before showing the next card |

## Finish

Deliver the final resume (Markdown), the list of unfilled placeholders, and the grill list from P11. Then offer to export to .docx/PDF or to re-run Stage 6 for a different job description, reusing the handbook.
