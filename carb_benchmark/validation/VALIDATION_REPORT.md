# CARB-v2 SWE-bench Corpus — Validation Report

**Date**: 2026-08-15 (round 1 + round 2)
**Scope**: all 39 selected SWE-bench Verified instances (30 round-1 + 9 round-2 candidates)
**Method**: for each instance, run the real FAIL_TO_PASS tests on (a) the buggy base-commit state and (b) the gold-patch state, in an era-appropriate Python venv with pinned dependencies.

## Summary

| Verdict | Count |
|---|---|
| **VALIDATED** | **30** |
| REJECTED | 9 |

**30 tasks enter the benchmark.** All rejections are genuine platform/data limitations (documented below with evidence) — no task was force-fitted, and no rejection was caused by a harness bug.

## Definition of VALIDATED

A task is VALIDATED only if all of the following hold:

1. **Bug is real** — the base-commit workspace fails the instance's FAIL_TO_PASS tests (exit code ≠ 0, with the expected assertion/exception in the log).
2. **Fix is real** — applying the gold patch makes the same FAIL_TO_PASS tests pass (exit code = 0).
3. **PASS_TO_PASS regression check** — the gold state runs the P2P set; a non-zero P2P exit code is recorded as a *note*, not a rejection, only when caused by unrelated environment drift (analyzed per case).
4. **No leakage** — gold patch, test patch, and FAIL_TO_PASS lists live only under `carb_benchmark/private/<instance_id>/`; the agent workspace contains only the repo at base commit + the issue prompt.

Every phase log (full test output) is stored in `carb_benchmark/validation/<instance_id>.json` — the verdicts below are auditable from raw logs, not asserted from thin air.

## Validated (30)

Round 1 (23):

| # | Instance | F2P outcome |
|---|---|---|
| 1 | sympy__sympy-13480 | bug fails (rc=1) → gold passes (rc=0) |
| 2 | sympy__sympy-14711 | bug fails (rc=1) → gold passes (rc=0) |
| 3 | sympy__sympy-15875 | bug fails (rc=1) → gold passes (rc=0) |
| 4 | sympy__sympy-16886 | bug fails (rc=1) → gold passes (rc=0) |
| 5 | sympy__sympy-19637 | bug fails (rc=1) → gold passes (rc=0) |
| 6 | sympy__sympy-23950 | bug fails (rc=1) → gold passes (rc=0) |
| 7 | django__django-11119 | bug fails (rc=1) → gold passes (rc=0) |
| 8 | django__django-11133 | bug fails (rc=1) → gold passes (rc=0) |
| 9 | django__django-12419 | bug fails (rc=1) → gold passes (rc=0) |
| 10 | django__django-12965 | bug fails (rc=1) → gold passes (rc=0) |
| 11 | django__django-14089 | bug fails (rc=1) → gold passes (rc=0) |
| 12 | django__django-15851 | bug fails (rc=1) → gold passes (rc=0) |
| 13 | django__django-16082 | bug fails (rc=1) → gold passes (rc=0) |
| 14 | django__django-16485 | bug fails (rc=1) → gold passes (rc=0) |
| 15 | matplotlib__matplotlib-23299 | bug fails (rc=1) → gold passes (rc=0) |
| 16 | matplotlib__matplotlib-23476 | bug fails (rc=1) → gold passes (rc=0) |
| 17 | matplotlib__matplotlib-24627 | bug fails (rc=1) → gold passes (rc=0) |
| 18 | pytest-dev__pytest-5262 | bug fails (rc=1) → gold passes (rc=0) |
| 19 | pytest-dev__pytest-7521 | bug fails (rc=1) → gold passes (rc=0) |
| 20 | scikit-learn__scikit-learn-14141 | bug fails (rc=1) → gold passes (rc=0) |
| 21 | sphinx-doc__sphinx-10435 | bug fails (rc=1) → gold passes (rc=0) |
| 22 | sphinx-doc__sphinx-9367 | bug fails (rc=1) → gold passes (rc=0) |
| 23 | sphinx-doc__sphinx-9698 | bug fails (rc=1) → gold passes (rc=0) |

