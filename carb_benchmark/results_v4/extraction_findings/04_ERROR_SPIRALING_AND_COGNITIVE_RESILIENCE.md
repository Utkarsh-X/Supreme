# 🛡️ Extraction Dossier 04: Error Spiraling, Markov Transitions & Cognitive Resilience
### Post-Failure Dynamics Across 267 Canonical Terminal-Bench 2.1 Runs

---

## 1. Executive Abstract

In autonomous command-line agent evaluation, failure is not an anomaly; it is an intrinsic phase of the development loop. Compilers return syntax errors, unit tests fail assertions, and dependencies break. The decisive differentiator between production-grade agents and toy implementations is **cognitive resilience**: *When a terminal command crashes, does the agent systematically localize the bug, or does it spiral into repetitive, thrashing retry loops?*

This dossier analyzes post-failure behavioral dynamics across 1,102 command errors encountered during the 267 canonical runs:
1. **Immediate Error Recovery Rate**: Supreme achieved an immediate single-turn recovery rate of **76.91%** $P(\text{Success}_{t+1} \mid \text{Error}_t)$, outperforming Superpowers (70.2%) and Baseline (68.4%).
2. **The "Task Polling Spin Trap"**: Baseline and Superpowers frequently collapsed into passive background process polling loops (`manage_task -> manage_task`), with Superpowers generating 299 triple-polling cycles. Supreme reduced re-polling by **42%**.
3. **The Destructive Rewrite Churn**: Superpowers fell into 172 `write -> run -> write` churn loops, repeatedly rewriting code without inspecting intermediate failure logs.
4. **Deepest Error Spirals**: An autopsy of the worst error streaks in the benchmark (Streak 8 in `polyglot-rust-c`, Streak 6 in `torch-pipeline-parallelism`).

---

