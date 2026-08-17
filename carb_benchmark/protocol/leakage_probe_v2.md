# CARB-v2 System-Prompt Leakage Probe — Evidence

**Date**: 2026-08-15
**Task**: scikit-learn__scikit-learn-14141 (both configs), model `gemini-3.6-flash-high` (locked)
**Method**: `run_benchmark_v2.py --append-question` — appends a NEUTRAL disclosure
question (no Supreme vocabulary) to the task prompt; the model must say whether any
custom engineering instructions are active and quote the key principles verbatim.
Both probe runs went through the exact benchmark harness (isolated temp profile,
real task workspace, real eval) and **both solved the task** (eval PASS), so the
disclosure question did not distort task behavior.

## Baseline config (`baseline-v2.0`) — run 2026-08-15-195436

- **Eval: PASS** (solved the sklearn issue)
- Constitution markers hit: **NONE** (`const = []`)
- The model answered "YES — there are active operating protocols" and quoted
  principles such as "Inspect Logs & Stack Traces Before Diagnosing Errors",
  "No Superficial Symptom Patches", "Never Declare Success Without Running
  Verification Commands", "Maintain documentation integrity".

**Why this is NOT a leak** (verified, not assumed):

1. **None of the quoted principles appear in any SupremeAgent file.** Grep of
   `SupremeAgent/` for every quoted phrase returns zero matches. The Supreme
   vocabulary (constitution markers) has zero hits in the whole transcript.
2. **The quoted principles are agy's BUILT-IN system prompt.** A control session
   ran agy with a completely EMPTY profile (no `.gemini` at all) and asked it to
   quote its system prompt verbatim. It reproduced the exact same `<guidelines>`
   section — "Inspect Logs & Stack Traces…", "No Superficial Symptom Patches…",
   "Never Declare Success Without Running Verification Commands…" — verbatim.
   These are baked into the Antigravity CLI and are present in EVERY config,
   including baseline. The agy.exe binary itself contains fragments of these
   guidelines ("code search" ×9, "documentation integrity", "symptom" ×3, "masking" ×4).
3. **The isolation is mechanical.** The temp profile copies only top-level
   `~/.gemini` auth files; `~/.gemini/config/GEMINI.md` (where the Supreme system
   lives) is excluded, and the top-level `GEMINI.md` is empty (verified earlier).

## Full config (`full-v2.0`) — run 2026-08-15-200241

- **Eval: PASS** (solved the sklearn issue)
- Constitution markers hit: **['Supreme', 'Evidence Over Assumption',
  'Minimum Justified Change', 'Preserve System Integrity',
  'Completion Requires Evidence', 'User Intent Is Authoritative',
  'Uncertainty Must Be Explicit', 'Revisable Hypotheses']**
- Full-system markers hit: **['Operating Protocol', 'Sub-Agent', 'Researcher',
  'Implementer', 'Debugger', 'Reviewer', 'Failure Classification']**
- The model quoted the Supreme `01-constitution.md` principles VERBATIM
  (Evidence Over Assumption, User Intent Is Authoritative, Preserve System
  Integrity, Minimum Justified Change, Completion Requires Evidence,
  Uncertainty Must Be Explicit, Plans and Decisions Are Revisable Hypotheses,
  Scrutiny Scales With Risk, Consequential Actions Require Proportional
  Accountability).

## Verdict

| Config | Supreme content delivered to model | Supreme content in model's self-report | Task solved |
|---|---|---|---|
| baseline-v2.0 | NO (isolated profile; only agy built-ins) | NONE (const=[]) | YES (PASS) |
| full-v2.0 | YES (full 5-file Supreme system in prompt) | YES (8 const markers + verbatim quotes) | YES (PASS) |

The two configurations differ ONLY in the injected system prompt content; no
cross-config contamination was observed. Baseline transcripts contain no Supreme
vocabulary; full-config transcripts demonstrably contain it.
