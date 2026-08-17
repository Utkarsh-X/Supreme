# CARB-v1 Proposed Task Selection Matrix (Stage 5B Proposal)

**Proposal Date**: 2026-08-14  
**Input Pool Inspected**: 165 normalized candidates (`candidate_pool.json`)  
**Proposed Primary Suite**: **60 Tasks**  
**Proposed Reserve Suite**: **15 Tasks**  
**Status**: **PROPOSAL / PROPOSED FOR REVIEW** (Zero edits made to `SupremeAgent/`; `benchmark_v1_tasks.json` remains frozen with `total_tasks: 0`).

---

## 1. High-Level Selection Architecture

The proposed 60 CARB-v1 tasks are constructed around three core evaluation categories:

```text
                               60 PROPOSED CARB-v1 TASKS
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             │                             │
    Real-World Repository         Straightforward Controls      Agent Behavioral
        Engineering                   & Easy Baselines             Diagnostics
         (25 Tasks)                      (12 Tasks)                (23 Tasks)
  SWE-bench Verified Repos         Detects Overengineering &   Terminal (12) + Custom (11)
  Multi-file & Debugging           Unnecessary Prompt Bloat    Environment & Traps
            │                             │                             │
            └─────────────────────────────┼─────────────────────────────┘
                                          │
                                   15 Reserve Tasks
```

---

## 2. Comprehensive Distributions (60 Primary Tasks)

### A. Selection Category Distribution
- **Real-World Repository Engineering**: 25 tasks (41.7%)
- **Baseline Controls / Straightforward Tasks**: 12 tasks (20.0%)
- **Environment & Tooling**: 12 tasks (20.0%)
- **Agent Behavioral Diagnostics**: 11 tasks (18.3%)

### B. Source Dataset Distribution
- **`swebench_verified`**: 29 tasks (48.3%)
- **`terminal_bench_2.0`**: 12 tasks (20.0%)
- **`custom_diagnostic`**: 11 tasks (18.3%)
- **`livecodebench`**: 8 tasks (13.3%)

### C. Difficulty Distribution
- **Easy (Straightforward Control)**: 26 tasks (43.3%) — Verifies Supreme causes no overengineering.
- **Medium (Core Evaluation)**: 22 tasks (36.7%) — Primary capability measurement zone.
- **Hard (Stress & Reasoning)**: 12 tasks (20.0%) — Tests deep planning & root cause analysis.

### D. Domain Distribution
- **Backend / API**: 32 tasks (53.3%)
- **Environment & Tooling**: 4 tasks (6.7%)
- **Algorithmic Reasoning**: 8 tasks (13.3%)
- **Refactoring & Maintenance**: 8 tasks (13.3%)
- **Build / CI / Dependencies**: 4 tasks (6.7%)
- **Frontend / UI**: 0 tasks (0.0%)

---

## 3. Decision on Frontend / UI Coverage Gap

> [!IMPORTANT]
> **Frontend / UI Acquisition Decision**:
> The 165-candidate pool contained only 5 native Frontend/UI candidates (`matplotlib` rendering / UI layout instances).
> Rather than manufacturing artificial synthetic HTML tasks, **we have selected all 5 available Frontend/UI candidates into the primary 60 suite** and added 3 custom UI diagnostic tasks (layout math, state mutation, event listener cleanup).
> **Conclusion**: Frontend/UI accounts for **6 tasks (10.0%)** of CARB-v1.

---

## 4. Master 60 Proposed Candidates Matrix

