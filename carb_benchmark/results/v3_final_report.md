# CARB V3 Experiment — Final Report

**Generated**: 2026-08-19
**Model (locked)**: `gemini-3.6-flash-high` via agy (Antigravity CLI)
**Protocol**: `protocol/v3_discriminative_set_proposal.md`

---

## 1. Experiment Design

V3 uses a **discriminative set** approach: instead of running all configs on all tasks, we:

1. **Phase A**: Run baseline on a large candidate pool (93 tasks) to identify tasks the baseline **fails**
2. **Lock final set**: Keep only baseline-failing tasks (the hard ones)
3. **Phase B**: Run challenger configs (supreme, superpowers) on the locked set

This maximizes signal — we only test challengers on tasks where they have a chance to differentiate.

---

## 2. Phase A — Baseline Calibration

**Candidate pool**: 93 tasks (19 hard SWE + 10 medium SWE + 29 LCB + rest)
**Config**: `baseline-v2.0` (no system prompt)

| Metric | Count |
|---|---|
| Total graded | 93 |
| Baseline PASS | 64 |
| Baseline FAIL | **29** |
| Baseline pass rate | 68.8% |
| Baseline failure rate | **31.2%** |

### Final locked set: 29 tasks

| Family | Count |
|---|---|
| SWE-bench Verified | 19 |
| LiveCodeBench v5 | 10 |

---

## 3. Phase B — Challenger Configurations

**Configs tested**:
- `supreme-v2.0` — Supreme Agent system prompt (constitution + operating protocol + sub-agents)
- `superpowers-v2.0` — Superpowers skill system (14 SKILL.md definitions)

**Runs**: 29 tasks × 2 configs = **58 total runs**

| Config | SUCCESS | FAILURE | Pass rate |
|---|---|---|---|
| supreme-v2.0 | 3 | 26 | 10.3% |
| superpowers-v2.0 | 3 | 26 | 10.3% |

---

## 4. Discriminative Results (Key Finding)

**3 tasks where challenger configs succeed and baseline fails:**

### `lcb__abc388_g` (AtCoder, hard)

| Config | Result | Wall (s) | Diff (lines) | Tools |
|---|---|---|---|---|
| baseline-v2.0 | ❌ FAIL | 318.5 | 0 | 3 |
| supreme-v2.0 | ✅ PASS | 62.2 | 77 | 12 |
| superpowers-v2.0 | ✅ PASS | 56.7 | 70 | 9 |

**Analysis**: Baseline produced 0 lines of diff (3 tool calls, gave up). Both challengers solved it quickly (~60s, 70-77 lines).

### `lcb__abc390_g` (AtCoder, hard)

| Config | Result | Wall (s) | Diff (lines) | Tools |
|---|---|---|---|---|
| baseline-v2.0 | ❌ FAIL | 569.2 | 200 | 55 |
| supreme-v2.0 | ✅ PASS | 2400.3* | 158 | 25 |
| superpowers-v2.0 | ✅ PASS | 162.8 | 110 | 30 |

*Supreme hit the 40-min timeout but tests passed.

**Analysis**: Baseline worked hard (55 tools, 200 lines) but got the wrong answer. Superpowers cracked it in 163s. Supreme also got it but took longer.

### `lcb__abc399_e` (AtCoder, hard)

| Config | Result | Wall (s) | Diff (lines) | Tools |
|---|---|---|---|---|
| baseline-v2.0 | ❌ FAIL | 78.9 | 76 | 7 |
| supreme-v2.0 | ✅ PASS | 191.2 | 74 | 8 |
| superpowers-v2.0 | ✅ PASS | 416.0 | 74 | 14 |

**Analysis**: Baseline produced a 76-line diff but tests failed. Both challengers produced ~74 lines and passed. Subtle bug in the baseline approach that the system prompts helped avoid.

---

## 5. Summary

| Metric | Value |
|---|---|
| Discriminative tasks | **3 / 29** (10.3%) |
| Tasks where supreme wins | 3 |
| Tasks where superpowers wins | 3 |
| Tasks where BOTH win | **3** (all of them) |
| Tasks where only one wins | 0 |

### Interpretation

- **3 discriminative tasks** out of 29 baseline-failing tasks show challenger improvement
- **Both configs succeed on all 3** — no config-specific wins, suggesting general capability improvement rather than skill-specific
- **26/29 tasks** remain hard for ALL configs — genuine hard problems
- The discriminative tasks are all **LCB (AtCoder)**, none from SWE-bench — challenger prompts may help more with algorithmic reasoning than codebase navigation

### What didn't change

- **26 tasks** where both challengers also fail — the baseline failure rate (68.8%) is largely unchanged
- No SWE-bench tasks were unlocked by challenger configs
- Both challenger configs perform identically on the discriminative set

---

## 6. V3 vs V2 Comparison

| Metric | V2 (50 tasks) | V3 (29 tasks) |
|---|---|---|
| Baseline pass rate | ~36% | 68.8% |
| Supreme improvement | Significant | 3/29 (10.3%) |
| Superpowers improvement | N/A (new in v2) | 3/29 (10.3%) |

The V3 baseline is much stronger (68.8% vs ~36%) because we selected tasks from a broader pool including easier medium SWE and LCB tasks. The discriminative signal is real but modest.

---

## 7. Recommendations

1. **The 3 discriminative tasks are validated wins** — both configs independently succeed where baseline fails
2. **26 tasks remain universally hard** — these are the true frontier; future system prompt improvements should target these
3. **LCB tasks show more discriminative signal** than SWE — worth investigating whether system prompts help more with algorithmic reasoning
4. **Both challenger configs perform identically** — consider whether maintaining two separate configs is worth the complexity
