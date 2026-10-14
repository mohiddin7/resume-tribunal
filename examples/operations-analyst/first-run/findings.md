# What the council found

Three participants from three companies: the host (Seat A) and two outside seats (B and C). Each wrote a draft without seeing the others. Seats B and C each critiqued the drafts they did not write, under neutral labels and in different orders. The merge ran in a new session that saw only the drafts and critiques, not who wrote them.

## Caught by one participant and missed by the others

- **Seat A's draft** was the only one to credit "the team" for moving the loads, and the only one to keep the employer's size.
- **Seat B's critique** flagged "automating" as overstated, and four phrases in another draft that the candidate never said.
- **Seat B's final look** noticed that "freight and logistics" stretched four years over a customer service job, and that "failing" was a loaded word.
- **Seat C's critique** caught a draft saying the candidate personally moved the loads when the team did, "Train four" in the wrong tense, and "carrier performance" borrowed from the posting into a bullet about a late-delivery report.
- **Seat C's final look** noticed the summary repeating a bullet word for word.
- **The merge** settled ten factual conflicts from the candidate's own material, and refused a call to drop "simple" from the SQL line.

## Rejected as invented or enlarged

From the drafts, removed at the merge:

- "automating operational reporting" and "automated workflow"
- "ensure schedule adherence across regional logistics operations"
- SQL queries "to retrieve order records"
- training on "carrier communication standards, and reporting workflows"
- performance goals "for customer service quality, inquiry resolution, and response timeliness"
- "carrier performance management", "root-cause analysis", "cross-carrier coordination"
- "maintain accurate financial accounting and restaurant standards"
- sole credit for moving the loads
- "communicate findings to operations leadership"
- "Supported daily operations in a fast-paced restaurant environment"

From the reviews:

- "advanced pivot table and Power Query automation capabilities"
- "led operational leadership to reallocate carrier volume"
- "defect-tracking spreadsheet analyzing root causes ... adopted by leadership"
- "from 4 hours to 40 minutes", where the candidate said "half a day"
- dropping "simple" from the SQL lines, suggested four times

Three more suggestions needed facts the candidate had not given (what the training covered, how issues were resolved, whether anything was automated). They were put to the candidate, who did not confirm them, so they stayed out.

## Cost of this run

| Step | Calls | Text sent (characters) | Text received | Seconds |
|---|---|---|---|---|
| Drafts | 2 | 14,346 | 9,953 | 328 |
| Critiques | 2 | 17,205 | 12,054 | 237 |
| Merge, in a new session | 1 | 26,218 | 5,738 | 84 |
| Blind review | 1 | 5,991 | 6,867 | 101 |
| Final blind look | 2 | 12,896 | 10,896 | 154 |
| **Total** | **8** | **76,656** | **45,508** | **904** |

About 30,000 tokens in all at four characters a token, before each model's own reasoning. Calls in the same step ran side by side, so the wait was about 12 minutes. A quick review would have made the last three calls only: about 6,000 tokens. No call failed or needed a retry.

## Limits of this run

- One fictional candidate. It shows how the process works, not how it performs across many resumes.
- Seat B ran a tier below the host, the closest its plan offered.
- The simulated candidate answered the sign-off questions about new facts but gave no blanket "yes" to the other changed lines. The host kept those because each restates the candidate's own words.
- The PDF's text layer was not machine-checked, because the tool for that was not installed.
- The merge chose the host's draft as its base. It did so without knowing whose draft it was.
