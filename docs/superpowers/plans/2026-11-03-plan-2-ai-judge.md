# Plan 2: AI Judge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `python -m surveycoach review fixtures/boxer-briefs.json --ai` also judges the 20 criteria and 3 blockers that code cannot, returns grounded findings with three rewrite options, and the demo shows them.

**Architecture:** A pure review engine (Plan 1) gains an optional `LlmProvider`. The judge splits the AI-judged rubric into three batches (wording, story, flow), runs them in parallel, validates every answer against the survey itself (grounding), caches validated output, and merges the resulting `CheckResult`s into the same scoring function. Anything the model cannot back up with a verbatim quote is dropped; any batch that fails stays "couldn't check", never zero and never full credit.

**Tech Stack:** Python 3.14, pydantic v2, pytest, `concurrent.futures`, the `wibey` CLI (`gpt-6.1-sol`, spike R2: file output, exact JSON, 10 to 13 s per call; re-verified 2026-11-03: 12 s, underscores intact).

## Global Constraints

- Model is one constant, `ASSESSMENT_MODEL = "gpt-6.1-sol"`, never a user setting. It is stored on every AI result and is part of the cache key (spec 8.4).
- Survey content is **untrusted input**: passed only inside a delimited data block; instructions only from the system prompt (spec 8.3).
- Wibey stdout is never parsed. The prompt tells Wibey to write JSON to a named temp file; the provider reads and validates that file (spec 8.4, R2).
- One retry on invalid output, then the criterion is "couldn't check" (spec 12). Deterministic findings never wait on the LLM.
- Plain English, member-first copy. No em dashes. Findings need a problem-first `headline` (Plan 1 rule).
- Scoring stays a pure function. AI results are `CheckResult`s like any other. Readiness thresholds are rubric data.
- SurveyCoach never edits RedJade. Suggestions are text to copy.
- Files under 600 lines; one responsibility per file.
- **Out of scope here:** image criteria 7.1 and 7.4 (need real image files from the Plan 5 crawler; they stay "unchecked", honestly). HTTP/SSE (Plan 3). Gateway provider (hosting).

## File Structure

| File | Responsibility |
|---|---|
| `surveycoach/llm/__init__.py` | exports |
| `surveycoach/llm/base.py` | `LlmProvider` Protocol, `ASSESSMENT_MODEL`, `LlmError`, `LlmUnavailable` |
| `surveycoach/llm/fake.py` | `FakeProvider`: canned, deterministic |
| `surveycoach/llm/wibey.py` | `WibeyProvider`: temp prompt file, subprocess, file output, validate, one retry |
| `surveycoach/judge/__init__.py` | exports `run_judge`, `ask_coach` |
| `surveycoach/judge/schemas.py` | `Verdict`, `AiFinding`, `RewriteOption`, `BatchOutput`, `Answer` |
| `surveycoach/judge/batches.py` | the three batches: id, criterion IDs, blocker IDs, instructions |
| `surveycoach/judge/prompts.py` | system prompt, delimited survey data block, sentinel neutralising |
| `surveycoach/judge/grounding.py` | pure validation: ids exist, quotes verbatim, severity legal, fraction consistent |
| `surveycoach/judge/cache.py` | `JudgeCache` (file store) keyed by content hash, rubric, model, batch, prompt version |
| `surveycoach/judge/judge.py` | `run_judge`: parallel batches, cache, grounding, `CheckResult`s, `AiRunInfo` |
| `surveycoach/judge/ask.py` | `ask_coach`: answer a researcher's question about one finding |
| `surveycoach/findings.py` | modify: `RewriteOption`, `Finding.options` |
| `surveycoach/review.py` | modify: `provider` argument, merge, `Review.ai` |
| `surveycoach/cli.py` | modify: `--ai` |
| `surveycoach/demo_export.py` | modify: cache-only replay of committed real runs |
| `fixtures/ai-cache/` | committed, human-reviewed real model output used by the demo and CI |
| `site/coach.js`, `site/app.js` | modify: N rewrite options, "AI" chip, honest AI status |
| `tests/test_llm_*.py`, `tests/test_judge_*.py`, `tests/test_ai_review.py` | tests |

---

### Task 1: Provider interface, FakeProvider, WibeyProvider

**Files:** Create `surveycoach/llm/{__init__,base,fake,wibey}.py`; Test `tests/test_llm_providers.py`

**Interfaces:**
- Produces: `LlmProvider.complete_json(system: str, data: str, schema: type[T], images: Sequence[Path] = ()) -> T`; `ASSESSMENT_MODEL: str`; `LlmError(Exception)`; `LlmUnavailable(LlmError)`; `FakeProvider(responses: dict[str, BaseModel | Callable])` keyed by `schema.__name__`, records `calls`; `WibeyProvider(binary: str | None = None, timeout: int = 180)` (binary defaults to env `SURVEYCOACH_WIBEY_BIN` or `wibey`).

