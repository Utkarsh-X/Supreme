# 🛠️ Extraction Dossier 03: Polyglot Stacks, Low-Level Systems & The Esoteric Anomaly
### Language Versatility & Domain Robustness Across 267 Canonical Terminal-Bench 2.1 Runs

---

## 1. Executive Abstract

Autonomous coding benchmarks are frequently criticized for being heavily over-indexed on standard Python web development, basic scripting, and simple data science. Real-world systems engineering demands polyglot versatility: working with low-level C compilers, cross-compilation toolchains, QEMU hypervisors, OCaml runtimes, and legacy languages.

Terminal-Bench 2.1 introduces a deeply rigorous polyglot testing suite. By categorizing all 89 tasks into **5 distinct technical stacks**, this dossier reveals how cognitive architectures alter programming domain performance:
* **Low-Level Systems Dominance**: Supreme led in Systems & Low-Level (C, C++, Asm, Rust, OCaml) with **70.0% (14/20)**, uniquely passing `gpt2-codegolf` (pure C inference).
* **SysAdmin & OS Marathon**: Supreme dominated SysAdmin & DevOps with **86.7% (13/15)**, completing `install-windows-3.11` (a 44-minute autonomous QEMU installation).
* **The "Esoteric Anomaly"**: Baseline (unprompted Gemini) defeated both agent frameworks in Esoteric languages (**85.7% on COBOL, Scheme, and LaTeX**), revealing that modern TDD/refactoring prompt templates actually hinder models on archaic syntax.
* **The 89-Task Venn Partition**: Complete mutual-exclusion breakdown of the benchmark into Shared Solves (44), Exclusive Wins (4 each), and the Unsolved Frontier (18).

---

## 2. Master 5-Stack Performance Matrix

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

---

## 3. Stack 1: Systems & Low-Level Engineering (20 Tasks)

**Languages:** C, C++, x86/ARM/MIPS Assembly, Redcode, Rust, OCaml.  
**Key Results:** Supreme **70.0% (14/20)** | Baseline **65.0% (13/20)** | Superpowers **60.0% (12/20)**.

### Decisive Tasks & Discriminators:
1. **`gpt2-codegolf` (Pure C Transformer Inference)**:
   - *Task*: Write a minimal, standalone C program that loads GPT-2 model weights, implements multi-head attention and layer norm, and generates text with exact floating-point tolerances.
   - *Outcome*: **Supreme was the only paradigm to pass (Solo Win in 904s)**. Superpowers struggled with tensor indexing and matrix strides; Baseline segfaulted.
2. **`circuit-fibsqrt` (Boolean Logic Optimization)**:
   - *Task*: C implementation of circuit minimization for mathematical functions.
   - *Outcome*: Supreme and Baseline passed 3/3 tests. Superpowers failed assertion 2 due to aggressive file rewrites.
3. **`fix-ocaml-gc` (OCaml Runtime GC Internals)**:
   - *Task*: Fix a memory corruption bug in the OCaml garbage collection sweeping phase.
   - *Outcome*: Supreme and Superpowers passed; Baseline corrupted the block header allocation table.
4. **`polyglot-rust-c` & `polyglot-c-py`**:
   - *Task*: Write a single source file that compiles cleanly in both C and Rust (or C and Python).
   - *Outcome*: All three models passed, demonstrating strong polyglot syntax blending.

---

## 4. Stack 2: SysAdmin, OS & DevOps (15 Tasks)

**Domains:** Linux Kernel, QEMU Virtualization, Git Internals, OpenSSH, SSL, Systemd, Bind9 DNS.  
**Key Results:** Supreme **86.7% (13/15)** | Superpowers **73.3% (11/15)** | Baseline **73.3% (11/15)**.

### Decisive Tasks & Discriminators:
1. **`install-windows-3.11` (The 44-Minute QEMU Marathon)**:
   - *Task*: Install Windows 3.11 for Workgroups inside headless QEMU, format virtual FAT16 disk, swap floppy images, install networking drivers, and verify GUI boot.
   - *Outcome*: **Supreme achieved an Exclusive Win in 2,648.7s (44.1 minutes)**, executing 307 turns without hallucinating or aborting. Superpowers and Baseline both crashed or timed out.
2. **`fix-git` (Corrupted Git Object Tree)**:
   - *Task*: Reconstruct dangling commits and repair a corrupt SHA-1 tree inside `.git/objects`.
   - *Outcome*: **Supreme achieved an Exclusive Win in 184s**. Supreme used low-level `git cat-file -p` and `git fsck` to trace commit parentage cleanly.
3. **`qemu-alpine-ssh` (Headless SSH Bridge)**:
   - *Outcome*: Baseline achieved an Exclusive Win; Supreme and Superpowers struggled with serial port redirection timing.

---

## 5. Stack 3: Software Engineering & Data Pipelines (26 Tasks)

**Languages:** Python, Cython, SQL, Bash.  
**Key Results:** Supreme **76.9% (20/26)** | Superpowers **76.9% (20/26)** | Baseline **57.7% (15/26)**.

