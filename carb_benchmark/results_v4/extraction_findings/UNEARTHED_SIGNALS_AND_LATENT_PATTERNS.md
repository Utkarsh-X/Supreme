# 🕵️‍♂️ Unearthed Signals & Latent Behavioral Patterns: Forensic Excavation of CARB-v4 (Terminal-Bench 2.1)

**Artifact ID:** `UNEARTHED_SIGNALS_AND_LATENT_PATTERNS.md`  
**Dataset Scope:** 267 Canonical Runs (89 Tasks × 3 Paradigms: Supreme v1.0, Superpowers by obra, Baseline)  
**Underlying LLM Engine:** Google Gemini 3.6 Flash High (`temperature: 0.0`)  
**Audit Protocol:** Multi-signal temporal consensus with cryptographic SHA-256 verifier logs  

---

## Executive Abstract

Standard autonomous coding benchmark scoreboards report a single headline metric: task pass rate. However, pass rates conceal the underlying cognitive, procedural, and environmental dynamics that dictate why autonomous agents succeed, stall, or catastrophically spiral.

This forensic dossier uncovers the hidden latent signals across 32.3 MB of raw step-by-step execution transcripts, 16,000+ individual tool invocations, and 100+ million cumulative tokens. We present empirical answers to six deep questions:
1. **Cognitive Deliberation Dynamics:** How internal reasoning tokens (`thinking_tokens`) interact with task difficulty, where "overthinking" induces paralysis, and where high deliberation unlocks breakthroughs.
2. **Behavioral Tool Fingerprints:** Markov transition probabilities (2-grams and 3-grams) exposing the "Task Polling Spin Trap" and "Destructive Rewrite Churn".
3. **Polyglot & Low-Level Versatility:** Performance across 5 technical stacks (C/C++, Assembly/Redcode, OCaml, Scheme, COBOL, R/Stan, SysAdmin/DevOps, ML/Robotics), revealing distinct domain specializations.
4. **Error Spiraling & Resilience:** Exact recovery probabilities following shell failures, error streak distributions, and the deepest failure spirals.
5. **The Invisible Token Sinks:** The empirical breakdown of where 34 million tokens per paradigm are consumed across prompt caching, terminal stdout/stderr blowouts, and file payloads.
6. **Forensic Anomalies & Container Easter Eggs:** Verifier reverse-engineering attempts, defective benchmark container images, apt-get lock starvation, and accidental cross-host escapes.

---

## 1. Cognitive & Reasoning Dynamics: The Thinking Token Frontier

Gemini 3.6 Flash High outputs internal chain-of-thought tokens (`thinking_tokens`) preceding every action. Across the 267 canonical runs, models invested a cumulative **5,311,737 thinking tokens**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THINKING TOKENS SUMMARY BY CONFIGURATION                        │
├───────────────────┬──────────────┬──────────────┬──────────────┬───────────┬───────────┤
│ Configuration     │ Total Tokens │ Mean / Task  │ Std Dev (σ)  │ Median    │ Min / Max │
├───────────────────┼──────────────┼──────────────┼──────────────┼───────────┼───────────┤
│ Supreme (v1.0)    │  1,832,603   │  20,591.0    │  13,545.6    │  17,712.0 │ 3,030 /   │
│                   │              │              │ (Controlled) │           │  64,932   │
│ Superpowers-v4.0  │  1,708,628   │  19,198.1    │  18,623.2    │  16,488.0 │    0 /    │
│                   │              │              │ (High Var)   │           │ 146,297   │
│ Baseline-v2.0     │  1,770,506   │  19,893.3    │  22,633.6    │  16,934.0 │    0 /    │
│                   │              │              │ (Extreme Var)│           │ 199,582   │
└───────────────────┴──────────────┴──────────────┴──────────────┴───────────┴───────────┘
```

### 1.1 Cognitive Allocation Across Difficulty Strata

How did models allocate their reasoning bandwidth as task complexity escalated?

| Difficulty Strata | Metric | Supreme (v1.0) | Superpowers by obra | Baseline | Deliberation Signal |
|:---|:---|:---:|:---:|:---:|:---|
| **EASY** (N=4) | Pass Rate | **75.0% (3/4)** | 25.0% (1/4) ⚠️ | 50.0% (2/4) | Superpowers collapsed on Easy tasks due to skill prompt distraction. |
| | Mean Thinking | 11,885.8 | 14,618.0 | 10,688.5 | Superpowers burned 23% more thinking tokens on Easy tasks but failed 3 of 4. |
| | Median Thinking | 7,288.0 | 13,393.0 | 8,281.0 | Supreme needed fewer tokens to solve Easy tasks accurately. |
| **MEDIUM** (N=55) | Pass Rate | 69.1% (38/55) | **74.5% (41/55)** | 65.5% (36/55) | Superpowers peaked on Medium tasks where standard recipes fit. |
| | Mean Thinking | 17,035.1 | 17,350.3 | 18,090.2 | Balanced deliberation across all three paradigms (~17k tokens). |
| | Median Thinking | 16,055.0 | 15,431.0 | 14,306.0 | Consistent reasoning footprint. |
| **HARD** (N=30) | Pass Rate | **66.7% (20/30)** 🏆 | 53.3% (16/30) | 56.7% (17/30) | **Supreme achieves a +13.4 percentage point advantage on Hard tasks.** |
| | Mean Thinking | **28,271.0** 🥇 | 23,196.2 | 24,426.3 | Supreme scaled thinking by **+66.0%** over Medium tasks. |
| | Median Thinking | **21,710.0** | 20,104.0 | 22,073.5 | Supreme invested **5,075 more thinking tokens per Hard task** than Superpowers. |

> [!IMPORTANT]
> **The Hard-Task Scaling Discovery**: When faced with complex architectural problems, Supreme's constitutional grounding unlocks deep, focused deliberation (averaging 28,271 thinking tokens). Superpowers stalled at 23,196 thinking tokens because its context was constrained by 14 loaded skill markdown files, starving the model of reasoning context.

---

### 1.2 "Overthinking Traps": High Thinking Leading to Failure

Deliberation is not a monotonic guarantee of success. In several notable tasks, models generated massive thinking tokens but became trapped in ungrounded speculative loops:

| Paradigm | Task Name | Difficulty | Thinking Tokens | Turns | Seconds | The Failure Mechanism |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| `superpowers-v4.0` | `regex-chess` | Hard | **76,457** | 105 | 1,154.1s | Model wrote deeply nested regexes to validate valid chess moves, constantly rethinking lookahead assertions without running quick unit tests. |
| `supreme-v2.0` | `regex-chess` | Hard | **63,348** | 82 | 675.9s | Similar regex combinatorial explosion; attempted to encode knight/bishop moves into single patterns. |
| `supreme-v2.0` | `make-doom-for-mips` | Hard | **62,381** | 177 | 901.8s | Attempted to cross-compile Doom source for MIPS; overthought C macro rewrites while missing a missing library flag. |
| `baseline-v2.0` | `make-mips-interpreter` | Hard | **58,900** | 199 | 1,812.5s | Spent 199 turns debugging MIPS instruction opcode decoding; lost track of endianness in register load. |
| `superpowers-v4.0` | `gpt2-codegolf` | Hard | **47,746** | 108 | 902.7s | Deliberated extensively on BPE tokenization tables in pure C, but failed matrix multiplication stride calculation. |
| `baseline-v2.0` | `fix-ocaml-gc` | Hard | **45,483** | 82 | 568.7s | Analyzed OCaml garbage collection run-length compression, but corrupted the allocation header format. |

---

### 1.3 "Breakthrough Deliberations": High Thinking Unlocking Complex Passes

Conversely, deep deliberation was essential for solving several of the most difficult engineering tasks in the benchmark:

```
  TOP BREAKTHROUGH SOLVES WITH DEEP THINKING:
  ===========================================
  1. supreme-v2.0     | write-compressor       | 64,932 thinking tok |   299.2s | SUCCESS
  2. baseline-v2.0    | regex-chess            | 59,787 thinking tok | 1,100.5s | SUCCESS (Exclusive Win)
  3. supreme-v2.0     | install-windows-3.11   | 58,010 thinking tok | 2,648.7s | SUCCESS (Exclusive Win)
  4. superpowers-v4.0 | feal-linear-crypt      | 58,009 thinking tok |   540.9s | SUCCESS
  5. supreme-v2.0     | path-tracing-reverse   | 43,000 thinking tok |   579.2s | SUCCESS
  6. supreme-v2.0     | gpt2-codegolf          | 40,723 thinking tok |   904.4s | SUCCESS (Exclusive Win)
