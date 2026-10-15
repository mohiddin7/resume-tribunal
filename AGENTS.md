# Working on this repository

This repository holds one Agent Skill, `resume-tribunal`, in `skills/resume-tribunal/`.

## Layout

- `skills/resume-tribunal/SKILL.md`: the skill's instructions. Keep it under 500 lines.
- `skills/resume-tribunal/references/`: prompts and seat handling, loaded on demand.
- `skills/resume-tribunal/scripts/`: Python scripts. `check_resume.py`, `prompt.py` and `seats.py` use the standard library only; `make_pdf.py` needs reportlab, and pypdf for its text check.
- `manual-prompts/`: the original hand-run prompts, kept unedited for the record.
- `examples/`: runs on fictional candidates. `operations-analyst/` is written up by hand; every other folder is a recorded run, exported by `examples/tools/` (see its README) and shown on the site by `docs/build.py`.
- `docs/`: the project website (GitHub Pages). `python3 docs/build.py` regenerates the drawings (from `docs/art.py`), the blog pages (from `docs/blog/*.md`), the homepage, the example run pages (from `examples/*/run.json`, played by `docs/assets/viewer.js`), `docs/resume-tribunal.md` (the skill and its references in one file, for any chat app), `feed.xml` and `sitemap.xml`; `python3 docs/build.py media` also renders the PNGs and blog GIFs. Edit the sources, not the generated HTML. `docs/llms.txt` is written by hand.

## Support

Users report problems to tribunal@warmhop.com or GitHub issues. When a run fails in a way the user cannot fix, point them there.

## Rules

- Prompts sent to other assistants never mention other assistants or how their inputs were made.
- The skill never invents facts for a resume. Do not weaken that rule.
- No em dashes in skill text, prompts or the README; the skill's own checker flags them.
- Examples are of fictional candidates only. `export.py` refuses a run whose contact details are not on example domains and 555-01xx numbers, or that shares lines with a resume in `research/real-resumes/`; never work around it.
- Keep the version in `SKILL.md`, `plugin.json` and `.claude-plugin/` in step.

## Checks before a change is done

```bash
python3 skills/resume-tribunal/scripts/check_resume.py --self-test
python3 skills/resume-tribunal/scripts/seats.py --self-test
python3 skills/resume-tribunal/scripts/prompt.py --self-test
python3 examples/tools/export.py --self-test
(cd examples/operations-analyst && python3 ../../skills/resume-tribunal/scripts/check_resume.py after.md --final --source before.md --source own-words.md --source signoff.md --vocab job.md)
python3 -m py_compile skills/resume-tribunal/scripts/*.py examples/tools/*.py
pip install skills-ref && agentskills validate skills/resume-tribunal
claude plugin validate --strict .
```
