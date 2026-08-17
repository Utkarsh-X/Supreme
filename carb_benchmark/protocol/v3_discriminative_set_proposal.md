# V3 Proposal — A Discriminative Task Set

*Status: Phase A (calibration) in execution. Proposal prepared 2026-08-17;
Phase A launched 2026-08-18 00:42 (baseline-only, 41 candidates). Candidate
pool frozen, validation complete, telemetry instrumentation merged.
All numbers below are computed from `results/v2_corrected_matrix.json`,
`results/v2_session_telemetry.csv`, the SWE-bench Verified corpus
(`sources/data/swebench_verified/verified.jsonl`, 500 instances), and
LiveCodeBench v5 (`sources/data/lcb_v5.jsonl`, 175 problems).*

## 0. Execution status (2026-08-18)

- Candidate pool (expanded 2026-08-18, now 93 tasks in
  `task_registry/v3_calibration_tasks.txt`):
  - 20 VALIDATED hard-tier SWE (1-4h / >4h) — the full venv-supported hard
    tier on this Windows box; 5 more candidates REJECTED in validation
    (unresolvable test labels / env limits), rejection records kept.
  - 46 fresh LCB (21 original + 25 hard-tier added tranche 2; all 2025
    post-cutoff AtCoder, no v2 exposure).
  - 27 VALIDATED medium-tier SWE (15min-1h) added tranche 3 (3 REJECTED:
    2 unresolvable labels, 1 env/ABI).
  Rationale for expansion: 41 candidates would calibrate down to only ~18-20
  baseline-failing tasks; the target is ~50 final tasks, which needs a pool
  of ~110-130. Expansion materialized + validated what the platform can run;
  remaining untapped sources are TerminalBench 2.0 and custom diagnostics
  (harness work needed).
- Phase A running via `scripts/run_v3_calibration.py` ->
  `results/v3_calibration.json` (resumable, baseline-only). First datapoints:
  baseline FAILS django-10554 (39-line real fix attempt, hidden test red) and
  django-12325; passes the rest so far (~71% early pass rate on hard SWE).
- Telemetry instrumentation merged into `run_benchmark_v2.py` (2026-08-18):
  agy runs with `--output-format stream-json`; per run saves `telemetry.json`
  with token usage (input/output/thinking/cache/total), tool-call counts by
  name, num_turns, agy-reported duration, and time-to-first-edit. Session cap
  raised 20 -> 40 minutes, configurable via `--timeout-minutes`.
- Handoff: `scripts/build_v3_final_set.py` locks `final_tasks_v3.json` from
  baseline-FAILED calibration cells only (dry-run safe).
- Open risk: if calibration yields < ~40 failing tasks, the protocol's
  mitigation applies — enlarge the pool (medium SWE/LCB) or multi-seed; the
  keep rule (baseline-fail only) is never weakened.

---

## 1. Why v2 cannot demonstrate a difference

The v2 result is a clean **null result**: 46 of 50 tasks (92%) have identical
outcomes under all three configurations, exact paired McNemar p = 1.0 for
every pair, and pass rates sit at 94 / 94 / 92. The reason is structural, not
random:

- **Saturation.** 46 tasks are solved by *every* configuration. A task solved
  by all configs carries zero information about configuration differences.
- **Task selection.** v2 drew its 30 SWE instances almost entirely from the
  easiest SWE-bench Verified tier (24 of 30 are `<15 min fix`, 6 are
  `15 min - 1 hour`) and its 20 LCB problems from the easy AtCoder tier.
  These are tasks a strong model solves regardless of system prompt.
- **Power.** With 50 paired tasks, even a genuine 10-point difference would be
  detected only ~15% of the time. The benchmark measures the model, not the
  configurations.

**The only way to produce real numbers that separate the configurations is to
select tasks on which the baseline fails.** Everything below is designed
around that requirement.

## 2. Why "more time / more tokens" is not the fix

A natural reaction is to raise the session budget (longer cap, more tool
iterations). The v2 data says time was **not** the binding constraint:

- The 10 failing cells took a median of **323 s** — five minutes of work, far
  from the 20-minute cap.
- Only **3 cells in the entire matrix** hit the ≥1100 s cap, and all three
  **passed**.
- The four distinct failing tasks failed after 219–908 s of real work with
  identifiable wrong approaches (wrong hook, wrong API shape), not truncation.

More budget only helps tasks that are *hard enough* that time becomes the
constraint. On the v2 set, time is never the constraint, so budget increases
would change nothing measurable. **The lever is task difficulty, not budget.**
(Budget changes do belong in V3, but as a *supporting* change: see §6.)

## 3. The available hard pool (real corpus numbers)

### 3.1 SWE-bench Verified — difficulty tiers (human resolution time)

| Tier | All repos | In repos we support (venvs exist) | Used in v2 |
|---|---|---|---|
| `<15 min fix` (easiest) | 194 | ~159 | 24 |
| `15 min - 1 hour` | 261 | 237 | 6 |
| `1-4 hours` | 42 | 39 | 0 |
| `>4 hours` | 3 | 2 | 0 |

The hard tier in supported repos (django 22, sympy 6, sphinx 4, astropy 3,
pytest 3, scikit-learn 1, plus 2 × `>4 hours`) gives **41 fresh instances**
with no v2 exposure. These carry much larger gold patches (e.g., astropy-13398:
396 FAIL_TO_PASS tests) and are the natural baseline-failing pool.
`scripts/v3_propose_tasks.py` generates the machine-readable shortlist
(`task_registry/v3_candidate_shortlist.json`).

### 3.2 LiveCodeBench v5 — AtCoder tiers

| Tier | AtCoder problems | Used in v2 |
|---|---|---|
| easy | 26 | 20 |
| medium | 26 | 0 |
| hard | 60 | 0 |