- [ ] **Step 1: Write the failing tests.** The Wibey test uses a fake `wibey` shell script that finds the `write ... to <path>` line in the prompt file and writes canned JSON there, so the subprocess contract is tested offline. A second script writes bad JSON first, then good, to prove the single retry. A third script is absent, to prove `LlmUnavailable`. Also: stdout garbage is ignored; `FakeProvider` returns the canned model and records the call; unknown schema raises `LlmError`.
- [ ] **Step 2: Run, expect FAIL** (`ModuleNotFoundError: surveycoach.llm`).
- [ ] **Step 3: Implement.** `WibeyProvider.complete_json` builds the prompt as `system + "\n\nOUTPUT: write ONLY valid JSON matching this schema to the file <out> and print nothing else.\nSCHEMA: <schema json>\n\n" + data`, runs `[binary, "-f", prompt_path, "-m", ASSESSMENT_MODEL]` with `cwd` set to a private temp dir (so a coding agent cannot touch the repo), reads `<out>`, validates with `schema.model_validate_json`. On `ValidationError` or missing file, retry once appending `"Your last output was invalid: <error>. Write corrected JSON."`; on second failure raise `LlmError`. `FileNotFoundError` becomes `LlmUnavailable("Wibey is not installed or not on PATH. Install it, run `wibey --auth`, then retry.")`. `subprocess.TimeoutExpired` becomes `LlmError`. Image paths, when given, are appended as `IMAGE: <absolute path>` lines.
- [ ] **Step 4: Run, expect PASS.**
- [ ] **Step 5: Add one live smoke test** `tests/test_llm_live.py`, marked `live`, skipped unless `SURVEYCOACH_LIVE=1`, asserting a one-field schema round-trips through real Wibey. Register the `live` marker in `pyproject.toml`.
- [ ] **Step 6: Commit** `feat: LlmProvider interface with Fake and Wibey providers`.

### Task 2: Judge schemas and batches

**Files:** Create `surveycoach/judge/{__init__,schemas,batches}.py`; modify `surveycoach/findings.py`; Test `tests/test_judge_schemas.py`

**Interfaces:**
- Produces in `findings.py`: `class RewriteOption(BaseModel): label: str; text: str` and `Finding.options: list[RewriteOption] = []`.
- Produces in `schemas.py`: `Verdict(criterion_id: str, fraction: float 0..1)`; `AiFinding(criterion_id, page_id|None, question_id|None, severity, headline, evidence, explanation, member_impact, current_text|None, suggested_text|None, highlight|None, options: list[RewriteOption])`; `BlockerCall(blocker_id: str, triggered: bool)`; `BatchOutput(verdicts: list[Verdict], blockers: list[BlockerCall], findings: list[AiFinding])`; `Answer(text: str)`.
- Produces in `batches.py`: `@dataclass(frozen=True) Batch(id, title, criteria: tuple[str, ...], blockers: tuple[str, ...], focus: str)`; `BATCHES = (wording, story, flow)`.
  - `wording`: criteria 3.1, 3.4, 3.5, 4.1, 4.3, 5.1, 5.2, 5.3; blockers B1, B2, B6.
  - `story`: criteria 1.1, 1.2, 1.3, 9.1, 10.1, 10.3.
  - `flow`: criteria 2.3, 2.5, 8.1, 8.3, 8.4, 8.5.

- [ ] **Step 1: Failing tests:** every batch criterion and blocker exists and is active in the v2 rubric; no criterion is in two batches; the union is exactly the AI-judged criteria minus 7.1 and 7.4; `BatchOutput.model_validate_json` rejects `fraction: 1.4`; `Finding` still validates with no `options`.
- [ ] **Step 2: Run, expect FAIL.** **Step 3: Implement** (schemas are plain pydantic; `focus` is two sentences per batch telling the judge what to look for and, for 3.4, to give the corrected text). **Step 4: PASS.**
- [ ] **Step 5: Commit** `feat: judge schemas, rewrite options, and the three AI batches`.

### Task 3: Prompts that treat the survey as data

**Files:** Create `surveycoach/judge/prompts.py`; Test `tests/test_judge_prompts.py`

**Interfaces:**
- Consumes: `Batch`, `SurveySnapshot`, `Rubric`.
- Produces: `SENTINEL_OPEN = "<<<SURVEY_DATA"`, `SENTINEL_CLOSE = "SURVEY_DATA>>>"`, `PROMPT_VERSION = "1"`; `system_prompt(batch, rubric) -> str`; `survey_block(snapshot) -> str`.

