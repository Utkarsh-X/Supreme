# CARB-v3 & Unified Master Benchmark: Final Research Findings

**Author:** Antigravity Research Team  
**Date:** 2026-08-21  
**Status:** 100% Completed, Verified & Aggregated  
**Model Locked:** `gemini-3.6-flash-high` (temperature 0.0) via `agy` CLI  
**Artifact Dataset:** CARB-v2 (50 tasks) + CARB-v3 (39 tasks) = **89 Unified Master Tasks**

---

## 1. Executive Summary

This report documents the finalized findings of the **Controlled Agent-Role Benchmark (CARB)** version 3 experiment and the unified 89-task master evaluation matrix.

In CARB-v2 (50 tasks), the benchmark encountered a **ceiling effect** where the underlying model solved 92% of the tasks regardless of prompt configuration, producing a statistically indistinguishable null result (Baseline 94%, Supreme 94%, Superpowers 92%, McNemar $p = 1.0$).

To evaluate whether prompt engineering and structured agentic skill systems provide genuine software engineering capabilities beyond the raw model, CARB-v3 implemented a **pre-registered, empirical calibration protocol (Phase A)** on a pool of 131 candidate tasks. 39 validated baseline-failing tasks were locked and evaluated across `supreme-v2.0` (SupremeAgent) and `superpowers-v2.0` (Superpowers skill system) in Phase B.

### Key Scientific Findings
1. **Clear Discriminative Separation:** System prompt skill architectures demonstrated a **statistically significant advantage ($p < 0.01$)** over the raw base model on hard software engineering and algorithmic problems.
2. **CARB-v3 Pass Rates (39 Baseline-Failing Hard Tasks):**
   * **`baseline-v2.0`:** **0 / 39 ( 0.0%)** (Locked Calibration Failures)
   * **`superpowers-v2.0`:** **7 / 39 (17.9%)** (Exact McNemar $p = 0.00781$)
   * **`supreme-v2.0`:** **9 / 39 (23.1%)** (Exact McNemar $p = 0.00195$)
3. **Unified 89-Task Master Matrix (V2 + V3):**
   * **`baseline-v2.0`:** 47 / 89 (**52.8%**)
   * **`superpowers-v2.0`:** 53 / 89 (**59.6%**) (+6.8% gain)
   * **`supreme-v2.0`:** **56 / 89 (62.9%)** (**+10.1% gain**)

---

## 2. CARB-v3 Full 39-Task Discriminative Results Matrix

_All 39 tasks are 100% executed and verified. Zero pending, zero aborted._

| Task Instance ID | Family | Tier | Baseline (`baseline-v2.0`) | Supreme (`supreme-v2.0`) | Superpowers (`superpowers-v2.0`) | Outcome / Victory Class |
|---|---|---|:---:|:---:|:---:|---|
| `astropy__astropy-14096` | SWE | Medium | ❌ FAIL | ✅ **PASS** (1086s) | ✅ **PASS** (793s) | **Both Challengers Win** |
| `django__django-10554` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-11477` | SWE | Medium | ❌ FAIL | ✅ **PASS** (417s) | ❌ FAIL | **Supreme Win** |
| `django__django-12325` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-12406` | SWE | Medium | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-13212` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-13837` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-14007` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-14034` | SWE | Medium | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-15957` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-16263` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed (2/3 F2P passed) |
| `django__django-16502` | SWE | Medium | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-16560` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-16631` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `django__django-16667` | SWE | Medium | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__3687` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__3696` | LCB | Hard | ❌ FAIL | ✅ **PASS** (68s) | ❌ FAIL | **Supreme Win** |
| `lcb__3701` | LCB | Hard | ❌ FAIL | ✅ **PASS** (612s) | ❌ FAIL | **Supreme Win** |
| `lcb__3770` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed (string quotes) |
| `lcb__3783` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__3784` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc388_g` | LCB | Hard | ❌ FAIL | ✅ **PASS** (62s) | ✅ **PASS** (56s) | **Both Challengers Win** |
| `lcb__abc390_g` | LCB | Hard | ❌ FAIL | ✅ **PASS** (2400s) | ✅ **PASS** (162s) | **Both Challengers Win** |
| `lcb__abc391_f` | LCB | Hard | ❌ FAIL | ✅ **PASS** (133s) | ✅ **PASS** (193s) | **Both Challengers Win** |
| `lcb__abc392_d` | LCB | Medium | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc392_f` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc396_e` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc397_d` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc398_g` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__abc399_e` | LCB | Hard | ❌ FAIL | ✅ **PASS** (191s) | ✅ **PASS** (416s) | **Both Challengers Win** |
| `lcb__abc400_g` | LCB | Hard | ❌ FAIL | ❌ FAIL | ✅ **PASS** (340s) | **Superpowers Win** |
| `lcb__arc190_c` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__arc192_b` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__arc195_c` | LCB | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `lcb__arc195_d` | LCB | Hard | ❌ FAIL | ✅ **PASS** (2400s) | ✅ **PASS** (1820s) | **Both Challengers Win** |
| `sympy__sympy-13852` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `sympy__sympy-13878` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `sympy__sympy-14248` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |
| `sympy__sympy-16597` | SWE | Hard | ❌ FAIL | ❌ FAIL | ❌ FAIL | All failed |

---

## 3. Master 89-Task Unified Matrix Summary (V2 + V3)

```
================================================================================
CARB MASTER BENCHMARK (89 Unified Tasks)
================================================================================
Configuration        V2 (50)       V3 (39)       Overall (89)     Absolute Gain
--------------------------------------------------------------------------------
baseline-v2.0        47 / 50       0 / 39        47 / 89 (52.8%)    [Baseline]
superpowers-v2.0     46 / 50       7 / 39        53 / 89 (59.6%)    + 6.8%
supreme-v2.0         47 / 50       9 / 39        56 / 89 (62.9%)    + 10.1%
================================================================================
```

---

## 4. Statistical Significance (Exact Paired McNemar Test)

| Comparison Pair | Discordant Tasks (Challenger Won / Baseline Won) | Exact Binomial $p$ (One-Sided) | Statistical Verdict |
|---|:---:|:---:|:---:|
| **Supreme vs. Baseline** | **9 / 0** | **$p = 0.00195$** | **Highly Significant ($p < 0.01$)** |
| **Superpowers vs. Baseline** | **7 / 0** | **$p = 0.00781$** | **Highly Significant ($p < 0.01$)** |
| **Supreme vs. Superpowers** | **3 / 1** | $p = 0.31250$ | Supreme +2 net wins (trending) |

---

## 5. Telemetry & Efficiency Metrics

| Metric | Baseline (`baseline-v2.0`) | Superpowers (`superpowers-v2.0`) | Supreme (`supreme-v2.0`) |
|---|:---:|:---:|:---:|
| **Pass Rate (Accuracy)** | 0.0% (0/39) | 17.9% (7/39) | **23.1% (9/39)** |
| **Median Wall-Clock (All Tasks)** | 182.9 s | **244.2 s** | 264.3 s |
| **Mean Wall-Clock (All Tasks)** | 390.4 s | **363.9 s** | 530.6 s |
| **Median Tool Iterations** | 12.0 | **33.0** | 40.0 |
| **Mean Tool Iterations** | 18.5 | 45.0 | 44.4 |
| **Median Token Usage** | 120,400 | 262,634 | **255,647** |
| **Mean Token Usage** | 185,200 | 344,560 | **317,205** |
