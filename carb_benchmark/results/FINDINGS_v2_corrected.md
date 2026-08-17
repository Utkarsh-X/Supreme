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

## 5. Notes / limitations

- The 6 original pytest FAILs and the 2 aborted `matplotlib-23299` runs were artifacts; corrected verdicts supersede them. Raw artifacts preserved for audit.
- Some run transcripts are short or show network errors at the end; verdicts come from the evaluator records (real diffs + hidden-test runs), not transcripts.
- 40 of 50 supreme sessions were executed under the legacy config id `full-v2.0` (identical prompt construction); merged and documented above.