## 2. Quantitative Error Resilience Summary

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MACRO ERROR DYNAMICS & RECOVERY MATRIX                          │
├───────────────────────────────────┬──────────────────┬──────────────────┬──────────────┤
│ Metric                            │ Supreme (v1.0)   │ Superpowers-v4.0 │ Baseline     │
├───────────────────────────────────┼──────────────────┼──────────────────┼──────────────┤
│ Total Command Errors Encountered  │ 419              │ 329              │ 354          │
│ Runs Encountering ≥ 1 Error       │ 64 / 89 (71.9%)  │ 58 / 89 (65.2%)  │ 60 / 89(67.4%)│
│ Resilient Solves (Hit Error & Pass│ **44 / 64 (68.8%)**🥇 39/58 (67.2%) │ 34/60 (56.7%)│
│ Clean Solves (Zero Errors & Pass) │ 17 / 89          │ 19 / 89          │ 21 / 89      │
│ P(Success | Prior Error)          │ **76.91%** 🏆    │ 70.20%           │ 68.40%       │
│ Max Consecutive Error Streak      │ 6                │ **8** ⚠️         │ 7            │
│ Hard Timeouts (≥ 890 seconds)     │ **14** 🥇        │ 21 ⚠️            │ 18           │
└───────────────────────────────────┴──────────────────┴──────────────────┴──────────────┘
```

### Key Statistical Takeaway:
* **Active Hypothesis Testing vs. Passive Hesitation**: Supreme logged 419 command errors—the highest total. Detailed transcript review reveals this was not due to poor code quality, but active exploratory probing: Supreme routinely ran quick syntax probes (`python -c "import ..."` or `gcc -v`) to map out container environments before attempting tasks.
* **Higher Resilient Conversion**: When Supreme hit an error, it converted that run to a verified PASS **68.8% of the time**, compared to only **56.7%** for Baseline.

---

## 3. Markov State Transitions Post-Failure ($P(\text{Next} \mid \text{Error})$)

What tool does an agent invoke immediately after a command exits with code $\ne 0$?

```
  POST-ERROR ACTION DISTRIBUTION:
  ===============================
  1. Supreme (v1.0):
     run_command (error) ──► view_file (Inspect Logs/Code)     : 24.8%
     run_command (error) ──► replace_file_content (Patch)     :  9.5%
     run_command (error) ──► run_command (Diagnose via Bash)  : 58.2%
     run_command (error) ──► write_to_file (Full Overwrite)   :  7.5%

  2. Superpowers by obra:
     run_command (error) ──► write_to_file (Full Overwrite)   : 26.4% ⚠️
     run_command (error) ──► run_command (Retry Command)      : 44.1%
     run_command (error) ──► view_file (Inspect Documentation): 21.0%
     run_command (error) ──► replace_file_content (Patch)     :  1.2%

  3. Baseline:
     run_command (error) ──► run_command (Blind Retry)        : 61.2% ⚠️
     run_command (error) ──► write_to_file (Full Overwrite)   : 22.8%
     run_command (error) ──► view_file (Inspect)              : 14.5%
     run_command (error) ──► replace_file_content (Patch)     :  1.5%
```

### Architectural Insights:
1. **The Blind Retry Reflex in Baseline**: In 61.2% of post-error situations, Baseline immediately re-executed bash commands without reading source code or modifying files, often repeating the exact same command line.
2. **The Destructive Overwrite Reflex in Superpowers**: In over 26% of post-error situations, Superpowers completely overwrote the file with `write_to_file`. If a 400-line C file failed due to a missing semicolon on line 380, Superpowers rewrote the entire 400 lines, frequently introducing new syntax errors on line 40.
3. **Supreme's Diagnostic Reflex**: Supreme had the highest rate of surgical inspection (`view_file` on error logs) and targeted line replacement (`replace_file_content`), isolating the root cause before mutating code.

---

## 4. The "Task Polling Spin Trap" ($manage\_task$)

One of the most consequential behavioral defects uncovered in CARB-v4 is the **Task Polling Spin Trap**:

```
  PROBABILITY OF RE-POLLING MANAGE_TASK IMMEDIATELY:
  ==================================================
  Baseline:             [████████████████████] 50.1% (500 events)
  Superpowers by obra:  [█████████████████]    42.7% (423 events)
  Supreme (v1.0):       [███████████]          28.6% (244 events) 🥇
```

### Why this Occurred:
* The Antigravity harness supports asynchronous background process monitoring via `manage_task`.
* However, Antigravity features **reactive messaging**: when a background command finishes or writes to stdout, the system automatically notifies the agent context.
* **Superpowers and Baseline lacked awareness of reactive wakeups**, entering tight polling loops:
  - Superpowers recorded **299 occurrences** of the 3-gram `manage_task -> manage_task -> manage_task`.
  - Baseline recorded **310 occurrences**.
* **Supreme's Constitution (Rule 4: Loop Management)** explicitly forbids passive polling loops, instructing the agent to proceed with other tasks or pause execution until a reactive notification arrives. This saved Supreme **179 wasted tool turns**.

---

## 5. Case Studies: The Deepest Error Spirals

### Case 1: Superpowers on `polyglot-rust-c` (Streak 8 Error Loop)
- **Task**: Write a single polyglot file compiling in both Rust and C.
- **The Spiral**: Superpowers attempted to write the polyglot using inline bash heredocs:
  ```bash
  cat << 'EOF' > polyglot.c
  /* C and Rust code */
  EOF
  ```
- In PowerShell/Windows subshells, the nested quoting triggered unexpected syntax errors. Instead of using the native `write_to_file` tool, Superpowers retried variations of `echo` and `printf` 8 consecutive times, burning 400 seconds before switching tools.

### Case 2: Superpowers on `torch-pipeline-parallelism` (Streak 6 Host/Container Confusion)
- **The Spiral**: In Task 82, Superpowers attempted to execute PyTorch distributed training using:
  ```bash
  torchrun --nproc_per_node=2 pipeline.py
  ```
- The Docker container lacked PyTorch in its root path. Superpowers repeatedly attempted to execute `C:\Users\...\torchrun.exe` through the Windows host mount, triggering 6 consecutive `command not found` and `access denied` errors before timing out at 900s.

### Case 3: Supreme on `custom-memory-heap-crash` (Streak 6 Resilient Recovery)
- **Task**: Debug a memory heap corruption in a custom C++ memory allocator.
- **The Spiral & Recovery**: Supreme encountered 6 consecutive `Segmentation fault (core dumped)` errors while modifying pointer alignment arithmetic in the heap header.
- **The Breakthrough**: Rather than rewriting the entire file, Supreme enabled GDB (`gdb --batch -ex run -ex bt ./test`), located the exact off-by-8 byte alignment bug on line 142, applied a surgical 2-line patch with `replace_file_content`, and successfully passed 100% of test assertions.

---

## 6. Architectural Rules for Resilient Autonomous Agents

1. **Explicit Reactive Wakeup Invariance**: Agents must be explicitly instructed that background tasks will notify upon completion. Unbounded status polling must be hard-capped at 2 consecutive cycles.
2. **Surgical Diff over Whole-File Mutation**: Destructive whole-file overwrites on compiler failures drastically increase the probability of introducing secondary regression bugs.
3. **Diagnostic Tool Escalation**: Following a non-zero exit code, agent architectures should bias next-turn tool availability toward read/diagnostic tools (`view_file`, `grep_search`) rather than code rewrite tools.
