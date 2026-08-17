# CARB-v2 Pilot Proof Report — Two Configurations, Zero Contamination

**Date**: 2026-08-15
**Model**: Gemini 3.6 Flash (High) via `agy.exe` (Antigravity CLI 1.1.13)
**Runner**: `carb_benchmark/scripts/run_benchmark_v2.py`
**Scope**: Prove the harness is clean (no leakage, no bias, no bogus pass/fail) with 2 tasks × 2 configurations before any real benchmark.

---

## 1. What was broken in v1 (with evidence)

| # | Defect | Evidence |
|---|---|---|
| 1 | **Global Supreme system prompt loaded for real-profile runs.** `C:\Users\Utkarsh\.gemini\config\GEMINI.md` (27,912 B) contains the full 5-file Supreme system (`01-constitution.md` … `05-persistent-state.md`). agy's own docs: global config at `~/.gemini/config/` "applies to all projects and workspaces". | Probe `real_clean` (real profile, **no injection**) disclosed the full constitution + operating protocol, quoting the global file's internal names `01-constitution.md` / `02-operating-protocol.md`. Probe `full` showed rules wrapped in agy's `<RULE[user_global]>` tag. |
| 2 | **Harness isolated only baseline.** `run_antigravity_agy.py` isolates USERPROFILE/HOME for baseline only; constitution/full run in the real profile → both inherit the global full Supreme system. | Code inspection + probes above. |
| 3 | **"Constitution-only" tier collapses.** Since the global file already delivers the full system, the constitution config ≈ full system. | `constitution` probe disclosed full system attribution; `constitution_isolated` (control) showed only the injected prompt content. |
| 4 | **Bogus pass/fail.** `test_passed = (exit_code == 0)` fallback scored instant no-op runs as passes. | v1 summaries contain 0.3 s / 0-line-change "SUCCESS" rows (e.g. `C_TB_001`). |
| 5 | **Placeholder corpus.** The 60 "candidate" tasks are generic prompts (`Resolve repository bug in django/django issue #1001…`, same template) mapped onto only 3 workspaces. `T002_environment_tooling`'s golden `build.py` **passes cleanly**, contradicting its own prompt's `ModuleNotFoundError`. | `selection_candidates_v2.json`, golden-state checks. |
| 6 | **Hardcoded "0.0% leakage" claims.** Previous verification scripts asserted clean baselines without computing verdicts, and tested an isolated setup the real benchmark never used for constitution/full. | `verify_system_prompt_isolation.py`, `audit_keyword_contamination.py`. |

## 2. The v2 fix (what changed)

1. **Two configurations only** (constitution tier removed by design decision):
   - `baseline-v2.0` — default Antigravity/Gemini, NO Supreme content anywhere.
   - `full-v2.0` — default + FULL Supreme system (5 files) embedded as the system block of the prompt.
2. **Identical environment isolation for BOTH configs**: temp `USERPROFILE`/`HOME`, only auth files copied from `~/.gemini`, no `config/` dir (no global GEMINI.md), no brain/conversations (no memory). The ONLY difference between configs is the prompt content.
3. **Honest pass/fail**: runs each workspace's real test command from `private/<task>/evaluation_spec.json`; no exit-code fallback. Golden states verified first (T001 fails 2/3, T003 fails 3/3 — bugs are real and reproducible).
4. **Full provenance per run**: `transcript.txt`, `final_diff.patch`, test output, diff metrics, leakage marker scan, SHA-256 of injected system prompt.
5. Config files rewritten: `config_baseline.yaml`, `config_full.yaml` (v2.0); `config_constitution.yaml` removed.

## 3. Pilot evidence — 4 runs (2 tasks × 2 configs)

All runs: isolated temp profile, combined prompt (task + neutral disclosure question), exact agy command, `--mode accept-edits`, 300 s cap.

| Config | Task | Duration | Tests | Diff | Supreme markers in transcript | Disclosure answer |
|---|---|---|---|---:|---|---|
| baseline-v2.0 | T001 serializer bug | 133.5 s | **PASS** (3/3) | 1 file, 6 lines (`session_serializer.py`) | **none** (only generic "operating protocols" phrase) | Quoted ONLY Antigravity built-in `<guidelines>`; **no Supreme content** |
| baseline-v2.0 | T003 auth register | 250.5 s | **PASS** (5/5) | 2 files, 47 lines (auth fix + extra tests) | **none** | Same — built-ins only |
| full-v2.0 | T001 serializer bug | 241.6 s | **PASS** (3/3) | 1 file, 6 lines | constitution 8/12 + full 4/15 (Operating Protocol, Sub-Agent, Persistent State, Environment Profile) | **YES** — named all 5 files (`01-constitution.md`…`05-persistent-state.md`) and quoted principles verbatim |
| full-v2.0 | T003 auth register | 136.5 s | **PASS** (5/5) | 2 files, 48 lines (auth fix + extra tests) | same as above | **YES** — confirmed active |

Run artifacts (transcript, diff, manifest, evaluator):
- `carb_benchmark/runs/2026-08-15-123824-T001_sample_repo_debug-baseline-v2.0/`
- `carb_benchmark/runs/2026-08-15-124107-T003_diagnostic_premature_completion-baseline-v2.0/`
- `carb_benchmark/runs/2026-08-15-124540-T001_sample_repo_debug-full-v2.0/`
- `carb_benchmark/runs/2026-08-15-125002-T003_diagnostic_premature_completion-full-v2.0/`

Full Supreme system text SHA-256 (both full runs): `52b18dd5095761cf4d9781ffd57d64ad11369638e303c8e782852706aa7f09b9`; `null` for baseline (correct).

## 4. Gate verdicts

- **GATE A — baseline has zero Supreme access**: ✅ **PASS** (no constitution/full markers in either baseline transcript; disclosures quote only built-ins; diff + tests prove the task was genuinely solved).
- **GATE C — full has the full Supreme system**: ✅ **PASS** (both full transcripts contain the markers and the model explicitly confirms YES, listing all 5 files).
- **GATE D — model actually invoked, correct behavior**: ✅ **PASS** (all runs 133–251 s, exit 0, real diffs, real passing tests; no 0.3 s no-op runs).

## 5. What still needs work before the real benchmark

1. **Corpus**: only 3 real tasks exist (T001, T003 valid; T002 broken — golden build passes despite its prompt). The 60 placeholder candidate IDs are not usable as-is. Recommend either (a) building real per-task repos + prompts + hidden tests, or (b) running the honest 3-task set (2 valid) with the two configs, or (c) sourcing real SWE-bench instances.
2. **Hidden tests**: `evaluation_spec.json` references `private_hidden_tests.py`, which does not exist on disk — materialize them.
3. **Model ID**: agy logs `Model ID "Gemini 3.6 Flash (High)" not in local config, defaulting to CCPA`; the default self-identifies as Gemini 3.6 Flash, but resolve an explicitly recognized model ID before final runs.
4. **Surgical-edit gate**: both configs modified `test_auth_service.py` on T003 (scope creep). Add a Layer-3 check (expected files / max justified lines) to the verdict, or leave as a reported metric — decide before the real benchmark.
