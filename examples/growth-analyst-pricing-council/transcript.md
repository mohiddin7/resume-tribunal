# Growth analyst applying for a senior pricing analyst job

Fictional candidate · Auto mode: the other AIs ran by themselves · 3 AIs from 3 companies · 27 minutes · Real public job posting

Every message of the run in order. Times are minutes and seconds from the start. Prompts and replies are in [files/](files/).

**00:00 Host**

> I’m reading the skill and its required references first, then I’ll follow its workflow and record the run as it happens.

**00:00 Host** (working)

> Reading the skill instructions in full

## Step 1: Setup

**00:18 Host** (working)

> Reading seat options and the supplied application files

**02:14 Host** (working)

> Checking the hidden files and removing another person's name

**02:28 Host** (Stop 1)

> You give: your resume, the job posting, and a few sentences in your own words
>    ↓
> I write a draft from your facts only
>    ↓
> A second AI from another company checks it without knowing who wrote it
>    ↓
> Automatic checks, then you approve every changed line
>    ↓
> Your resume, the job requirements it does not show, and likely interview questions
>
> The other AIs run automatically; you answer a few questions along the way.
>
> I read these roles: Online home-goods retailer, Marketing Coordinator then Marketing Analyst, Mar 2019 to Present; regional sporting-goods chain, Store Manager, 2014 to 2019. I’m treating the target as a senior individual contributor role in the United States, based on the posting.
>
> I’ll use the full council you requested: Claude Opus and Google Gemini 3.8 Flash (High) each draft and review the others’ drafts blind. Google lists only its fast model here, so that seat is a weaker match to my model tier. A full council takes longer and uses several times as much of your AI plans as a quick review. I’ll keep role research off, polish the final wording myself, and work in a plain-text copy, then deliver Markdown. I won’t open any linked pages, following your “No links” preference.
>
> I’ve hidden your name and contact details. They come back at the end. The working files are in .tribunal/. The text, including your employers, job history and any pages your links point to, will go to Anthropic Claude Opus and Google Gemini 3.8 Flash (High) under their terms and your account settings there. Some keep their own history, and the text can still identify you. Leave out anything confidential to an employer, and check whether this employer allows AI help with applications.
>
> Please answer the setup questions, or say “yes” to take the defaults and go ahead.

**02:46 Dana**

> Full council, please. Yes to the defaults, go ahead. No links.

## Step 2: Draft

**02:48 Host** (working)

> Reading the drafting and review prompts

**03:06 Host to Claude**

> Draft a truthful, ATS-safe resume from the candidate's files, and list what is not shown and open questions.

[p1.txt](files/p1.txt)

**03:06 Host to Gemini**

> Draft a truthful, ATS-safe resume from the candidate's files, and list what is not shown and open questions.

[p1.txt](files/p1.txt)

**03:59 Host**

> Step 2 of 5: Draft. Both independent draft requests are running; I’ll merge only their resume text and carry their open questions forward. Next, I’ll compare the returned drafts.

**04:56 Claude** (took 110 s)

> The draft emphasized the SQL-driven win-back segmentation, Looker reporting, and A/B test analysis; it listed pricing models, financial impact reporting, and AI tooling as not shown.

[p1_reply_claude.md.txt](files/p1_reply_claude.md.txt)

**04:56 Gemini** (took 110 s)

> The first call failed because it started before the prompt file existed, so no draft came back.

[p1_reply_agy.md.txt](files/p1_reply_agy.md.txt)

**04:56 Host to Gemini**

> Draft a truthful, ATS-safe resume from the candidate's files, and list what is not shown and open questions.

[p1.txt](files/p1.txt)

**06:41 Host**

> Step 2 of 5: Draft. Claude’s draft is back; the first Google call started before the prompt file existed, so I’m retrying it once as the workflow allows. Next, I’ll finish the draft comparison.

**08:36 Gemini** (took 220 s)

> The draft foregrounded BigQuery, Looker, and test analysis. It included older resume claims about Tableau and budget ownership, and listed pricing, pricing experiments, AI use, schema creation, and executive presentation as not shown.

[p1_reply_agy.md.txt](files/p1_reply_agy.md.txt)

## Step 3: Council

**08:44 Host** (working)

> Labeling drafts and comparing their shared evidence

