# Data scientist applying for an AI engineer role

Real resume, shared with consent · Auto mode: the other AIs ran by themselves · 3 AIs from 2 companies · 14 minutes · Real public job posting

Every message of the run in order. Times are minutes and seconds from the start. Prompts and replies are in [files/](files/).

**00:00 Sofia**

> I want to apply for this job. My resume is before.md and the posting is job.md. Can you tailor my resume for it?

## Step 1: Setup

**00:06 Host** (working)

> Reading the resume and the posting, and hiding her name and contact details

**00:30 Host** (Stop 1)

> Step 1 of 4: Setup
>
> ```
> You give:  your resume, the job posting, a few sentences in your own words
>    ↓
> I write a draft, from your facts only
>    ↓
> A second AI, from a different company, checks it without knowing who wrote it
>    ↓
> Automatic checks, then you approve every changed line
>    ↓
> Your resume, the job requirements it does not show, and likely interview questions
> ```
> It runs by itself; you answer a few questions along the way.
>
> What I read from your resume, so a misread file is caught now:
> - Large cloud provider: Solutions Architect Intern – Data Science, May 2023 - Aug 2023
> - University school of public health: Graduate Research Assistant, Nov 2022 - Dec 2023
> - Policy research nonprofit: Data Analyst, Jun 2020 - Jul 2022
> - Four projects (Jun 2022 to May 2023), a Data Science master's (Dec 2023) and a bachelor's in Electronics and Communication (May 2020)
>
> The posting gives no level, so I assumed mid level (it asks for 4+ years) in Chicago, United States. Tell me if that's wrong.
>
> Two questions:
> 1. Pick two or three things this job asks for that you have really done. For each, tell me one time you did it: what it was, what you did, what changed. Plain sentences; dictating is fine. These details are what set you apart from other applicants.
> 2. Any links to add: LinkedIn, GitHub, a portfolio, project pages, papers or certificates? Most recruiters look for LinkedIn.
>
> My plan:
> 1. Quick review: I write the draft and one second AI, from OpenAI, checks it. About 6 minutes, and it runs by itself. Say "full council" for three AIs that each write a draft and check each other's work blind, so two can outvote one that is wrong: about 15 minutes and about five times as much of your AI plans. The Google tool on this computer offers only its fast model, which is why I suggest the quick review.
> 2. No role research, I polish the final wording, and a plain-text copy while we work, with PDF or Word when it's final.
>
> I've hidden your name and contact details. They come back at the end. The other AIs: OpenAI's Codex running GPT-6-astra, and for a full council also Google's Antigravity running Gemini 3.8 Flash (High), plus a fresh copy of me (Claude) that sees only the drafts, to merge them. The working files are in .tribunal. This text, including your employers, job history and the pages your links point to, will go to Codex and Antigravity under their terms and your account settings there. Some keep their own history, and the text can still identify you. Leave out anything confidential to an employer, and check whether this employer allows AI help with applications.
>
> Answer the questions, or say "yes" to take the defaults and go ahead.

**00:30 Sofia**

> Full council, please. Yes to the defaults, go ahead. No links.

## Step 2: Draft

**00:46 Host**

> Step 2 of 5: Draft
>
> Full council it is. Since you have no extra notes or links, I'll use your resume's own wording as your voice. Two other AIs, from OpenAI and Google, are each writing a draft now, and I'm writing a third. This takes a few minutes; nothing needed from you until the sign-off questions.

**00:53 Host to Codex**

> Write a resume for this AI Engineer job using only the candidate's own material, and list what it does not show and what to ask.

[p1.txt](files/p1.txt)

**00:53 Host to Gemini**

> Write a resume for this AI Engineer job using only the candidate's own material, and list what it does not show and what to ask.

[p1.txt](files/p1.txt)

**01:39 Host** (working)

> Writing its own draft from her resume while the other two AIs draft

**02:15 Codex** (took 82 s)

> A full draft in 57 seconds, leading with the graduate research role and keeping her numbers. Its "Not shown" list starts with "4+ years as an engineer shipping production systems" and "Deployed AI agents or LLM-powered tools".

[p1_reply_codex.md.txt](files/p1_reply_codex.md.txt)

**02:15 Host** (working)

> Recording that Google's AI hit its usage limit and carrying on with two drafts

**02:15 Host**

> Step 2 of 5: Draft
>
> The Google AI could not take part: its account has reached its usage limit, which resets in about five days. I'll carry on with two drafts, mine and the OpenAI AI's, which is still a blind check of each by an AI that did not write it. If you'd rather add a Google chat by copy and paste, say so; otherwise nothing is needed from you yet.

**02:26 Gemini** (took 93 s)

> No draft: the tool answered "Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 117h18m16s."

## Step 3: Council

**02:31 Host to Codex**

> Read the other draft as the recruiter and hiring manager for this job and report what is wrong with it, quoting each line.

