# Working on this repository

This repository holds one Agent Skill, `resume-tribunal`, in `skills/resume-tribunal/`.

## Layout

- `skills/resume-tribunal/SKILL.md`: the skill's instructions. Keep it under 500 lines.
- `skills/resume-tribunal/references/`: prompts and seat handling, loaded on demand.
- `skills/resume-tribunal/scripts/`: Python scripts. `check_resume.py`, `prompt.py` and `seats.py` use the standard library only; `make_pdf.py` needs reportlab, and pypdf for its text check.
- `manual-prompts/`: the original hand-run prompts, kept unedited for the record.
- `examples/`: a full run on a fictional candidate.
- `docs/`: the project website (GitHub Pages). `python3 docs/build.py` regenerates the images, the blog pages from `docs/blog/*.md`, the homepage, `feed.xml` and `sitemap.xml`; edit the sources, not the generated HTML. `docs/llms.txt` is written by hand.

## Rules

- Prompts sent to other assistants never mention other assistants or how their inputs were made.
- The skill never invents facts for a resume. Do not weaken that rule.
- No em dashes in skill text, prompts or the README; the skill's own checker flags them.
- Keep the version in `SKILL.md`, `plugin.json` and `.claude-plugin/` in step.

## Checks before a change is done

```bash
python3 skills/resume-tribunal/scripts/check_resume.py --self-test
python3 skills/resume-tribunal/scripts/seats.py --self-test
python3 skills/resume-tribunal/scripts/prompt.py --self-test
(cd examples/operations-analyst && python3 ../../skills/resume-tribunal/scripts/check_resume.py after.md --final --source before.md --source own-words.md --source signoff.md --vocab job.md)
python3 -m py_compile skills/resume-tribunal/scripts/*.py
pip install skills-ref && agentskills validate skills/resume-tribunal
claude plugin validate --strict .
```
