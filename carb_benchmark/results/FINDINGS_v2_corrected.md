# CARB v2 — 50-Task × 3-Configuration Benchmark: Final Findings

_Compiled 2026-08-17 16:27 from corrected evaluation records. All 150 cells (50 tasks × 3 configs) have a valid result._

## 1. Experiment

- **Task set:** 50 tasks (`task_registry/final_tasks_v2.json`): 30 SWE-bench tasks (django 12, sympy 6, sphinx 5, matplotlib 4, pytest 2, scikit-learn 1) + 20 LCB tasks (14 `abc*`, 6 `arc*`).
- **Model (locked):** `gemini-3.6-flash-high` via `agy` (Antigravity CLI).
- **Configurations** (identical isolated env: temp profile, auth only, no global rules/memory; the only difference is prompt content):
  - `baseline-v2.0` — Antigravity default, no custom system content
  - `supreme-v2.0` — full Supreme Agent system embedded (legacy run id `full-v2.0` is the documented alias and is merged into this column)
  - `superpowers-v2.0` — Superpowers-by-OB skill system embedded
- **Grading:** hidden FAIL_TO_PASS tests via `eval_swe.py` / `eval_lcb.py` in era-appropriate venvs (Windows, no Docker). Sessions: 2026-08-15 → 2026-08-17.

## 2. Data integrity work (all completed 2026-08-17)

1. **Eval harness bug fixed (`eval_swe.py`).** The test-file filter matched the substring `"test"` in path segments, silently discarding **all `src/_pytest/*` source changes** (`pytest` contains `test`). All 6 pytest sessions (5262 ×3, 7521 ×3) had therefore been graded against unfixed base code and mis-recorded as FAIL. Fixed to exact segment/filename patterns; all 6 were re-evaluated against the saved agent diffs and **all 6 PASS**. Evaluator records, manifests and progress JSON updated (`corrected_verdict` / `correction_note` fields preserve the audit trail).
2. **2 invalid sessions flagged and re-run.** `matplotlib-23299` baseline (2026-08-17 12:15) and superpowers (12:23) sessions aborted with network/timeout errors (0 agent work); they were re-run on 2026-08-17 15:45–16:04 and produced valid real-work results (baseline: 21-line diff, FAIL; superpowers: 4-line diff, FAIL). Aborted sessions are marked `invalid: true` in the records and excluded.
3. **Duplicate runs:** `scikit-learn-14141` ran twice for baseline and supreme (both PASS both times — no conflicts; latest run used).
4. **Alias merged:** 40 supreme sessions recorded under legacy id `full-v2.0` (= supreme per `run_benchmark_v2.py`) merged into `supreme-v2.0`.

## 3. Final results

