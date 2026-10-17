---
title: I let three AIs argue over my resume. Here's what they caught.
description: It started as sixteen prompts and three browser tabs. It became a free tool where a second AI, from a different company, checks the first one's work.
date: 2026-10-11
tags: Behind the scenes, AI review, Building in public
---

[[tldr]]

- An AI that writes your resume will also tell you it's great. It's biased, and the research agrees.
- So I made a second AI, from a different company, check the first one's work without knowing who wrote it.
- That became Resume Tribunal: free, works in ChatGPT, Gemini, Claude or any AI, and a quick review takes about 2 minutes of your time.

[[/tldr]]

## The AI that loved its own homework

Earlier this year I was job hunting and doing what everyone does: paste the resume, paste the job, ask the AI to make me shine.

It made me shine a little too brightly. It used words I never use, like "spearheaded", made claims a size bigger than what I'd done, and echoed the job post so neatly it felt like cheating on a test.

Then I asked the same AI to check its work. It said the draft was strong.

> Which is a bit like asking a chef to rate their own soup.

[[figure:self-grade|Same draft, two graders. Guess which one wrote it.]]

Researchers have measured this. In one 2026 study, AI judges could be [more than 50% more likely to pass a failed answer](https://arxiv.org/abs/2604.06996) when the answer was their own.

[[figure:self-preference|AI judges go easier on their own mistakes. Illustration of the reported effect.]]

## Sixteen prompts and a notes file

So I got a second opinion: a different company's AI, in a fresh chat, told to read the draft like a skeptical hiring manager.

It was far more willing to point out problems. So I kept going, all summer:

- **May 2026:** prompts to decode the job, screen my resume, and rewrite the weak bullets, run in three different AIs.
- **June and July 2026:** all three reviewed the merged result, and two of them researched the role itself.

The resume I ended up with was the best I'd had. It also took hours, three browser tabs, and a notes file just to remember which reply came from which AI.

[[figure:manual-vs-skill|Sixteen prompts by hand, or one message with Resume Tribunal.]]

Nobody else was going to spend hours on that, so I turned it into a skill.

## What Resume Tribunal does now

A skill is a set of instructions your AI app loads when it needs them. You paste one message into ChatGPT, Gemini, Claude or any AI, and it knows the whole routine. Try it: you do two steps, and the AIs do the rest.

[[how]]

Before anything goes to a second AI, your name and contact details are swapped for stand-ins. The facts you confirm can be saved on your computer, or handed to you as a block to paste, so your next job takes a few questions instead of a full interview.

[[cta]]

## The test that hurt

I asked AI reviewers to tear the project apart, each playing a different kind of expert. The one that hurt most was the simplest: someone whose whole AI experience is typing a question into ChatGPT.

They closed the tab in 30 seconds, because the first thing on my page was a terminal command. They were right, so I rebuilt the page around one message you paste into any AI chat.

## What the second AI caught

I then had a fresh AI run the whole thing on a made-up candidate. The other AIs suggested more than twenty things the candidate never said. A few:

- **"from 4 hours to 40 minutes"**, when the candidate said "half a day"
- **"framework adopted by leadership"**, for a spreadsheet one supervisor used
- **dropping "simple"** from "simple SQL queries", four separate times

[[figure:rejected-claims|One of more than twenty suggestions Resume Tribunal turned down.]]

All of them were turned down, because the candidate's own words decide. You can [check every line yourself](https://github.com/mohiddin7/resume-tribunal/tree/main/examples/operations-analyst/first-run).

## Three things I'd tell anyone using AI for a resume

1. **Get a second opinion from a different AI.** The one that wrote it is the worst judge of it.
2. **Never keep a number you didn't give it.** If you can't explain it in an interview, it can hurt you.
3. **Keep your own words.** Words like "spearheaded" are what readers notice first, and they don't sound like you.

[[figure:buzzwords|Resume Tribunal flags the words people spot first, and keeps yours.]]

Resume Tribunal is free and open source. [Try it in your AI app](../#start), and tell me what broke.
