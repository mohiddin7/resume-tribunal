# The original manual prompts

These are the prompts Resume Tribunal grew out of. Before there was a skill, this was a manual routine: paste a prompt into one AI assistant, copy the answer, paste it into another, and repeat until three assistants had drafted, audited and merged the same resume.

They are kept here as they were written, for the record. To tailor a resume today, use the skill in [`skills/resume-tribunal/`](../skills/resume-tribunal/). It does the same job with far fewer steps and safer rules.

## Timeline

- **May 2026:** first drafts, written and tried by hand across several AI assistants.
- **June 2026:** revised into the two phases below. The files in this folder were last saved on 13 and 16 June, and the commits carry those dates.
- **Late July 2026:** three more days of edits and test runs.
- **October 2026:** rebuilt as an Agent Skill, researched, tested on a real application and released as version 1.0.

Only the last saved version of each prompt survives, so earlier drafts are not in the history.

## The idea

One assistant grading its own resume draft tends to like what it wrote. So the same prompts went to three different assistants, each audit was run in a fresh chat with no context, and a final pass merged the best of the three.

## Phase 1: draft, audit, merge

Run prompts 1.1 to 1.4 in each of three assistants, audit each result with 1.5 in a fresh chat, then merge with 1.6.

| File | Step |
|---|---|
| [1.1-Chat.md](phase-1-draft-audit-merge/1.1-Chat.md) | Decode the job description: the real objective, unwritten demands, keywords |
| [1.2-Chat.md](phase-1-draft-audit-merge/1.2-Chat.md) | Screen the resume against it as a skeptical hiring manager |
| [1.3-Chat.md](phase-1-draft-audit-merge/1.3-Chat.md) | Rewrite the three weakest bullets |
| [1.4-Chat.md](phase-1-draft-audit-merge/1.4-Chat.md) | Write the full resume in Markdown |
| [1.5-Audit-generate-feedback.md](phase-1-draft-audit-merge/1.5-Audit-generate-feedback.md) | Independent audit in a fresh chat |
| [1.6-Create-Unified-Resume.md](phase-1-draft-audit-merge/1.6-Create-Unified-Resume.md) | Merge three drafts and three audits, in three turns |

## Phase 2: council review and role handbook

Audit the merged resume in all three assistants, reconcile the feedback (2.1 to 2.4), then research the role, build a handbook and do a final rewrite (2.5 to 2.7).

```
        Deep research on the role (two assistants)        2.5.1
                          |
        Combine into one resume handbook                  2.5.2
                          |
        Compile the resume against the handbook           2.6
                          |
        Line-by-line evaluation and final rewrite         2.7
```

| File | Step |
|---|---|
| [2.1-Open-new-chat.md](phase-2-council-and-handbook/2.1-Open-new-chat.md) | Start the comparison log with the first review |
| [2.2-in-the-same-new-chat.md](phase-2-council-and-handbook/2.2-in-the-same-new-chat.md) | Add the second review: overlaps, contradictions, new findings |
| [2.3-in-the-same-new-chat.md](phase-2-council-and-handbook/2.3-in-the-same-new-chat.md) | Add the third review and produce a master checklist |
| [2.4-in-the-same-new-chat.md](phase-2-council-and-handbook/2.4-in-the-same-new-chat.md) | Rewrite the resume against the checklist |
| [2.5-Create-Unified-Resume-handbook.md](phase-2-council-and-handbook/2.5-Create-Unified-Resume-handbook.md) | Overview of the handbook workflow |
| [2.5.1-Create-Unified-Resume-handbook.md](phase-2-council-and-handbook/2.5.1-Create-Unified-Resume-handbook.md) | Deep research prompt for the target role |
| [2.5.2-Create-Unified-Resume-handbook.md](phase-2-council-and-handbook/2.5.2-Create-Unified-Resume-handbook.md) | Synthesize the research into a handbook |
| [2.6-in-the-same-new-chat.md](phase-2-council-and-handbook/2.6-in-the-same-new-chat.md) | Compile the resume under the handbook's rules |
| [2.6.reply-in-the-same-new-chat.md](phase-2-council-and-handbook/2.6.reply-in-the-same-new-chat.md) | What to answer when the compiler asks for details |
| [2.7-Create-Unified-Resume-handbook.md](phase-2-council-and-handbook/2.7-Create-Unified-Resume-handbook.md) | Final evaluation, interview questions and rewrite |

## What changed when this became the skill

| Manual prompts | The skill |
|---|---|
| 16 prompts and many copy-and-paste rounds | 7 prompts; automatic when other AI tools are installed |
| Five full rewrites of the resume | One draft round and one merge |
| Forceful wording and capital letters | Plain instructions with reasons |
| A fixed list of banned words in every prompt | A script that checks the finished text |
| Bullet-length rules by feel | Line breaks measured on the real PDF |
| Written for one candidate's background | Works for any role |

Some of these prompts name specific AI products and use wording the skill has since dropped. They are unedited on purpose.
