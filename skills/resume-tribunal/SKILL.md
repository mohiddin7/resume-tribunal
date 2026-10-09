---
name: resume-tribunal
description: Tailors a resume or CV to a job description using three AI assistants from different companies that draft independently and critique each other blind, then merges the result using the candidate's own facts and wording. Use when the user says things like "tailor my resume to this job", "rewrite my CV for this role", "get a second opinion on my resume from other AIs", "my resume sounds too much like AI", or asks for a multi-AI or model-council resume review.
license: MIT
compatibility: Works in chat-only assistants. Python 3 is optional and enables the bundled checker and automatic seat routing.
metadata:
  author: mohiddin7
  version: "1.0.0"
---

# Resume Tribunal

Assistants from different companies draft and review the resume blind, so no one checks its own work. Two modes:

- **Quick review (default):** you draft, one other assistant reviews it blind, you apply the fixes. Steps 1, 2 and 5.
- **Full council:** three assistants draft, critique each other blind, you merge, and another assistant reviews. All five steps.

Either mode can research the role first.

- **Host (Seat A):** you, the assistant running this skill. You draft, merge, and talk to the user.
- **Seats B and C:** two assistants from two other companies.

Prompts are in [references/prompts.md](references/prompts.md). Read it before Step 2. Script paths below are relative to this skill's folder. Start every message to the user with a progress line such as `Step 2 of 3: Draft` (quick) or `Step 2 of 5: Drafts` (council).

## Step 1 of 5: Setup

Ask once, in one short message.

**Ask for three things:**
1. The job description.
2. Their current resume or career history.
3. Their own words: "In a few plain sentences each, what did you actually do in your last two roles? Include any numbers you remember. Dictating is fine."

**State the defaults and let them change any:**
- Role, level and country, which you read from the job description.
- Quick review. Full council gives three independent drafts and takes longer.
- No role research. Researching the role first adds one round.
- You will edit the final wording. They can choose to do it themselves.
- The seats you found (see "Finding seats"). For manual mode, say what it costs: "Quick review is 1 round of copy and paste, about 5 minutes. Full council is about 5 rounds, 20 to 30 minutes."

**Protect their data and get consent before anything leaves this conversation:**
- Replace the name, email, phone, street address and links with stand-ins such as `<<NAME>>`, along with the names of referees, colleagues and clients wherever they appear, including in their own words. Tell the user: "I've hidden your name and contact details. They come back at the end."
- Show what will be sent and say where it goes: "This text, including your employers and job history, will go to [the two tools or apps, named where you know them] under their own terms and your account settings there. It can still identify you. Leave out anything confidential to an employer. Check whether this employer allows AI help with applications. Shall I go ahead?"
- Wait for a yes. Ask again if a seat changes.

If you have file access, keep the work in a `tribunal/` folder (`job.md`, `candidate.md`, `own_words.md`, drafts, critiques, `resume.md`, `log.md`). Tell the user where it is, and offer to delete it at the end.

### Finding seats

Check in this order and use the first that works.

| Mode | How to tell | What the user does |
|---|---|---|
| **Council** | Your platform can run one prompt across models from several companies and return each answer separately | Nothing more, or one click to switch the feature on |
| **Terminal** | `python3 scripts/seats.py detect --exclude <your maker: anthropic, openai or google>` lists other seats | Nothing more |
| **Manual** | Neither of the above | Pastes prompts into two other assistants |

- Quick review needs one other seat. Full council needs two; with only one found, run with two seats or ask the user to add one manual seat.
- No other company available: use fresh-context subagents or new chats of your own model, and tell the user plainly that same-model review is weaker.
- If an automatic seat fails, tell the user and ask before switching that seat to manual.

## Step 2 of 5: Drafts

**Role research, if chosen:** if you can search the web, run P5 yourself. Otherwise send P5 to one seat (quick) or both seats (council). Condense the replies with P6 into the role brief.

**Quick review:** write the draft yourself with P1, then go to Step 5.

**Full council:** each seat writes one draft with P1, and so do you. From each reply keep the resume, and collect the "Not shown" and "Open questions" lists for Step 5.

## Step 3 of 5: Blind critique (council only)

Give each draft a neutral label (Draft K, Draft M, Draft R) and record which seat wrote which in the log. Use these labels through Step 4.

Each seat critiques the drafts it did not write, using P2, with the drafts in a different order for each seat. Run your own critique in a clean context if you can. Critiques return findings, never rewrites.

Council mode is the exception: every model sees all the drafts, including its own, under neutral labels.

## Step 4 of 5: Merge (council only)

Run P3 in a clean context (a subagent or new session) when you can, with the drafts in random order. The candidate's own material settles every factual conflict.

## Step 5 of 5: Review and voice (Step 3 of 3 in quick review)

