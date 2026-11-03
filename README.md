# SurveyCoach

Reviews MMC (Member's Mark Community) surveys against the approved rubric, mobile first.
Design: `docs/superpowers/specs/`. Rubric: `docs/rubric/mmc-survey-rubric-v2.md`.
Build plan: `docs/superpowers/plans/2026-11-02-roadmap.md`.

## Status

Plan 1 (review engine) is done: a deterministic, offline review of a survey snapshot.
Not built yet: AI judge (Plan 2), backend (3), frontend (4), crawler reader (5).

## Try it

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev]" \
  --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple \
  --allow-insecure-host pypi.ci.artifacts.walmart.com

.venv/bin/python -m pytest -q
.venv/bin/python -m surveycoach review fixtures/boxer-briefs.json   # flawed sample: Needs work, one blocker
.venv/bin/python -m surveycoach review fixtures/coffee-pods.json    # clean sample
```

## How it works

`SurveySnapshot` (reader-independent) goes through pure checks registered by rubric ID
(`surveycoach/checks/`). Each check returns a score fraction plus plain-English findings.
`surveycoach/data/rubric-v2.yaml` is the only place points live; scoring is a weighted sum
over active criteria totaling exactly 100. A test keeps the YAML in sync with the approved
markdown rubric.

Honest by design: criteria that need the AI judge are reported as unchecked, the score is
flagged provisional, and a survey cannot be called Ready to launch while AI-judged blockers
(B1, B2, B6) are still pending.

Adding a check: write a function in `surveycoach/checks/<module>.py`, decorate it with
`@check("<rubric id>")`, and add tests. `tests/test_review.py` lists the checks not built yet.
