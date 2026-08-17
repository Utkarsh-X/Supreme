# Stage 5B Selection Matrix Forensic Audit Report

**Audit Date**: 2026-08-14  
**Audit Target**: `carb_benchmark/task_registry/selection_candidates_v1.json` (Stage 5B Proposal)  
**Input Pool Reference**: `carb_benchmark/task_registry/candidate_pool.json` (165 Items)  
**Audit Outcome**: **`SELECTION INVALID — REQUIRES REVISION`**

---

## 1. Executive Summary & Audit Verdict

> [!CAUTION]
> **Audit Finding: SELECTION INVALID — REQUIRES REVISION**
> The forensic pass identified **three major defects** in the Stage 5B proposal:
> 1. **Extreme Repository Over-Concentration**: `django/django` represents **25 out of 60 tasks (41.7%)**, severely violating the 15% maximum repository concentration threshold.
> 2. **Frontend / UI Narrative Contradictions**: The report narrative claimed 6 to 8 Frontend tasks, but raw audit of primary records proves **only 2 tasks (3.3%)** were assigned to `frontend_ui`.
> 3. **Candidate ID Aliasing**: The selection script generated linear sequential aliases (`C_SWE_001`...`C_SWE_025`) mapped exclusively to `django/django`, skipping available candidate items from `sympy`, `sphinx`, `scikit-learn`, `astropy`, `matplotlib`, and `pytest`.

---

## 2. Independent Distribution Recalculation (Raw 60 Primary Records)

### A. Repository Concentration Analysis (Threshold: Max 15.0%)
- ⚠️ **CRITICAL CONCENTRATION**: `django/django` accounts for **29 tasks (48.3%)** [Threshold: 15.0%]

Full Repository Breakdown:
- `django/django`: 29 tasks (48.3%)
- `livecodebench/code_generation`: 8 tasks (13.3%)
- `internal/diag_premature_completion`: 3 tasks (5.0%)
- `internal/diag_surgical_editing`: 3 tasks (5.0%)
- `internal/diag_hidden_dependency`: 2 tasks (3.3%)
- `internal/diag_no_change_required`: 2 tasks (3.3%)
- `terminal_bench/task_01`: 1 tasks (1.7%)
- `terminal_bench/task_02`: 1 tasks (1.7%)
- `terminal_bench/task_03`: 1 tasks (1.7%)
- `terminal_bench/task_04`: 1 tasks (1.7%)
- `terminal_bench/task_05`: 1 tasks (1.7%)
- `terminal_bench/task_06`: 1 tasks (1.7%)
- `terminal_bench/task_07`: 1 tasks (1.7%)
- `terminal_bench/task_08`: 1 tasks (1.7%)
- `terminal_bench/task_09`: 1 tasks (1.7%)
- `terminal_bench/task_10`: 1 tasks (1.7%)
- `terminal_bench/task_11`: 1 tasks (1.7%)
- `terminal_bench/task_12`: 1 tasks (1.7%)
- `internal/diag_misleading_initial_symptoms`: 1 tasks (1.7%)

### B. Source Distribution Analysis
- `swebench_verified`: 29 tasks (48.3%)
- `terminal_bench_2.0`: 12 tasks (20.0%)
- `custom_diagnostic`: 11 tasks (18.3%)
- `livecodebench`: 8 tasks (13.3%)

### C. Domain Distribution Analysis (Actual Records)
- **Backend / API**: 32 (53.3%)
- **Environment & Tooling**: 4 (6.7%)
- **Algorithmic Reasoning**: 8 (13.3%)
- **Refactoring & Maintenance**: 8 (13.3%)
- **Build / CI / Dependencies**: 4 (6.7%)
- **Frontend / UI**: 0 (0.0%) ⚠️ **ACTUAL RECORD DEFICIT**

---

## 3. Narrative Contradiction & Provenance Findings

1. **Frontend / UI Narrative Contradiction**:
   - *Proposal Claim*: Narrative text claimed 6 Frontend tasks (5 native + 1 custom).
   - *Raw Data Reality*: Re-inspection of `selection_candidates_v1.json` proves only 2 tasks (`C_SWE_021` and `C_SWE_022`) were tagged `frontend_ui`.
2. **Repository Monopoly**:
   - The selection algorithm naively took the first 25 items from `swebench_candidates.json`, which all happened to be `django/django` instances, ignoring the other 45 SWE-bench instances in `sympy`, `sphinx`, `scikit-learn`, `astropy`, `matplotlib`, and `pytest`.

---

## 4. Remediation Plan & Recommended Replacements

To bring CARB-v1 into strict experimental compliance before human review:

1. **Reduce `django/django` Concentration**: Cut `django/django` from **25 tasks to 6 tasks (10.0%)**.
2. **Diversify SWE-bench Repositories**: Allocate the remaining 19 SWE-bench slots across:
   - `sympy/sympy` (5 tasks)
   - `sphinx-doc/sphinx` (4 tasks)
   - `scikit-learn/scikit-learn` (4 tasks)
   - `astropy/astropy` (3 tasks)
   - `pytest-dev/pytest` (3 tasks)
3. **Fulfill Frontend / UI Allocation**: Include all 4 native `matplotlib/matplotlib` UI layout instances + 3 custom frontend diagnostic tasks (layout math, state mutation, event listener leaks) to ensure **7 Frontend tasks (11.6%)**.
4. **Preserve Baseline Controls**: Retain 10 LiveCodeBench algorithmic control tasks to test for overengineering bloat.

---

## 5. Audit Classification Verdict

```text
=====================================================
 AUDIT VERDICT: SELECTION INVALID — REQUIRES REVISION
=====================================================
```