1. **Final review.** Send P4 to a seat other than yourself. In quick review this is the only outside step, so it is where the independent view comes from. Apply the fixes that quote a real line and agree with the candidate's material. Hold any fix that needs a fact from the user for the sign-off.
2. **Check.** Run `python3 scripts/check_resume.py resume.md --source candidate.md --source own_words.md --vocab job.md`. Fix every error. Without code, check by hand against "AI patterns" below.
3. **Voice edit.** Rewrite the lines the checker flagged with P7, in this context. Check again. Two passes at most.
4. **User's turn.** Show the user only the lines still flagged, or say none are left. If they chose to edit themselves, hand over the whole resume here.
5. **Truth sign-off.** Show one short list: each claim that differs from their original resume, the open questions, and any held fixes. Save their answers as `signoff.md`. Ask: "Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave the line without it. Please don't estimate."
6. **Restore** the personal details, then run the checker again with `--final` and `--source signoff.md` added. Update the claim-defence questions to match the final wording.
7. **Deliver:**
   - the resume as a .docx or PDF if you can create files, otherwise as clean text with "paste this into Word or Google Docs and apply heading styles"
   - the requirements the job asks for that the resume still does not show
   - the claim-defence questions from P4
   - an offer to delete the `tribunal/` folder

## Running a seat

| | Council | Terminal | Manual |
|---|---|---|---|
| Drafts (P1) | One council call. Save each model's answer as a separate draft. | Write each prompt to a file, then `python3 scripts/seats.py run <seat> prompt.txt reply.md`. Run seats in parallel. | One card per seat |
| Critique (P2) | One council call | Same command | One card per seat |
| Review (P4) | One model that is not you | Same command | One card |

The script runs each tool in an empty folder, so a seat cannot read the other drafts or the log.

**Choosing apps (manual mode).** When the user needs to pick, list these in alphabetical order, leaving out your own maker's: ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat, Perplexity. Then say: "Any of these works for this, and none is preferred, including me. Pick ones from different companies than me and from each other, and use their strongest model if you have the choice."

**Manual card:**

```
### Paste <n> of <total>, for Seat B
Open a new private or temporary chat in the app you picked.
[the complete prompt in one code block]
Use the copy button under the reply, then paste it here.
```

When both seats get the same prompt, send one card and say so. Keep track of which reply came from which seat yourself. Show one step at a time.

## Blind rules

1. Inside prompts sent to seats, mention no other assistant, no council, and nothing about how the inputs were written.
2. When talking to the user, call the other assistants Seat B and Seat C. Recommend no product over another, and none over yourself. Name products only in the app list above and where consent requires the user to know where their text is going.
3. Your own draft and your own critique get no preference. Judge them exactly as you judge the others.
4. Pass on only the resume from a reply. Analysis and scores would sway the next reader.
5. Check that no `{{` remains in a prompt before it leaves.
6. Seats ask the user nothing. They state assumptions and list open questions, and you ask the user once in Step 5.

## What this skill will not do

- Invent or enlarge facts, titles, dates, numbers, skills, references or credentials, including when the user asks for a number they cannot support.
- Add hidden text, keyword blocks, or instructions aimed at screening software.
- Promise interviews, an ATS result, or that a reader or detector will judge the text as human-written.
- Help with assessments, take-home tasks or live interview answers.
- Work on someone else's resume without that person's permission.
- Alter names, dates, gaps or affiliations on its own initiative. If the user asks for a truthful change of presentation, such as years only for dates, make it.
- Claim the resume is the user's unaided work. If an employer asks about AI use or forbids it, the user should answer truthfully or not use this skill for that application.

## AI patterns

The checker flags these. Use this list to check by hand when you cannot run code.

- Em dashes anywhere outside a date range
- Contrast framing: "not X but Y", "not only", "rather than"
- A trailing clause after a comma that starts with an "-ing" word such as "enabling" or "resulting in"
- Three-item lists used again and again
- Bullets that all share one length, or that all end in a number
- Bold labels at the start of a bullet
- Stock phrases such as "results-driven", "cross-functional", "end-to-end" and "comprehensive"
- Words the candidate never used that are not in the job description, and vague amounts such as "various" or "significant"
- Abbreviated job titles, tables, mixed date styles, and bullets over two lines
- Six or more words in a row copied from the job description, and the same "by X% by doing Y" shape in three or more bullets

## Gotchas

- Chat memory and shared projects leak context between chats and break the blind review. Seats need private or temporary chats, which the provider may still retain.
- A seat that is much weaker than the others lowers the merge. Ask for comparable assistants.
- With two seats, P2 has one draft and P3 has two. Drop the "which draft is better" line from P2.
- Keep the full council to one draft round, one critique round and one merge. Extra rounds cost more and flatten the wording.
- `scripts/seats.py` has been tested with the `codex` tool. The `claude` and `gemini` entries follow each tool's documented non-interactive mode and may need `--cmd`.