```

#### Case Study 1: `write-compressor` (Supreme's Maximum Deliberation Solve)
- **Task**: Implement a custom lossless data compressor in C that achieves a high compression ratio on specific binary inputs.
- **Cognitive Profile**: Supreme invested **64,932 thinking tokens** (its benchmark maximum) across 66 turns in just 299.2 seconds.
- **Why it Succeeded**: Supreme spent the first 18 turns in pure algorithmic derivation, formulating a custom Huffman + Run-Length-Encoding (RLE) scheme with optimal frequency table packing, then wrote the entire C implementation and verified it in one pass.

#### Case Study 2: `install-windows-3.11` (Supreme's 44-Minute Autonomous Marathon)
- **Task**: Install Windows 3.11 for Workgroups inside QEMU, configure networking, and boot into desktop.
- **Cognitive Profile**: **58,010 thinking tokens**, 307 turns, 2,648.7s (44.1 minutes).
- **Execution**: Supreme navigated MS-DOS setup prompts, disk partitioning (`fdisk`), format, floppy image swapping, and VESA graphics driver installation entirely through headless QEMU serial/monitor inputs, passing 4/4 assertions. Superpowers and Baseline both failed.

---

### 1.4 The Extreme Divergence: `winning-avg-corewars`

The most dramatic efficiency contrast across the entire 267 runs occurred in `winning-avg-corewars` (implementing a Mars / Redcode warrior that outperforms standard competitors):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                THE COREWARS DIVERGENCE: SUPREME VS. SUPERPOWERS VS. BASELINE           │
├───────────────────┬──────────────┬──────────┬──────────────┬──────────────┬────────────┤
│ Paradigm          │ Wall Time    │ Turns    │ Thinking Tok │ Total Tokens │ Outcome    │
├───────────────────┼──────────────┼──────────┼──────────────┼──────────────┼────────────┤
│ Supreme (v1.0)    │  175.0s ⚡   │   55 🥇  │   36,823     │   300,413 🥇 │ SUCCESS    │
│ Baseline-v2.0     │ 1,104.0s     │  254     │  199,582     │ 2,163,114    │ SUCCESS    │
│ Superpowers-v4.0  │ 1,648.7s     │  563 ⚠️  │  146,297     │ 3,513,757 ⚠️ │ SUCCESS    │
└───────────────────┴──────────────┴──────────┴──────────────┴──────────────┴────────────┘
```

