---
title: Resume skills for AI assistants, compared honestly
description: Six free skills that tailor your resume to a job, including the one I made. What each one does well, where each falls short, and how to pick.
date: 2026-10-11
---

**Disclosure first:** I made one of the six, Resume Tribunal. I've tried to be fair, and I've said where mine loses. Everything below comes from reading each skill's own files on 11 October 2026, and the star counts are from GitHub on that day. Skills change quickly, so check before you rely on any detail.

## First, what is a "skill"?

If your experience of AI is typing a question into ChatGPT and getting an answer, a skill is a small addition to that. It is a folder of written instructions that an AI assistant loads when your request matches. Instead of pasting a long prompt every time, you install the skill once and say "tailor my resume to this job".

Skills work in coding tools such as Claude Code, Codex and Cursor, and some chat apps, including the Claude app, let you upload them.

**Do you need one?** Not always. If you want one bullet point reworded, a plain prompt is fine. A skill earns its place when you'll apply to many jobs and want the AI to follow the same careful process each time.

## What a good resume skill should do

Here's what I looked for, and why.

1. **Never invent.** A number you can't explain in an interview does more harm than a line with no number at all.
2. **Keep the layout readable by screening software.** Applicant tracking systems (ATS) are the software employers use to collect applications. Columns, tables, text in headers and images can scramble what they read.
3. **Skip the ATS myths.** You'll often see "75% of resumes are rejected by ATS". That figure [traces back to a vendor that closed in 2013](https://hrtact.com/2020/10/05/your-job-application-was-rejected-by-a-human-not-a-computer/), and no study supports it. [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/41131886674075-Talent-Matching-FAQ), a widely used ATS, describes its matching as a way to sort applicants. It does not reject them automatically. Most resumes are rejected by people.
4. **Use the job's words where they're true, and don't stuff keywords.** A recruiter searching for "Power Query" should find it if you've used it. A list of keywords you don't have helps no one.
5. **Get an independent check.** AI models are [noticeably more lenient with their own output](https://arxiv.org/abs/2604.06996). Self-review catches less.
6. **Protect personal details, and be upfront about time and cost.**

## The six skills

### ResumeSkills

[Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills), about 2,650 stars, MIT license.

**What it is:** a collection of 22 skills covering the whole job search: tailoring, an ATS optimizer, bullet writing, cover letters, interview prep, cold emails and filling in application forms.

**Good at:** breadth. One install covers most of a job search, and it installs with a single `npx skills add` command.

**Watch out for:** I read two of the 22 closely. The tailoring skill asks the AI to add missing keywords from the posting, with a principle of staying truthful. The ATS optimizer repeats the 75% figure and computes a keyword match score against the job posting. Neither one checks the new resume against what you originally said.

### Resume Tailoring Skill

[varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill), about 770 stars, MIT license.

**What it is:** the most thorough of the group. It builds a library from your past resumes and researches the company and role. It matches content with confidence scores and asks branching questions to surface experience you forgot to write down. It also has a batch mode for three to five similar jobs, and gives you Word and PDF files plus interview prep.

**Good at:** finding experience that isn't on your resume yet, and reusing your history across many applications. It stops at checkpoints for your approval.

**Watch out for:** it works best with a library of past resumes; the README suggests ten or more for best results. At about 4,600 words, it is also the longest skill here, which means more for the AI to read on every run. The same AI researches, writes and judges.

### resume-cover-letter

Part of [jezweb/claude-skills](https://github.com/jezweb/claude-skills), a collection with about 1,060 stars, MIT license.

**What it is:** a single skill for a resume or CV and a cover letter, with regional formats for Australia and New Zealand, the US and the UK.

**Good at:** cover letters and country conventions, with clear, practical advice on structure and tone.

**Watch out for:** it tells the AI to mirror the listing's language and aim for at least 60% of bullets with a measurable result. That's reasonable advice for a person. For an AI, pressure to add numbers is where invention starts if you didn't supply any. There's no independent check.

### Proficiently tailor-resume

[proficientlyjobs/proficiently-claude-skills](https://github.com/proficientlyjobs/proficiently-claude-skills), about 420 stars, no license file.

**What it is:** resume tailoring as one part of a job-search product that also finds jobs and applies for you.

**Good at:** the strictest anti-invention rules I read. Never infer scope, never add responsibilities, never assume partnerships that aren't listed. It bans long dashes, reviews the draft sentence by sentence for AI-sounding writing, and saves your corrections so you don't have to repeat them.

**Watch out for:** with no license file, the terms for reusing it are unclear, and it belongs to a larger commercial product. Review is done by the same AI that wrote the draft.

### Claude Code Job Tailor

[javiera-vasquez/claude-code-job-tailor](https://github.com/javiera-vasquez/claude-code-job-tailor), about 170 stars, CC BY-NC 4.0 license.

**What it is:** closer to an app than a skill. You write your experience once in a structured file. Three agents analyse the posting, weight the requirements, and produce a tailored PDF in about a minute, with a live preview in your browser.

**Good at:** speed and polished PDFs, once it's set up.

**Watch out for:** it needs Claude Code plus a JavaScript runtime and some setup, it only works with Claude, and the license forbids commercial use.

### Resume Tribunal (mine)

[mohiddin7/resume-tribunal](https://github.com/mohiddin7/resume-tribunal), new, MIT license.

**What it is:** tailors your resume to one job. Your assistant writes the draft, and an AI from a different company reviews it without being told who wrote it. A "full council" option has three AIs from three companies draft and critique each other first. A script checks that every number and name in the resume appears in your own words, and you approve each changed line.

**Good at:** independent review, a check on invented facts that runs as code instead of a request in a prompt, and privacy. Personal details are replaced with placeholders before anything goes to another AI. It is also plain about what no tool can promise.

**Watch out for:** it's slower and uses more AI time than the others. A quick review takes about 5 minutes, and a full council about 15 minutes with roughly five times the AI usage. It works best if you have accounts with two or three AI companies. It doesn't write cover letters or keep a library of your history between jobs. It's new, and so far it has one worked example and few users.

## Side by side

| | Independent reviewer from another AI company | Script checks claims against your own words | Asks you to approve changes | Cover letters | Reuses your history across jobs |
|---|---|---|---|---|---|
| ResumeSkills | No | No | Not built in | Yes, separate skill | No |
| Resume Tailoring Skill | No | No | Yes, at checkpoints | Suggestions only | Yes |
| resume-cover-letter | No | No | Not built in | Yes | No |
| Proficiently | No | No | Yes | Yes, separate skill | Yes, saved corrections |
| Claude Code Job Tailor | No | No | Yes, live preview | Yes | Yes, one data file |
| Resume Tribunal | Yes | Yes | Yes, every changed line | No | No |

## Which one should you use?

- **You want help with the whole job search**, cover letters and interview prep included: ResumeSkills, or resume-cover-letter if you also need UK or Australian conventions.
- **You're applying to lots of similar jobs and have plenty of old resumes:** Resume Tailoring Skill.
- **You live in Claude Code and want a fast, polished PDF:** Claude Code Job Tailor.
- **You're worried about an AI inventing things, or you want a second opinion you can trust:** Resume Tribunal. You can also use it to review a resume another skill wrote. Just say "get a second opinion on my resume".

## Whatever you use

- Read every line before you send it, and ask yourself whether you could explain it in an interview.
- Never keep a number you didn't give the AI yourself.
- Check whether the employer has a policy on AI help with applications.

No tool can promise you an interview. What you can control is whether every line is true, and whether you can talk about it.
