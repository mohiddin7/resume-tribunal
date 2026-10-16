# Example run tools

How a run becomes a folder here and a page on the site, with nothing written by hand. The candidate is invented, or a real person who agreed to publish their de-identified resume.

1. **Make a run folder** with the inputs: `before.md` (the resume), `job.md` (the posting) and, if the candidate has one, `own-words.md` (what they say about their work). The candidate is either invented, or a real person who agreed to publish their resume, de-identified first: an invented name, an email on `example.com` and a 555-01xx phone number, project names rewritten from their descriptions, and every date shifted by the same amount so the timeline still adds up. Export the second kind with `--real-with-consent` instead of `--fictional`.
2. **Run the skill with a recording host.** Fill in [host-prompt.md](host-prompt.md) (the candidate, the run folder, the skill and tools folders, how the other AIs are reached, the user's first message and setup reply) and give it to an agent. In manual mode the host stops at each paste card; paste the prompt into the app it names (or the same company's model through its command-line tool) and send back the reply. As it works, the host calls [record.py](record.py) to log every step, message, seat call and check to `.tribunal/events.jsonl`, word for word and timed. At the sign-off it stops; answer its questions as the candidate would, from what is true for them. At the end it writes `.tribunal/changes.json`, a reason for each changed line, and checks the record with `export.py RUN --check`.
3. **Export it**:

   ```bash
   python3 examples/tools/export.py RUN growth-analyst-pricing-council \
     --title "Growth analyst applying for a senior pricing analyst job" --fictional --fact "Real public job posting"
   ```

   This writes `examples/<slug>/`: `run.json` for the site, a `transcript.md` and `README.md` for GitHub, the resumes and inputs, and every prompt and reply the other AIs saw in `files/`. It refuses a run that is not clearly fictional, and lists anything missing from the record. Add `--replace` to export over an earlier version of the same example, for example after a new release.
4. **Build the site**: `python3 docs/build.py` turns every `examples/*/run.json` into a page under `docs/examples/`, adds it to the examples index and the sitemap, and copies its files.

To rerun the examples after a release, rerun step 2 with the same inputs and answers, then steps 3 and 4 with `--replace`.

`export.py --self-test` checks the parsing, line matching, timeline and privacy checks. Both scripts use the standard library only.