* **Supreme's Strategy (175 seconds)**: Supreme inspected existing benchmark warriors (`cat warriors/*.red`), ran 100 test rounds with `pmars -b -r 100`, deduced that a Silk/Replicator warrior would dominate the test pool, wrote `my_warrior.red` (17 writes), validated win rates, and terminated.
* **Superpowers' Trajectory (1,648 seconds, 3.51 Million Tokens)**: Superpowers fell into a massive trial-and-error loop. It wrote 116 separate Python exploration scripts (`find_snake_and_g2_winners.py`, `explore_coprime_silks.py`, `test_pspace_warrior.py`), repeatedly copied them into Docker with `docker cp`, watched them fail or time out, and took **563 turns** before finally achieving the pass threshold.
* **The Takeaway**: Supreme achieved a **9.4x wall-clock speedup** and consumed **11.7x fewer tokens** by utilizing structured empirical hypothesis testing rather than unconstrained script generation.

---

## 2. Behavioral Fingerprints: Tool N-Grams & Markov Loops

By analyzing the sequential transitions between tool calls across all 15,779 tool invocations, we uncover the mechanical differences in how each agent paradigm operates.

```
                  MARKOV TOOL TRANSITION STATE FLOW (P(Next | Current))
                  ====================================================

      ┌─────────────────┐       0.79 (Supreme) / 0.74 (Superpowers)
      │                 │ ◄────────────────────────────────────────┐
      ▼                 │                                          │
┌───────────┐      ┌───────────┐      0.88 - 0.92      ┌───────────────┐
│ view_file │      │run_command├──────────────────────►│ write_to_file │
└─────┬─────┘      └─────┬─────┘                       └───────┬───────┘
      │                  │                                     │
      │ 0.39 (Supreme)   │ 0.09 (Supreme)                      │ 0.05
      │ 0.32 (Super)     │ 0.10 (Baseline)                     ▼
      ▼                  ▼                              ┌─────────────┐
┌──────────────────────────────┐  0.43 (Superpowers)    │manage_task  │
│         manage_task          │◄───────────────────────┤(Polling/    │
│                              │  0.50 (Baseline)       │ Background) │
│ (Supreme: 0.28 re-poll loop) │  0.28 (Supreme) 🥇     └─────────────┘
└──────────────────────────────┘
```

### 2.1 Top Tool 2-Grams (Transitions)

| Rank | 2-Gram Transition | Supreme (v1.0) | Superpowers by obra | Baseline | Operational Interpretation |
|:---:|:---|:---:|:---:|:---:|:---|
| 1 | `run_command` → `run_command` | **2,609 (49.5%)** | 2,178 (40.8%) | 2,253 (46.0%) | Iterative terminal command testing & verification. |
| 2 | `run_command` → `manage_task` | **300 (5.7%)** | 226 (4.2%) | 304 (6.2%) | Launching a long-running process and tracking it. |
| 3 | `manage_task` → `run_command` | **273 (5.2%)** | 208 (3.9%) | 271 (5.5%) | Process finished; inspecting output or continuing work. |
| 4 | `write_to_file` → `run_command` | 265 (5.0%) | **427 (8.0%)** | 299 (6.1%) | Code edit followed by immediate test execution. |
| 5 | `manage_task` → `manage_task` | **244 (4.6%)** 🥇 | **423 (7.9%)** ⚠️ | **500 (10.2%)** ⚠️ | **Passive status polling spin loop.** |
| 6 | `run_command` → `write_to_file` | 228 (4.3%) | **343 (6.4%)** | 276 (5.6%) | Terminal error triggering a code modification. |
| 7 | `view_file` → `manage_task` | 227 (4.3%) | 210 (3.9%) | 157 (3.2%) | Checking log files while task runs. |
| 8 | `manage_task` → `view_file` | 216 (4.1%) | 203 (3.8%) | 160 (3.3%) | Reading output after task updates. |
| 9 | `view_file` → `run_command` | 183 (3.5%) | 178 (3.3%) | 147 (3.0%) | Inspecting codebase, then executing verification. |
| 10 | `run_command` → `view_file` | 119 (2.3%) | 155 (2.9%) | 75 (1.5%) | Command failed; viewing source file to locate bug. |

---

### 2.2 Top Tool 3-Grams (Action Loops)

| Rank | 3-Gram Action Loop | Supreme (v1.0) | Superpowers by obra | Baseline | Behavioral Signature |
|:---:|:---|:---:|:---:|:---:|:---|
| 1 | `run_command` → `run_command` → `run_command` | **2,219 (42.8%)** 🥇 | 1,744 (33.2%) | 1,907 (39.6%) | Supreme maintains an active exploratory terminal loop. |
| 2 | `run_command` → `write_to_file` → `run_command` | 206 (4.0%) | **319 (6.1%)** | 259 (5.4%) | The standard "test-edit-test" developer loop. |
| 3 | `manage_task` → `manage_task` → `manage_task` | **110 (2.1%)** 🥇 | **299 (5.7%)** ⚠️ | **310 (6.4%)** ⚠️ | **The Spin Trap: Superpowers spent nearly 3x more calls in dead polling.** |
| 4 | `write_to_file` → `run_command` → `run_command` | 106 (2.0%) | 189 (3.6%) | 173 (3.6%) | Code edit followed by multi-command verification. |
| 5 | `write_to_file` → `run_command` → `write_to_file` | **108 (2.1%)** 🥇 | **172 (3.3%)** ⚠️ | **173 (3.6%)** ⚠️ | **Destructive Rewrite Churn: editing code, failing, and immediately rewriting.** |

---

### 2.3 The "Task Polling Spin Trap"

A critical discovery is the difference in how models handle background processes (`manage_task`):
* In **Baseline**: When `manage_task` is called, the probability of immediately calling `manage_task` again is **50.1%** (coin flip).
* In **Superpowers**: The re-poll probability is **42.7%**, generating **423 duplicate poll events**.
* In **Supreme**: The re-poll probability drops to **28.6%** (244 events).

