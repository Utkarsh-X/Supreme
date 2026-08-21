# CARB-v3: Empirical Calibration Methodology & Pool Dynamics

---

## 1. The Pre-Registered Calibration Protocol (Phase A)

To eliminate the risk of task cherry-picking, CARB-v3 enforced a strict pre-registered selection rule:
1. **Candidate Pool Selection:** 131 candidate tasks drawn from SWE-bench Verified (Medium/Hard tiers) and LiveCodeBench (Hard/Contest tiers).
2. **Baseline Calibration Run:** `baseline-v2.0` was executed on all candidate tasks under standard runtime limits.
3. **Inclusion Boundary:** A task was admitted to the final CARB-v3 evaluation set **if and only if the baseline configuration failed it**.
4. **Challenger Blindness:** Challenger configurations (`supreme`, `superpowers`) were strictly never executed or evaluated during candidate selection.

---

## 2. Candidate Pool Outcome

- **Total Candidate Pool Graded:** 131 instances
- **Baseline Passed:** 92 instances (**70.2%**)
- **Baseline Failed (Locked Set):** **39 instances** (**29.8%**)
