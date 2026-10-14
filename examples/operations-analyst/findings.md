# What the council found

Three participants from three companies: the host (Seat A) and two outside seats (B and C). Each wrote a draft without seeing the others. Seats B and C each critiqued the drafts they did not write, under neutral labels. The merge ran in a fresh session that saw only the drafts and critiques, not who wrote them, and chose Seat A's draft as its base.

## Caught by one participant and missed by the others

- **Seat A's draft** was the only one to open with a summary built from the candidate's specifics (400 shipments, 12 carriers, the weekly report) and the only one to keep the employer's size.
- **Seat B's draft** was the only one to say "contributed to" for the team's result.
- **Seat B's critique** flagged a long Dayton sentence as hard to scan and a soft-skills list as filler.
- **Seat C's critique** caught the Monday report shown twice in one draft, a vague "those problems", and a draft that read junior.
- **Seat B's blind review** alone noticed that "half a day" was the previous person's time, so the report line now says it "took half a day".
- **The host** caught what neither critique did: "Carrier management" in a Skills list, the posting's phrase for something the candidate never said they do, and "directly" added to "resolve issues".

## Rejected as invented or enlarged

From the drafts and critiques, removed at the merge:

- "Carrier management" as a skill, from the posting
- "resolve shipment issues directly"
- "driving the rerouting decision": the candidate wrote "we moved those loads"
- removing "simple" from "simple SQL queries" (both critiques asked). It is the candidate's own word.
- a list of communication, teamwork, problem solving and time management with nothing behind it

From the final blind look:

- an example of what the SQL queries look up. The candidate said they could not say more than "simple queries a few times a week".
- "carrier performance tracking", "logistics operations" and "root-cause analysis" as skills
- an "operations analyst" title in the summary, a job the candidate has not held
- changing the tracking bullet to past tense, which would say the work had ended
- "team leadership" for the candidate's "supervisor", and "shift scheduling" for a Shift Lead line that says nothing about scheduling

## Calls and time

| Step | Calls | Time per call |
|---|---|---|
| Drafts | 2 outside, plus the host's own | 53 s and 305 s |
| Critiques | 2 | 56 s and 156 s |
| Merge, in a fresh session | 1 | 80 s |
| Blind review | 1 | 54 s |
| Final blind look | 2 | 58 s and 191 s |
| **Total** | **8** | |

About 99,000 characters went out and came back, roughly 25,000 tokens at four characters a token, before each model's own reasoning. The run took about 19 minutes from the first message to the PDF, including the candidate's answers. The slowest seat ran a fast-tier model, the strongest its tool offered. No call failed or needed a retry.

## Limits of this run

- One fictional candidate. It shows how the process works, not how it performs across many resumes.
- The candidate's replies were scripted, and answered the sign-off from a fixed list of what is true.
- Seat C ran a tier below the host, the closest its tool offered.
- The candidate said "it's final" without accepting any of the final look's six surviving suggestions, so none were applied. Two lines were then tightened to fit the page, without changing a fact.
- The host changed one word of its own draft ("my supervisor" to "the supervisor") before any seat saw it. No seat's draft or reply was edited.