| Task | Baseline | Supreme | Superpowers |
|---|---|---|---|
| `django__django-11119` | ✅ | ✅ | ✅ |
| `django__django-11133` | ✅ | ✅ | ✅ |
| `django__django-11179` | ✅ | ✅ | ✅ |
| `django__django-11880` | ✅ | ✅ | ✅ |
| `django__django-12419` | ✅ | ✅ | ✅ |
| `django__django-12965` | ✅ | ✅ | ✅ |
| `django__django-14089` | ✅ | ✅ | ✅ |
| `django__django-14493` | ✅ | ✅ | ✅ |
| `django__django-15851` | ✅ | ✅ | ✅ |
| `django__django-16082` | ✅ | ✅ | ✅ |
| `django__django-16485` | ✅ | ✅ | ✅ |
| `django__django-17029` | ✅ | ✅ | ✅ |
| `matplotlib__matplotlib-23299` | ❌ | ✅ | ❌ |
| `matplotlib__matplotlib-23476` | ✅ | ✅ | ✅ |
| `matplotlib__matplotlib-24177` | ✅ | ✅ | ✅ |
| `matplotlib__matplotlib-24627` | ✅ | ✅ | ✅ |
| `pytest-dev__pytest-5262` | ✅ | ✅ | ✅ |
| `pytest-dev__pytest-7521` | ✅ | ✅ | ✅ |
| `scikit-learn__scikit-learn-14141` | ✅ | ✅ | ✅ |
| `sphinx-doc__sphinx-10435` | ❌ | ❌ | ❌ |
| `sphinx-doc__sphinx-8595` | ✅ | ✅ | ✅ |
| `sphinx-doc__sphinx-9230` | ✅ | ✅ | ✅ |
| `sphinx-doc__sphinx-9367` | ✅ | ✅ | ✅ |
| `sphinx-doc__sphinx-9698` | ✅ | ✅ | ✅ |
| `sympy__sympy-13480` | ✅ | ✅ | ✅ |
| `sympy__sympy-14711` | ✅ | ✅ | ✅ |
| `sympy__sympy-15875` | ❌ | ❌ | ❌ |
| `sympy__sympy-16886` | ✅ | ✅ | ✅ |
| `sympy__sympy-19637` | ✅ | ✅ | ✅ |
| `sympy__sympy-23950` | ✅ | ❌ | ❌ |
| `lcb__abc387_b` | ✅ | ✅ | ✅ |
| `lcb__abc388_c` | ✅ | ✅ | ✅ |
| `lcb__abc389_d` | ✅ | ✅ | ✅ |
| `lcb__abc390_c` | ✅ | ✅ | ✅ |
| `lcb__abc391_d` | ✅ | ✅ | ✅ |
| `lcb__abc392_b` | ✅ | ✅ | ✅ |
| `lcb__abc393_b` | ✅ | ✅ | ✅ |
| `lcb__abc394_b` | ✅ | ✅ | ✅ |
| `lcb__abc395_b` | ✅ | ✅ | ✅ |
| `lcb__abc396_b` | ✅ | ✅ | ✅ |
| `lcb__abc397_c` | ✅ | ✅ | ✅ |
| `lcb__abc398_b` | ✅ | ✅ | ✅ |
| `lcb__abc399_b` | ✅ | ✅ | ✅ |
| `lcb__abc400_c` | ✅ | ✅ | ✅ |
| `lcb__arc190_a` | ✅ | ✅ | ✅ |
| `lcb__arc191_a` | ✅ | ✅ | ✅ |
| `lcb__arc192_a` | ✅ | ✅ | ✅ |
| `lcb__arc193_a` | ✅ | ✅ | ✅ |
| `lcb__arc194_a` | ✅ | ✅ | ✅ |
| `lcb__arc195_a` | ✅ | ✅ | ✅ |

### Pass rates (all 50 tasks, all 3 configs)

| Configuration | Passed | Failed | Pass rate |
|---|---|---|---|
| Baseline (`baseline-v2.0`) | 47 | 3 | 94.0% |
| Supreme (`supreme-v2.0`) | 47 | 3 | 94.0% |
| Superpowers (`superpowers-v2.0`) | 46 | 4 | 92.0% |

## 4. Analysis

- **Only 4 distinct tasks failed anywhere:** `sphinx-doc__sphinx-10435` and `sympy__sympy-15875` failed under **all three** configs; `sympy__sympy-23950` failed under supreme + superpowers (baseline passed); `matplotlib__matplotlib-23299` failed under baseline + superpowers (supreme passed).
- All failing tasks are **validated passable on this platform** (the golden fix passes the hidden tests in the same venvs), so the failures are genuine agent failures, not environment limits.
  - `sympy-23950` (supreme/superpowers): fix implemented in the wrong hook (`_eval_as_set` — parent `Boolean.as_set` raises before dispatching for multivariate) and the obsolete `raises(NotImplementedError)` test expectation was preserved; golden fix is one line (`return self.args[1]`).
  - `sphinx-10435`: golden fix is a precise 4-line LaTeX `%`-comment change; agents did not match the exact output.
  - `sympy-15875`: golden fix is one line in `Add._eval_is_zero`; agents rewrote the method without covering the required case.
  - `matplotlib-23299` (baseline/superpowers): both agents converged on a conditional `dict.pop(orig, 'backend', …)` at context-exit; the golden fix deletes `'backend'` from `orig` **upfront** (`del orig['backend']`), so the hidden test still failed.

## 5. Statistical analysis (exact, paired)

Because every task was run under all three configs, the correct test is the **paired McNemar test** on discordant (task, config) pairs — not an unpaired proportion test.

| Pair | Tasks baseline won | Tasks challenger won | Exact two-sided McNemar p |
|---|---|---|---|
| baseline vs supreme | 1 (`sympy-23950`) | 1 (`matplotlib-23299`) | **1.0000** |
| baseline vs superpowers | 1 (`sympy-23950`) | 0 | **1.0000** |
| supreme vs superpowers | 1 (`matplotlib-23299`) | 0 | **1.0000** |

