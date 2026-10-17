# Backend software engineer applying for a senior backend role

Real resume, shared with consent · Auto mode: the other AIs ran by themselves · 2 AIs from 2 companies · 12 minutes · Real public job posting

Every message of the run in order. Times are minutes and seconds from the start. Prompts and replies are in [files/](files/).

## Step 1: Setup

**00:00 Host** (working)

> Reading its setup instructions and detecting the available reviewers

**00:00 Host**

> Step 1 of 4: Setup
>
> I'm using the resume-tribunal skill to tailor your resume from your facts and arrange an independent review. I'll read your files and check which reviewers are available before asking for consent.
>
> Next, review the setup choices I'll show you.

**00:38 Host** (Stop 1)

> Step 1 of 4: Setup
>
> You give: your resume, the job posting, a few sentences in your own words
> ↓
> I write a draft, from your facts only
> ↓
> A second AI, from a different company, checks it without knowing who wrote it
> ↓
> Automatic checks, then you approve every changed line
> ↓
> Your resume, the job requirements it does not show, and likely interview questions
>
> The second AI runs by itself; you answer a few questions along the way. Its independent review helps catch mistakes and unsupported claims.
>
> I read these roles:
> - Health insurer (USA), Software Engineer, Aug 2023 - Present.
> - Large retailer's technology division (USA), Software Engineer III, May 2023 - Aug 2023.
> - Enterprise software company (India), Software Engineer, Feb 2021 - Jul 2022.
> - Enterprise software company (India), Software Engineer in Test, Jun 2020 - Feb 2021.
>
> The target is Brex's senior backend role in New York, United States. It asks for 7+ years; your resume says 4+, so that gap will remain visible.
>
> Pick two or three things this job asks for that you have really done. For each, tell me one time you did it: what it was, what you did, what changed. Plain sentences; dictating is fine. You can skip this and I'll use your resume's wording. Do you have LinkedIn, GitHub, portfolio, project, paper or certification links to include? Your college degree title is incomplete; please supply it if you can.
>
> My default is a quick review: I write and one other AI checks. A full council adds drafts and reviews, takes longer and uses several times as much of your AI plans. Role research stays off, I'll polish the wording, and we'll work in Markdown, a plain-text format, with PDF or Word available at the end.
>
> Model line: I am OpenAI GPT-6, flagship tier; the proposed reviewer is Anthropic's opus, listed as its most capable model, at high effort. Both automatic tools were detected; Google's available models are Flash, so I propose the closer tier match for this quick review.
>
> I've hidden your name and contact details. They come back at the end. Working files are in `.tribunal/` inside this run folder.
>
> This text, including your employers, job history and the pages your links point to, will go to Anthropic through Claude Code using opus under their terms and your account settings there. Some keep their own history, and the text can still identify you. Leave out anything confidential to an employer, and check whether this employer allows AI help with applications.
>
> Answer the questions, or say "yes" to take the defaults and go ahead.

**01:00 Marcus**

> Quick review, please. Yes to the defaults, go ahead. No links.

## Step 2: Draft

**01:01 Host** (working)

> Writing its draft from his original resume and keeping the seniority gap visible

**01:05 Host**

> Step 2 of 4: Draft
>
> I'll emphasize Java, Spring Boot, databases, testing and deployment work, while keeping all four roles and their original titles. I'll trim repeated tool lists and less relevant front-end detail to aim for one page. With no links or extra stories, your original resume supplies the facts and voice. Most recruiters look for LinkedIn; I'll respect your choice to leave links out.
>
> Next, I'll send the draft for the independent review you approved.

**01:40 Checker**