[p2_codex.txt](files/p2_codex.txt)

**04:08 Codex** (took 97 s)

> Screen decision "No": the draft "does not demonstrate the required four years of engineering experience shipping production systems." It found no unsupported additions; its fixes ask what "overall model efficiency" and the "100% increase in user interaction" measure, and whether the master's was completed.

[critique_codex.md.txt](files/critique_codex.md.txt)

**04:13 Host to Fresh Claude**

> Merge the two anonymous drafts into one resume, applying the critique's findings that hold up against the candidate's material.

[p3.txt](files/p3.txt)

**06:42 Fresh Claude** (took 149 s)

> A merged resume built on Draft R with the role order and several bullet openings from Draft K. It removed the summary and cut "20% increase in overall model efficiency" and "100% increase in user interaction" because "neither metric is defined", and dropped the donor-funds bullet so the older role has fewer bullets.

[p3_reply.md.txt](files/p3_reply.md.txt)

## Step 4: Review and sign-off

**06:55 Checker**

> 0 errors, 20 warnings (nine line-length, four old-skill groups, three wording, two layout patterns, two trailing clauses)

**06:55 Host**

> Step 4 of 5: Review and sign-off
>
> The two drafts are merged into one, and the automatic checks found no errors. The OpenAI AI is now reading the merged resume as the hiring manager would, without knowing who wrote it. This takes a minute or two; your sign-off questions come next.

**06:56 Host to Codex**

> Review the merged resume as the hiring manager: check each claim against her material, suggest fixes, and list likely interview questions.

[p4.txt](files/p4.txt)

**09:09 Codex** (took 133 s)

> Screen decision "No phone screen for this mid-level role", for lack of "four years of engineering experience shipping production systems". The claim check marks no line MORE THAN THE MATERIAL; its fixes ask about work after Dec 2023, whether the master's was completed, moving Linux out of the cloud line, and the baselines behind several numbers.

[p4_reply_codex.md.txt](files/p4_reply_codex.md.txt)

**09:09 Host** (working)

> Applying the review's wording fixes and the checker's, and holding the fixes that need facts from her

**09:39 Checker**

> 0 errors, 13 warnings after two wording passes (six line-length, four old-skill groups, one AI-sounding word she wrote herself, one hyphen, one three-item-list pattern)

**10:07 Host** (Stop 2)

> Step 4 of 5: Review and sign-off
>
> The draft is at .tribunal/resume.md (your name and contact details go back in at the end). The OpenAI AI checked every line against your resume and found none that claims more than your resume says.
>
> One straight answer first: reading as the hiring manager, it would not phone yet, because the job asks for 4+ years shipping production systems and the page shows two years as an analyst, a research role and an internship. Better wording can't close that gap; only facts you really have can.
>
> Changed without asking (same facts, new wording): bullets reordered for this job and some reworded with the result first, "Masters" spelled "Master's", the skills regrouped under Cloud and systems, Data platforms and databases, Machine learning and Analytics, and the "Advance knowledge" label dropped. The automatic checks found no errors; what remains are wording notes: a few bullets run just over one line, and "enhanced" and "real-time" are flagged, though "enhanced" is your own word.
>
> Cut to keep the page on what this job wants: the summary, the monthly-reports bullet (doubled publications, 45% more donor funds), the basketball shot-selection project, and two numbers a reader would not know how to read: "20% increase in overall model efficiency" and "100% increase in user interaction".
>
> Questions about facts. Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave it out, so please don't estimate.
> 1. The skills line calls your CNN and YOLOv7 work "computer vision". Is that fair?
> 2. These skills appear only in your old skills list, with nothing on the page showing them: R, SAS, HTML, CSS, Azure, Linux, Snowflake, Databricks, Hive, Hadoop, HDFS, Alteryx, Microsoft Power BI and SPSS. Which have you really used, and which should go?
> 3. Your resume stops at Dec 2023. Have you worked, studied or built anything since then?
> 4. Was the Data Science master's awarded, and when? If so, I'll show it as a degree instead of "Candidate".
> 5. The PDF invoice automation: what did you build, and who used it?
> 6. Is the 14% accuracy gain on the basketball models percentage points or relative, and compared with what? And how was the 0.9916 F1-score tested (which data, and was there a held-out set)?
> 7. The two numbers I cut: can you say what "overall model efficiency" and "user interaction" measured? If so, they go back in.
> 8. The job asks for things your resume doesn't show: building or deploying AI agents or LLM tools, Ruby, Node.js or Next.js, deploying and monitoring on the cloud, debugging backend systems, and using AI tools in your own coding. Have you done any of these? Tell me only what you really did.
>
> Answer what you can in plain sentences; "skip" is fine for any question.

**11:06 Sofia**