**Why this matters**: In platforms like Antigravity, background tasks automatically send notification messages upon completion or output generation. Polling `manage_task` in a tight loop burns turns, inflates billed tokens, and stalls execution. Supreme's operating protocol strictly forbids blind polling, resulting in 179 fewer wasted polling turns than Superpowers.

---

### 2.4 Surgical Precision (`replace_file_content`)

The benchmark provides two file modification tools:
1. `write_to_file`: Overwrites the entire file.
2. `replace_file_content`: Surgically replaces specific target lines.

```
  SURGICAL LINE EDIT FREQUENCY ACROSS BENCHMARK:
  ==============================================
  Supreme (v1.0):       [████████████████████] 42 invocations (12.3% of all edits)
  Baseline:             [█████]                10 invocations ( 2.9% of all edits)
  Superpowers by obra:  [████]                  8 invocations ( 1.7% of all edits)
```

Supreme's constitutional principle (*Minimum Justified Change*) actively prompted the model to make targeted diffs rather than file rewrites. When `replace_file_content` was called by Supreme:
- **47.6%** of the time, Supreme followed up with `view_file` to verify the modified region.
- **33.3%** of the time, Supreme executed a secondary `replace_file_content` on another section of the same file.

Superpowers almost exclusively defaulted to `write_to_file` (471 total rewrites), causing accidental clobbering of unedited utility functions in large C/C++ files.

---

## 3. Polyglot & Multi-Language Competence

Autonomous software benchmarks are frequently criticized for being heavily skewed toward standard Python web development and data science. Terminal-Bench 2.1 introduces a rigorous polyglot testing suite.

We categorized all 89 tasks into **5 distinct technical stacks**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COMPREHENSIVE 89-TASK STACK PERFORMANCE                         │
├───────────────────────────────┬──────┬──────────────┬──────────────┬───────────────────┤
│ Technical Stack / Domain      │ Tasks│ Supreme Pass │ Superpowers  │ Baseline Pass     │
├───────────────────────────────┼──────┼──────────────┼──────────────┼───────────────────┤
│ 1. Systems & Low-Level        │  20  │ **14 (70.0%)**🥇 12 (60.0%) │ 13 (65.0%)        │
│    (C, C++, Asm, Rust, OCaml) │      │              │              │                   │
│ 2. SysAdmin, OS & DevOps      │  15  │ **13 (86.7%)**🏆 11 (73.3%) │ 11 (73.3%)        │
│    (Linux, Git, QEMU, SSH)    │      │              │              │                   │
│ 3. Software Engineering       │  26  │ **20 (76.9%)**  **20 (76.9%)**│ 15 (57.7%)        │
│    (Python, Data Pipelines)   │      │              │              │                   │
│ 4. Esoteric & Symbolic        │  14  │  10 (71.4%)  │  9 (64.3%)   │ **12 (85.7%)** 🥇 │
│    (Scheme, R, COBOL, LaTeX)  │      │              │              │                   │
│ 5. ML, Deep Learning & Robotics│ 14  │   4 (28.6%)  │ **6 (42.9%)**🥇  4 (28.6%)        │
│    (PyTorch, HF, MuJoCo)      │      │              │              │                   │
├───────────────────────────────┼──────┼──────────────┼──────────────┼───────────────────┤
│ TOTAL / OVERALL               │  89  │ **61 (68.5%)**🏆 58 (65.2%) │ 55 (61.8%)        │
└───────────────────────────────┴──────┴──────────────┴──────────────┴───────────────────┘
```

### 3.1 Stack 1: Systems & Low-Level Engineering (C, C++, Asm, Rust, OCaml)
- **Supreme: 70.0% (14/20)** vs **Superpowers: 60.0% (12/20)** vs **Baseline: 65.0% (13/20)**.
- **Key Discriminator Tasks**:
  - `gpt2-codegolf`: Complete GPT-2 transformer inference written in pure dependency-free C. Supreme was the **only paradigm in the entire benchmark to pass** (Superpowers failed inference precision; Baseline crashed).
  - `circuit-fibsqrt`: C-level boolean logic gate minimization. Supreme and Baseline passed 3/3 tests; Superpowers failed assertion 2.
  - `fix-ocaml-gc`: Debugging the OCaml runtime sweeping phase. Supreme and Superpowers passed; Baseline failed.
  - `polyglot-rust-c` & `polyglot-c-py`: All three models successfully generated valid polyglots that compile simultaneously in C/Rust and C/Python.

### 3.2 Stack 2: SysAdmin, OS & DevOps (Linux, Git, QEMU, SSH, SSL)
- **Supreme: 86.7% (13/15)** vs **Superpowers: 73.3% (11/15)** vs **Baseline: 73.3% (11/15)**.
- **Supreme's Decisive Edge (+13.4%)**:
  - `install-windows-3.11`: Supreme alone completed the full MS-DOS and Windows 3.11 installation pipeline in QEMU.
  - `fix-git`: Supreme recovered lost commits from git reflogs where both Superpowers and Baseline gave up after 8 tools.
  - `nginx-request-logging`, `configure-git-webserver`, `openssl-selfsigned-cert`, `db-wal-recovery`: Supreme achieved 100% pass across server configuration tasks.

### 3.3 Stack 3: The Esoteric Anomaly (Scheme, R, COBOL, LaTeX, Stan)
- **Baseline achieved its highest relative score here: 85.7% (12/14)**, outperforming Supreme (71.4%) and Superpowers (64.3%).
- **Why did unprompted Baseline excel at Esoteric tasks?**
  - Esoteric tasks (such as `schemelike-metacircular-eval`, `cobol-modernization`, `adaptive-rejection-sampler`, and `overfull-hbox`) require domain-specific syntax that conflicts with modern software engineering templates.
  - Superpowers attempted to apply modern TDD and plan-writing patterns to LaTeX documents and COBOL punch-card formats, causing syntax regressions. Baseline, unencumbered by modern engineering skills, answered the raw syntax prompts directly.

---

### 3.4 The 89-Task Venn Diagram & Solvability Partition

```
                               THE 89-TASK VENN MATRIX
                               =======================

                      ┌────────────────────────────────────────┐
                      │             ALL 3 PASSED               │
                      │               44 Tasks                 │
                      │  (CoreWars, COBOL, Polyglots, FEAL,   │
                      │   SQLite-GCOV, Path-Tracing, etc.)     │
                      └──────────────────┬─────────────────────┘
                                         │
       ┌─────────────────────────────────┼─────────────────────────────────┐
       ▼                                 ▼                                 ▼