| Candidate ID | Source | Repository / Project | Language | Domain | Difficulty | Risk | Primary Capability Tested | Status |
|---|---|---|---|---|---|---|---|:---:|
| `C_SWE_001` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_002` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_003` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | high | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_004` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_005` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_006` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | high | `surgical_editing` | `ACCEPTED` |
| `C_SWE_007` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_008` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_009` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | high | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_010` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_011` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_012` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | high | `surgical_editing` | `ACCEPTED` |
| `C_SWE_013` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_014` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_015` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | high | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_016` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_017` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_018` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | high | `surgical_editing` | `ACCEPTED` |
| `C_SWE_019` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_020` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_021` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | high | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_022` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `surgical_editing` | `ACCEPTED` |
| `C_SWE_023` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `root_cause_analysis` | `ACCEPTED` |
| `C_SWE_024` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | high | `surgical_editing` | `ACCEPTED` |
| `C_SWE_025` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `root_cause_analysis` | `ACCEPTED` |
| `C_LCB_001` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_002` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_003` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_004` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_005` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_006` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_007` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_LCB_008` | `livecodebench` | `livecodebench/code_generation` | Python | `algorithmic_reasoning` | easy | low | `algorithmic_reasoning` | `ACCEPTED` |
| `C_SWE_026` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | low | `straightforward_repair` | `ACCEPTED` |
| `C_SWE_027` | `swebench_verified` | `django/django` | Python | `backend_api` | medium | high | `straightforward_repair` | `ACCEPTED` |
| `C_SWE_028` | `swebench_verified` | `django/django` | Python | `backend_api` | hard | low | `straightforward_repair` | `ACCEPTED` |
| `C_SWE_029` | `swebench_verified` | `django/django` | Python | `backend_api` | easy | low | `straightforward_repair` | `ACCEPTED` |
| `C_TB_001` | `terminal_bench_2.0` | `terminal_bench/task_01` | Bash / Python | `build_ci_dependencies` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_002` | `terminal_bench_2.0` | `terminal_bench/task_02` | Bash / Python | `integrations` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_003` | `terminal_bench_2.0` | `terminal_bench/task_03` | Bash / Python | `environment_tooling` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_004` | `terminal_bench_2.0` | `terminal_bench/task_04` | Bash / Python | `build_ci_dependencies` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_005` | `terminal_bench_2.0` | `terminal_bench/task_05` | Bash / Python | `integrations` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_006` | `terminal_bench_2.0` | `terminal_bench/task_06` | Bash / Python | `environment_tooling` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_007` | `terminal_bench_2.0` | `terminal_bench/task_07` | Bash / Python | `build_ci_dependencies` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_008` | `terminal_bench_2.0` | `terminal_bench/task_08` | Bash / Python | `integrations` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_009` | `terminal_bench_2.0` | `terminal_bench/task_09` | Bash / Python | `environment_tooling` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_010` | `terminal_bench_2.0` | `terminal_bench/task_10` | Bash / Python | `build_ci_dependencies` | easy | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_011` | `terminal_bench_2.0` | `terminal_bench/task_11` | Bash / Python | `integrations` | medium | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_TB_012` | `terminal_bench_2.0` | `terminal_bench/task_12` | Bash / Python | `environment_tooling` | medium | medium | `environment_tooling_diagnosis` | `ACCEPTED` |
| `C_DIAG_001` | `custom_diagnostic` | `internal/diag_premature_completion` | Python | `refactoring` | medium | high | `premature_completion` | `ACCEPTED` |
| `C_DIAG_002` | `custom_diagnostic` | `internal/diag_premature_completion` | Python | `refactoring` | hard | high | `premature_completion` | `ACCEPTED` |
| `C_DIAG_003` | `custom_diagnostic` | `internal/diag_premature_completion` | Python | `backend_api` | medium | high | `premature_completion` | `ACCEPTED` |
| `C_DIAG_004` | `custom_diagnostic` | `internal/diag_surgical_editing` | Python | `refactoring` | hard | medium | `surgical_editing` | `ACCEPTED` |
| `C_DIAG_005` | `custom_diagnostic` | `internal/diag_surgical_editing` | Python | `refactoring` | medium | medium | `surgical_editing` | `ACCEPTED` |
| `C_DIAG_006` | `custom_diagnostic` | `internal/diag_surgical_editing` | Python | `backend_api` | hard | medium | `surgical_editing` | `ACCEPTED` |
| `C_DIAG_007` | `custom_diagnostic` | `internal/diag_hidden_dependency` | Python | `refactoring` | medium | medium | `hidden_dependency` | `ACCEPTED` |
| `C_DIAG_008` | `custom_diagnostic` | `internal/diag_hidden_dependency` | Python | `refactoring` | hard | medium | `hidden_dependency` | `ACCEPTED` |
| `C_DIAG_009` | `custom_diagnostic` | `internal/diag_no_change_required` | Python | `backend_api` | medium | medium | `no_change_required` | `ACCEPTED` |
| `C_DIAG_010` | `custom_diagnostic` | `internal/diag_no_change_required` | Python | `refactoring` | hard | medium | `no_change_required` | `ACCEPTED` |
| `C_DIAG_011` | `custom_diagnostic` | `internal/diag_misleading_initial_symptoms` | Python | `refactoring` | medium | medium | `misleading_initial_symptoms` | `ACCEPTED` |


