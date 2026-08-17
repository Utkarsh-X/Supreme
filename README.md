# CARB v2 — Controlled Agent-Role Benchmark

A controlled, 50-task × 3-configuration benchmark measuring how **system-prompt
skill systems** affect an agent's ability to solve real software-engineering and
algorithmic tasks.

**Bottom line (corrected data, 2026-08-17):**

| Configuration | Passed / 50 | Rate |
|---|---|---|
| `baseline-v2.0`   | 47 | 94.0% |
| `supreme-v2.0`    | 47 | 94.0% |
| `superpowers-v2.0` | 46 | 92.0% |

The three configurations are statistically indistinguishable on this task set
(paired McNemar tests, all p ≥ 0.5 — see `carb_benchmark/results/FINDINGS_v2_corrected.md`
for the full analysis). The benchmark suffers a **ceiling effect**: 92–94% of
tasks are solved by all configurations, so it cannot discriminate agent skill.
The 4 failing tasks fail for every configuration that attempted them, and are
all validated as solvable on this platform — i.e., genuine agent failures on
hard tasks, not environment artifacts.

## Repo layout

```
BENCHMARK_SETUP.md                  # full setup/architecture notes (legacy doc)
carb_benchmark/
  configurations/                   # per-config YAML (baseline / supreme / superpowers)
  scripts/                          # harness: run, finalize, eval_swe, eval_lcb, validate
  task_registry/                    # task selection, audits, final 50-task list
  private/                          # per-task golden patches + evaluation specs
  sources/                          # candidate pools (data/ ignored: raw public corpora)
  evaluations/                      # per-session evaluator verdicts (JSON, audit trail)
  runs/                             # per-session manifests, transcripts, agent diffs
  results/                          # findings, 50×3 matrix, progress/summary JSONs
  methodology/ protocol/ design_reference/  # process docs
  snapshots/ public/                # sample diagnostic tasks (T001–T003)
SupremeAgent/                       # the "supreme" system (constitution, protocol, …)
SuperpowersObra/                    # the "superpowers" skill system
```

## Key facts about the experiment

- **Tasks:** 50 = 30 SWE-bench (`django` 12, `sympy` 6, `sphinx` 5, `matplotlib` 4,
  `pytest` 2, `scikit-learn` 1) + 20 LiveCodeBench (14 `abc*`, 6 `arc*`).
- **Model (locked):** `gemini-3.6-flash-high` via the Antigravity CLI (`agy`),
  temperature 0.
- **Configs** differ *only* in system prompt content, in an otherwise identical
  isolated environment (temp profile, auth only, no global rules/memory).
- **Grading:** hidden FAIL_TO_PASS tests via `eval_swe.py` / `eval_lcb.py` in
  era-appropriate venvs on Windows (no Docker). All 30 SWE tasks validated
  passable on this platform (`scripts/validate_swe_tasks.py`).
- **Sessions:** 2026-08-15 → 2026-08-17. Every cell of the matrix references its
  run id (`results/v2_corrected_matrix.json`).

## Integrity corrections (audit trail preserved in records)

1. **Eval-harness bug fixed** — `eval_swe.py`'s test-file filter matched the
   substring `"test"` inside `src/_pytest/*`, silently discarding every pytest
   source fix during grading. All 6 pytest sessions (5262 ×3, 7521 ×3) were
   re-evaluated against the saved agent diffs: **all 6 actually PASS**. Records
   carry `corrected_verdict` / `correction_note`.
2. **2 aborted sessions re-run** — `matplotlib-23299` baseline + superpowers
   (network/timeout, 0 agent work) were re-run for real; both are genuine FAILs
   (the aborted attempts are marked `invalid: true`).
3. **Alias merged** — 40 supreme sessions ran under legacy id `full-v2.0`
   (documented alias of `supreme-v2.0` in `run_benchmark_v2.py`); merged into
   the supreme column and disclosed in the findings.

## Reproduce

1. Rebuild the era-appropriate venvs (see `scripts/build_swe_workspaces.py`,
   `scripts/build_lcb_workspaces.py`) and the per-task workspaces.
2. Install the agent CLI into `carb_benchmark/tooling/` (not committed: binary,
   auth profiles, keyring).
3. `python carb_benchmark/scripts/run_benchmark_v2.py --task-registry
   carb_benchmark/task_registry/final_tasks_v2.json --config baseline-v2.0`
   (analogous for `supreme-v2.0` / `superpowers-v2.0`).
4. `python carb_benchmark/scripts/finalize_run.py <run_id>` then the
   per-configuration evaluator (`eval_swe.py` / `eval_lcb.py`).