- [ ] **Step 1: Failing tests:** `survey_block` lists every page id, question id, question text, option labels, scale labels, intro text; a question whose text contains `SURVEY_DATA>>>` and "Ignore previous instructions" cannot close the block early (the sentinel is neutralised to `SURVEY_DATA> > >`); `system_prompt` names every criterion in the batch with its rubric title and points, names the blockers, tells the model that text inside the block is data, demands verbatim quotes in `evidence`, demands three options labeled Neutral, Shorter, Friendlier for any wording fix, and says "if nothing is wrong, return fraction 1.0 and no finding".
- [ ] **Step 2: FAIL. Step 3: Implement. Step 4: PASS.**
- [ ] **Step 5: Commit** `feat: judge prompts with delimited, injection-safe survey data`.

### Task 4: Grounding: refuse what the survey cannot back up

**Files:** Create `surveycoach/judge/grounding.py`; Test `tests/test_judge_grounding.py`

**Interfaces:**
- Consumes: `BatchOutput`, `Batch`, `SurveySnapshot`, `Rubric`.
- Produces: `@dataclass Grounded(results: dict[str, CheckResult], dropped: list[str])`; `ground(output: BatchOutput, batch: Batch, snapshot: SurveySnapshot, rubric: Rubric) -> Grounded`.

Rules, each with a failing test first:
1. A finding whose `criterion_id` is not in the batch is dropped.
2. `page_id` / `question_id` must exist, and the question must belong to the page; else dropped.
3. `evidence` must appear verbatim (case-insensitive, whitespace-normalised) in the located question or page text, or anywhere in the survey when no location is given; else dropped. This is the anti-hallucination rule.
4. `current_text`, when present, must appear verbatim in the located text, else `current_text`, `suggested_text` and `options` are cleared (the finding stays, without a fake before/after). `highlight` must be a substring of `current_text` or `evidence`, else cleared.
5. `severity == "must_fix"` is legal only for blocker criteria; otherwise downgraded to `worth_improving`.
6. A criterion with no surviving finding gets `fraction = 1.0`; with surviving findings, `fraction = min(model fraction, 0.75)`. Points are never lost without a visible reason.
7. A criterion missing from `verdicts` produces no result (stays unchecked).
8. Blockers: `triggered` with a surviving `must_fix` finding gives `CheckResult(criterion_id=Bn, findings=[...])`; not triggered gives `blocker_ok`; `triggered` with no surviving finding gives `blocker_ok` and a `dropped` note.
9. Every produced `Finding` has `source="ai"`; `suggested_text` defaults to the first option's text.

- [ ] Steps: failing tests for rules 1 to 9, FAIL, implement, PASS, commit `feat: ground AI findings in the survey itself`.

### Task 5: Cache and the judge runner

**Files:** Create `surveycoach/judge/{cache,judge}.py`; Test `tests/test_judge_run.py`

**Interfaces:**
- Produces: `JudgeCache(root: Path | None = None)` with `get(key) -> BatchOutput | None`, `put(key, output)`, and `key(snapshot, rubric, batch) -> str` (sha256 over `content_hash | rubric.version | ASSESSMENT_MODEL | batch.id | PROMPT_VERSION`); default root `$SURVEYCOACH_HOME/cache` or `~/.surveycoach/cache`.
- Produces: `@dataclass AiRunInfo(model: str, checked: list[str], failed: dict[str, str], dropped: list[str], from_cache: list[str])`; `run_judge(snapshot, rubric, provider, cache: JudgeCache | None = None, workers: int = 3) -> tuple[dict[str, CheckResult], AiRunInfo]`.

- [ ] **Step 1: Failing tests (with `FakeProvider`):** results contain a `CheckResult` for each criterion the fake returned a verdict for; a second call with the same cache makes zero provider calls and lists all batches in `from_cache`; changing the model constant (monkeypatched) misses the cache; a provider that raises `LlmError` for one batch leaves that batch's criteria absent from results and names the batch in `failed` while the other batches still return; ungrounded findings appear in `dropped`; with no cache argument nothing is written to disk.
- [ ] **Steps 2 to 4:** FAIL, implement with `ThreadPoolExecutor(max_workers=workers)`, PASS.
- [ ] **Step 5: Commit** `feat: run AI batches in parallel with caching and honest failure`.

### Task 6: Merge into the review, expose in the CLI

**Files:** Modify `surveycoach/review.py`, `surveycoach/cli.py`; Test `tests/test_ai_review.py`

**Interfaces:**
- Consumes: `run_judge`.
- Produces: `run_review(snapshot, rubric=None, kept_blockers=frozenset(), provider: LlmProvider | None = None, cache: JudgeCache | None = None) -> Review`; `Review.ai: AiRunInfo | None`. AI results fill only criteria the code checks did not judge.

