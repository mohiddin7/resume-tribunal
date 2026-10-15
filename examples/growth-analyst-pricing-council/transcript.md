# Growth analyst applying for a senior pricing analyst job

Fictional candidate · 4 AIs from 3 companies · 19 minutes · Real public job posting

Every message of the run in order. Times are minutes and seconds from the start. Prompts and replies are in [files/](files/).

## Step 1: Setup

**00:00 Host** (working)

> Reading the resume, the job posting and Dana's own words, and hiding her name and contact details

**00:51 Host** (Stop 1)

> Step 1 of 5: Setup
>
> Here is how this works:
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
>
> It runs by itself; you answer a few questions along the way. (A second AI checks the work because an AI tends to go easy on its own writing.)
>
> **What I read from your resume**, so a misread file shows up now:
> - Online home-goods retailer: Marketing Coordinator, then Marketing Analyst, Mar 2019 to present
> - Regional sporting-goods chain: Store Manager, 2014 to 2019
> - BA Communications, 2014; Google Data Analytics Certificate, 2020
>
> The posting is for a Senior Analyst, Pricing and Business Analytics, remote anywhere in the US. I'm aiming at that level and country; tell me if that's wrong.
>
> **One question:** your resume has two links (your portfolio and a Linktree). Do you have others to add, such as LinkedIn, GitHub, or a certificate link? Most recruiters look for a LinkedIn profile.
>
> **My plan, unless you say otherwise:**
> 1. Full council: three AIs each write a draft and then critique each other's drafts without knowing who wrote which, so two can outvote one that is wrong. About eight calls and 15 minutes. Say "quick" for one checker instead: about 6 minutes and about a fifth of the AI usage on your plans.
> 2. No extra research on the role (the posting is detailed enough), I polish the final wording, and you get a plain-text copy while we work, with PDF or Word when it's final.
>
> I've hidden your name and contact details, and the name of your colleague. They come back at the end.
>
> Taking part: OpenAI's GPT-6 Astra (through Codex) and Google's Gemini 3.8 Flash, high effort (through Antigravity), alongside me (Anthropic, Claude Opus 5.5). Google's tool here offers no model at the same level as the other two, so Gemini Flash is its strongest option. A fresh copy of me with no memory of this conversation combines the drafts, so I never judge my own. Working files are in `growth-analyst-real-jd-council/.tribunal/`.
>
> This text, including your employers and job history, will go to Codex (OpenAI) and Antigravity (Google) under their terms and your account settings there. Some keep their own history, and the text can still identify you. Leave out anything confidential to an employer, and check whether this employer allows AI help with applications.
>
> Answer the question, or say "yes" to take the defaults and go ahead.

**00:58 Dana**

> Full council, please. Yes to the defaults, go ahead. Only the links already on my resume.

## Step 2: Three drafts

**01:03 Host** (working)

> Writing its own draft first, before reading anything from the other two

**01:30 Host to Codex**

> Write a resume for this job using only the facts in the candidate's material. The name and contact details are hidden.

[p1.txt](files/p1.txt)

**01:30 Host to Gemini**

> Write a resume for this job using only the facts in the candidate's material. The name and contact details are hidden.

[p1.txt](files/p1.txt)

**02:34 Codex** (took 64 s)

> Here's my draft. (It kept the "Managed $2.4M email marketing budget" line from the old resume.)

[p1_reply_codex.md.txt](files/p1_reply_codex.md.txt)

**05:17 Gemini** (took 227 s)

> Here's my draft. (It kept "15 associates" next to "about 12 part-time staff", and the Tableau dashboards.)

[p1_reply_agy.md.txt](files/p1_reply_agy.md.txt)

## Step 3: Council

**05:33 Host**

> Step 3 of 5: Council. All three drafts are in and each has been checked by the other AIs; now combining them into one. Nothing to do yet; I'll come back with a short list of facts to confirm.

**05:50 Host to Codex**

> Read drafts K and M as the hiring manager would. Would you phone this person? What would you fix?

[p2_codex.txt](files/p2_codex.txt)

**05:50 Host to Gemini**

> Read drafts R and K as the hiring manager would. Would you phone this person? What would you fix?

[p2_agy.txt](files/p2_agy.txt)

**07:06 Codex** (took 76 s)

> On draft K: "Screen decision: No. It does not demonstrate the pricing analytics experience central to this role." It also flagged the combined Coordinator/Analyst dates, which hide how long she has been an analyst.

[critique_codex.md.txt](files/critique_codex.md.txt)

**08:59 Gemini** (took 189 s)