> I confirm everything in my original resume is true as written.
>
> 1. Yes, that's fair.
> 2. They're all on my original resume and true, so keep the ones that fit.
> 3. Nothing to add.
> 4. Leave it as my resume has it.
> 5. I don't know more than what's on my resume.
> 6. I don't know, so keep them as my resume has them.
> 7. No, leave them out.
> 8. No.

**11:07 Host** (working)

> Writing her sign-off answers into the confirmed facts and the not-true list

**11:19 Checker**

> 0 errors, 9 warnings (five line-length, one AI-sounding word she wrote herself, one hyphen, one three-item-list pattern); the old-skill notes cleared by her sign-off

## Step 5: Finalise

**11:20 Host**

> Step 5 of 5: Finalise
>
> Thank you. Your answers changed no line on the page: everything stays as your resume has it, the two unclear numbers stay out, and the requirements you said no to go on the list of what the resume does not show. The OpenAI AI is taking one last blind look at the finished version now, with your confirmed answers beside it; about a minute.

**11:20 Host to Codex**

> Take a last look at the signed-off resume as the hiring manager, with her confirmed answers, and check each claim against her material.

[p4_final.txt](files/p4_final.txt)

**13:26 Codex** (took 126 s)

> Screen decision still "No", for lack of "production software engineering experience"; "no line warrants MORE THAN THE MATERIAL". Seven optional fixes: trim the skills lists, move Skills below Experience, "using AWS S3 and AWS EC2", "analysis time", restore "instrumental in advocating for and facilitating policy change", and cut the pandemic project.

[p4_final_reply_codex.md.txt](files/p4_final_reply_codex.md.txt)

**13:26 Host** (Stop 3)

> Step 5 of 5: Finalise
>
> Your resume, with your name and contact details back in, is at .tribunal/final.md.
>
> The last blind look found no line that claims more than you told me. It suggested seven optional changes. I dropped one and a half: moving Skills below Experience, which would hide your tools from a quick scan, and changing your "analyzing time" to its own wording. The six that survived:
> 1. Programming languages: keep only Python and SQL.
> 2. Databases: put MS SQL Server first and keep only the ones you'd want to discuss in an interview.
> 3. Analytics: keep Excel and Tableau and cut Power BI, SPSS and Alteryx, so the page reads less like an analytics profile.
> 4. "Designed and tested over 30 ML models on AWS S3 and AWS EC2": say "using AWS S3 and AWS EC2", as your resume does.
> 5. The 100+ SQL queries bullet: put back your fuller wording, "reports instrumental in advocating for and facilitating policy change".
> 6. Cut the pandemic impact analysis project, to give the Python and Solutions Architect work more room.
>
> Is it final? Tell me which of these to apply, or say it's final as it is, and whether you want a plain-text copy, a PDF or a Word file.

**13:49 Sofia**

> Yes, it's final. Markdown is fine.

**14:07 Checker**

> Final: 0 errors, 9 warnings (five line-length, one AI-sounding word she wrote herself, one hyphen, one three-item-list pattern); 508 words, one page

**14:07 Host**

> Step 5 of 5: Finalise
>
> Done. Your resume is .tribunal/final.md, a plain-text copy you can paste into Word or Google Docs and give heading styles. It is about 508 words, so it fits one page, and the final check found no errors. None of the optional changes were applied, as you said it's final as it is.
>
> What this job asks for that the resume does not show:
> - 4+ years as an engineer shipping production systems
> - Building or deploying AI agents or LLM-powered tools (your Python automation counts as workflow automation, but not this)
> - A second language from Ruby, Node.js or Next.js alongside Python
> - Backend debugging, tracing issues across services, and working across several codebases at once
> - Cloud deployment, monitoring and basic DevOps beyond training models on AWS and GCP
> - Using AI tools in your own coding
> - Custom demos or proofs of concept for customers, Stripe or payments experience, and Salesforce or Gong integrations
>
> Questions an interviewer is likely to ask, so you can prepare:
> 1. For the PDF invoice automation, what did your Python code do, and how was the 80% cut in data entry time measured? (Tests how much you built yourself.)
> 2. In the SQL Server and Tableau work, what did you do and what did the IT team do? (Tests your own part in a team result.)
> 3. What did "accuracy" mean in the basketball video analysis, and what produced the 14% gain and the 25% runtime cut? (Tests whether you can explain your numbers.)
> 4. How was the news classifier's 0.9916 F1-score tested, and how did you rule out duplicate articles between training and test data? (Tests how carefully you evaluate models.)
> 5. How did the Tableau dashboards lead to annual savings of 800K rupees, and who worked that figure out? (Tests the link between your work and the result.)
>
> Save what you told me (your resume, your own words and the facts you confirmed) on this computer, so your next job needs fewer questions? It stays in ~/.resume-tribunal/, goes nowhere else, and you can delete the folder any time. I can also delete the working files in .tribunal/ if you'd like.

**14:07 Sofia**

> No thanks.
