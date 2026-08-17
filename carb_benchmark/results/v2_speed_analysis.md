# v2 Speed / Latency Analysis — Superpowers vs Baseline

_Compiled 2026-08-18 from `results/v2_session_telemetry.csv` (150 cells, 50 tasks
× 3 configs, `gemini-3.6-flash-high` via agy, isolated temp profile, temp 0)._

## 1. The headline

Superpowers solved the same tasks in **~35% less wall-clock time** than baseline,
with **identical accuracy** (92% vs 94%, p = 1.0 — no correctness difference).
The speed gap is real but it is **concentrated in the LiveCodeBench family**,
and it survives removing every 20-minute cap-hit session.

| Metric (median) | Baseline | Supreme | Superpowers |
|---|---|---|---|
| Wall-clock, all cells | 156 s | 151 s | 102 s |
| Wall-clock, passed cells | 138 s | 131 s | 98 s |
| Wall-clock, passed **LCB** cells | 66 s | 65 s | **46 s** |
| Wall-clock, passed **SWE** cells | 221 s | 169 s | 150 s |
| Diff lines / files (passed) | 21 / 2 | 22 / 2 | 21 / 2 |

## 2. Statistical picture (Mann-Whitney U, two-sided)

| Comparison | Sample | z | p |
|---|---|---|---|
| baseline vs superpowers | all cells | 1.41 | 0.159 |
| baseline vs superpowers | **passed LCB cells** | **2.38** | **0.017** |
| baseline vs superpowers | passed SWE cells | 0.80 | 0.423 |
| supreme vs superpowers | passed LCB cells | 1.79 | 0.074 |

Only one contrast is significant: superpowers solves LCB problems faster than
baseline. On SWE tasks the latency gap (221 s vs 150 s median) is not
significant (p = 0.42).

## 3. Robustness: does the LCB effect survive the confounds?

Two confounds were checked.

**(a) 20-minute cap-hits.** Five cells in the whole matrix hit the ≥1100 s cap
(4 LCB + 1 SWE: baseline 2, superpowers 2, supreme 1 — all PASSED, but they
dominate any mean and inflate medians). Excluding cap-hits, the LCB effect
**gets stronger**, not weaker:

| Sample (LCB passed, caps excluded) | n | median | p vs superpowers |
|---|---|---|---|
| baseline | 18 | 60.2 s | **0.005** |
| supreme | 20 | 64.5 s | 0.012 |
| superpowers | 18 | 43.1 s | — |

The cap-hits are symmetric across configs, so they do not create the effect;
they merely add noise.

**(b) Day-level drift.** Superpowers LCB ran almost entirely on 2026-08-17,
while baseline LCB ran mostly on 08-15/16. Baseline was *slower* on 08-17
(median 282 s vs 97 s on 08-15) — i.e., if anything the late-day baseline was
slower, which would *understate* the superpowers advantage, not create it.
Within the same day (08-17, paired LCB tasks), baseline took 1211 s / 191 s /
40 s vs superpowers 42 s / 63 s / 39 s on the same tasks — consistent with the
aggregate. The direction of the day confound works against the finding, so the
effect is not an artifact of when the arms ran.

## 4. Interpretation

- **It's a behavioral, not a correctness, signal.** Both configs produce the
  same answers (same diff size, same files touched, same pass rate); superpowers
  gets there faster on algorithmic tasks. This is exactly the kind of secondary
  metric the v2 report flagged as worth studying when accuracy saturates.
- **The effect is LCB-specific.** SWE latency is statistically flat across
  configs (p > 0.4). A plausible mechanism: superpowers' explicit test-driven /
  verify-early skills shorten the edit→test loop that dominates LCB (write
  `main.py`, run grader, fix, rerun), while SWE latency is dominated by
  repo-wide search and dependency work that system prompts don't compress.
- **Caveats (unchanged from FINDINGS_v2):** single run per cell, multiple
  comparisons, and the day-level scheduling imbalance. The v3 protocol
  addresses all three: interleaved daily scheduling, randomized order, and
  per-session token/tool-call telemetry to explain *why* superpowers is faster
  (fewer test runs? fewer edit iterations? shorter reasoning?).

## 5. What v3 needs to capture to explain the mechanism

The v2 records have no token counts and `tool_iterations` is always 0 (never
populated by `finalize_run.py`). To turn this behavioral finding into a
mechanism, v3 must record per session: prompt/response tokens, tool-call count
by type (edit/test/read/search), time-to-first-edit, and test-run count — per
`protocol/v3_discriminative_set_proposal.md` §7. If the skill system's advantage
is "fewer wasted iterations," the token and tool-call curves should show it;
if it's "shorter deliberation," the reasoning/token curves should show it.