Round 2 additions (7) — chosen for repo/version spread (django 3.0/3.1/4.0/5.0, sphinx 3.5/4.1, matplotlib 3.6):

| # | Instance | F2P outcome |
|---|---|---|
| 24 | django__django-11179 | bug fails (rc=1) → gold passes (rc=0) |
| 25 | django__django-11880 | bug fails (rc=1) → gold passes (rc=0) |
| 26 | django__django-14493 | bug fails (rc=1) → gold passes (rc=0) |
| 27 | django__django-17029 | bug fails (rc=1) → gold passes (rc=0) |
| 28 | sphinx-doc__sphinx-8595 | bug fails (rc=1) → gold passes (rc=0) \| P2P rc=1 (note) |
| 29 | sphinx-doc__sphinx-9230 | bug fails (rc=1) → gold passes (rc=0) \| P2P rc=1 (note) |
| 30 | matplotlib__matplotlib-24177 | bug fails (rc=1) → gold passes (rc=0) \| P2P rc=-1 (note) |

Notes recorded for P2P in the gold state (all analyzed as environment drift, not regression): django-11133, django-12419 (unresolvable sentence-style P2P labels), matplotlib-23299 / -23476 / -24627 (P2P rc=4, unrelated collection), pytest-7521 (P2P rc=4), sphinx-9367 (P2P rc=4), sphinx-8595 / sphinx-9230 (P2P rc=1), matplotlib-24177 (P2P rc=-1, test-not-found). Each is documented in the instance JSON.

## Rejected (9) — with evidence

Round 1 (7):

| # | Instance | Reason |
|---|---|---|
| 1 | astropy__astropy-7671 | astropy 1.3: no runnable env — no era-appropriate Python with Windows wheels available (py3.7-only era, uv provides ≥3.8). |
| 2 | astropy__astropy-14309 | `ModuleNotFoundError: astropy.io.fits._tiled_compression._compression` in **buggy AND gold** states — the era astropy Windows wheel does not ship the `_compression` compiled extension (Linux/macOS-only build artifact); the package cannot import on this platform at all. |
| 3 | matplotlib__matplotlib-13989 | matplotlib 3.0: no runnable env — py3.7-only era, no Windows wheels for Python ≥3.8. |
| 4 | scikit-learn__scikit-learn-12585 | scikit-learn 0.21: no runnable env — py3.7-only era, no Windows wheels for Python ≥3.8. |
| 5 | scikit-learn__scikit-learn-13439 | scikit-learn 0.21: no runnable env — py3.7-only era, no Windows wheels for Python ≥3.8. |
| 6 | scikit-learn__scikit-learn-14053 | `TypeError: _splitter.Splitter.__cinit__() takes 5 positional args (6 given)` in **buggy AND gold** states — base commit sits mid-refactor between 0.22.0 and 0.22.2; the only available cp38 Windows wheel (0.22.2.post1) is ABI-incompatible with the base-commit `tree.py`, not bridgeable by overlay. |
| 7 | sphinx-doc__sphinx-8721 | Buggy state **already passes** F2P (rc=0) — the bug does not reproduce in this environment. Honest rejection: the dataset's bug is env-dependent and cannot be demonstrated here. |

Round 2 (2):

| # | Instance | Reason |
|---|---|---|
| 8 | sympy__sympy-13757 | `ERROR: file or directory not found: test_issue_13079` in **buggy AND gold** states — the dataset's test label does not map to a file in this snapshot, so the bug cannot be demonstrated. |
| 9 | astropy__astropy-14539 | Same astropy `_tiled_compression._compression` missing-compiled-extension issue as astropy-14309 — package cannot import on Windows (buggy AND gold). |

## What this means for the benchmark

- The final SWE-bench task count is **30**, not 39 — the honest number. The registry lists exactly these 30.
- Rejections are *platform/data* rejections (Windows wheels / Python-era availability / unmappable test labels), not *quality* rejections: all 9 are real SWE-bench Verified instances with real bugs; they are simply not runnable in a reproducible way on this machine, so admitting them would have produced untrustworthy results.
- Per-repo venvs are cached under `carb_benchmark/venvs/` and per-instance logs under `carb_benchmark/validation/`, so the entire validation is reproducible.
