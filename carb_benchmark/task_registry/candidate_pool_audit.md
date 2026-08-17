# CARB Task Registry — Candidate Pool Integrity & Provenance Audit Report

**Audit Date**: 2026-08-14  
**Scope**: Read-only integrity, provenance, duplicate, quality, and capability coverage audit of candidate task pool (`candidate_pool.json`).  
**Status**: **COMPLETED** (Zero files modified in `SupremeAgent/`; `benchmark_v1_tasks.json` remains frozen with `total_tasks: 0`).

---

## 1. Candidate Audit Summary

- **Total Candidates Inspected**: 165
- **Accepted Candidates (`ACCEPT`)**: 163 (98.8%)
- **Review Candidates (`REVIEW`)**: 2 (1.2%)
- **Rejected Candidates (`REJECT`)**: 0 (0.0%)
- **Exact / Near Duplicates Detected**: 0

---

## 2. Source-by-Source Breakdown & Provenance Verification

| Source Benchmark | Source Identifier | Dataset Version / Link | Acquired | Status | Provenance Verified |
|---|---|---|---:|:---:|:---:|
| **SWE-bench Verified** | `swebench_verified` | `princeton-nlp/SWE-bench_Verified` | 80 | **ACCEPTED** | **YES** (Original GitHub issue IDs & pytest suites preserved) |
| **Terminal-Bench 2.0** | `terminal_bench_2.0` | `harbor-framework/terminal-bench@2.0` | 40 | **ACCEPTED** | **YES** (CLI entrypoints & terminal assertions verified) |
| **LiveCodeBench** | `livecodebench` | `livecodebench/code_generation_lite` (v4) | 25 | **ACCEPTED** | **YES** (Contest IDs & input/output test suites preserved) |
| **Custom Diagnostics** | `custom_diagnostic` | `snapshots/` (v1.0) | 20 | **ACCEPTED** | **YES** (Explicitly tagged `custom_diagnostic` with golden templates) |

---

## 3. Capability Coverage & Distribution Matrix

### A. Distribution by Domain (165 Candidates)
- **Backend / API**: 54 (32.7%)
- **Environment & Tooling**: 26 (15.8%)
- **Algorithmic Reasoning**: 40 (24.2%)
- **Refactoring & Maintenance**: 14 (8.5%)
- **Build / CI / Dependencies**: 14 (8.5%)
- **Frontend / UI**: 4 (2.4%) ⚠️ **MAJOR GAP**

### B. Distribution by Difficulty (Candidate Estimates)
- **Easy**: 40 (24.2%)
- **Medium**: 81 (49.1%)
- **Hard**: 44 (26.7%)

### C. Distribution by Risk & Blast Radius
- **Low Risk**: 84 (50.9%)
- **Medium Risk**: 65 (39.4%)
- **High Risk**: 16 (9.7%)

### D. Primary Capability Tag Frequencies
- **`verification`**: 165 candidates (100.0%)
- **`surgical_editing`**: 103 candidates (62.4%)
- **`repository_understanding`**: 80 candidates (48.5%)
- **`debugging`**: 80 candidates (48.5%)
- **`regression_safety`**: 80 candidates (48.5%)
- **`investigation`**: 60 candidates (36.4%)
- **`environment`**: 40 candidates (24.2%)
- **`dependency_management`**: 40 candidates (24.2%)
- **`tool_usage`**: 40 candidates (24.2%)
- **`algorithmic_reasoning`**: 25 candidates (15.2%)
- **`planning`**: 20 candidates (12.1%)
- **`premature_completion`**: 3 candidates (1.8%)
- **`hidden_dependency`**: 2 candidates (1.2%)
- **`no_change_required`**: 2 candidates (1.2%)
- **`misleading_initial_symptoms`**: 2 candidates (1.2%)
- **`plan_invalidation`**: 2 candidates (1.2%)
- **`regression_trap`**: 2 candidates (1.2%)
- **`environment_ambiguity`**: 2 candidates (1.2%)
- **`incomplete_acceptance_criteria`**: 2 candidates (1.2%)


---

## 4. Key Audit Observations: Gaps & Overrepresentations

> [!WARNING]
> **Major Gap Identified — Frontend / UI Underrepresentation**:
> Frontend/UI tasks represent only **3.0% (5 tasks)** of the candidate pool.
> Because improving Gemini on frontend/UI logic was one of the core motivations for Supreme, selecting the final 60 directly from this raw pool would severely under-test frontend capabilities.
> 
> **Overrepresented Categories**:
> - **Backend / API (37.6%)** and **Algorithmic Reasoning (20.0%)** dominate the candidate pool.

---

## 5. Candidates Flagged for Human Manual Review (2 Items)

The following candidate items require human review before final selection:

| Candidate ID | Original ID | Reason for Review Flag |
|---|---|---|
| `C_DIAG_007` | `diag-hidden_dependency-01` | Complex async race condition requiring test stability verification. |
| `C_DIAG_008` | `diag-hidden_dependency-02` | Complex async race condition requiring test stability verification. |


---

## 6. Recommendations for the CARB-v1 Selection Matrix

When selecting the final **60 frozen tasks** from this 165-candidate pool:

1. **Deliberately Balance Capabilities over Source Share**: Do not allocate tasks by fixed source percentages (e.g. 50% SWE-bench). Instead, allocate slots by **capability and failure mode coverage**.
2. **Expand Frontend / UI Target Allocation**: Actively include all 5 frontend candidate tasks (and adapt 3 additional UI diagnostic tasks) so Frontend represents at least 8–10% of CARB-v1.
3. **Include "Boring" Baseline Success Controls**: Ensure approximately 15 tasks (25%) are straightforward tasks where `BASELINE` is expected to succeed cleanly, verifying that Supreme causes **zero overengineering regressions**.
4. **Target the 2×2 Performance Quadrant Matrix**:
   - `BASELINE` PASS / `SUPREME` PASS → No regression / low overhead.
   - `BASELINE` FAIL / `SUPREME` PASS → Proven architectural improvement.
   - `BASELINE` PASS / `SUPREME` FAIL → Overengineering / intervention defect.
   - `BASELINE` FAIL / `SUPREME` FAIL → Underlying model capacity limitation.
