# CARB-v2 — System-Prompt Effectiveness Benchmark: Final Report

> **Status: DRAFT — results pending driver completion (aggregate with `scripts/aggregate_results.py`)**

**Policy note (2026-08-15, mid-run)**: the initial agy turn budget was 300s. During the
first runs it was discovered that agy buffers its entire text output until the end of a
turn, so a 300s kill produced empty transcripts and truncated work (one spurious
FAILURE on django-12965-baseline that a re-run overturned). The budget was raised to
**600s** (`run_benchmark_v2.py` `RUN_TIMEOUT_SECONDS`) and the affected runs
(django-11880 ×2, django-12419-full, django-12965-baseline, django-14493-full) were
re-run under the new budget. All runs in the final table used the same 600s budget.

## 1. What this benchmark measures

Whether injecting a custom engineering system prompt (the "Supreme" agent system
or the "Superpowers by OB" skill system) into the Antigravity (agy) coding agent
changes its ability to solve real software engineering tasks, compared to the same
agent with no custom system prompt.

- **Model (locked)**: `gemini-3.6-flash-high` via agy (Antigravity) — the ONLY
  entry point; no external APIs, no GenAI SDK.
- **Three configurations** (identical in every way except the injected prompt):
  - `baseline-v2.0`: no custom system text; isolated temp profile (no
    `~/.gemini/config/GEMINI.md`, no memory, no global rules).
  - `supreme-v2.0`: the complete 5-file Supreme system (constitution +
    operating protocol + sub-agent profiles + environment profile + persistent state)
    prepended to the task prompt. *(Renamed from `full-v2.0` on 2026-08-17.)*
  - `superpowers-v2.0`: the Superpowers by OB skill system (all 14 SKILL.md
    definitions + the agy platform reference) prepended to the task prompt.
    Introduced 2026-08-17 as the third CARB-v2 arm.
- **Corpus**: 50 real tasks — 30 SWE-bench Verified instances + 20 LiveCodeBench v5
  (AtCoder/ARC, Jan–Apr 2025) problems. Every task passed a validation gate
  (bug fails / fix passes on the real hidden tests; reference solutions pass 40/40
  private tests; discriminators reject wrong solutions).

## 2. Corpus integrity (how you know the tasks are real)

- SWE: `validation/VALIDATION_REPORT.md` — 30 VALIDATED / 9 REJECTED, with raw
  phase logs per instance. All 9 rejections are platform/data limitations
  (Windows wheels unavailable for py3.7-era repos, astropy missing compiled
  extension, unmappable test label), never harness bugs.
- LCB: every reference solution passes all 40 private tests; wrong solutions fail
  (no vacuous tests). Grading = official LiveCodeBench comparison semantics.
  `lcb__arc190_a` uses a real checker (valid + minimal) because the problem
  accepts any optimal assignment; the dataset's own stored outputs are not
  minimal-verified, so exact matching would be unfair.
- Terminal-Bench 2.0 was NOT integrated — proven impossible without breaking
  integrity (Linux agy cannot authenticate; silently downgrades the locked model).
  Documented in `sources/data/CORPUS_STATUS.md`.

## 3. Harness integrity (how you know the comparison is fair)

- **System-prompt isolation (leakage probes)**: `protocol/leakage_probe_v2.md`.
  - Baseline probe: model reports ONLY agy's built-in `<guidelines>` (verified by
    capturing the built-in prompt verbatim from an empty-profile control session);
    zero Supreme markers; no Supreme vocabulary in the transcript.
  - Full probe: model quotes the Supreme constitution verbatim
    (8+ constitution markers).
  - Both probes SOLVED the task (proving the disclosure question didn't distort behavior).
- **Identical environments**: all three configs run in the same isolated temp
  profile; the only difference is the injected prompt text.
- **2026-08-17 corrections**: 7 tasks whose evaluation specs had
  `test_command: null` (false `PASS` verdicts with no real test) were re-wired to
  the real `eval_swe.py` hidden-test harness and re-run on baseline & supreme;
  `pytest-5262` supreme (previously crashed on the 32k Windows command-line limit)
  was re-run under the `-p @file` prompt path. Invalid runs are quarantined in
  `runs/_invalid_quarantine_no_test_cmd/`.
- **Model lock**: `--model gemini-3.6-flash-high` in every run; manifest bug where
  the identifier was mis-recorded was fixed (`start_run.py`) and patched retroactively.
- **Eval**: hidden tests never touch the workspace; agent edits to test files are
  ignored in SWE grading (hidden tests come from the clean patch, so test-weakening
  cannot inflate scores).

## 4. Results

<!-- filled by scripts/aggregate_results.py once the driver completes -->

## 5. Discussion

<!-- filled after results -->

## 6. Reproducibility

- Registry: `task_registry/final_tasks_v2.json` (50 tasks).
- Run artifacts: `carb_benchmark/runs/<ts>-<task>-<config>-v2.0/` — transcript,
  diff, manifest, evaluator output.
- Validation logs: `carb_benchmark/validation/*.json`.
- Corpus sources: `carb_benchmark/sources/data/`.
- Driver: `scripts/run_carb_v2_batch.py` (resumable; skips finalized runs).
  `scripts/run_full_benchmark.py` / `scripts/run_retry_batch.py` are superseded.