> On draft R's budget line: "A hiring manager will doubt this claim because managing a multi-million-dollar marketing budget attributes department-level spend authority to an individual analyst."

[critique_agy.md.txt](files/critique_agy.md.txt)

**09:12 Host to Fresh Claude**

> Merge the three drafts, starting from K. Where they disagree, go with the candidate's own words, and list what you couldn't settle.

[p3.txt](files/p3.txt)

**10:21 Fresh Claude** (took 69 s)

> Merged. Settled the disagreements from her own words: "about 12 part-time staff", the 2.1% to 2.5% result with the email manager credited, and analysis of the team's tests instead of "Led A/B testing". The $2.4M budget went to the questions for Dana.

[p3_reply.md.txt](files/p3_reply.md.txt)

## Step 4: Review and sign-off

**10:37 Host to Codex**

> You're the hiring manager for this job. Would you phone this candidate? Check every claim against their material.

[p4.txt](files/p4.txt)

**10:38 Checker**

> Checked the merged resume against Dana's material.

**12:10 Codex** (took 93 s)

> "Screen decision: No." The deciding reason is pricing, which her material doesn't show. The claim check found no line that says more than her material does.

[review_codex.md.txt](files/review_codex.md.txt)

**12:34 Host** (working)

> Applying the review's wording fixes and checking the resume again

**13:17 Host** (Stop 2)

> Step 4 of 5: Review and sign-off
>
> The three drafts are combined, a second AI has checked the result without knowing who wrote it, and the automatic checks have run. Your working copy is `.tribunal/resume.md` (your name and contact details go back in at the end).
>
> **Wording I changed without asking** (no facts changed): a summary built from your own description of the job instead of "results-driven professional"; your win-back, A/B test, Looker and pandas lines in your own words, keeping "about" and "maybe"; "Analyze" in US spelling; the win-back work split into two shorter lines.
>
> **What I left out of your old resume**, because your own words describe it differently or nothing backs it. Say the word and I'll put any of it back, in your words:
> - "10+ years of experience" (your analytics work starts in 2019)
> - "Increased email conversion rate by 18%", replaced by your 2.1% to 2.5%
> - "Led A/B testing program across email and landing pages", replaced by what you said you do
> - "Managed $2.4M email marketing budget"
> - "Built Tableau dashboards for executive stakeholders"
> - "Coordinated the social media calendar and weekly reporting in Google Analytics"
> - "Managed a team of 15 associates", replaced by your "about 12 part-time staff"; and "Consistently exceeded sales targets"
> - The soft-skills list (stakeholder management, data storytelling, cross-functional leadership)
>
> **Please check these facts:**
> 1. You said "about 12 tests in the last year". The resume says "About 12 tests in the year to Oct 2026". Is that the right period?
> 2. When were you promoted from Marketing Coordinator to Marketing Analyst (month and year)? With it, each title gets its own dates, so a reader can see how long you've been an analyst. Without it, they stay together.
> 3. Older skills that only your old resume mentions: Tableau, R, dbt, Google Analytics and Excel (Excel also appears in the store-manager line). Do you still use each of these, enough to talk about it in an interview?
> 4. The $2.4M email budget: what was your part in it? If you didn't manage it yourself, it stays off.
> 5. This job centres on pricing. Have you done any pricing work at all, such as analysing a discount, promotion or price test? If not, that's fine; it stays off.
> 6. The posting asks for using AI tools to speed up or check analysis, and for creating tables in SQL. Have you done either? Tell me what you did, in a sentence.
>
> Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave it out, so please don't estimate.
>
> One small layout note: the win-back line runs just past one line; I'll tighten it after your answers.
>
> Reply with your answers to 1 to 6, and anything to put back or fix.

**14:20 Dana**

> 1. Roughly, yes: it's about the last twelve months, but I couldn't tell you exactly when it started.
> 2. July 2022.
> 3. Tableau only in the certificate course, not at work. R was one course, I wouldn't put it on. I've read the dbt models our data engineer wrote, but I've never written one. I use GA4 most days, and Excel was the store's scheduling and inventory sheets.
> 4. I never managed a budget. $2.4M was the email channel's revenue last year in our dashboard, nothing I controlled.
> 5. I've never worked on pricing or built a pricing model.
> 6. I sometimes ask ChatGPT to help me fix a SQL query. I haven't built any automations. I write queries, and I've made a few saved views in BigQuery, never schemas.
>
> Please put the coordinator line back: as coordinator it was mostly social posting, plus the weekly reporting in Google Analytics.

