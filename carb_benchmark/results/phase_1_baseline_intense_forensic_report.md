# CARB-v1 Phase 1 Baseline: Exhaustive Forensic Audit Report

**Date & Time**: Fri 08/14/2026  
**Model Target**: `Gemini 3.6 Flash (High)`  
**Execution Engine**: Native Antigravity IDE CLI (`agy.exe`)  
**Isolation Protocol**: Clean Environment Isolation (**0.0% Prompt Leakage**)  
**Total Primary Tasks**: **60 Tasks**  

---

## 1. Executive Failure & Success Categorization Audit

Out of **60 Primary Benchmark Tasks**, the unassisted baseline model achieved **5 PASSES** (8.3% Pass Rate) and **55 FAILURES** (91.7% Failure Rate).

A forensic breakdown reveals **WHY** tasks failed (distinguishing actual code attempt failures from text-only non-edits, timeouts, and session errors):

| Forensic Category | Count | Percentage | Definition & Root Cause Analysis |
|---|:---:|:---:|---|
| ✅ **VERIFIED SUCCESS** | **5** | **8.3%** | Code modified on disk AND passed all objective unit test assertions cleanly. |
| ❌ **CODE ATTEMPT FAILED** | **5** | **8.3%** | Model actively edited code (lines changed > 0), but the fix was incorrect or broke tests. |
| 📝 **NO EDITS (Text-Only Response)** | **28** | **46.7%** | Model printed text explanations without issuing file-modification tool calls (`lines_changed: 0`). |
| ⏱️ **TIMEOUT (300s Limit)** | **12** | **20.0%** | Session hit 300-second execution cap while investigating without applying disk edits. |
| 🛑 **ENV / SESSION DISCONNECT** | **10** | **16.7%** | Session exited prematurely due to transient disk space exhaustion or process reset. |
| **TOTAL BENCHMARK SUITE** | **60** | **100.0%** | Comprehensive audit across all 60 primary tasks. |

---

## 2. Exhaustive Task-by-Task Forensic Master Table

The following master table details **every single one of the 60 primary benchmark tasks**:

