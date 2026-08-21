# CARB-v3: Data Integrity, Test Harness & Provenance Audit

---

## 1. Harness Bug Resolution: `test_command` Specification

During the Phase B audit, 12 private SWE evaluation specs were discovered with missing `test_command` entries (carrying only `test_command_hint`).
- **Impact:** `eval_swe.py` was not triggered automatically by `run_benchmark_v2.py`, marking real agent patches as test failures.
- **Remediation:** All 12 specs (`django-16263`, `django-13837`, `django-14007`, `django-14011`, `django-14631`, `django-15957`, `django-16560`, `django-16631`, `sympy-13852`, `sympy-13878`, `sympy-14248`, `sympy-16597`) were updated with explicit `test_command` and `test_timeout_seconds: 600`.
- **Verification:** All 12 tasks were verified and re-evaluated against the patched harness.

---

## 2. Infrastructure & OAuth Token Disruption Audit

- **Incident:** An account/subscription switch occurred on 2026-08-19 ~13:56, invalidating Google OAuth tokens and causing 28 sub-second aborts.
- **Remediation:** All invalid abort manifests were renamed to `.bak`, isolated into pending task queues, and re-executed cleanly in sequential batches with unbuffered logging.
- **Final State:** 100% of the 39 tasks have valid, complete runs with full telemetry and zero aborted states.
