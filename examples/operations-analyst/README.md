# Worked example: operations coordinator to operations analyst

A complete run of Resume Tribunal in full council mode, on a fictional candidate. Three AI assistants from three different companies took part: the host and two outside seats, which ran automatically through their command-line tools. A fresh agent ran the skill from its files alone, with the candidate's replies scripted from a fixed list of what is true. No draft or reply was edited by hand.

The candidate and employers are invented. Employers are described by type, and there are no links.

| File | What it is |
|---|---|
| [job.md](job.md) | The job description |
| [before.md](before.md) | The resume the candidate started with |
| [own-words.md](own-words.md) | What the candidate said about their work, in their own words |
| [signoff.md](signoff.md) | What the candidate confirmed at the sign-off |
| [after.md](after.md) | The resume the skill produced ([PDF](Resume.pdf), one page at 10.5 pt) |
| [findings.md](findings.md) | What each seat caught, what was rejected as invented, and what the run cost |
| [review.md](review.md) | The final blind look, suggestion by suggestion, with the interview questions |
| [not-shown.md](not-shown.md) | Job requirements the resume still does not show |

[first-run/](first-run/) is the first full run on the same candidate, made with an earlier version of the skill. The blog post about how Resume Tribunal was made describes that run.

## Check it yourself

Every number and name in the new resume traces to the candidate's material. From this folder:

```bash
python3 ../../skills/resume-tribunal/scripts/check_resume.py after.md --final \
  --source before.md --source own-words.md --source signoff.md --vocab job.md
```

It prints 0 errors and one warning: "late-delivery" is not a word the candidate used (they wrote "late deliveries"). Add "Tableau" to a bullet and run it again to see the check fail.

## Before and after, one role

Before:

```
- Responsible for daily shipment tracking and reporting
- Worked with carriers and customers to resolve issues
- Helped improve on-time delivery
- Utilized Excel for various reports
- Assisted with training of new hires
```

After:

```
- Traced one carrier's late Dayton terminal loads to its Friday pickups in six months of Excel data;
  after the team moved them to another carrier, on-time delivery there went from 81% to 93% over
  about three months.
- Presented the Friday pickup finding to the operations manager and the terminal manager.
- Built the Monday late-delivery report in pivot tables and Power Query; it took half a day, now
  about 40 minutes.
- Track about 400 shipments a day across 12 carriers and resolve delivery issues with carriers and
  customers.
- Write simple SQL queries against the shipment database a few times a week.
- Trained four new coordinators.
```

## What the blind review was for

- **Each participant caught something the others missed.** One reviewer noticed that "half a day" was the previous person's time. The host caught "Carrier management" in a Skills list, the posting's phrase for something the candidate never said they do.
- **Enlarged or invented claims were rejected.** A critique wanted the candidate credited with "driving the rerouting decision"; the candidate wrote "we moved those loads". A final reviewer offered an example of what the SQL queries look up, which the candidate never gave. Both critiques asked to drop "simple" from "simple SQL queries". [findings.md](findings.md) lists them all.
- **The resume stayed honest about gaps.** The job asks for Power BI or Tableau. The candidate has used neither, so neither appears, and the gap is listed in [not-shown.md](not-shown.md) for the candidate to address.

Both outside reviewers, reading blind, said they would phone-screen this candidate. The limits of this run are listed at the end of [findings.md](findings.md).