**14:29 Host** (working)

> Putting Dana's answers in and checking the resume again

## Step 5: Final

**14:43 Host to Codex**

> One last blind look before this goes out. Anything to fix?

[p4_final.txt](files/p4_final.txt)

**14:43 Host to Gemini**

> One last blind look before this goes out. Anything to fix?

[p4_final.txt](files/p4_final.txt)

**16:00 Codex** (took 77 s)

> Last look done. Its suggestions went back to the host, which keeps only the ones that add nothing new.

[final_review_codex.md.txt](files/final_review_codex.md.txt)

**18:11 Gemini** (took 208 s)

> Last look done. Its suggestions went back to the host too.

[final_review_agy.md.txt](files/final_review_agy.md.txt)

**18:40 Checker**

> Final check of the finished resume: no errors.

**18:51 Host** (Stop 3)

> Step 5 of 5: Finalise
>
> Your resume with your name and contact details back in is at `growth-analyst-real-jd-council/.tribunal/final.md`. It passes the automatic checks and fits on one page (256 words).
>
> What changed since your answers:
> - Your two titles now have their own dates: Marketing Analyst from Jul 2022, Marketing Coordinator Mar 2019 to Jul 2022, with your coordinator line back in your words ("mostly social posting, plus the weekly reporting in Google Analytics").
> - Added your saved views in BigQuery and your use of ChatGPT to help fix SQL queries.
> - Skills now list GA4; Tableau, R and dbt are off, as you said.
> - I put the win-back, Looker and A/B test work under Marketing Analyst, since you describe it as your analyst work. Tell me if any of it was before July 2022.
>
> The other two AIs took one more blind look. One of them read "build its Looker dashboards" in the summary as claiming more than the email and paid social dashboards you built, so I put your own wording back there. Two suggestions survived, both optional:
> 1. Split "Made a few saved views in BigQuery; sometimes ask ChatGPT to help fix a SQL query" into two separate lines.
> 2. Cut the ChatGPT part, as one reviewer thought it reads oddly. (The posting asks for AI use, which is why I kept it.)
>
> I dropped 6 other suggestions because they would have dropped your "maybe" and "mostly", swapped your words for stock phrases like "partnered with", left the test count undated, or made a line too long.
>
> One line still runs a few words past a single line (the win-back result); it is fine as it is.
>
> Is it final? Tell me which of the two suggestions to apply, if any, or say "it's final".

**18:51 Dana**

> Yes, it's final. Markdown is fine.

**19:09 Host**

> Step 5 of 5: Finalise
>
> Done. Your final resume, as a plain-text copy, is at `growth-analyst-real-jd-council/.tribunal/final.md`. It passes the automatic checks with no errors and fits on one page.
>
> **What this job asks for that your resume does not show.** Be ready for these, or decide whether to apply:
> - Pricing analytics: pricing models and pricing A/B tests. This is the centre of the role, and you told me you have not done it. Both reviewing AIs said they would not phone for this reason, so expect it to be the main question.
> - Working with Finance and Product teams, and presenting findings to senior executives (your dashboards go to the marketing director)
> - Creating new tables or schemas in SQL (you have made a few saved views)
> - Building automations or AI tooling (you use ChatGPT to help fix SQL)
> - Maintaining company-wide KPI datasets
> - Nice to have: experience at a subscription business
>
> **Questions an interviewer is likely to ask about your claims:**
> 1. For one of your roughly 12 tests, how did you decide there was enough traffic, and what did you recommend from the results? (Tests whether you understand sample size and can turn results into a recommendation.)
> 2. How was win-back conversion measured, how many customers were in each group, and what else changed between 2.1% and 2.5%? What was your part and what was the email manager's? (Tests how the result was measured and who did what.)
> 3. Walk me through one of your saved views in BigQuery: what data, which joins, and how you checked the output. (Tests SQL depth.)
> 4. What decisions did the marketing director make from your Looker dashboards? (Tests whether your reporting changed anything.)
> 5. Tell me about a SQL problem ChatGPT helped you fix, and how you checked its answer. (Tests how you use and verify AI help.)
>
> The working files stay in `.tribunal/` unless you'd like me to delete them.
>
> Save what you told me (your resume, your own words and the facts you confirmed) on this computer, so your next job needs fewer questions? It stays in `~/.resume-tribunal/`, goes nowhere else, and you can delete the folder any time.
>
> One optional tip, from the person who made this skill and also makes the product: warmhop™ is a resume link tracker that shows when a recruiter opens your links. Your resume works the same without it.
