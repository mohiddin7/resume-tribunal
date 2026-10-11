---
title: How I built Resume Tribunal: three AIs, one resume, and no made-up numbers
description: It started as sixteen prompts I copied between three AI chats by hand. Here is how it became a free tool, what the research said, and what testing it taught me.
date: 2026-10-11
---

Earlier this year I was applying for jobs and doing what most people do now. I pasted my resume and a job posting into an AI and asked it to make me look good.

It did. A little too good.

The rewrites read well, but they didn't read like me. They used words I never use, like "spearheaded" and "leveraged". They echoed the job posting a bit too neatly. And now and then a claim came out bigger than what I had actually done.

When I asked the same AI to check its own draft, it liked it. Of course it did. It had written it.

So I started pasting the draft into a different company's AI, in a fresh chat with no history, and asking it to read like a skeptical hiring manager. It was far more willing to point out problems. That was the start of this project.

## The manual version

Over the next few months I wrote a set of prompts and ran them by hand. They are all still in the repository, unedited, in a folder called [manual-prompts](https://github.com/mohiddin7/resume-tribunal/tree/main/manual-prompts).

The first set, in May, covered the basics. Work out what the job actually wants. Screen my resume against it as a tough hiring manager. Rewrite the weakest bullets. Write the full resume. I ran those in three different assistants, audited each result in a fresh chat, and merged the best of the three.

In June and July I added a second round. All three assistants reviewed the merged resume and I reconciled what they said. Then I had two of them research the role itself: what hiring managers for this job look for, what reads as inflated, and what is changing in the field. That became a short handbook the final rewrite had to follow.

It worked. The resume I ended up with was the best I'd had, and I could explain every line of it in an interview.

It also took hours. Sixteen prompts, three browser tabs, and a lot of copy and paste. I kept a notes file just to remember which reply came from which AI, so I wouldn't favour one without meaning to.

Nobody else was going to do all that.

## Turning it into a skill

In October I turned the prompts into an Agent Skill. If you haven't come across these, a skill is a folder of instructions that an AI assistant loads when it needs them. You install it once. After that you say "tailor my resume to this job" and the assistant already knows the whole process.

Before writing anything, I went looking for evidence. Two findings shaped the design.

First, AI models really do go easy on their own work. In one study, AI judges were [up to 50% more likely](https://arxiv.org/abs/2604.06996) to pass a failed check when the output was their own. Another, on resume screening, found models [favoured summaries they had written](https://arxiv.org/abs/2509.00462) over the human originals. My hunch had a name: self-preference bias. A third study helped too. Across 37 models, a checker from a [different model family](https://arxiv.org/abs/2512.02304) did better than self-checking.

Second, and this one was humbling, nobody has shown that a group of AIs writes a better resume than one strong AI. The evidence for an outside reviewer comes from maths and logic tasks, so for writing it is an analogy. "Three AIs beat one" is a design choice. The README says so in plain words.

I built the skill itself with an AI coding agent, and I had other AIs review it. That felt right for a project about not trusting one AI.

## What I kept, and what I changed

The core idea stayed. The AI that writes a line never gets to be the one that approves it. A second AI, from a different company, reviews the draft without being told who wrote it. In the full version, three AIs each write a draft and then critique each other under shuffled labels like "Draft K" and "Draft M".

Almost everything around that changed.

**The important rules moved into code.** A prompt can say "don't invent numbers" and the AI can still do it. So there is a small checker script that compares every number and every name in the resume to what you actually wrote. If "Tableau" shows up and you never mentioned Tableau, the check fails.

**You sign off on every changed line.** Before you get a file, the assistant lists each claim that differs from your original resume. It asks whether each one is true and whether you could explain it in an interview. Anything you don't confirm comes out.

**Your details stay with you.** Your name, email, phone number and links are swapped for placeholders before anything goes to a second AI. The skill asks before it sends anything.

**The copy and paste is optional.** If you have other AI tools on your computer, the skill runs them itself, each one locked in an empty folder where it can't see your files. If you don't, it hands you one block of text to paste into another AI app, and you paste the reply back. A quick review is one round.

## How I tested it

I ran it on my own resume first, for a real job. It took under half an hour. A blind reviewer said no to a phone screen for the original and yes for the new version.

Then I asked AI reviewers to pull the project apart, each one playing a different kind of expert who writes and critiques these tools. The most useful reviewer was the simplest one: a person whose whole experience of AI is typing a question into ChatGPT, the way most of us did in 2023.

That reviewer closed the tab in about 30 seconds. The first thing on the page was a terminal command, and they had no idea what a terminal was.

That stung, and it was right. The page now starts with what the tool does in plain words, shows a before and after, and has a "never used a terminal?" route near the top.

Last, I had a fresh AI agent run the whole skill from its files alone, with a made-up candidate whose answers were scripted in advance. It finished in about 12 minutes, with eight calls to other AIs and no failures. It also wrote down 32 places where my instructions were vague or contradicted each other. I fixed them.

That run is published as the [worked example](https://github.com/mohiddin7/resume-tribunal/tree/main/examples/operations-analyst), with the candidate's own words included, so anyone can check every number with one command.

## What it caught

In that example, the other AIs suggested more than twenty things the candidate never said. A few of them:

- "from 4 hours to 40 minutes", when the candidate had said "half a day"
- "root-cause tracking framework adopted by leadership", for a spreadsheet one supervisor used in a weekly meeting
- dropping the word "simple" from "simple SQL queries", four separate times

All of them were rejected. The candidate's own words decide.

## What I learned

1. **AI is generous with itself.** If you use AI for anything that matters, get a second opinion from a different one.
2. **Rules that matter belong in code.** "Please don't make things up" is a wish. A script that fails on a made-up number is a rule.
3. **Write for the least technical reader.** If they can follow it, everyone can.

## Try it

Resume Tribunal is free and open source: [github.com/mohiddin7/resume-tribunal](https://github.com/mohiddin7/resume-tribunal). If you've never used a terminal, start with the "New to this?" section. If you try it, I'd like to hear what broke.