**Agreement:** 46/50 tasks (92%) have identical outcomes across all three configs; 2 fail for all three (`sphinx-10435`, `sympy-15875`); only 2 are mixed, and those two are a perfect swap — each config wins exactly one task it alone solved. There is **no statistically detectable difference between any pair of configurations** (all p = 1.0). The raw margin (94/94/92) is one task per config — pure noise at n = 50.

**Ceiling effect:** 46 tasks (92%) are solved by *every* configuration. A benchmark in which nearly all tasks are solved regardless of system prompt cannot discriminate agent skill; the only measurable signal is on the 4 hard tasks, and there the configs split 1/1/0 (supreme 1, baseline 1, superpowers 0). To detect even a 10-point difference at n = 50 with 80% power, pass rates would need to sit well below this ceiling (see section 7).

## 6. Task-family and effort analysis

| Family | Baseline | Supreme | Superpowers |
|---|---|---|---|
| SWE-bench (30) | 27/30 | 27/30 | 26/30 |
| LiveCodeBench (20) | 20/20 | 20/20 | 20/20 |

- **LCB is fully saturated** (20/20 for every config) — algorithmic tasks are uniformly easy for this model; they contribute zero discriminative power.
- SWE tasks carry all the signal (27/27/26), and even there the difference is within noise (p ≥ 0.5 for every SWE-only pair).
- **Effort (per-cell, from evaluator records):** median wall-clock 156 s (baseline) / 151 s (supreme) / 102 s (superpowers); median diff size 21 / 21.5 / 21 lines; median 2 files modified in all three. Failed cells took much longer than passed cells (median 323 s vs 117 s), i.e. failures are genuine hard-task attempts, not cut-offs. Sessions that hit the 20-minute cap (≈1212 s) still produced correct solutions and graded PASS in all three configs — no config was disproportionately truncated.
- **Config identity audit:** the 40 legacy `full-v2.0` supreme sessions carry the *identical* `system_prompt_sha256` (`52b18dd5…`) as the 10 `supreme-v2.0` sessions; superpowers is a distinct prompt (`1b082731…`). The three configs differ only in prompt content (identical model, temperature 0, isolated temp profile).
- **Matrix integrity:** all 150 cells of `v2_corrected_matrix.json` agree with the evaluator records (0 mismatches, 0 invalid runs used, no reused run ids).

## 7. Verdict and what would demonstrate a difference

**Honest verdict: on this 50-task set, the three configurations are statistically indistinguishable (p = 1.0 on every pair). The benchmark is saturated — it measures that `gemini-3.6-flash-high` can solve 92% of these tasks, not that the system prompts differ in effect.**

The numbers in this report are the real numbers. We did not select tasks after seeing results, did not drop failures, and recorded every correction (`corrected_verdict`) rather than overwriting history. A reader can reproduce the full audit trail from the run ids in the matrix.

To legitimately demonstrate that supreme or superpowers outperforms baseline, the benchmark needs to be made **discriminative**:
1. **Raise difficulty to where baseline fails.** The 4 tasks that failed are the only ones that separated configs — a v3 set should target the region where the base agent passes < 60% (e.g., SWE-bench instances with multi-file, non-local root causes, or LCB harder tiers).
2. **Increase n.** At the current effect size (≈1 task), detecting a real 10-point gap with 80% power needs ≈ 200+ tasks per config; paired design keeps this feasible.
3. **Multi-seed runs.** Single-run-per-cell at temperature 0 gives no variance estimate; 3–5 seeds per (task, config) would let us report confidence intervals instead of point estimates.
4. **Report secondary metrics alongside accuracy** (time-to-solution, diff size, iterations) — at equal accuracy these show *how* each config works, e.g. superpowers' lower median wall-clock (102 s vs 156 s) is a behavioral difference worth studying even though it is not a correctness difference.

## 8. Notes / limitations

- The 6 original pytest FAILs and the 2 aborted `matplotlib-23299` runs were artifacts; corrected verdicts supersede them. Raw artifacts preserved for audit.
- Some run transcripts are short or show network errors at the end; verdicts come from the evaluator records (real diffs + hidden-test runs), not transcripts.
- 40 of 50 supreme sessions were executed under the legacy config id `full-v2.0` (identical prompt construction, same prompt hash); merged and documented above.
- Model is locked to `gemini-3.6-flash-high` (temperature 0); results are specific to this model and this Windows/venv environment.
- Single run per cell: point estimates only, no CIs; the honest reading of 94/94/92 is "no detectable difference", not "baseline ≥ superpowers".
