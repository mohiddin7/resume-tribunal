---
name: resume-tribunal
description: Tailors a resume or CV to a job description using three AI assistants from different companies that draft independently and critique each other blind, then merges the result in the candidate's own voice. Use when the user says things like "tailor my resume to this job", "rewrite my CV", "review my resume", "make my resume sound less like AI", "get a second opinion on my resume", or asks for a multi-AI or model-council resume review.
license: MIT
compatibility: Works in chat-only assistants. Python 3 is optional and enables the bundled checker and automatic seat routing.
metadata:
  author: mohiddin7
  version: "3.0.0"
---

# Resume Tribunal

Three assistants from different companies each draft the resume, critique the other drafts without knowing who wrote them, and the host merges the best lines. A model is lenient toward its own writing, so no draft is reviewed by its author. No study shows that a council writes a better resume than one strong model. What this process gives the user is independent review, a resume built from their own words and facts, and the interview questions its claims will invite.

- **Host (Seat A):** you, the assistant running this skill. You draft, merge, and talk to the user.
- **Seats B and C:** two assistants from two other companies.

Prompts are in [references/prompts.md](references/prompts.md). Read it before Step 2. Start every message to the user with a progress line such as `Step 2 of 5: Drafts`.

## Step 1 of 5: Setup

Do all of this in one message, so the user is asked once.

**Collect:**
- The job description, and the current resume or career history.
- Target role, seniority, and country or region.
- Their own words: ask "In a few plain sentences each, what did you actually do in your last two roles?" Speaking it aloud with dictation is fine. This is what the final resume's voice is built from.
- Any numbers they know but did not write down (team size, volumes, before and after).

**Ask three choices:**
1. **Depth:** quick (tailor to the job description, the default) or deep (research the role first, which takes longer).
2. **Final edit:** the host edits for a human voice (default), or the user does.
3. **Seats:** confirm the mode you found (see "Finding seats").

**Protect their data, and get consent:**
- Replace the name, email, phone, address, links, and the names of referees, colleagues and clients with tokens such as `<<NAME>>`. Put them back in Step 5.
- Tell the user once: "Your resume text will be sent to two other AI assistants under their own terms. Use private or temporary chats with memory and training turned off. Shall I go ahead?" Wait for a yes before anything leaves this conversation. Ask again only if the mode changes.

If you have file access, keep everything in a `tribunal/` folder: `job.md`, `candidate.md`, each draft and critique, and `log.md`.

### Finding seats

Check in this order and use the first that works.

| Mode | How to tell | What the user does |
|---|---|---|
| **Council** | Your platform can run one prompt across models from several companies and return each answer separately | Nothing more, or one click to switch the feature on |
| **Terminal** | `python3 scripts/seats.py detect --exclude <your vendor>` lists two seats | Nothing more |
| **Manual** | Neither of the above | Pastes prompts into two other assistants |

- One other seat found: run with two seats, or ask the user to add one manual seat.
- No other company available: use fresh-context subagents or new chats of your own model, and tell the user plainly that same-model review is weaker.
- If an automatic seat fails, switch that seat to manual and say so.

## Step 2 of 5: Drafts

Deep mode only, first: send P5 to Seats B and C, then condense their replies with P6 into the role brief.

Each seat writes one draft with P1. Write your own draft too. Keep only the resume code block from each reply, and collect the open questions for Step 5.

## Step 3 of 5: Blind critique

Each seat critiques the drafts it did not write, using P2. Label the drafts with neutral names (Draft K, Draft M) and change their order for each seat. Critiques return findings, never rewrites.

## Step 4 of 5: Merge

Run P3 in a clean context (a subagent or new session) when you can. Assign Version 1, 2 and 3 at random and record the mapping in the log. The candidate's own material settles every factual conflict.

## Step 5 of 5: Review and voice

1. **Final review.** Send P4 to one seat other than yourself (both seats in automatic modes). Apply only the fixes that quote a real line and agree with the candidate's material.
2. **Restore** the personal details you replaced.
3. **Check.** Run `python3 scripts/check_resume.py resume.md --source candidate.md`. Fix every error. Without code, check by hand against "AI patterns" below.
4. **Voice edit.** Rewrite only the flagged lines with P7, using the candidate's own words. Check again. Two passes at most.
5. **User's turn.** Show only the lines still flagged and the words the candidate never used. If they chose to edit themselves, hand over the whole resume here.
6. **Truth sign-off.** List every claim that differs from their original resume, ask for the open numbers, and have them confirm each line is true and that they can explain it in an interview. Finish when `--final` passes with no placeholders.
7. **Deliver** the resume in Markdown, the claim-defence questions from P4, and a note that Pandoc converts it to .docx or PDF.

## Running a seat

| | Council | Terminal | Manual |
|---|---|---|---|
| Drafts (P1) | One council call. Save each model's answer as a separate draft. | Write each prompt to a file, then `python3 scripts/seats.py run <seat> prompt.txt reply.md`. Run seats in parallel. | One card per seat |
| Critique (P2) | One council call with all drafts under neutral labels | Same command | One card per seat |
| Review (P4) | One model other than the base of the merge | Same command | One card |

**Manual card:**

```
### Seat B: open a new private or temporary chat, with memory off and outside any project
[the complete prompt in one code block]
Copy the whole reply and paste it here as "B-draft".
```

When both seats get the same prompt, send one card with two labels. Show one step at a time.

## Blind rules

1. Call the other assistants Seat B and Seat C. Name no products or companies, and if the user asks which is better, say the seats are interchangeable by design.
2. A prompt sent to a seat mentions no other assistant, no council, and nothing about how its inputs were written.
3. Pass on only the resume code block from a reply. Analysis and scores would sway the next reader.
4. Check that no `{{` remains in a prompt before it leaves.
5. Seats ask the user nothing. They state assumptions and list open questions, and you ask the user once in Step 5.

## What this skill will not do

- Invent or enlarge facts, titles, dates, numbers or skills.
- Add hidden text, keyword blocks, or instructions aimed at screening software.
- Promise interviews, an ATS result, or that a reader or detector will judge the text as human-written.
- Help with assessments, take-home tasks or live interview answers.
- Change names, dates, gaps or affiliations to hide who the candidate is. Those choices belong to the candidate.

## Keeping token use low

- One draft round, one critique round, one merge. Add no debate or extra rewrite rounds.
- Critiques and reviews return short quoted findings.
- Pass resumes between steps, never whole replies.
- Deep mode only when the user picks it. The role brief stays under 400 words.
- Let the checker do the mechanical checks.

## AI patterns

The checker flags these. Use this list to check by hand when you cannot run code.

- Em dashes anywhere outside a date range
- Contrast framing: "not X but Y", "not only", "rather than", "instead of"
- A trailing clause after a comma that starts with an "-ing" word such as "enabling" or "resulting in"
- Three-item lists used again and again
- Bullets that all share one length, or that all end in a number
- Bold labels at the start of a bullet
- Stock openers such as "results-driven professional with 8 years of experience"
- Words the candidate never used, and vague amounts such as "various" or "significant"
- Abbreviated job titles, tables, mixed date styles, and bullets over two lines

## Gotchas

- Chat memory and shared projects leak context between chats and break the blind review. Seats need private or temporary chats.
- A seat that is much weaker than the others lowers the merge. Ask for comparable assistants.
- Some assistants open long answers in a side document. The prompts ask for the reply in the chat, so copy from there.
- `scripts/seats.py` has been tested with one tool only. The others follow their documented non-interactive mode and may need `--cmd`.