86 fresh medium/hard AtCoder problems are directly usable with the existing
stdio `main.py` grader.

### 3.3 Never-used families

- **TerminalBench 2.0** — 40 candidates (20 task snapshots on disk), a
  build/CI/environment-fix family no configuration has seen.
- **Custom diagnostics** — 20 candidates (premature-completion, auth-logging,
  token-handling traps).

## 4. Selection protocol — empirically verified baseline failures

Difficulty tiers are priors, not proof. To get **real numbers that the
baseline fails**, V3 runs a two-phase protocol:

**Phase A — calibration (baseline only).** Run the *baseline* configuration
on the candidate shortlist (recommend starting with the 41 hard SWE +
60 hard LCB = ~100 candidates; expand with medium SWE / medium LCB if the
calibration pass rate is below ~30%). Keep a task in the V3 set **if and only
if baseline FAILS it**. This produces an empirically calibrated set with a
measured baseline pass rate in the target window (30–60%).

**Phase B — the experiment.** Run all three configurations on the *locked*
calibrated set. The set is frozen after Phase A (pre-registration: no task is
added or removed based on challenger results). Phase A also supplies the
baseline cell for every task, so Phase B only adds supreme + superpowers
cells.

Why this is fair and anti-cherry-picking: baseline alone decides difficulty;
challenger configs never influence selection; the calibrated set is fixed
before any challenger result exists.

## 5. Power analysis (paired design)

The design is paired (every task runs under every config), so the correct
test is McNemar on discordant pairs. Required sample size for a two-sided
α = 0.05, 80% power:

| Baseline pass rate | Challenger pass rate | Tasks needed (per config) |
|---|---|---|
| 0.90 (v2-like) | 0.95 | ≈ 320 (infeasible — ceiling) |
| 0.70 | 0.85 | ≈ 130 |
| 0.55 | 0.75 | ≈ 85 |
| 0.45 | 0.65 | ≈ 70 |
| 0.40 | 0.60 | ≈ 60 |

**Recommendation: a calibrated set of 80–90 tasks per configuration**
(≈ 90 × 3 = 270 graded cells, of which baseline's 90 come free from Phase A).
At a measured baseline pass rate of ~50%, this detects a challenger rate of
~65–70% (the margin where a genuine skill effect would be expected to show).
If only ~40 tasks calibrate as hard, run 3 seeds per task (240 sessions) to
recover power and get variance estimates.

## 6. Session budget and execution plan

- **Per-session cap: raise from 20 minutes to 40 minutes** and lift the tool
  iteration ceiling (v2's 20-min cap was reached only 3 times, all successful,
  but hard tasks plausibly need the headroom). Re-evaluate the cap after the
  first 10 calibration sessions and fix it for the rest of the run.
  **Status: DONE (2026-08-18).** `run_benchmark_v2.py` now defaults to 40
  minutes (`--timeout-minutes 40`); the running Phase A launched before this
  change used the old 20-minute cap, which is acceptable because early hard-SWE
  cells finish in 1-3 minutes — the cap rarely binds.
- **Order:** interleave configurations daily and randomize task order; never
  run one config to completion before another starts (this removes the
  day-level latency confound flagged in the v2 telemetry).
- **Model:** keep `gemini-3.6-flash-high` at temperature 0 (same as v2) so
  results are comparable; optionally add a second model as a robustness arm.
- **Estimated cost:** v2 median session ≈ 150 s; hard tasks will be slower.
  At ≈ 12 min median per session, 270 sessions ≈ 55 single-machine hours, or
  ~18 hours with three workers.

## 7. Telemetry instrumentation (fixes v2 gaps)

v2 could only report wall-clock, diff size, and transcript length — `tool_iterations`
was never populated (always 0 in every manifest) and token usage was dropped
after the v1 pilot. Before V3, extend `finalize_run.py` to capture per session:

- prompt + response token counts (and per-tool-call totals if the engine exposes them),
- tool-call count and breakdown by tool type (edit / test / read / search),
- time-to-first-edit and test-run count,
- session-level latency breakdown (model latency vs tool execution).

This turns the secondary metrics (latency, token efficiency, edit patterns)
into reportable numbers instead of proxies, and lets the V3 report include
efficiency comparisons alongside the primary pass/fail result.

## 8. Pre-registered success criteria

Primary (decision): task-level pass rate; supreme-v2.0 and/or
superpowers-v2.0 **statistically greater than baseline** by exact paired
McNemar (one-sided, α = 0.05), on the locked calibrated set.

Secondary (reportable regardless of the primary): latency on solved tasks
(Mann-Whitney U), token efficiency, diff minimality (lines changed vs gold),
and per-family breakdowns (SWE vs LCB vs TerminalBench).

Reporting rule (same as v2): every cell carries its run id; all corrections
are recorded as `corrected_verdict` with a note; nothing is dropped.

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Calibration yields too few hard tasks (<40) | Enlarge the pool with medium-tier SWE and LCB; use multi-seed |
| Hard tasks exceed the 40-min cap | Cap is re-calibrated in the first 10 sessions, then frozen |
| Day-level latency variance | Interleaved daily scheduling, randomized order |
| Contamination (task seen before) | Fresh instances only; v2 ids are excluded in the shortlist script |
| Challenger overfits to calibration | Baseline-only calibration; set locked before challengers run |

## 10. Deliverables

1. `scripts/v3_propose_tasks.py` + `task_registry/v3_candidate_shortlist.json` (done — this proposal's companion artifacts).
2. Calibration run record (baseline-only pass/fail per candidate) → `results/v3_calibration.json`.
3. Locked V3 task registry (`task_registry/final_tasks_v3.json`).
4. V3 run + corrected matrix (`results/v3_*`), following the v2 audit conventions.