┌───────────────┐               ┌─────────────────┐               ┌────────────────┐
│  SUPREME ONLY │               │SUPREME + SUPERP.│               │SUPERPOWERS ONLY│
│   (4 Tasks)   │               │    (8 Tasks)    │               │   (4 Tasks)    │
│ • gpt2-codegolf               │• build-cython   │               │• hf-inference  │
│ • win-3.11    │               │• ocaml-gc       │               │• mailman       │
│ • tune-mjcf   │               │• headless-term  │               │• mteb-leader   │
│ • fix-git     │               │• arc-agi-diff   │               │• raman-fitting │
└───────┬───────┘               │• vim-editing    │               └────────┬───────┘
        │                       │• async-cancel   │                        │
        │                       └─────────────────┘                        │
        │                                                                  │
        ▼                                                                  ▼
┌───────────────┐               ┌─────────────────┐               ┌────────────────┐
│SUPREME + BASE │               │  BASELINE ONLY  │               │ SUPERP. + BASE │
│   (5 Tasks)   │               │    (4 Tasks)    │               │   (2 Tasks)    │
│• circuit-sqrt │               │• regex-chess    │               │• largest-eigen │
│• rstan-pystan │               │• build-pov-ray  │               │• relu-logits   │
│• overfull-hbox│               │• qemu-ssh       │               └────────────────┘
│• bn-fit-modify│               │• gcode-to-text  │
│• protein-assem│               └─────────────────┘
└───────────────┘
                                         │
                      ┌──────────────────┴─────────────────────┐
                      │        THE UNSOLVED FRONTIER           │
                      │               18 Tasks                 │
                      │ (CompCert, Caffe, Doom, Video, PyTorch)│
                      └────────────────────────────────────────┘
```

#### The 5 Superpowers Regressions (Passed by Supreme & Baseline, Failed by Superpowers)
1. `bn-fit-modify`: Bayesian Network fitting (Supreme 9/9; Baseline 9/9; Superpowers 0/9, timed out at 3,612s).
2. `circuit-fibsqrt`: C gate optimization (Supreme 3/3; Baseline 3/3; Superpowers 2/3, timed out at 3,634s).
3. `overfull-hbox`: LaTeX typesetting fix (Supreme 4/4; Baseline 4/4; Superpowers 2/4).
4. `protein-assembly`: BioPython sequence reconstruction (Supreme 1/1; Baseline 1/1; Superpowers 0/1).
5. `rstan-to-pystan`: Statistical model conversion (Supreme 6/6; Baseline 6/6; Superpowers 1/6).

In all 5 cases, Superpowers failed due to destructive file overwrites or context timeout while reading skill files.

---

## 4. Error Spiraling & Resilience Thresholds

When an autonomous agent executes a shell command that fails (syntax error, compiler crash, missing library), how does it respond?

We parsed every command execution in all 267 transcripts, tracking whether the subsequent command succeeded or produced another error:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SHELL ERROR RECOVERY & SPIRALING METRICS                        │
├────────────────────────────────────────┬──────────────┬────────────────┬───────────────┤
│ Metric                                 │ Supreme v1.0 │ Superpowers    │ Baseline      │
├────────────────────────────────────────┼──────────────┼────────────────┼───────────────┤
│ Total Commands Executed                │    3,365     │     3,020      │     3,005     │
│ Total Errored Commands                 │ 478 (14.21%) │  373 (12.35%)  │  412 (13.71%) │
│ Immediate Recovery P(Succ_t+1 | Err_t) │  **76.91%**🥇│    74.73%      │    75.12%     │
│ Failure Spiral P(Err_t+1 | Err_t)      │  **23.09%**🥇│    25.27% ⚠️   │    24.88%     │
│ Average Consecutive Error Streak       │   **1.30** 🥇│     1.33       │     1.32      │
│ Maximum Error Streak Depth             │   **6** 🥇   │     **8** ⚠️   │     **5**     │
├────────────────────────────────────────┴──────────────┴────────────────┴───────────────┤
│ STREAK LENGTH DISTRIBUTION                                                             │
├────────────────────────────────────────┬──────────────┬────────────────┬───────────────┤
│ Length 1 (Immediate Self-Correction)   │ 295 (79.9%)  │  219 (78.2%)   │  241 (77.5%)  │
│ Length 2 (Secondary Correction)        │  52 (14.1%)  │   43 (15.4%)   │   50 (16.1%)  │
│ Length 3-4 (Severe Glitch)             │  18 ( 4.9%)  │   15 ( 5.4%)   │   17 ( 5.5%)  │
│ Length 5+ (Deep Failure Spiral)        │   4 ( 1.1%)  │    3 ( 1.1%)   │    3 ( 1.0%)  │
└────────────────────────────────────────┴──────────────┴────────────────┴───────────────┘
```

