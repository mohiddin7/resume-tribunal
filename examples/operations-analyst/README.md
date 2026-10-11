# Worked example: operations coordinator to operations analyst

A complete run of Resume Tribunal in full council mode, on a fictional candidate. Three AI assistants from three different companies took part: the host and two outside seats, which ran automatically through their command-line tools. A fresh agent ran the skill from its files alone, with the candidate's replies scripted in advance. Nothing was edited by hand afterwards.

The candidate and employers are invented. Employers are described by type, and there are no links.

| File | What it is |
|---|---|
| [job.md](job.md) | The job description |
| [before.md](before.md) | The resume the candidate started with |
| [own-words.md](own-words.md) | What the candidate said about their work, in their own words |
| [signoff.md](signoff.md) | What the candidate confirmed at the sign-off |
| [after.md](after.md) | The resume the skill produced ([PDF](Resume.pdf), one page at 10.5 pt) |
| [findings.md](findings.md) | What each seat caught, what was rejected as invented, and what the run cost |
| [review.md](review.md) | The final blind look, fix by fix, with the interview questions |
| [not-shown.md](not-shown.md) | Job requirements the resume still does not show |

## Check it yourself

Every number and name in the new resume traces to the candidate's material. From this folder:

```bash
python3 ../../skills/resume-tribunal/scripts/check_resume.py after.md --final \
  --source before.md --source own-words.md --source signoff.md --vocab job.md
```

It prints `0 error(s), 0 warning(s), 0 placeholder(s) to fill`. Add "Tableau" to a bullet and run it again to see the check fail.

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
- Track about 400 shipments a day across 12 carriers and work with carriers and customers to resolve issues.
- Helped raise Dayton terminal on-time delivery from 81 to 93 percent over about three months, after the team moved one carrier's Friday pickups to another carrier.
- Showed in six months of Excel data that the carrier, late on almost a third of its Dayton loads, was late on its Friday pickups, and presented the finding to the operations manager and the terminal manager.
- Cut the Monday report on late deliveries for the operations manager from half a day's work to about 40 minutes by building it with Excel pivot tables and Power Query.
- Write simple SQL queries against the shipment database a few times a week.
- Trained four new coordinators.
```

## What the blind review was for

- **Each participant caught something the others missed.** One noticed a draft crediting the candidate alone for a decision the team made. Another noticed that "freight and logistics" stretched four years over a customer service job.
- **Enlarged or invented claims were rejected.** Two reviewers suggested "from 4 hours to 40 minutes"; the candidate had said "half a day". Another suggested "root-cause tracking framework adopted by leadership" for a spreadsheet one supervisor used. [findings.md](findings.md) lists them all.
- **The resume stayed honest about gaps.** The job asks for Power BI or Tableau. The candidate has used neither, so neither appears, and the gap is listed in [not-shown.md](not-shown.md) for the candidate to address.

Both outside reviewers, reading blind, said they would phone-screen this candidate. The limits of this run are listed at the end of [findings.md](findings.md).