> 0 errors, 5 warnings (four possible short wraps and the candidate's own word Enhanced), 3 contact placeholders; 426 words

## Step 3: Review and sign-off

**01:40 Host**

> Step 3 of 4: Review and sign-off
>
> The draft is ready for independent review. The automatic check found no errors and five wording or line-length warnings; I'll resolve those alongside the review. Your name and contact details are still hidden.
>
> Next, I'll bring you the draft and the factual questions that need your sign-off.

**01:46 Host to Claude**

> Review the resume against the candidate's facts and job requirements, check each claim, and suggest interview questions.

[p4-review.txt](files/p4-review.txt)

**02:39 Host**

> Step 3 of 4: Review and sign-off
>
> The independent review is still running. It is checking each claim against your original resume, including the Kafka architecture claim and the incomplete education entry.
>
> Next, I'll combine its findings with the automatic checks for your sign-off.

**03:47 Claude** (took 121 s)

> The reviewer found every resume claim supported, but would not phone for this senior role because the experience requirement is not shown. It suggested clarifying Kafka scope, the college degree and certification, and supplied five interview questions.

[p4-review-reply.md.txt](files/p4-review-reply.md.txt)

**03:47 Host** (working)

> Applying its review's safe wording fixes and holding factual changes for his sign-off

**04:04 Checker**

> 0 errors, 3 warnings (one short wrap, Enhanced from the original, and the new word supported), 3 contact placeholders; 428 words

**04:04 Checker**

> 0 errors, 2 warnings (one possible short wrap in the Kafka bullet and Enhanced from the original), 3 contact placeholders; 427 words

**04:28 Host** (working)

> Correcting its last recorded word count to 428 words, as the checker printed

**04:28 Host** (Stop 2)

> SIGN-OFF QUESTIONS
> Step 3 of 4: Review and sign-off
>
> Please review every rewritten line in the [draft](.tribunal/resume.md). Your contact details are still hidden.
>
> I shortened the summary, moved the AWS credential to its own section, split long bullets and removed repeated environment lists, coursework and less relevant front-end detail. All four roles, titles and dates remain. The draft is 428 words. Two warnings remain: “Enhanced” is your original word, and the Kafka bullet may wrap slightly onto a second line; I kept its meaning intact.
>
> The independent review found the claims supported by your resume, but judged the application short of this role's senior experience requirement. I kept your original 4+ years and did not replace it with a calculated total.
>
> Please confirm or correct these facts:
>
> 1. The draft says you “Designed and implemented a scalable Kafka Messaging Cluster for distributed publishing across business applications.” What was your own part: broker/cluster design and operation, application producers and consumers, or something else? If you know the scale, give only a figure you can verify.
> 2. Did you create the Apache Beam framework described, and can you explain a concrete use of Threads, Multithreading, Synchronization and the Collection API? If either line overstates your part, tell me the narrower version.
> 3. Skills listed without a work example need one grouped check: can you stand behind SQL and MongoDB, and is the AWS Certified Solutions Architect – Associate credential accurate as shown? What year was it earned, and is it current? Python is currently omitted; only if you want it included, describe your actual use.
> 4. What is the exact engineering-college degree title? Were any roles contract, part-time or internships, including the three-month Software Engineer III role? I'll keep the original dates and unnamed employers and schools.
> 5. Only if true, is there evidence we have missed for 7+ years of professional backend work, owning a feature from concept through production and monitoring, or working directly with Sales or Support on customer needs? You can also add a specific architecture decision, verified result, or New York office availability. Otherwise these remain unshown; no number is required.
>
> Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave it out, so please don't estimate.

**09:28 Marcus** (answered after 16 min)

> I confirm everything in my original resume is true as written.
> 1. Leave it as my resume has it. I don't know the scale.
> 2. Leave those as my resume has them.
> 3. Yes, SQL, MongoDB and the AWS certification are true as my resume has them. Leave Python out.
> 4. Leave the degree and the roles as my resume has them.
> 5. Nothing to add for those.

**09:28 Host** (working)

> Recording its candidate's confirmation and keeping the original scope without new numbers

**09:28 Host**

> Step 3 of 4: Review and sign-off
>
> Your original claims stay, with no added scale figures, credential dates or degree title. Python stays out. I'll finish the plain-text copy and leave the unshown requirements in the accompanying notes.
>
> Next, review the final file when I show its path.

**09:36 Checker**

> 0 errors, 2 warnings (one possible short wrap in the Kafka bullet and Enhanced from the original), 3 contact placeholders; 428 words

## Step 4: Finalise

**09:54 Host** (Stop 3)

> Step 4 of 4: Finalise
>
> Your [resume is ready in final.md](.tribunal/final.md), with your name and contact details restored. No new facts were added after your confirmation. The two explained wording and possible wrapping warnings remain.
>
> Would you like one more independent look? Otherwise, is this final, and is Markdown, the plain-text copy, the format you want?

**10:01 Marcus**

> No thanks.

**10:01 Marcus**

> Yes, it's final. Markdown is fine.

**10:01 Checker**

> 0 errors, 2 warnings (one possible short wrap in the Kafka bullet and Enhanced from the original), 0 placeholders; 430 words

**10:01 Host** (working)

> Writing its line-by-line change reasons and checking the public recording for completeness

**10:07 Host** (working)

> Correcting its final recorded word count to 431 words, as the checker printed

**11:25 Host**

> Step 4 of 4: Finalise
>
> Your [final Markdown resume](.tribunal/final.md) is ready. The final check found 0 errors, 2 explained warnings and no placeholders, at 431 words. The warnings are the possible Kafka line wrap and your original word “Enhanced.”
>
> The application still does not show 7+ years of backend experience, direct Sales or Support collaboration, or ownership from concept through ongoing production outcomes. New York office availability and measured scale remain unspecified. Your original architecture claims remain intact.
>
> Prepare to explain:
> - Which Kafka design and implementation decisions were yours?
> - How does a claim move through your services, and what happens when a step fails?
> - What existed before the microservices architecture, and why were those design choices made?
>
> The [notes](.tribunal/notes.md) preserve these gaps and interview prompts. The recording completeness check passed.
>
> I can delete the working folder after you keep your final resume; otherwise I'll retain this recording. Save what you told me on this computer so your next job needs fewer questions? It would stay in `.resume-profile/` inside this run folder, go nowhere else, and you could delete it any time.

**11:48 Marcus**

> No thanks.

**12:05 Host**

> Step 4 of 4: Finalise
>
> Final file: [final.md](.tribunal/final.md). Final checker output:
>
> ```text
> WARN  line 19: short-second-line: about 1.01 lines; tighten it to one line if you can
> WARN  line 33: ai-marker-word: "Enhanced"
> 0 error(s), 2 warning(s), 0 placeholder(s) to fill; 431 words (about 650 fit one page)
> ```
>
> No profile saved.