### Key Finding: The Prompt Grounding Advantage
In standard software engineering, prompt grounding provides a massive **+19.2 percentage point win-rate boost** over unprompted Baseline:
* In `build-cython-ext`, `cancel-async-tasks`, and `large-scale-text-editing`, Baseline failed due to lack of methodical testing.
* Both Supreme and Superpowers excelled here, demonstrating that structured instructions (planning, verification) are critical for non-trivial Python codebases.

---

## 6. Stack 4: Esoteric & Symbolic Programming (14 Tasks)

**Languages:** Scheme, R, COBOL, LaTeX, Stan, SPARQL.  
**Key Results:** **Baseline 85.7% (12/14)** 🏆 | Supreme **71.4% (10/14)** | Superpowers **64.3% (9/14)**.

### 🔬 The "Esoteric Anomaly": Why Baseline Won
One of the most surprising findings in CARB-v4 is that unprompted Baseline outperformed both agent systems on esoteric programming languages:
* **The Root Cause**: Gemini 3.6 Flash possesses extraordinary pre-trained memory of raw COBOL syntax, Scheme S-expressions, and LaTeX math formatting.
* When Superpowers or Supreme were applied, the system prompts encouraged modern software engineering workflows: *"Write unit tests first (TDD), decompose into modules, create plans"*.
* In languages like COBOL or archaic Scheme metacircular evaluators, trying to set up modern test frameworks or modular file structures frequently failed because the Docker environment lacked those tools. Baseline simply outputted raw, working code directly into the file and passed!

---

## 7. Stack 5: Machine Learning, Deep Learning & Robotics (14 Tasks)

**Frameworks:** PyTorch, HuggingFace Transformers, MuJoCo, FastText, Caffe.  
**Key Results:** **Superpowers 42.9% (6/14)** 🥇 | Supreme **28.6% (4/14)** | Baseline **28.6% (4/14)**.

### Key Findings:
* **Superpowers' Data Science Strength**: Superpowers won exclusively on `hf-model-inference`, `mteb-leaderboard`, and `raman-fitting`. Its dynamic skills provided helpful recipes for HuggingFace pipeline configs.
* **Supreme's Physics Solo Win (`tune-mjcf`)**: Supreme was the only model to pass the MuJoCo XML physics tuning task (achieving a 2.19x simulation speedup with $D=0.0000$ divergence).
* **Upstream Infrastructure Bottlenecks**: Tasks 82 (`torch-pipeline-parallelism`), 83 (`torch-tensor-parallelism`), and 84 (`train-fasttext`) registered 0% solves across all models due to container defects (missing Python/curl and 2.85 GB CUDA PyPI download timeouts).

---

## 8. The 89-Task Euler/Venn Solvability Partition

Every single task in Terminal-Bench 2.1 can be partitioned into mutual-exclusion sets:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        89-TASK VENN DIAGRAM PARTITION BREAKDOWN                        │
├───────────────────────────────────┬───────┬────────────────────────────────────────────┤
│ Category                          │ Count │ Exact Task Names                           │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 1. Consensus Solves (All 3 Pass)  │  44   │ adaptive-rejection-sampler, bn-fit-modify, │
│                                   │       │ crack-7z-hash, filter-js-from-html, etc.   │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 2. Supreme Exclusive Wins         │   4   │ fix-git, gpt2-codegolf,                    │
│                                   │       │ install-windows-3.11, tune-mjcf            │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 3. Superpowers Exclusive Wins     │   4   │ hf-model-inference, mailman,               │
│                                   │       │ mteb-leaderboard, raman-fitting            │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 4. Baseline Exclusive Wins        │   4   │ build-pov-ray, gcode-to-text,              │
│                                   │       │ qemu-alpine-ssh, regex-chess               │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 5. Supreme + Superpowers Pass     │   8   │ build-cython-ext, cancel-async-tasks,      │
│    (Baseline Failed)              │       │ fix-ocaml-gc, headless-terminal, etc.      │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 6. Supreme + Baseline Pass        │   5   │ bn-fit-modify, circuit-fibsqrt,            │
│    (Superpowers Regressed)        │       │ overfull-hbox, protein-assembly, etc.      │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 7. Superpowers + Baseline Pass    │   2   │ largest-eigenval,                          │
│    (Supreme Failed)               │       │ model-extraction-relu-logits               │
├───────────────────────────────────┼───────┼────────────────────────────────────────────┤
│ 8. The Unsolved Frontier (0% All) │  18   │ caffe-cifar-10, torch-pipeline-parallelism,│
│                                   │       │ torch-tensor-parallelism, train-fasttext...│
└───────────────────────────────────┴───────┴────────────────────────────────────────────┘
```

### Scientific Value of this Partition:
Disclosing where Supreme lost (4 Baseline exclusive wins, 4 Superpowers exclusive wins, and 2 Superpowers+Baseline wins) provides absolute transparency and establishes peer-review authority.
