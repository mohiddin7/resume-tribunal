# Backend software engineer applying for a senior backend role

Real resume, shared with consent · Auto mode: the other AIs ran by themselves · 2 AIs from 2 companies · 7 minutes · Real public job posting

Every message of the run in order. Times are minutes and seconds from the start. Prompts and replies are in [files/](files/).

**00:00 Marcus**

> I want to apply for this job. My resume is before.md and the posting is job.md. Can you tailor my resume for it?

## Step 1: Setup

**00:00 Host** (working)

> Reading the skill's instructions and the seat guide, then looking for other AIs on this computer

**01:14 Host** (Stop 1)

> Step 1 of 4: Setup
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
> It runs by itself; you answer a few questions along the way.
>
> What I read from your resume, so you can catch a misread:
> - Health insurer (USA), Software Engineer, Aug 2023 - Present
> - Large retailer's technology division (USA), Software Engineer III, May 2023 - Aug 2023
> - Enterprise software company (India), Software Engineer, Feb 2021 - Jul 2022
> - Enterprise software company (India), Software Engineer in Test, Jun 2020 - Feb 2021
> - MS in Computer Science, May 2024, and a Computer Science degree from an engineering college, May 2020
>
> The job is Senior Software Engineer, Backend, in New York. One thing to know now: it asks for 7+ years of backend experience, and your dates add up to about 5 and a half. I won't stretch that; I'll list it with the requirements the resume does not show.
>
> Two questions:
> 1. Pick two or three things this job asks for that you have really done (for example building backend systems that scale, or working with SQL or NoSQL databases). For each, tell me one time you did it: what it was, what you did, what changed. Plain sentences; dictating is fine. These details are what set you apart from other applicants. If you skip this, I'll use your resume's wording as your voice.
> 2. Do you have links to add: LinkedIn, GitHub, a portfolio or project pages, certificate pages? Most recruiters look for LinkedIn.
>
> My plan, unless you say otherwise:
> - Quick review: I write the draft and one other AI checks it, about 6 minutes in all. The other choice is a full council, where three AIs each draft and check each other; here one of them only offers its fast models, so I'd keep it to a quick review. A council takes about 15 minutes and five times the AI usage.
> - No research on hiring trends for this role (say if you want it; it adds a minute or two), I polish the final wording, and you get a plain-text copy while we work, with a PDF or Word file when it's final.
>
> I've hidden your name and contact details. They come back at the end. The second AI is OpenAI's Codex, running GPT-6 Astra; I'm Anthropic's Claude Opus 5.5. The working files are in .tribunal/ inside this folder. This text, including your employers, job history and the pages your links point to, will go to Codex under OpenAI's terms and your account settings there. Some keep their own history, and the text can still identify you. Leave out anything confidential to an employer, and check whether this employer allows AI help with applications.
>
> Answer the questions, or say "yes" to take the defaults and go ahead.

**01:21 Marcus**

> Quick review, please. Yes to the defaults, go ahead. No links.

## Step 2: Draft

**01:57 Host**

> Step 2 of 4: Draft
>
> Thanks. Quick review it is, with no links. You didn't add your own sentences, so I'll keep to your resume's wording as your voice. I'm writing the draft now; then the second AI checks it.

**01:57 Host** (working)

> Writing its own draft from Marcus's resume, trimmed to one page for a backend role

**02:32 Checker**

> 0 errors, 10 warnings (four short second lines, one trailing -ing clause, four lines of old skills only the original resume names, one word Marcus never used)

## Step 3: Review and sign-off

**02:41 Host**

> Step 3 of 4: Review and sign-off
>
> The draft is written: one page, about 490 words, and the automatic checks found no errors. The second AI is reading it now as the hiring manager would, without knowing who wrote it. That usually takes a couple of minutes.

**02:41 Host to Codex**

> Review this resume as the hiring manager for the backend job, check every claim against the candidate's resume, and suggest up to eight fixes and some interview questions.

[p4.txt](files/p4.txt)

**04:50 Codex** (took 129 s)

> As the hiring manager it would not phone yet: "the dated experience falls short of the required seven years", and it reads as mid-level. Its claim check marks three lines as more than the material (the summary joining the Kafka and Beam work to claims processing, JUnit for API tests, and "every build"), and it suggests eight fixes, some needing facts only Marcus has.

[p4_reply_codex.md.txt](files/p4_reply_codex.md.txt)

**04:50 Host** (working)

> Applying the review's wording fixes and the checker's warnings, and holding the fixes that need facts from Marcus

**05:06 Checker**