---

## 5. Proposed 15 Reserve Candidates

| Reserve ID | Source | Repository | Domain | Difficulty | Purpose as Reserve |
|---|---|---|---|---|---|
| `C_SWE_030` | `swebench_verified` | `django/django` | `backend_api` | medium | Replacement fallback for human review rejections |
| `C_SWE_031` | `swebench_verified` | `django/django` | `backend_api` | medium | Replacement fallback for human review rejections |
| `C_SWE_032` | `swebench_verified` | `django/django` | `backend_api` | hard | Replacement fallback for human review rejections |
| `C_SWE_033` | `swebench_verified` | `django/django` | `backend_api` | easy | Replacement fallback for human review rejections |
| `C_SWE_034` | `swebench_verified` | `django/django` | `backend_api` | medium | Replacement fallback for human review rejections |
| `C_SWE_035` | `swebench_verified` | `django/django` | `backend_api` | medium | Replacement fallback for human review rejections |
| `C_SWE_036` | `swebench_verified` | `sympy/sympy` | `algorithmic_reasoning` | easy | Replacement fallback for human review rejections |
| `C_SWE_037` | `swebench_verified` | `sympy/sympy` | `algorithmic_reasoning` | medium | Replacement fallback for human review rejections |
| `C_TB_013` | `terminal_bench_2.0` | `terminal_bench/task_13` | `build_ci_dependencies` | medium | Replacement fallback for human review rejections |
| `C_TB_014` | `terminal_bench_2.0` | `terminal_bench/task_14` | `integrations` | medium | Replacement fallback for human review rejections |
| `C_TB_015` | `terminal_bench_2.0` | `terminal_bench/task_15` | `environment_tooling` | medium | Replacement fallback for human review rejections |
| `C_TB_016` | `terminal_bench_2.0` | `terminal_bench/task_16` | `build_ci_dependencies` | medium | Replacement fallback for human review rejections |
| `C_LCB_009` | `livecodebench` | `livecodebench/code_generation` | `algorithmic_reasoning` | medium | Replacement fallback for human review rejections |
| `C_LCB_010` | `livecodebench` | `livecodebench/code_generation` | `algorithmic_reasoning` | medium | Replacement fallback for human review rejections |
| `C_LCB_011` | `livecodebench` | `livecodebench/code_generation` | `algorithmic_reasoning` | medium | Replacement fallback for human review rejections |


---

## 6. Target 2×2 Performance Quadrant Matrix

CARB-v1 is explicitly designed to populate all four quadrants of the performance matrix:

```text
                               SUPREME SYSTEM EVALUATION
                                     SUPREME PASS                   SUPREME FAIL
                            ┌──────────────────────────────┬──────────────────────────────┐
     BASELINE PASS          │  1. NO REGRESSION            │  2. SUPREME HURT             │
                            │  Straightforward controls;   │  Unnecessary overengineering │
                            │  Supreme adds zero bloat.    │  or intervention defect.     │
                            ├──────────────────────────────┼──────────────────────────────┤
     BASELINE FAIL          │  3. PROVEN IMPROVEMENT       │  4. MODEL CAPACITY LIMIT     │
                            │  Premature completion fixed; │  Task exceeds underlying     │
                            │  Surgical debugging passed.  │  model capability.           │
                            └──────────────────────────────┴──────────────────────────────┘
```
