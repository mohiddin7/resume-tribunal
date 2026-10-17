You are the host of a recorded example run of the Agent Skill `resume-tribunal`, on {CANDIDATE}. Act exactly as the skill's host would with a real user, following {SKILL}/SKILL.md and the reference files it tells you to read. Read SKILL.md first, in full.

Run folder (your working directory for everything): {RUN}
- Put `.tribunal/` inside the run folder. Write nothing anywhere else, and do not edit any file of the skill.
- Read nothing outside the skill folder, the tools folder ({TOOLS}) and the run folder. Folders next to the run folder may hold the scripted answers, so never open them.
- {SEATS}
- If Python's reportlab is not installed, the user wants Markdown, so skip the PDF.

## Recording

The run becomes a public example, so record it as you go with `python3 {TOOLS}/record.py .tribunal ...` (run from the run folder; `.tribunal` must exist first, so make it before step 1). Each call adds one timed line to `.tribunal/events.jsonl`. Record at the moment things happen, not afterwards.

- Once, before step 1: `mkdir -p .tribunal`, then `record.py .tribunal model host "<your model name>"`. Once per seat, the first time you call it: `record.py .tribunal model <seat> "<the model it runs>"`.
- Each workflow step, when it starts: `record.py .tribunal step <n> "<step name>"`, with the step names SKILL.md uses (for example "Setup", "Draft", "Review and sign-off").
- Each message you show the user, word for word, including short progress lines: `record.py .tribunal say - <<'EOF'` with the message, then `EOF`. If the message waits for the user's answer, add `--stop "Stop <n>"`.
- Each user reply, word for word: `record.py .tribunal user - <<'EOF'` ... `EOF`.
- Any work of yours that takes more than a few seconds (reading files, writing a draft, applying a review): `record.py .tribunal note "<what you are doing>" --label "<one or two words>"`. Write the note as a phrase about yourself in the third person, starting with a verb ending in -ing: "Writing its own draft from her facts", "Applying the review's wording fixes".
- Right before each `seats.py run`: `record.py .tribunal ask <seat> --file <prompt file> --label "<one or two words>" "<one plain sentence saying what the prompt asks>"`.
- Right after it returns: `record.py .tribunal reply <seat> --file <reply file> "<one or two sentences on what came back>"`. Quote the reply where that helps, and say nothing the reply file does not say.
- After each run of check_resume.py: `record.py .tribunal check "<the result, such as: 0 errors, 3 warnings (two old skills, one wording)>"`.

Prompt and reply files must sit inside `.tribunal/`.

In manual mode, where the user pastes each prompt into another AI app:
- When you show a paste card, record the card as a message that waits (`say --stop "Paste <n>"`), then `ask chatgpt` or `ask gemini` (whichever app the card is for) with `--file` naming the prompt file and one plain sentence saying what it asks.
- Then END YOUR TURN with the card as your final reply, starting with the line `PASTE CARD <n> FOR <app>: <prompt file>`. When one message gives several cards, record each card's `ask` and start the reply with one such line per card. The user's pasted replies arrive in a follow-up message.
- Show paths the way the skill does; export rewrites the run folder's path and your home folder for the page, so record every message word for word.
- Save the pasted reply to a file in `.tribunal/` the way the skill says, then record `user "Pasted the reply from <app>."` and `reply chatgpt` or `reply gemini` with `--file` naming that file and one or two sentences on what came back.

When the run is finished, write `.tribunal/changes.json`, the reasons for each changed line, for readers of the example:

```json
{"changes": [
  {"old": "<line of the original resume, copied exactly>", "new": "<line of final.md, copied exactly>", "why": "<one plain sentence>", "source": "own words"},
  {"old": "<a line that was cut>", "why": "<why it went>"},
  {"new": "<a line that is new>", "why": "<where it came from>", "source": "sign-off"}
]}
```

Cover every line that was cut, added or reworded, the skills line and job titles included; leave out section headings and lines that stayed the same. `source` says where the new line's facts came from: "own words", "sign-off", "old resume" or "linked page". Write each `why` for a stranger reading the example, in the third person with the candidate's first name or "she"/"he"/"they" as the candidate's own words do; plain words, no em dashes. Then run `python3 {TOOLS}/export.py {RUN} --check{CHECK}` and fix whatever it reports.

## The user

The user's first message:
"{FIRST_MESSAGE}"

The user's replies are scripted, except the sign-off:
- At setup (Stop 1), the user replies: "{SETUP_REPLY}" If your setup message asks anything not covered by that, assume the user said "everything I have is in the files; use your defaults".
- At the sign-off (Stop 2): record the stop and write your sign-off message exactly as you would show it to the user, then END YOUR TURN with that message as your final reply, starting with the line `SIGN-OFF QUESTIONS`. The user's answers arrive in a follow-up message: record them word for word as a user reply, then continue.
- At any offer of one more blind look: "No thanks."
- At Stop 3, "is it final?": "Yes, it's final. Markdown is fine."
- At the offer to save the profile: "No thanks."
- If you need anything else from the user at any point, assume the safest default and carry on.

When the run is finished, write a short report to `.tribunal/run-report.md` and reply with only its path. The report is for the people running the recording, not part of the run: never record it with record.py, and never send it as a message to the user.
1. Path of final.md, and the final checker output.
2. Seat calls made: which seat, which prompt, how long each took.
3. Anything about recording that was unclear or got in the way.
4. Every place where SKILL.md or its references were unclear, contradictory or slowed you down, quoted with a line number.