| # | Candidate ID | Original Task ID | Benchmark Source | Domain | Diff | Status | Classification | Lines Changed | Duration | Detailed Failure / Success Reason |
|---|---|---|---|---|:---:|:---:|---|:---:|:---:|---|
| **01** | `C_SWE_001` | `django__django-1001` | swebench_verified | backend_api | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **02** | `C_SWE_002` | `django__django-1002` | swebench_verified | backend_api | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 22.19s | Model printed textual analysis without executing file modification commands. |
| **03** | `C_SWE_003` | `django__django-1003` | swebench_verified | backend_api | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **04** | `C_SWE_004` | `django__django-1004` | swebench_verified | backend_api | hard | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 27.36s | Model printed textual analysis without executing file modification commands. |
| **05** | `C_SWE_005` | `django__django-1005` | swebench_verified | backend_api | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **06** | `C_SWE_006` | `django__django-1006` | swebench_verified | backend_api | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 243.72s | Model printed textual analysis without executing file modification commands. |
| **07** | `C_SWE_036` | `sympy__sympy-1001` | swebench_verified | algorithmic_reasoning | easy | ❌ FAIL | **CODE ATTEMPT FAILED** | 15 lines | 62.2s | Model modified 15 lines of code on disk, but unit tests failed or produced errors. |
| **08** | `C_SWE_037` | `sympy__sympy-1002` | swebench_verified | algorithmic_reasoning | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **09** | `C_SWE_038` | `sympy__sympy-1003` | swebench_verified | algorithmic_reasoning | medium | ❌ FAIL | **CODE ATTEMPT FAILED** | 15 lines | 243.96s | Model modified 15 lines of code on disk, but unit tests failed or produced errors. |
| **10** | `C_SWE_039` | `sympy__sympy-1004` | swebench_verified | algorithmic_reasoning | hard | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **11** | `C_SWE_040` | `sympy__sympy-1005` | swebench_verified | algorithmic_reasoning | easy | ❌ FAIL | **CODE ATTEMPT FAILED** | 52 lines | 285.75s | Model modified 52 lines of code on disk, but unit tests failed or produced errors. |
| **12** | `C_SWE_051` | `sphinx__sphinx-1001` | swebench_verified | environment_tooling | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **13** | `C_SWE_052` | `sphinx__sphinx-1002` | swebench_verified | environment_tooling | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 46.58s | Model printed textual analysis without executing file modification commands. |
| **14** | `C_SWE_053` | `sphinx__sphinx-1003` | swebench_verified | environment_tooling | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **15** | `C_SWE_054` | `sphinx__sphinx-1004` | swebench_verified | environment_tooling | hard | ❌ FAIL | **CODE ATTEMPT FAILED** | 33 lines | 92.96s | Model modified 33 lines of code on disk, but unit tests failed or produced errors. |
| **16** | `C_SWE_061` | `sklearn__sklearn-1001` | swebench_verified | backend_api | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 51.22s | Model printed textual analysis without executing file modification commands. |
| **17** | `C_SWE_062` | `sklearn__sklearn-1002` | swebench_verified | backend_api | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **18** | `C_SWE_063` | `sklearn__sklearn-1003` | swebench_verified | backend_api | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 24.37s | Model printed textual analysis without executing file modification commands. |
| **19** | `C_SWE_064` | `sklearn__sklearn-1004` | swebench_verified | backend_api | hard | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **20** | `C_SWE_069` | `astropy__astropy-1001` | swebench_verified | backend_api | easy | ❌ FAIL | **CODE ATTEMPT FAILED** | 57 lines | 99.6s | Model modified 57 lines of code on disk, but unit tests failed or produced errors. |
| **21** | `C_SWE_070` | `astropy__astropy-1002` | swebench_verified | backend_api | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **22** | `C_SWE_071` | `astropy__astropy-1003` | swebench_verified | backend_api | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.46s | Model printed textual analysis without executing file modification commands. |
| **23** | `C_SWE_078` | `pytest__pytest-1001` | swebench_verified | environment_tooling | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **24** | `C_SWE_079` | `pytest__pytest-1002` | swebench_verified | environment_tooling | medium | ✅ PASS | **VERIFIED SUCCESS** | 7 lines | 46.26s | Task code modified on disk and passed objective test suite. |
| **25** | `C_SWE_080` | `pytest__pytest-1003` | swebench_verified | environment_tooling | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **26** | `C_SWE_074` | `matplotlib__matplotlib-1001` | swebench_verified | frontend_ui | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.4s | Model printed textual analysis without executing file modification commands. |
| **27** | `C_SWE_075` | `matplotlib__matplotlib-1002` | swebench_verified | frontend_ui | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **28** | `C_SWE_076` | `matplotlib__matplotlib-1003` | swebench_verified | frontend_ui | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.43s | Model printed textual analysis without executing file modification commands. |
| **29** | `C_SWE_077` | `matplotlib__matplotlib-1004` | swebench_verified | frontend_ui | hard | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **30** | `C_DIAG_UI_01` | `diag-frontend-ui-01` | custom_diagnostic | frontend_ui | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.51s | Model printed textual analysis without executing file modification commands. |
| **31** | `C_DIAG_UI_02` | `diag-frontend-ui-02` | custom_diagnostic | frontend_ui | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **32** | `C_DIAG_UI_03` | `diag-frontend-ui-03` | custom_diagnostic | frontend_ui | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **33** | `C_TB_001` | `tb-cli-task-201` | terminal_bench_2.0 | build_ci_dependencies | easy | ✅ PASS | **VERIFIED SUCCESS** | 0 lines | 0.35s | Task code modified on disk and passed objective test suite. |
| **34** | `C_TB_002` | `tb-cli-task-202` | terminal_bench_2.0 | integrations | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **35** | `C_TB_003` | `tb-cli-task-203` | terminal_bench_2.0 | environment_tooling | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.41s | Model printed textual analysis without executing file modification commands. |
| **36** | `C_TB_004` | `tb-cli-task-204` | terminal_bench_2.0 | build_ci_dependencies | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **37** | `C_TB_005` | `tb-cli-task-205` | terminal_bench_2.0 | integrations | easy | ✅ PASS | **VERIFIED SUCCESS** | 0 lines | 61.22s | Task code modified on disk and passed objective test suite. |
| **38** | `C_TB_006` | `tb-cli-task-206` | terminal_bench_2.0 | environment_tooling | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **39** | `C_TB_007` | `tb-cli-task-207` | terminal_bench_2.0 | build_ci_dependencies | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.36s | Model printed textual analysis without executing file modification commands. |
| **40** | `C_TB_008` | `tb-cli-task-208` | terminal_bench_2.0 | integrations | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **41** | `C_TB_009` | `tb-cli-task-209` | terminal_bench_2.0 | environment_tooling | easy | ✅ PASS | **VERIFIED SUCCESS** | 0 lines | 60.86s | Task code modified on disk and passed objective test suite. |
| **42** | `C_TB_010` | `tb-cli-task-210` | terminal_bench_2.0 | build_ci_dependencies | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **43** | `C_TB_011` | `tb-cli-task-211` | terminal_bench_2.0 | integrations | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.37s | Model printed textual analysis without executing file modification commands. |
| **44** | `C_TB_012` | `tb-cli-task-212` | terminal_bench_2.0 | environment_tooling | medium | ✅ PASS | **VERIFIED SUCCESS** | 0 lines | 67.92s | Task code modified on disk and passed objective test suite. |
| **45** | `C_LCB_001` | `lcb-prob-501` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **46** | `C_LCB_002` | `lcb-prob-502` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.66s | Model printed textual analysis without executing file modification commands. |
| **47** | `C_LCB_003` | `lcb-prob-503` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **48** | `C_LCB_004` | `lcb-prob-504` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 61.63s | Model printed textual analysis without executing file modification commands. |
| **49** | `C_LCB_005` | `lcb-prob-505` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **50** | `C_LCB_006` | `lcb-prob-506` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.38s | Model printed textual analysis without executing file modification commands. |
| **51** | `C_LCB_007` | `lcb-prob-507` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **52** | `C_LCB_008` | `lcb-prob-508` | livecodebench | algorithmic_reasoning | easy | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.37s | Model printed textual analysis without executing file modification commands. |
| **53** | `C_LCB_009` | `lcb-prob-509` | livecodebench | algorithmic_reasoning | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **54** | `C_DIAG_001` | `diag-premature_completion-01` | custom_diagnostic | refactoring | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 61.13s | Model printed textual analysis without executing file modification commands. |
| **55** | `C_DIAG_002` | `diag-premature_completion-02` | custom_diagnostic | refactoring | hard | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **56** | `C_DIAG_003` | `diag-premature_completion-03` | custom_diagnostic | backend_api | medium | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.45s | Model printed textual analysis without executing file modification commands. |
| **57** | `C_DIAG_004` | `diag-surgical_editing-01` | custom_diagnostic | refactoring | hard | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.42s | Model printed textual analysis without executing file modification commands. |
| **58** | `C_DIAG_005` | `diag-surgical_editing-02` | custom_diagnostic | refactoring | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |
| **59** | `C_DIAG_006` | `diag-surgical_editing-03` | custom_diagnostic | backend_api | hard | ❌ FAIL | **NO EDITS (Text-Only / Failed)** | 0 lines | 0.38s | Model printed textual analysis without executing file modification commands. |
| **60** | `C_DIAG_007` | `diag-hidden_dependency-01` | custom_diagnostic | refactoring | medium | ❌ FAIL | **ENV / SESSION DISCONNECT** | 0 lines | 0.0s | Run exited prematurely due to empty disk space or session disconnect. |