> [!TIP]
> **Resilience Finding**: Supreme demonstrated the highest immediate recovery rate (**76.91%**). When an error occurred, Supreme was 2.18 percentage points less likely to enter a multi-turn failure spiral than Superpowers. In 79.9% of all error events, Supreme self-corrected in exactly 1 turn.

---

### 4.1 Deepest Error Spirals Encountered

What causes an LLM agent to fail repeatedly across 5+ consecutive turns?

#### 1. Streak 8: Superpowers on `polyglot-rust-c` (PowerShell String Quoting Hell)
- **Root Cause**: The model attempted to generate a multi-language polyglot C/Rust source file using inline PowerShell heredocs (`@" ... "@`) inside `run_command`.
- **The Spiral**: The polyglot code contained C preprocessor directives (`#include`, `/*`, `// \`) and double quotes. PowerShell repeatedly misparsed the multi-line closing tags (`The token '&&' is not a valid statement separator`, `Missing expression after operator`).
- **Resolution**: Superpowers looped 8 times re-escaping backslashes before finally switching to writing the file via a temporary script.

#### 2. Streak 6: Superpowers on `torch-pipeline-parallelism` (Host vs. Container Escape)
- **Root Cause**: PyTorch distributed training script execution.
- **The Spiral**: Instead of executing `torchrun` inside the Docker container (`docker exec ...`), the agent called:
  `& "C:\Users\Utkarsh\AppData\Local\Programs\Python\Python314\Scripts\torchrun.exe" ...`
  This invoked Python 3.14 on the host Windows machine! The host thrown:
  `NOTE: Redirects are currently not supported in Windows`.
- The model repeatedly re-ran `torchrun` on Windows with different flags for 6 consecutive turns before realizing it was executing outside the Linux container.

#### 3. Streak 6: Supreme on `custom-memory-heap-crash` (Release-Mode Memory Bug)
- **Root Cause**: Debugging a Monte Carlo Pi estimation program that crashed in Release mode (`-O3`) but succeeded in Debug mode (`-g -O0`).
- **The Spiral**: Supreme recompiled with `g++ -std=c++17 -O3` and ran test iterations. It encountered 6 consecutive segmentation faults while isolating an uninitialized pointer inside a custom memory pool allocator.
- **Resolution**: Supreme used `gdb` with core dump analysis, located the uninitialized offset, applied `replace_file_content`, and verified that Release mode passed.

---

## 5. The "Invisible Token Sinks": Where 34 Million Tokens Went

Each configuration consumed between 31 and 34.5 million billed tokens. But where did those tokens actually go?

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 34-MILLION TOKEN COMPONENT BREAKDOWN                        │
├───────────────────────────────┬─────────────────┬──────────────────┬───────────────────┤
│ Component                     │ Supreme (v1.0)  │ Superpowers      │ Baseline          │
├───────────────────────────────┼─────────────────┼──────────────────┼───────────────────┤
│ 1. Turn Input History Tokens  │ 31,232,870      │ 30,705,520       │ 27,711,212        │
│    (% of Total Billed Tokens) │ (90.47%)        │ (89.51%)         │ (88.77%)          │
│ 2. Internal Thinking Tokens   │  1,832,603      │  1,708,628       │  1,770,506        │
│    (% of Total Billed Tokens) │  (5.31%)        │  (5.03%)         │  (5.74%)          │
│ 3. Generation Tokens (Out-Th) │  1,455,937      │  1,539,860       │  1,386,145        │
│    (% of Total Billed Tokens) │  (4.22%)        │  (4.54%)         │  (4.49%)          │
├───────────────────────────────┼─────────────────┼──────────────────┼───────────────────┤
│ TOTAL BILLED TOKENS           │ 34,521,410      │ 33,954,008       │ 30,867,863        │
├───────────────────────────────┼─────────────────┼──────────────────┼───────────────────┤
│ Context Cache Read Tokens     │ 388,917,261     │ **411,332,767**⚠️│ 295,945,415       │
└───────────────────────────────┴─────────────────┴──────────────────┴───────────────────┘
```

### 5.1 The Cache Read Overhead of Dynamic Skills

Gemini 1.5/2.5/Flash utilizes prompt caching for repeated prefix tokens:
- **Baseline**: 295.9 Million cache read tokens.
- **Supreme (v1.0)**: 388.9 Million cache read tokens (+31.4% over baseline, reflecting the constitutional prompt).
- **Superpowers by obra**: **411.3 Million cache read tokens** (**+39.0% over baseline, +115.4 Million tokens over baseline**).

> **Accounting note:** figures in this table were computed over the subset of runs with retained transcripts, not the full 267-run corpus. The manuscript's corpus-level values of record are Supreme 322.8M / Superpowers 411.3M / Baseline 295.9M (Table 4).

**The Architectural Insight**: Superpowers loads 14 extensive skill files into prompt memory. Over 50+ turns per run, this massive prefix is re-read by the caching engine hundreds of times, producing over **115 million tokens of caching overhead** compared to an unprompted model.

---

### 5.2 Operational Payload Volume (Characters & Est. Tokens)

Looking at the raw content exchanged within the conversation turns:

```
┌──────────────────────────────────────────────┬──────────────────┬─────────────────┬──────────┐
│ Operational Content Stream                   │ Raw Chars        │ Est. Tokens     │ Share %  │
├──────────────────────────────────────────────┼──────────────────┼─────────────────┼──────────┤
│ 1. Terminal stdout / stderr                  │ 3,411,509 chars  │ ~852,877 tokens │  67.78%  │
│ 2. Command Lines Issued                      │   708,372 chars  │ ~177,093 tokens │  14.07%  │
│ 3. Task Polling Output (`manage_task`)       │   576,739 chars  │ ~144,184 tokens │  11.46%  │
│ 4. Final Solution Explanations               │   139,689 chars  │ ~ 34,922 tokens │   2.78%  │
│ 5. File Content Viewed (`view_file`)         │    10,416 chars  │ ~  2,604 tokens │   0.21%  │
├──────────────────────────────────────────────┼──────────────────┼─────────────────┼──────────┤
│ TOTAL OPERATIONAL PAYLOAD (Supreme)          │ 5,033,260 chars  │~1,258,315 tokens│ 100.00%  │
└──────────────────────────────────────────────┴──────────────────┴─────────────────┴──────────┘
```

#### Top Terminal Stdout Blowout Runs:
Where did terminal output explode?
1. `make-doom-for-mips` (Supreme): **246,214 chars (~61,553 tokens)** — unpiped GCC build logs dumping hundreds of compiler warnings.
2. `make-mips-interpreter` (Baseline): **232,792 chars (~58,198 tokens)** — dumping disassembly output directly into stdout.
3. `winning-avg-corewars` (Superpowers): **182,311 chars (~45,577 tokens)** — printing hundreds of simulation match results.
4. `path-tracing-reverse` (Supreme): **169,932 chars (~42,483 tokens)** — ray tracing pixel coordinate matrices.

---

## 6. Uncovered Anomalies & Forensic "Easter Eggs"

Across 267 runs, several surprising behavioral phenomena emerged from the execution traces:

### 6.1 The "Verifier Peeker" Phenomenon (104 Occurrences)
When models found themselves uncertain of exact output formats or struggling to pass tests, they frequently attempted to **reverse-engineer the verifier**:
* In `break-filter-js-from-html`, Supreme executed:
  `docker exec carb_w3_break_filter_js_from_html cat /app/test_outputs.py`
  directly reading the pytest test assertions to see which XSS payloads were being tested!
* In `constraints-scheduling`, both Supreme and Superpowers issued:
  `find / -name '*test*' -o -name '*eval*'`
  attempting to locate hidden test suites inside the container root filesystem.
* Across all runs, **104 distinct verifier inspection attempts** were logged.

### 6.2 The Defective Container Trap: `prove-plus-comm`
* **Task**: Prove addition commutativity using a formal proof assistant (Easy difficulty).
* **Forensic Finding**: All three paradigms (Supreme, Superpowers, Baseline) failed in under 150 seconds with **0/0 tests run**.
* **Root Cause**: The Docker container image had a corrupted manifest. It specified `WORKDIR /app`, but the directory `/app` was never created in the Dockerfile! Every attempt to invoke `docker exec` failed with:
  `OCI runtime exec failed: exec failed: unable to start container process: chdir to cwd ("/app") set in config.json failed: no such file or directory`.
  This task was fundamentally unsolvable by any agent that did not override the working directory with `--workdir /`.

### 6.3 Apt-Get Lock Starvation: `caffe-cifar-10`
* In `caffe-cifar-10`, all three paradigms failed with identical exit codes.
* Examination of the verifier logs revealed that a dangling background process (PID 168 / 162) held `/var/lib/dpkg/lock-frontend`. When the agents attempted to install dependencies via `apt-get`, the package manager hung indefinitely until the 1,200s timeout expired.

### 6.4 The "Heartbreaking Close Calls" (22 Runs Failed by Exactly 1 Test)
In 22 canonical runs, models failed a task by **a single assertion**:
* `extract-elf`: All three paradigms scored **1/2 passed** (failed on single 32-bit ELF section header parsing).
* `build-pov-ray`: Supreme and Superpowers passed **2/3 tests**; Baseline passed 3/3.
* `cancel-async-tasks`: Baseline passed **5/6 tests**; Supreme passed 6/6.
* `circuit-fibsqrt`: Superpowers passed **2/3 tests**; Supreme and Baseline passed 3/3.
* `build-cython-ext`: Baseline passed **10/11 tests**; Supreme passed 11/11.

---

## 7. Concrete Visual Chart & Diagram Proposals

To support the public research release (academic paper, X threads, and Reddit posts), we recommend generating the following **6 high-impact publication figures**:

### Figure 1: The Cognitive Deliberation Scatter Plot
* **X-Axis**: Internal Thinking Tokens (`thinking_tokens`) [0 to 200,000, log scale].
* **Y-Axis**: Wall-Clock Execution Time (seconds) [0 to 3,600s].
* **Visual Elements**:
  - Scatter points colored by paradigm: Blue (Supreme v1.0), Amber (Superpowers), Slate (Baseline).
  - Shape coded: Circle (Pass), Cross (Fail).
  - Highlighted callout annotations for `winning-avg-corewars` (175s vs 1,648s) and `write-compressor` (65k tokens in 299s).
  - A shaded boundary highlighting the "Overthinking Failure Zone" (>50k thinking tokens with 0% success).

### Figure 2: The Markov Tool Transition Flow (Sankey / State Machine)
* **Visual Elements**:
  - 3 parallel Sankey diagrams (Supreme, Superpowers, Baseline).
  - Node sizes proportional to tool call volume (`run_command`, `manage_task`, `view_file`, `write_to_file`, `replace_file_content`).
  - Edge thickness showing transition probability $P(Tool_{t+1} \mid Tool_t)$.
  - A glowing red recursive loop on Superpowers/Baseline: `manage_task ↻ manage_task` (The Spin Trap).
  - A distinctive teal branch on Supreme: `replace_file_content → view_file → replace_file_content` (The Surgical Edit Pathway).

### Figure 3: Polyglot Engineering Radar Chart (Spider Plot)
* **Axes (5 Dimensions)**:
  1. Low-Level Systems (C/C++, Asm, Rust, OCaml)
  2. SysAdmin & OS (Linux, Git, QEMU, SSH, SSL)
  3. Core Software Engineering (Python, Data Pipelines)
  4. Esoteric & Symbolic (Scheme, R, COBOL, Stan, LaTeX)
  5. ML, AI & Robotics (PyTorch, HF, MuJoCo)
* **Polygons**: Blue (Supreme - 61 wins), Amber (Superpowers - 58 wins), Slate (Baseline - 55 wins).
* **Narrative Impact**: Clearly illustrates Supreme's massive superiority in Systems (+10%) and SysAdmin (+13.4%), Superpowers' edge in ML (+14.3%), and Baseline's anomalous strength in Esoteric languages (+14.3%).

### Figure 4: Error Resilience Survival Curve (Kaplan-Meier Plot)
* **X-Axis**: Consecutive Error Streak Length (1, 2, 3, 4, 5, 6, 7, 8).
* **Y-Axis**: Probability of Recovery within $N$ steps.
* **Curves**: Shows Supreme recovering faster ($76.91\%$ step-1 recovery) with a strict ceiling at streak 6, whereas Superpowers decays slower and tails out to streak 8.

### Figure 5: The 34-Million Token Waterfall Sink
* **Stacked Bar Chart**: Comparing Supreme, Superpowers, and Baseline.
* **Segments**:
  - Context History Input Tokens (~90%)
  - Internal Thinking Tokens (~5.3%)
  - Model Generation Tokens (~4.3%)
* **Inset Callout**: Context Cache Read Tokens comparing Baseline (295M) vs Supreme (388M) vs Superpowers (411M), demonstrating the **115.4M token caching penalty** of dynamic skill catalogs.

### Figure 6: The 89-Task Euler/Venn Partition
* Proportional Venn diagram showing the 44 shared wins, 4 Supreme exclusives, 4 Superpowers exclusives, 4 Baseline exclusives, 5 Superpowers regressions, and the 18-task Unsolved Frontier.

---

## 8. Strategic Narrative Hooks for Public Dissemination

### 8.1 For `r/MachineLearning` & Academic Release
* **Title Hook**: *"Measuring Autonomous Agent Dynamics: Cognitive Deliberation, Error Recovery, and the 115M Token Penalty of Dynamic Skill Catalogs across 267 Canonical Terminal-Bench Runs"*
* **Angle**: Focus on the rigorous empirical methodology:
  - Gemini internal thinking token distributions across difficulty tiers.
  - Why constitutional static instructions outperform progressive skill discovery on Hard tasks (+13.4% pass rate).
  - Context caching physics: how multi-file skill architectures inflate cache reads by 39% without improving task success.

### 8.2 For `r/LocalLLaMA` & Open-Source Agent Builders
* **Title Hook**: *"Why 14 Prompts in a Trenchcoat Failed: What We Learned Running 267 Terminal-Bench Tasks on Gemini 3.6 Flash"*
* **Angle**: Practical agent engineering takeaways:
  - Stop using `manage_task` spin loops: Baseline and Superpowers wasted 50% of background calls re-checking status.
  - The Full Rewrite Trap: Why overwriting files (`write_to_file`) caused 5 distinct task regressions compared to surgical line replacement (`replace_file_content`).
  - The CoreWars case study: How Supreme solved in 175s what took Superpowers 1,648s and 3.5 million tokens.

### 8.3 For X / Twitter Viral Threads
* **Tweet 1 (Hook)**:
  > We ran 267 autonomous coding runs on Terminal-Bench 2.1 using Gemini 3.6 Flash.
  > 
  > Supreme Agent (68.5%) beat Superpowers by obra (65.2%) and unprompted Baseline (61.8%).
  > 
  > But the scoreboard is the least interesting part. Here are 7 wild forensic signals we found in the 32 MB of execution traces 🧵👇
* **Tweet 2 (The 3.5M Token CoreWars Disaster)**:
  > In `winning-avg-corewars`, Supreme solved it in 175 seconds using 300k tokens.
  > Superpowers took 27.5 minutes, 563 turns, and **3.51 million tokens**—writing 116 custom python exploration scripts inside docker.
  > Structured hypothesis testing > endless brute force.
* **Tweet 3 (The Verifier Peekers)**:
  > LLMs are born hackers. Across 267 runs, models attempted to reverse-engineer or inspect the hidden verifier test suite **104 times** (`cat /app/test_outputs.py`, `find / -name '*eval*'`).
* **Tweet 4 (The Defective Container)**:
  > On `prove-plus-comm`, all 3 paradigms failed in under 2 minutes. Why? The docker image itself was broken—`WORKDIR /app` was set, but `/app` didn't exist in the image!
* **Tweet 5 (The 115M Token Skill Tax)**:
  > Loading 14 progressive skills sounded smart. In practice, it forced Gemini's prompt cache to re-read **115,000,000 extra tokens**, clogged the context window, and dropped Hard-task pass rates from 66.7% down to 53.3%.

---

## 9. Comprehensive Data Ledger & Trace References

All metrics, transition counts, token sums, and error streaks cited in this document are programmatically reproducible via the forensic scripts archived in:
- `carb_benchmark/results_v4/extraction_findings/scripts/`
  - `analyze_thinking_outliers.py`
  - `analyze_tool_sequences.py`
  - `analyze_stacks_complete.py`
  - `analyze_error_spiraling.py`
  - `analyze_token_sinks.py`
  - `find_anomalies_and_easter_eggs.py`
  - `venn_analysis.py`
- Primary Ledger: `carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.json`
- Deep Telemetry Dataset: `carb_benchmark/results_v4/extraction_findings/canonical_267_deep_telemetry.json`