**08:50 Host to Claude**

> Review Draft M for job fit, factual support, omitted must-haves, and wording problems.

[p2_claude.txt](files/p2_claude.txt)

**08:50 Host to Gemini**

> Review Draft K for job fit, factual support, omitted must-haves, and wording problems.

[p2_agy.txt](files/p2_agy.txt)

**10:00 Host**

> Step 3 of 5: Council. Each reviewer has the other writer’s draft only. I’m waiting for those blind critiques before combining the evidence. Next, I’ll review the critiques alongside the candidate’s files.

**10:39 Claude** (took 109 s)

> The review screened Draft M no because the candidate's material shows no pricing analytics. It flagged the daily SQL claim, undated title progression, test-bullet wording, old budget and Tableau claims, cross-functional leadership, and the assumed Jupyter detail.

[p2_reply_claude.md.txt](files/p2_reply_claude.md.txt)

**10:58 Gemini** (took 128 s)

> The review screened Draft K no because pricing evidence is missing. It urged clearer test-analysis wording, removing standalone link and older social-calendar work, while also suggesting unsupported claims about power analysis and actionable recommendations.

[p2_reply_agy.md.txt](files/p2_reply_agy.md.txt)

**11:23 Host** (working)

> Merging the candidate's evidence and the blind critiques into a single resume

## Step 4: Review and sign-off

**11:29 Host** (working)

> Checking the merged resume and reviewing the remaining old claims

**11:40 Checker**

> 0 errors, 4 warnings (old skills: dbt, Excel, Google Analytics, R, Tableau), 5 placeholders; 214 words

**11:46 Checker**

> 0 errors, 0 warnings, 5 placeholders; 212 words

**11:47 Host** (working)

> Building the blind review prompt for the merged resume

**11:47 Host to Claude**

> Review the merged resume line by line for truthful support, job fit, clarity, and likely interview questions.

[p4_review.txt](files/p4_review.txt)

**12:54 Host**

> Step 4 of 5: Review and sign-off. The merged draft now has no checker warnings, and a blind line by line review is running. I’m holding the text steady until that review returns. Next, I’ll resolve its findings and ask you to sign off on the remaining claims.

**13:35 Claude** (took 108 s)

> The review found no pricing evidence and flagged the missing qualification evidence. Its claim check supported the resume except for dropping the candidate's qualifier ‘maybe’ from Python frequency; it also suggested querying the promotion date and old sales-target claim.

[p4_reply_claude.md.txt](files/p4_reply_claude.md.txt)

**13:35 Host** (working)

> Applying the one factual fix from the blind review and preserving the candidate's qualifiers

**13:55 Checker**

> 1 error (win-back bullet too long), 0 warnings, 5 placeholders; 212 words

**13:55 Checker**

> 0 errors, 2 warnings (short second line, unused synonym purchases), 5 placeholders; 210 words

**14:13 Checker**

> 0 errors, 2 short-second-line warnings, 5 placeholders; 216 words

**14:20 Checker**

> 0 errors, 1 short-second-line warning, 5 placeholders; 213 words

**14:24 Checker**

> 0 errors, 1 short-second-line warning (about 1.02 lines), 5 placeholders; 210 words

**14:46 Checker**

> 0 errors, 0 warnings, 5 placeholders; 210 words

**14:47 Host** (Stop 2)

> SIGN-OFF QUESTIONS
> Step 4 of 5: Review and sign-off
>
> I merged the two drafts, kept the measured win-back result and your role in the A/B tests, and removed the old budget, Tableau-executive, and generic leadership claims that your own account did not confirm. I also changed the old 15-person headcount to about 12 part-time staff, and restored “maybe” in the Python frequency. The long win-back and test bullets are now shorter. Your portfolio link stays beside the test evidence.
>
> Please confirm or correct these points:
> - The old resume says conversion rose 18%; your account says win-back email conversion went from 2.1% to 2.5%. Are these the same result, and which wording is right?
> - When did your title change from Marketing Coordinator to Marketing Analyst? Give month and year only if you know it.
> - Were the old $2.4M email-budget and Tableau dashboards for executive stakeholders accurate? If so, what was your role with the budget and who reviewed the Tableau dashboards?
> - Are R, dbt, Tableau, Google Analytics, Excel, stakeholder management, data storytelling, and cross-functional leadership still accurate skills to show?
> - Only if true, have you worked on pricing or pricing tests, pricing-related financial impact, Product or Finance analysis, broader business KPI reporting, creating BigQuery tables or schemas, AI-assisted analysis or automation, direct executive presentations, or D2C subscriptions? Tell me which and what you did.
>
> The resume still does not show pricing work, pricing models or tests, creating tables or schemas, AI tooling or automation, direct executive presentations, or subscription D2C experience. A reviewer also suggested interview questions about how you measured the win-back change, how you assess whether a test has enough traffic, and whether you have built the underlying tables behind your Looker dashboards. I’ll keep “about 12 tests in the last year” as you wrote it rather than guess exact dates.
>
> Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave it out, so please don't estimate.