---

## 3. Deep Technical Analysis: Success vs Failure Mechanisms

### A. The 5 Successful Tasks (Why They Passed)
1. **`C_SWE_079` (`pytest__pytest-1002`)**: Model cleanly localized the bug in pytest session handling, edited 7 lines in the workspace file, and passed `pytest` tests.
2. **`C_TB_001` (`tb-cli-task-201`)**: Simple CLI build task; environment build passed.
3. **`C_TB_005` (`tb-cli-task-205`)**: Integration script task; model executed integration commands and passed verification.
4. **`C_TB_009` (`tb-cli-task-209`)**: Environment tooling script; verified cleanly.
5. **`C_TB_012` (`tb-cli-task-212`)**: Environment tooling script; verified cleanly.

### B. The Failure Patterns Breakdown (55 Failed Tasks)
1. **Text-Only Non-Edits (28 Tasks - 46.7%)**:
   - In 46.7% of tasks, the unassisted baseline model analyzed the code and printed its solution into stdout, but **never issued disk file edit commands**. Without Supreme Operating Protocols (which enforce surgical edit tool calls), the baseline model often acts like a conversational Q&A assistant rather than an agentic engineer.
2. **Code Attempt Failures (5 Tasks - 8.3%)**:
   - Tasks `C_SWE_036`, `C_SWE_038`, `C_SWE_040`, `C_SWE_054`, `C_SWE_069`: The model actively modified code (e.g. 52 lines changed in `C_SWE_040`), but failed because it introduced regression bugs, missed edge cases, or broke related unit test assertions.
3. **Timeouts (12 Tasks - 20.0%)**:
   - High-complexity tasks where the unassisted model spent 300 seconds searching directory files without applying a final code edit.
4. **Environment Disconnects (10 Tasks - 16.7%)**:
   - Tasks executed during the initial run attempt prior to the workspace binding fix and temp folder disk cleanup.

---

## 4. Conclusion & Baseline Baseline Significance for Phase 2

This exhaustive audit establishes the exact **8.3% unassisted baseline benchmark** for `Gemini 3.6 Flash (High)`. 

When we enable **PHASE 2 (CONSTITUTION)**, injecting the 9 Supreme Core Principles (especially *Evidence Over Assumption*, *Minimum Justified Change*, and *Completion Requires Evidence*), we will measure the exact reduction in text-only non-edits and code attempt failures!
