# CARB-v2 Pass-1 Failure Investigation (2026-08-15/16)

This document records *why* every non-SUCCESS run in the first full 100-run pass
(50 tasks x 2 configs, gemini-3.6-flash-high, locked) failed. It is the audit
trail for the retry batch and feeds the final report.

## Driver summary (first pass)

```
total: 100 | passed: 74 | failed: 26 | skipped: 14
```

The 14 skipped = runs already finalized in the session before the 600s-turn-budget
restart (they were counted as valid; their dirs were kept).

## Failure taxonomy (26)

### A. agy API timeout — "Error: timeout waiting for response"  (13 runs)
agy's call to the Gemini API timed out; the agent was cut off mid-turn. Where the
agent had already written a fix, the diff exists but the turn was truncated.

| Run | diff | note |
|---|---|---|
| matplotlib-23299 baseline/full | 0B / 0B | zero work before cut |
| matplotlib-23476 baseline | 0B | agent launched a C-extension build, then cut |
| matplotlib-23476 full | 787B | fix written, turn cut before verify |
| matplotlib-24627 baseline/full | 0B / 0B | zero work |
| pytest-5262 baseline | 0B | zero work |
| pytest-7521 baseline | 1614B | fix written; visible suite ran "67 passed", then cut |
| pytest-7521 full | 1122B | fix written; summary being written when cut |
| sphinx-10435 baseline | 0B | zero work |
| sphinx-10435 full | 1731B | fix written, turn cut |
| sympy-15875 baseline/full | 1983B / 1983B | both configs wrote (different) fixes, turn cut |

### B. Network drop — "Eligibility check failed … dial tcp unreachable / no such host"  (5 runs)
The machine's network/DNS died for ~1 minute at 22:42-22:43. agy could not reach
`daily-cloudcode-pa.googleapis.com`. These ran back-to-back, ~1s apart, confirming
an outage window, not a model outcome.

| Run |
|---|
| sphinx-9367 baseline/full |
| sphinx-9698 baseline/full |
| lcb-abc388_c baseline |

### C. Authentication timeout — "authentication timed out"  (5 runs)
agy attempted to re-authenticate (the Antigravity session token had expired server-side
during the outage window) and the interactive auth flow timed out in the non-interactive
runner.

| Run |
|---|
| sympy-23950 full |
| lcb-abc387_b full |
| lcb-abc390_c baseline/full |
| lcb-abc391_d baseline |

### D. Generic agy error — "Agent execution terminated due to error."  (1 run)
| Run |
|---|
| sympy-23950 baseline |

### E. Stale run — never actually executed  (1 run)
| Run |
|---|
| pytest-5262 full — manifest stuck at IN_PROGRESS, 0-byte transcript, wall_clock=0 |

### F. GENUINE failure — kept, NOT re-run  (1 run)
| Run | verdict |
|---|---|
| lcb-arc191_a baseline | transcript shows a complete solution attempt with **no infra error**. The agent's greedy "place largest surviving digit" strategy is mathematically wrong for the lexicographic-optimization problem (misses the parity/spatial constraint). Eval failed on hidden tests. This failure **stands** as the model's honest outcome. (Notably, the **full** config PASSED the same task — a real baseline-vs-full difference.) |

## Retry policy

All 25 runs in categories A-E were moved (not deleted) to
`carb_benchmark/runs/_retry_quarantine/` and re-run once, through the identical
runner: same prompts, same locked model, same 600s turn budget, same eval.
The category-F run keeps its FAILURE status.

Rationale: infrastructure failures invalidate a run; the model never got a full
honest turn. Re-running them once under identical conditions is standard retry
semantics. The retry results replace the quarantined outcomes in the aggregate.

## Root cause of "timeout waiting for response" (found during retry)

Probing `agy -p ... --print-timeout 3s` reproduces the exact error string. agy's
print-mode wait defaults to **5m0s**; for large-context tasks Google's response
exceeds 5 minutes, so agy aborts with `Error: timeout waiting for response`
before the model produces anything (0 tool iterations). This invalidated all
the category-A runs (and explains the thin 37B transcripts on several SUCCESS
runs, where the agent had already applied its fix before the final call timed
out).

**Fix (2026-08-16):** `run_benchmark_v2.py` now passes `--print-timeout 20m`
to agy; `RUN_TIMEOUT_SECONDS` raised 600 -> 1500; driver `RUN_TIMEOUT` 1800 ->
2700. The retry batch was restarted under the new budget.

## Retry progress notes (20m print-timeout, restart #2)

With agy's wait raised to 20m, agents now complete full turns. The failures
that remain are GENUINE model outcomes (the eval's hidden tests discriminate):

- **matplotlib-23299 baseline -> FAILURE (genuine).** Official gold fix deletes
  `backend` from the restore dict unconditionally (`del orig['backend']`). The
  baseline agent's fix only popped it when it held `_auto_backend_sentinel`,
  so the hidden test `test_no_backend_reset_rccontext` (custom backend
  'module://aardvark' inside rc_context) fails. The full config used the
  official approach and PASSED.
- **matplotlib-23476 baseline -> FAILURE (genuine).** Official gold fix resets
  `_dpi` to `_original_dpi` in `Figure.__getstate__` at pickle time. The
  baseline agent patched `FigureCanvasBase.__init__` instead (skip overwriting
  `_original_dpi`), which only prevents the second unpickle from double-scaling;
  the first unpickle still yields the doubled DPI (294 vs expected 42).
  Hidden test `test_unpickle_with_device_pixel_ratio` fails.
- **matplotlib-23299 full -> SUCCESS** (matched official fix).

These are exactly the "specific environments" the user flagged: the heavy
compiled-extension repos (matplotlib etc.) now produce real, subtle signal.

## Retry batch (run_retry_batch.py)

- 25 runs; first start 2026-08-16 ~00:43, restarted with 20m print-timeout ~00:52
- log: `results/benchmark_v2_retry.log`
- progress: `results/benchmark_v2_retry_progress.json`
- monitor: `tasklist | grep -i agy`