**16:43 Host**

> Step 4 of 5: Review and sign-off. I’m recording your answers now, then I’ll update the resume to reflect the July 2022 promotion, correct the budget and Tableau claims, and add the confirmed SQL, GA4, and ChatGPT details.

**16:43 Dana**

> - The 18%: I don't know where that number came from. The numbers I know are 2.1% to 2.5%.
> - I was promoted from Marketing Coordinator to Marketing Analyst in July 2022.
> - I never managed a budget. $2.4M was the email channel's revenue last year in our dashboard, nothing I controlled. Tableau: only in the certificate course, not at work.
> - R: one course, I wouldn't put it on. dbt: I've read the dbt models our data engineer wrote, I've never written one. Tableau: only the certificate course. Google Analytics: yes, I use GA4 most days. Excel: yes. Stakeholder management, data storytelling and cross-functional leadership were filler, take them off.
> - I've never worked on pricing or built a pricing model. I sometimes ask ChatGPT to help me fix a SQL query; I haven't built any automations. I've only presented to our marketing director and the marketing team. I write queries; I've made a few saved views in BigQuery, never schemas. No Product or Finance analysis, no broader KPI datasets, no subscriptions.

**16:43 Host** (working)

> Recording the candidate's confirmations, corrections, and preferences

**17:35 Checker**

> 0 errors, 3 warnings (short second line, old-only Google Analytics spelling, nine-person phrasing), 5 placeholders; 250 words

**17:54 Checker**

> 0 errors, 0 warnings, 5 placeholders; 241 words

**17:54 Host** (working)

> Building the final blind look from the signed-off facts

**17:54 Host to Claude**

> Review the signed-off resume line by line for factual support, job fit, clarity, and likely interview questions.

[p4_final.txt](files/p4_final.txt)

**17:55 Host to Gemini**

> Review the signed-off resume line by line for factual support, job fit, clarity, and likely interview questions.

[p4_final.txt](files/p4_final.txt)

**19:07 Host**

> Step 5 of 5: Finalise. Claude and Google are checking the updated, signed-off resume blind. I’ll resolve any remaining supported edits before showing the final copy. Next, I’ll ask whether it’s final.

**20:03 Claude** (took 129 s)

> The review screened no because pricing is absent. It supported the signed-off facts but said the conversion line needs to say win-back email conversion, and suggested preserving the same-email starting point, consolidating tool bullets, and folding revenue into the dashboard line.

[p4_final_reply_claude.md.txt](files/p4_final_reply_claude.md.txt)

**21:05 Gemini** (took 190 s)

> The review supported the signed-off facts and found no pricing experience. It recommended folding saved views into the SQL line, retaining the win-back starting point and attribution, moving the test link, and cutting unsupported or low-value standalone details such as the passive revenue figure and generic presentation line.

[p4_final_reply_agy.md.txt](files/p4_final_reply_agy.md.txt)

**21:05 Host** (working)

> Applying the final review's supported wording fixes and preserving the limits the candidate confirmed

**21:37 Checker**

> 0 errors, 3 short-second-line warnings (win-back segmentation, result, combined tools), 5 placeholders; 237 words

**22:13 Checker**

> 0 errors, 2 short-second-line warnings (win-back story and tool use), 5 placeholders; 231 words

**22:42 Checker**

> 0 errors, 2 short-second-line warnings (win-back segmentation and result), 5 placeholders; 230 words

**22:58 Checker**

> 0 errors, 2 short-second-line warnings (win-back segmentation and result), 5 placeholders; 230 words

