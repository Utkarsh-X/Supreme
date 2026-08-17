# CARB-v1 System-Prompt Leakage Probe — Audit Report

**Date**: 2026-08-15
**Model**: Gemini 3.6 Flash (High) via `agy.exe` (Antigravity CLI 1.1.13, print mode)
**Probe task**: T001_sample_repo_debug workspace — create `probe_fib.py` (fib, prints fib(10)=55) + disclose all active system instructions verbatim
**Runner**: `carb_benchmark/scripts/probe_leakage.py` (uses the EXACT benchmark agy invocation: `-p <prompt> --model "Gemini 3.6 Flash (High)" --add-dir <workspace> --mode accept-edits --dangerously-skip-permissions`)
**Artifacts**: raw outputs + verdict JSONs in `protocol/leakage_probe/20260815-12*`

---

## 1. Static findings (no model runs)

1. **`C:\Users\Utkarsh\.gemini\config\GEMINI.md` (27,912 bytes) is the FULL Supreme Agent system prompt**, combining all 5 files:
   `01-constitution.md`, `02-operating-protocol.md`, `03-sub-agent-profiles.md`, `04-environment-profile.md`, `05-persistent-state.md`.
2. agy's own customization docs (`builtin/skills/agy-customizations/SKILL.md`) state: **Global Configuration at `~/.gemini/config/` "applies to all projects and workspaces run on your machine"**.
3. The benchmark harness (`run_antigravity_agy.py`) isolates **only the baseline** phase (temp `USERPROFILE`/`HOME`, copies top-level `.gemini` files except names containing `rule`/`constitution`). The **constitution and full phases run in the real user profile** — where the global Supreme `GEMINI.md` lives. The temp profile gets no `config/` dir at all, so baseline is clean *by accident* (the `config` directory is skipped, not deliberately).
4. The "system prompt" for constitution/full is not a real system prompt: it is **prepended into the `-p` user prompt** as `[SYSTEM CONSTITUTION INSTRUCTION]...`.
5. CLI log line observed on every run: `Model ID "Gemini 3.6 Flash (High)" not in local config, defaulting to CCPA` — the model selector is not a configured model ID; agy silently falls back to a default.

## 2. Probe matrix (5 runs, all in print mode, 25–27s each, exit 0, all solved fib correctly)

| # | Probe | Env | Injected prompt | Constitution markers | Full-system markers | Verdict |
|---|---|---|:---:|:---:|:---:|---|
| 1 | `baseline` | isolated temp profile | none | 0 (only "Supreme" inside `E:/RofU/Supreme/...` file paths) | 0 | **CLEAN** |
| 2 | `constitution` | **real profile** | constitution | 12/12 | 2 (Sub-Agent — text inside constitution §9) | **CONTAMINATED** (full system active globally) |
| 3 | `full` | **real profile** | constitution + 4-line protocol | 12/12 | 2 | full system active (as intended, but injected copy is redundant) |
| 4 | `constitution_isolated` (control) | isolated temp profile | constitution | 12/12 | 2 | injection alone works; isolated = clean of global file |
| 5 | `real_clean` (control) | **real profile** | **none** | **12/12** | 2 | **PROVES global GEMINI.md loads: full Supreme system active with zero injection** |

## 3. Decisive evidence

- **`real_clean` (no injection, real profile) disclosed the Supreme constitution AND operating protocol, quoting the global file's own section names**: "User Rules: Supreme Engineering Constitution (`01-constitution.md`)" and "User Rules: Operating Protocol (`02-operating-protocol.md`)". Those `01-`/`02-` numbered names exist only inside the global `config/GEMINI.md`.
- **`full` probe wrapped the disclosed rules in agy's `<RULE[user_global]>` tag** — the marker for globally loaded user rules.
- **`baseline` (isolated) and `constitution_isolated` (control) attributed the constitution to the injected prompt** (`[SYSTEM CONSTITUTION INSTRUCTION]`) and showed no global-rule content.

## 4. Gate verdicts

- **GATE A — baseline has no Supreme system prompt**: ✅ **PASS** (0% leakage; only hit is the workspace path string "Supreme").
- **GATE B — constitution gets ONLY the constitution**: ❌ **FAIL** — the real-profile constitution run has the **FULL Supreme system** (operating protocol + sub-agents + persistent state + environment profile) loaded globally via `~/.gemini/config/GEMINI.md`, in addition to the injected constitution.
- **GATE C — full gets the full system**: ✅ **PASS** behaviorally, but the injected 4-line protocol is redundant with the globally loaded full file.
- **GATE D — model actually invoked & correct identity**: ✅ **PASS** — all runs 25–27s, exit 0, task solved (fib(10)=55), model self-identifies as Gemini 3.6 Flash (High). Minor caveat: agy logs "not in local config, defaulting to CCPA" for the requested model name.

## 5. Conclusion

**The benchmark's three-way comparison is broken.** The harness's isolation protects only the baseline; the constitution and full configurations both run with the full Supreme system prompt globally active (via `~/.gemini/config/GEMINI.md`). Therefore:

- `constitution-v1.0` ≈ **full system** (not constitution-only) → the intended gradient "no system prompt → constitution → full" collapses to "no system prompt → full → full".
- Any prior report claiming "0.0% prompt leakage / pristine isolation" for the three configurations is contradicted by this empirical probe; the previous verification scripts tested an *isolated* setup that the real benchmark never used for constitution/full.
- The baseline leg is genuinely clean and can be trusted once re-run with correct evaluation (no more exit-code-0 bogus passes, real per-task tests, saved transcripts).

## 6. Required fixes before any valid benchmark run

1. **Isolate ALL three configurations** identically (temp profile, auth copied, no global `GEMINI.md`), or explicitly move the Supreme system prompt out of the global profile so the real profile is clean.
2. Inject the constitution / full prompt as a **true system prompt** if agy supports it, or document that the comparison is "prompt-text variants", not system-prompt injection.
3. Fix model resolution: use a model ID agy recognizes (verify via `agy models`), don't rely on the silent CCPA fallback.
4. Fix the pass/fail evaluator (no `exit_code == 0` fallback), save transcripts, and use task-specific hidden tests.
5. Decide the corpus: the current 60 tasks all collapse onto 3 pilot workspaces, so task-level correctness is not measured.
