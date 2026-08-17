# CARB Stage 4 — Candidate Dataset Acquisition Report

This document details the source acquisition, normalization, candidate breakdown, and suitability filtering for the **CARB Stage 4 Candidate Task Pool** (165 total normalized candidate items).

---

## 1. Candidate Source Summary

| Source Name | Version / Release | Original Candidate Count | Normalized Candidates Acquired | Purpose in CARB |
|---|---|---:|---:|---|
| **SWE-bench Verified** | `princeton-nlp/SWE-bench_Verified` | 500 | **80** | Real repository debugging, multi-file exploration, regression safety. |
| **Terminal-Bench 2.0** | `harbor-framework/terminal-bench@2.0` | 89 | **40** | Terminal environment, CLI tools, package setup, build script errors. |
| **LiveCodeBench** | `livecodebench/code_generation_lite` (v4) | 400+ | **25** | Algorithmic reasoning, self-repair, edge-case handling control group. |
| **Custom Diagnostics** | `v1.0` | 20 | **20** | Behavioral traps (premature completion, surgical edit boundaries, hidden dependencies). |
| **Total Candidate Pool** | | | **165** | |

---

## 2. Distributions & Capability Matrix

### A. Distribution by Domain (165 Total)
- **Backend / API**: 62 tasks (37.6%)
- **Environment & Tooling**: 38 tasks (23.0%)
- **Algorithmic Reasoning**: 33 tasks (20.0%)
- **Refactoring & Maintenance**: 18 tasks (10.9%)
- **Build / CI / Dependencies**: 9 tasks (5.5%)
- **Frontend / UI**: 5 tasks (3.0%)

### B. Distribution by Difficulty
- **Easy**: 46 tasks (27.9%) — Expected baseline success >80%
- **Medium**: 78 tasks (47.3%) — Expected baseline success 50–79%
- **Hard**: 41 tasks (24.8%) — Expected baseline success <50%

### C. Distribution by Primary Behavioral Property
- **`repository_understanding` & `investigation`**: 120 tasks
- **`surgical_editing` & `scope_control`**: 100 tasks
- **`regression_safety` & `verification`**: 145 tasks
- **`environment` & `dependency_management`**: 40 tasks
- **`premature_completion_trap`**: 20 tasks
- **`algorithmic_reasoning` (Control)**: 25 tasks

---

## 3. Suitability Filtering & Task Rejections

During candidate normalization, candidates were evaluated against six IDE environment suitability criteria:
1. **Clean Snapshot Execution**: Task can be executed from a self-contained clean repository directory.
2. **Objective Evaluation**: Task has automated unit tests, test scripts, or shell assertions.
3. **Sufficient Task Information**: Task prompt provides adequate instructions without exposing hidden answer keys.
4. **Evaluator Isolation**: Task allows strict separation of golden solution patches from workspace prompts.
5. **Deterministic Reset**: Workspace can be wiped and restored from golden snapshots.
6. **IDE / Gemini Environment Compatibility**: Task does not require proprietary external APIs, GUI desktop environments, or unsupported architecture binaries.

### Rejected Candidate Types (Excluded from Pool):
- **GUI-dependent tasks**: Tasks requiring live desktop display servers or manual mouse interactions (12 candidates rejected).
- **External Network Dependencies**: Tasks requiring live access to external cloud APIs or auth providers (18 candidates rejected).
- **Underspecified / Flaky Benchmark Instances**: Tasks identified in SWE-bench issue logs as having non-deterministic test suites (15 candidates rejected).

---

## 4. Master Candidate Registry Location

The full normalized candidate pool is archived at:
- [`carb_benchmark/task_registry/candidate_pool.json`](file:///e:/RofU/Supreme/carb_benchmark/task_registry/candidate_pool.json)

Individual source candidate files:
- [`carb_benchmark/sources/swebench_candidates.json`](file:///e:/RofU/Supreme/carb_benchmark/sources/swebench_candidates.json) (80 candidates)
- [`carb_benchmark/sources/terminalbench_candidates.json`](file:///e:/RofU/Supreme/carb_benchmark/sources/terminalbench_candidates.json) (40 candidates)
- [`carb_benchmark/sources/livecodebench_candidates.json`](file:///e:/RofU/Supreme/carb_benchmark/sources/livecodebench_candidates.json) (25 candidates)
- [`carb_benchmark/sources/custom_diagnostic_candidates.json`](file:///e:/RofU/Supreme/carb_benchmark/sources/custom_diagnostic_candidates.json) (20 candidates)

> [!IMPORTANT]
> **State Freeze Note**: [`carb_benchmark/task_registry/benchmark_v1_tasks.json`](file:///e:/RofU/Supreme/carb_benchmark/task_registry/benchmark_v1_tasks.json) remains **empty** (`total_tasks: 0`). The final 60 tasks will be selected in Stage 5 after human-in-the-loop review of the candidate pool.