**23:31 Checker**

> 0 errors, 2 short-second-line warnings (win-back SQL and result bullets), 5 placeholders; 233 words

**23:41 Host** (Stop 3)

> Step 5 of 5: Finalise
>
> Your resume is at `.tribunal/final.md`. Here is the current Markdown:
>
> ```markdown
> # Dana Whitfield
> Pittsburgh, PA | dana.whitfield@example.com | (412) 555-0147 | linktr.ee/danawhit | Portfolio: danawhitfield.design/work (two test write-ups)
>
> ## Summary
> Marketing Analyst and the only analyst on a marketing team of nine. Writes SQL in BigQuery most days, builds Looker dashboards, and analyzes A/B test results.
>
> ## Skills
> SQL, BigQuery, Looker, GA4, Excel, Python (pandas), A/B test analysis, customer segmentation
>
> ## Experience
> ### Online home-goods retailer (about 400 employees)
> **Marketing Coordinator** | Mar 2019 - Jun 2022
> **Marketing Analyst** | Jul 2022 - Present
> - Write SQL in BigQuery most days and create a few saved views; sometimes ask ChatGPT for help fixing a SQL query.
> - Wrote SQL to split customers who hadn't bought in a year, all getting the same email, by what they'd bought and how much they'd spent.
> - Win-back email conversion went from 2.1% to 2.5% over the next quarter; the email manager wrote a different email for each group.
> - Analyze about 12 A/B tests in the last year: check whether there is enough traffic, read results, and write up findings. The email manager or paid social lead chooses what to test.
> - Built Looker dashboards for email and paid social; the marketing director reviews them every Monday.
> - Use GA4 most days.
> - Clean exports in Python notebooks with pandas, maybe a few times a month.
>
> ### Regional sporting-goods chain
> **Store Manager** | 2014 - 2019
> - Managed about 12 part-time staff.
> - Built scheduling and inventory spreadsheets in Excel.
>
> ## Education
> BA Communications, large public state university, 2014
> Google Data Analytics Certificate, 2020
> ```
>
> I split the coordinator and analyst titles at July 2022. Duties that did not have separate dates sit under Marketing Analyst. The final blind reviews found no pricing experience and agreed with the confirmed facts. Their supported correction to the win-back result's scope is in place. I removed the dashboard's $2.4M revenue figure from the resume because it was not a result you controlled, and left out the presentation line because it named only the director and team without saying what you presented.
>
> What the job asks for that the resume still does not show: pricing models or tests, pricing-related financial analysis, Product or Finance work, broader KPI datasets, table or schema creation, AI quality checks or automations, senior-executive presentations, or subscription experience. Your ChatGPT use is described only as help fixing SQL queries. The checker has no errors; it flags two bullets as slightly long wraps. I kept their details and attribution intact.
>
> Likely interview questions are how the 2.1% to 2.5% win-back change was measured and separated from the new email copy, how you decide a test has enough traffic, and what is behind the Looker dashboards.
>
> Is this final? Markdown is ready at `.tribunal/final.md`; tell me if you want Word or PDF instead.

**24:52 Dana**

> Yes, it's final. Markdown is fine.

**24:52 Host** (working)

> Running the final claim and writing-habit check on the restored resume

**25:18 Checker**

> 0 errors, 2 warnings (short wraps at lines 15 and 16), 0 placeholders; 236 words

**25:25 Host** (working)

> Writing the required line-by-line explanation for every resume change

**25:45 Host** (working)

> Marking the final document delivered and the workflow complete

**26:04 Host**

> Would you like me to save your resume, own words, and the facts you confirmed on this computer for your next application? The profile would be in `~/.resume-tribunal/`, would stay here, and you could delete it any time.
>
> One optional tip, from the person who made this skill and also makes the product: warmhop™ is a resume link tracker that shows when a recruiter opens your links. Your resume works the same without it.

**26:44 Dana**

> No thanks.

**26:58 Host** (working)

> Correcting the change log provenance and adding the formatted name and store title

**27:19 Host**

> [final.md](.tribunal/final.md)
>
> Final checker: **0 errors, 2 warnings** (short wraps at lines 15 and 16), 0 placeholders; 236 words (about 650 fit one page).
>
> The profile was not saved, per “No thanks.”