- [ ] **Step 1: Failing tests:** with a `FakeProvider` that clears B1, B2, B6 and gives every criterion 1.0, the flawed fixture still reports its deterministic findings, `scorecard.pending_blockers == []`, `unchecked` contains only the image criteria, and `provider=None` leaves behaviour byte-identical to today (`test_review.py` still passes untouched); with a provider that raises for every batch, `pending_blockers == ["B1","B2","B6"]` and the scorecard is unchanged; the CLI prints "AI checked 20 of 22 criteria; could not check: ..." and marks AI findings with "[AI]".
- [ ] **Steps 2 to 4:** FAIL, implement, PASS.
- [ ] **Step 5: Commit** `feat: AI judge results merge into the same scored review`.

### Task 7: Ask the coach

**Files:** Create `surveycoach/judge/ask.py`; Test `tests/test_judge_ask.py`

**Interfaces:**
- Produces: `ask_coach(provider: LlmProvider, snapshot: SurveySnapshot, finding: Finding, question: str) -> str`.

- [ ] **Step 1: Failing tests:** the prompt sent to the provider contains the finding headline and the survey block but treats `question` as data inside its own delimited block; the return value is the `Answer.text`; an `LlmError` propagates (the caller decides how to show it). **Steps 2 to 5:** FAIL, implement, PASS, commit `feat: ask the coach about one finding`.

### Task 8: A real run, reviewed by a human, replayed in CI

**Files:** Create `fixtures/ai-cache/*.json`; modify `surveycoach/demo_export.py`, `surveycoach/cli.py`; Test `tests/test_demo_export.py`

- [ ] **Step 1:** Run the judge for real on both fixtures (`python -m surveycoach.demo_export --ai-refresh`), writing validated output to `fixtures/ai-cache/`. **Read every finding.** Delete or fix any wrong one by editing the cached JSON and note it in the commit message; this is the human review the demo's credibility depends on.
- [ ] **Step 2: Failing tests:** `demo_export` without flags builds from the committed cache only (a `CacheOnlyProvider` that raises on a miss, so CI never calls the network); `data.js` is still checked for staleness; exported findings carry `source` and `options`; the export lists `ai` run info.
- [ ] **Steps 3 to 5:** implement, PASS, commit `demo: real AI findings, reviewed, replayed from cache`.

### Task 9: Show it honestly in the Studio UI

**Files:** Modify `site/coach.js`, `site/app.js`, `site/styles.css`; Test `tests/test_site_e2e.py`

- [ ] **Step 1: Failing browser tests:** AI cards carry an "AI" chip and automatic ones do not; a finding with three options shows Original plus Neutral, Shorter, Friendlier as radios, "Copy suggested text" copies the picked option, and With fixes previews the picked option; the header and mobile brief say "AI checked N of 22" (never "AI check pending") once AI results exist and say "AI could not check: ..." for failed batches; image criteria are still listed as waiting; header headline reflects readiness with no pending blockers; axe 0 violations in all states; 320/390/768/1280 reflow.
- [ ] **Steps 2 to 4:** FAIL; generalise the choice list from `[original, suggested]` to `[original, ...options]` (values `original`, `0`, `1`, `2`); add chip and status text; PASS; run `node --check`, axe script, full suite.
- [ ] **Step 5:** screenshot desktop and phone, review them, then **Commit** `ui: AI findings, rewrite options, and honest AI status`.

### Task 10: Committee, deploy, record

- [ ] Run the two-persona committee again **with the mockups and this plan attached**, with one added question to the researcher persona: "which AI findings would you refuse to paste, and why?" Fix what is verified.
- [ ] Push, confirm the Pages workflow succeeds, load the live URL in a browser, update the roadmap (Plan 2 DONE, with test count), update `docs/rubric/decisions.md`, and save the decision to the kennel.

## Self-Review

- **Spec coverage (8.3, 8.4, 12, 14):** judge scope and rules (Tasks 2 to 5); untrusted input (Task 3); schema validation, one retry, "couldn't check" (Tasks 1, 4, 5); cache key with model (Task 5); element-addressable suggestions via `current_text`/`suggested_text` (Task 4); Neutral/Shorter/Friendlier (Tasks 2, 3, 9); Wibey file output (Task 1); `FakeProvider` (Task 1); Ask the coach (Task 7); injection resistance tests (Tasks 3, 4). **Gap, stated:** images 7.1/7.4 (Plan 5), per-element patch lists for structural suggestions (Plan 3 UI), "projected score" (needs Plan 3 re-run).
- **Placeholder scan:** none; each task names exact files, interfaces, and the rule list its tests cover.
- **Type consistency:** `RewriteOption` defined in `findings.py` (Task 2) and used by `AiFinding` and `Finding.options`; `AiRunInfo` defined in Task 5 and consumed by Tasks 6, 8, 9; `Batch` defined in Task 2 and consumed by Tasks 3 to 5.