> 0 errors, 7 warnings (two short second lines, one flagged word that is Marcus's own, four lines of old skills only the original resume names)

**05:34 Host** (Stop 2)

> Step 3 of 4: Review and sign-off
>
> The second AI read the draft as the hiring manager would. Its honest view: the work reads as solid mid-level backend engineering, but the job asks for 7+ years and your dates add up to about 5 and a half, so it would not phone yet for this senior opening. Better wording can't close that gap, and I haven't tried to.
>
> The draft is one page, about 480 words, in .tribunal/resume.md. Changes I made without asking, since they change no fact:
> - Shortened the long summary to two lines about your claims-processing work, the Kafka cluster and your AWS certification, and kept it from implying the Kafka and Beam work fed the claims services.
> - Moved the AWS certification into its own section, and the skills near the top, grouped for a backend job.
> - Reworded bullets in plain resume style, keeping your verbs ("designed and implemented", "enhanced", "minimized the need for manual testing").
> - "Every build got quality checks" became your own "continuous quality checks and rapid feedback on builds", and JUnit stays with unit tests, not API tests.
> - Cut to fit one page: C#, Bootstrap, Eclipse, STS IDE, ServiceNow, Splunk, TCP/IP, AWS EC2 and Agile from the summary and skills, plus the bullets on POJOs and Hibernate mappings, Git, JavaScript form validation, test environments, Agile meetings and JIRA, and the "Environment" lists.
>
> Now the facts. Are all of these true, and could you explain each in an interview? Tell me any to fix. If you don't know a number, I'll leave it out, so please don't estimate.
> 1. Skills that only your old skills list or summary mentions, with nothing in your jobs showing them: Python, TypeScript, Node.js, Express, MySQL, SQL Server, MongoDB, Angular, HTML5, CSS3, Kubernetes and AWS. Which do you really use? Python matters most, because the job names it.
> 2. Your AWS Certified Solutions Architect – Associate: is it still current, and what year did you earn it?
> 3. Your engineering college degree: what is it called? Your resume says "( in Computer Science)", so the degree name is missing.
> 4. The Kafka messaging cluster: what was your own part, and do you know its size (for example how many applications or messages a day)? This is the strongest backend line for this job.
> 5. The line on threads and synchronization: can you name one problem you solved with them? If not, I'll keep the line as it is or cut it, your choice.
> 6. The job is in New York, three days a week in the office, and your resume says Austin. Should the resume say you are relocating, or leave it out?
>
> Answer what you can; anything you skip about a new claim comes out.

**06:21 Marcus**

> I confirm everything in my original resume is true as written.
>
> 1. They're all on my original resume and they're true, so keep the ones that fit. I don't have more detail on Python than what's there.
> 2. I don't know the year offhand, so leave the year off.
> 3. Leave it as my resume has it.
> 4. I don't know more than what's on my resume.
> 5. Keep the line as it is.
> 6. Leave it out.

**06:21 Host** (working)

> Writing Marcus's answers into the sign-off and not-true files, then checking the resume against them

**06:28 Checker**

> 0 errors, 3 warnings (two short second lines, one flagged word that is Marcus's own)

## Step 4: Finalise

**06:36 Host** (Stop 3)

> Step 4 of 4: Finalise
>
> Thanks. Your answers changed nothing on the page: every line already comes from your original resume, which you've confirmed. I left off the certification year and any more detail on the Kafka cluster, said nothing about relocating, and kept the degree and the threads line as they were. The automatic checks find no errors.
>
> Your resume with your name and contact details back in is at .tribunal/final.md.
>
> Want one more blind look from the second AI before it's final? About a minute.
>
> Otherwise, is it final? This computer can't make a PDF or Word file without installing extra software, so you'd get the plain-text copy, which you can paste into Word or Google Docs. Say if you'd rather I install what the PDF needs.

**06:36 Marcus**

> No thanks.

**06:36 Marcus**

> Yes, it's final. Markdown is fine.

**06:36 Host** (working)

> Running the final check on the finished resume

**06:46 Checker**

> 0 errors, 3 warnings (two short second lines, one flagged word that is Marcus's own); 487 words, one page

**06:46 Host**

> Step 4 of 4: Finalise
>
> Your resume is done: .tribunal/final.md, one page, 487 words, with no errors in the final check. Three small style notes remain and I've left them: two lines run a few words onto a second line, and "Enhanced" is a word AI tools overuse, but it's your own.
>
> What the job asks for that this resume does not show:
> - 7+ years of backend experience: your dates add up to about 5 and a half, about 8 months of it in testing.
> - Working with Sales or Support teams to understand customers.
> - Owning a feature through launch and the numbers that follow it.
> - Examples of communication, or of holding a team to high standards.
> - Kotlin (Java and Python are there).
> - Living near New York for three office days a week.
>
> Questions an interviewer is likely to ask about it:
> 1. For the Kafka cluster, what did you design and build yourself, and what decided how you set it up? (Your own part, and real design choices.)
> 2. Walk through one claims-processing feature from request to production. (What you owned from start to finish.)
> 3. What made the Apache Beam framework user-friendly, and who used it? (Whether it solved a real problem for people.)
> 4. For the digital asset management microservices, how did you split the services, and what went wrong later? (Design judgment and production experience.)
> 5. What ran in the Jenkins pipeline, and how did it cut manual testing? (How far the automation went.)
>
> Want me to save what you told me (your resume and the facts you confirmed) on this computer, so your next job needs fewer questions? It stays in ~/.resume-tribunal/, goes nowhere else, and you can delete the folder any time. I can also delete the working files in .tribunal/ now if you'd like; otherwise I'll leave them.

**06:46 Marcus**

> No thanks.
