---
name: resume-tribunal
description: Tailors and rewrites a resume or CV for a specific job description. Three independent AI assistants each draft and cross-audit the resume blind, and the host assistant merges their work. Use when a user wants to tailor, rewrite, audit, de-bias, or ATS-optimize a resume or CV; asks for a second opinion or a multi-AI / model-council resume review; or wants a role-specific resume handbook, an AI-detection cleanup, or interview questions that test their resume's claims.
license: MIT
metadata:
  author: mohiddin7
  version: "2.0.0"
---

# Resume Tribunal

## Why this works

Language models favor their own writing. In a 2025 hiring study, models preferred resumes they had rewritten themselves 68–88% of the time ([Laurito et al.](https://arxiv.org/abs/2509.00462)), and judge models also show strong position bias. A resume written and graded by one model inherits that model's blind spots. Resume Tribunal splits the work across **three independent assistants** and keeps every hand-off **blind**, so each line has to win on merit.

- **Seat A (presiding)** is you, the assistant this skill is installed on. You run Seat A's prompts yourself and handle the merging and judging.
- **Seats B and C** are two other independent AI assistants that the user opens in separate tabs. You give the user copy-ready prompts for them, and the user pastes the replies back to you.

The prompts are in [references/prompts.md](references/prompts.md). Read that file before Stage 1.

## Blind-seat protocol

The de-biasing only works if no seat can recognize another seat's work, or its own. So:

1. **Refer to the other assistants only as Seat B and Seat C.** When telling the user what to open, say "a separate AI assistant from a different company than this one, in a new chat", and ask the user to pick Seats B and C from two different companies too. Leave that choice to the user rather than checking it yourself. Name no products or companies, even if the user does. If they ask which one is better, explain that the seats are interchangeable by design.
2. **Keep hand-off prompts self-contained.** A prompt contains its role, its inputs, and its task, and nothing that mentions other assistants, a council, this skill, or the fact that any input was written by AI.
3. **Anonymize, strip, and shuffle.** Pass on only the resume code block from each reply. Leave out any diagnosis, scores, or commentary, because they would bias the next reader. In Stages 3 and 4, assign the Version 1/2/3 and Feedback A/B/C labels at random and record the mapping in the run log.
4. **Judge in a clean context.** Run Seat A's P2 audit, P3, and P4 in a subagent or fresh session that sees only the labeled inputs, when you can. Otherwise, tell the user once that you are treating all versions as anonymous.
5. **Use only the candidate's own facts.** Every unconfirmed number, tool, or skill becomes a placeholder for the user to fill in.

## Intake

Ask for everything that's missing in one message:
- The job description
- The current resume, or raw career history
- Target role title and seniority
- Optional: career threads to blend (for example "IC data science plus fellowship leadership")
- How many other assistants the user can open: 2 (full tribunal), 1 (two seats), or 0 (solo). With fewer than 2, say once that the de-biasing will be weaker, then carry on.

If you have file access, create a `tribunal/` folder and save every input and output there, including `run-log.md`, so the run survives long sessions.

## Stages

| # | Stage | Who | Prompt | Result |
|---|---|---|---|---|
| 1 | Independent drafts | Every seat, new chat | P1 | 3 drafts |
| 2 | Blind cross-audit | New chat, rotated: B audits A's draft, C audits B's, A audits C's | P2 | 3 audits |
| 3 | Merge | Presiding, clean context | P3 | Master resume |
| 4 | Panel review | Seats B and C each run P2 on the master resume in a new chat. Seat A doesn't audit its own merge. Then Presiding runs P4 | P2, P4 | Panel resume |
| 5 | Role handbook (recommended) | Seats B and C run P5 in deep-research or web mode, then Presiding runs P6 | P5, P6 | Handbook |
| 6 | Compile and final review | Presiding runs P7. Seat B or C runs P8, with the handbook included | P7, P8 | Final resume and interview stress test |

- **Skipped Stage 5:** fill `{{HANDBOOK}}` with the house rules.
- **Two-seat mode:** drop Seat C and the third slot in each prompt. A and B audit each other.
- **Solo mode:** run every prompt yourself, each stage in a fresh context where you can, and tell the user that self-review is the weakest setup.

## Hand-off card

Use this format for every Seat B and Seat C step:

```
### Seat B · Stage 2 · open a new chat
[the filled prompt, in its own code block]
Paste the full reply back here, labelled "B-audit".
```

Paste-back labels are `<seat>-<stage output>`: `B-draft`, `C-audit`, `B-review`, `C-research`.

- When Seats B and C get the same prompt (Stages 1, 4, and 5), use one card with two paste-back labels.
- Before sending a card, check that every `{{…}}` has been filled. If any `{{` remains, the prompt isn't finished.
- Show one stage at a time and wait for the pasted replies. Keep progress in the run log.

## Finish

1. **Mechanical check.** If you can run code, run `python3 scripts/check_resume.py final.md` (or pipe the text in with `-`). Fix every issue it reports and pass the TODO placeholders to the user. If you can't run code, check by hand for banned words, bullet length, repeated opening verbs, and mixed date dashes.
2. **User-voice pass.** Recruiters spot unedited AI text, not AI help as such. Ask the user to read the resume aloud and to rewrite the summary and at least two bullets in their own words. Then apply the house rules to their edits.
3. **Deliver.** Give the user the final Markdown resume, the list of unfilled placeholders, and the interview stress test from P8. Offer to export to .docx or PDF, or to rerun Stage 6 for a different job description using the same handbook.

## Common mistakes

| Mistake | Fix |
|---|---|
| Telling the user to paste into a named product | "Open a separate assistant from a different company, in a new chat" |
| Mentioning another assistant inside a hand-off prompt | Present inputs as plain text. P2 already tells the auditor it doesn't know how the resume was produced. |
| Seat A's draft always ends up as Version 1 | Shuffle the order and log the mapping |
| Presiding seat auditing or reviewing its own merge or compile (Stage 4 P2, P8) | Send those to Seats B and C |
| Passing a seat's whole reply, including its diagnosis and score | Pass only the resume code block |
| Filling metric gaps with plausible-sounding numbers | Use placeholders and list them at the end |
| Handing over all six stages at once | One stage per message |
