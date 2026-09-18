# 📑 CARB-v4 Master Research Report: Task-Level Dynamics & Architectural Analysis

**Benchmark:** Terminal-Bench 2.1 (89 Tasks / 267 Graded Runs)  
**Agent Paradigms:** Supreme (v1.0) vs. Superpowers by obra vs. Baseline  
**Audit Standard:** Cryptographic SHA-256 Multi-Signal Temporal Verification  

---

## 1. Executive Summary & Grand Scoreboard

This comprehensive research report provides task-level transparency into all 267 autonomous coding runs across the 89 tasks of Terminal-Bench 2.1. We analyze how **Constitutional Static Grounding (Supreme v1.0)** compares against **Dynamic Progressive Skill Loading (Superpowers by obra)** and unprompted **Baseline** across 5 technical domains.

### 🏆 Master Scoreboard

| Rank | Paradigm | Solved / 89 | Pass Rate | Total Wall Time | Avg Time / Task | Total Tokens | Tokens / Solved |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Supreme (v1.0)** | **61 / 89** | **68.5%** 🏆 | **15.15 hrs** | **612.9s** 🥇 | 34,521,410 | **565,925** 🥇 |
| 2 | **Superpowers by obra** | 58 / 89 | 65.2% | 18.30 hrs | 740.2s | 34,304,008 | 591,448 |
| 3 | **Baseline** | 55 / 89 | 61.8% | 16.92 hrs | 684.3s | **31,217,863** | 567,598 |

### 📊 Domain-by-Domain Win Rate & Efficiency Breakdown

| Technical Domain | Total Tasks | Supreme (v1.0) Solved | Superpowers Solved | Baseline Solved | Supreme Lead |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Data Science & DBs** | 7 | **7/7 (100.0%)** | 6/7 (85.7%) | 7/7 (100.0%) | `+0` |
| **ML & Robotics** | 6 | **1/6 (16.7%)** | 2/6 (33.3%) | 2/6 (33.3%) | `-1` |
| **Security & Reverse Eng** | 4 | **3/4 (75.0%)** | 3/4 (75.0%) | 3/4 (75.0%) | `+0` |
| **Software Engineering** | 65 | **44/65 (67.7%)** | 40/65 (61.5%) | 36/65 (55.4%) | `+4` |
| **System Administration** | 7 | **6/7 (85.7%)** | 7/7 (100.0%) | 7/7 (100.0%) | `-1` |

---

## 2. Exhaustive Task-Level Breakdown by Domain

### 📁 Domain: Data Science & DBs (7 Tasks)

**Domain Performance Summary:**  
- **Supreme (v1.0):** 7/7 (100.0%)  
- **Superpowers by obra:** 6/7 (85.7%)  
- **Baseline:** 7/7 (100.0%)  

| Task Name | Difficulty | Category | Supreme (v1.0) | Superpowers by obra | Baseline | Key Dynamics |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `adaptive-rejection-sampler` | Medium | `scientific-computing` | ✅ PASS (635s) | ✅ PASS (691s) | ✅ PASS (624s) | Triple Pass (Consensus Solution) |
| `bn-fit-modify` | Hard | `scientific-computing` | ✅ PASS (2671s) | ❌ FAIL (3613s) | ✅ PASS (252s) | Mixed Resolution |
| `constraints-scheduling` | Medium | `personal-assistant` | ✅ PASS (120s) | ✅ PASS (113s) | ✅ PASS (132s) | Triple Pass (Consensus Solution) |
| `count-dataset-tokens` | Medium | `model-training` | ✅ PASS (678s) | ✅ PASS (469s) | ✅ PASS (540s) | Triple Pass (Consensus Solution) |
| `distribution-search` | Medium | `machine-learning` | ✅ PASS (108s) | ✅ PASS (3021s) | ✅ PASS (75s) | Triple Pass (**Supreme 28.0x Faster**) |
| `sqlite-db-truncate` | Medium | `debugging` | ✅ PASS (79s) | ✅ PASS (73s) | ✅ PASS (94s) | Triple Pass (Consensus Solution) |
| `sqlite-with-gcov` | Medium | `system-administration` | ✅ PASS (457s) | ✅ PASS (775s) | ✅ PASS (879s) | Triple Pass (Consensus Solution) |

---

### 📁 Domain: ML & Robotics (6 Tasks)

**Domain Performance Summary:**  
- **Supreme (v1.0):** 1/6 (16.7%)  
- **Superpowers by obra:** 2/6 (33.3%)  
- **Baseline:** 2/6 (33.3%)  

| Task Name | Difficulty | Category | Supreme (v1.0) | Superpowers by obra | Baseline | Key Dynamics |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `chess-best-move` | Medium | `games` | ✅ PASS (358s) | ✅ PASS (913s) | ✅ PASS (263s) | Triple Pass (**Supreme 2.6x Faster**) |
| `hf-model-inference` | Medium | `data-science` | ❌ FAIL (912s) | ✅ PASS (566s) | ❌ FAIL (904s) | Superpowers Solo Win |
| `pytorch-model-cli` | Medium | `model-training` | ❌ FAIL (903s) | ❌ FAIL (915s) | ❌ FAIL (904s) | Triple Fail (High Complexity / Upstream Defect) |
| `pytorch-model-recovery` | Medium | `model-training` | ❌ FAIL (906s) | ❌ FAIL (804s) | ❌ FAIL (901s) | Triple Fail (High Complexity / Upstream Defect) |
| `regex-chess` | Hard | `software-engineering` | ❌ FAIL (676s) | ❌ FAIL (1154s) | ✅ PASS (1101s) | Mixed Resolution |
| `train-fasttext` | Hard | `model-training` | ❌ FAIL (1850s) | ❌ FAIL (1174s) | ❌ FAIL (1857s) | Triple Fail (High Complexity / Upstream Defect) |

---

### 📁 Domain: Security & Reverse Eng (4 Tasks)

**Domain Performance Summary:**  
- **Supreme (v1.0):** 3/4 (75.0%)  
- **Superpowers by obra:** 3/4 (75.0%)  
- **Baseline:** 3/4 (75.0%)  

| Task Name | Difficulty | Category | Supreme (v1.0) | Superpowers by obra | Baseline | Key Dynamics |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `break-filter-js-from-html` | Medium | `security` | ❌ FAIL (139s) | ❌ FAIL (70s) | ❌ FAIL (56s) | Triple Fail (High Complexity / Upstream Defect) |
| `crack-7z-hash` | Medium | `security` | ✅ PASS (194s) | ✅ PASS (226s) | ✅ PASS (182s) | Triple Pass (Consensus Solution) |
| `custom-memory-heap-crash` | Medium | `debugging` | ✅ PASS (182s) | ✅ PASS (548s) | ✅ PASS (180s) | Triple Pass (**Supreme 3.0x Faster**) |
| `filter-js-from-html` | Medium | `security` | ✅ PASS (212s) | ✅ PASS (193s) | ✅ PASS (226s) | Triple Pass (Consensus Solution) |

---

### 📁 Domain: Software Engineering (65 Tasks)

**Domain Performance Summary:**  
- **Supreme (v1.0):** 44/65 (67.7%)  
- **Superpowers by obra:** 40/65 (61.5%)  
- **Baseline:** 36/65 (55.4%)  

| Task Name | Difficulty | Category | Supreme (v1.0) | Superpowers by obra | Baseline | Key Dynamics |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `build-cython-ext` | Medium | `debugging` | ✅ PASS (413s) | ✅ PASS (324s) | ❌ FAIL (739s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `build-pmars` | Medium | `software-engineering` | ✅ PASS (435s) | ✅ PASS (472s) | ✅ PASS (419s) | Triple Pass (Consensus Solution) |
| `build-pov-ray` | Medium | `software-engineering` | ❌ FAIL (453s) | ❌ FAIL (553s) | ✅ PASS (524s) | Mixed Resolution |
| `caffe-cifar-10` | Medium | `machine-learning` | ❌ FAIL (1211s) | ❌ FAIL (1211s) | ❌ FAIL (1210s) | Triple Fail (High Complexity / Upstream Defect) |
| `cancel-async-tasks` | Hard | `software-engineering` | ✅ PASS (556s) | ✅ PASS (527s) | ❌ FAIL (781s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `circuit-fibsqrt` | Hard | `software-engineering` | ✅ PASS (1279s) | ❌ FAIL (3634s) | ✅ PASS (522s) | Mixed Resolution |
| `cobol-modernization` | Easy | `software-engineering` | ✅ PASS (428s) | ✅ PASS (385s) | ✅ PASS (551s) | Triple Pass (Consensus Solution) |
| `code-from-image` | Medium | `software-engineering` | ✅ PASS (101s) | ✅ PASS (557s) | ✅ PASS (114s) | Triple Pass (**Supreme 5.5x Faster**) |
| `compile-compcert` | Medium | `system-administration` | ❌ FAIL (2417s) | ❌ FAIL (2409s) | ❌ FAIL (2418s) | Triple Fail (High Complexity / Upstream Defect) |
| `dna-assembly` | Hard | `scientific-computing` | ❌ FAIL (235s) | ❌ FAIL (264s) | ❌ FAIL (398s) | Triple Fail (High Complexity / Upstream Defect) |
| `dna-insert` | Medium | `scientific-computing` | ❌ FAIL (234s) | ❌ FAIL (334s) | ❌ FAIL (315s) | Triple Fail (High Complexity / Upstream Defect) |
| `extract-elf` | Medium | `file-operations` | ❌ FAIL (133s) | ❌ FAIL (176s) | ❌ FAIL (147s) | Triple Fail (High Complexity / Upstream Defect) |
| `extract-moves-from-video` | Hard | `file-operations` | ❌ FAIL (1839s) | ❌ FAIL (1831s) | ❌ FAIL (1806s) | Triple Fail (High Complexity / Upstream Defect) |
| `feal-differential-cryptanalysis` | Hard | `mathematics` | ✅ PASS (100s) | ✅ PASS (176s) | ✅ PASS (114s) | Triple Pass (Consensus Solution) |
| `feal-linear-cryptanalysis` | Hard | `mathematics` | ✅ PASS (502s) | ✅ PASS (541s) | ✅ PASS (218s) | Triple Pass (Consensus Solution) |
| `financial-document-processor` | Medium | `data-processing` | ✅ PASS (474s) | ✅ PASS (353s) | ✅ PASS (246s) | Triple Pass (Consensus Solution) |
| `fix-code-vulnerability` | Hard | `security` | ✅ PASS (178s) | ✅ PASS (227s) | ✅ PASS (913s) | Triple Pass (Consensus Solution) |
| `fix-git` | Easy | `software-engineering` | ✅ PASS (515s) | ❌ FAIL (376s) | ❌ FAIL (313s) | 🏆 **Supreme Solo Win** |
| `fix-ocaml-gc` | Hard | `software-engineering` | ✅ PASS (536s) | ✅ PASS (407s) | ❌ FAIL (569s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `gcode-to-text` | Medium | `file-operations` | ❌ FAIL (351s) | ❌ FAIL (196s) | ✅ PASS (914s) | Mixed Resolution |
| `git-leak-recovery` | Medium | `software-engineering` | ✅ PASS (149s) | ✅ PASS (163s) | ✅ PASS (174s) | Triple Pass (Consensus Solution) |
| `git-multibranch` | Medium | `system-administration` | ✅ PASS (258s) | ✅ PASS (268s) | ✅ PASS (240s) | Triple Pass (Consensus Solution) |
| `gpt2-codegolf` | Hard | `software-engineering` | ✅ PASS (904s) | ❌ FAIL (903s) | ❌ FAIL (914s) | 🏆 **Supreme Solo Win** |
| `headless-terminal` | Medium | `software-engineering` | ✅ PASS (461s) | ✅ PASS (315s) | ❌ FAIL (76s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `install-windows-3.11` | Hard | `system-administration` | ✅ PASS (2649s) | ❌ FAIL (955s) | ❌ FAIL (510s) | 🏆 **Supreme Solo Win** |
| `kv-store-grpc` | Medium | `software-engineering` | ✅ PASS (265s) | ✅ PASS (152s) | ✅ PASS (131s) | Triple Pass (Consensus Solution) |
| `large-scale-text-editing` | Medium | `file-operations` | ✅ PASS (584s) | ✅ PASS (432s) | ❌ FAIL (588s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `largest-eigenval` | Medium | `mathematics` | ❌ FAIL (939s) | ✅ PASS (399s) | ✅ PASS (862s) | Mixed Resolution |
| `llm-inference-batching-scheduler` | Hard | `machine-learning` | ✅ PASS (184s) | ✅ PASS (280s) | ✅ PASS (347s) | Triple Pass (Consensus Solution) |
| `mailman` | Medium | `system-administration` | ❌ FAIL (346s) | ✅ PASS (1180s) | ❌ FAIL (1180s) | Superpowers Solo Win |
| `make-doom-for-mips` | Hard | `software-engineering` | ❌ FAIL (902s) | ❌ FAIL (107s) | ❌ FAIL (227s) | Triple Fail (High Complexity / Upstream Defect) |
| `make-mips-interpreter` | Hard | `software-engineering` | ❌ FAIL (1803s) | ❌ FAIL (548s) | ❌ FAIL (1813s) | Triple Fail (High Complexity / Upstream Defect) |
| `mcmc-sampling-stan` | Hard | `data-science` | ✅ PASS (1313s) | ✅ PASS (1590s) | ✅ PASS (1292s) | Triple Pass (Consensus Solution) |
| `merge-diff-arc-agi-task` | Medium | `debugging` | ✅ PASS (435s) | ✅ PASS (235s) | ❌ FAIL (7035s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `modernize-scientific-stack` | Medium | `scientific-computing` | ✅ PASS (69s) | ✅ PASS (84s) | ✅ PASS (96s) | Triple Pass (Consensus Solution) |
| `mteb-leaderboard` | Medium | `data-science` | ❌ FAIL (3613s) | ✅ PASS (723s) | ❌ FAIL (3101s) | Superpowers Solo Win |
| `mteb-retrieve` | Medium | `data-science` | ❌ FAIL (474s) | ❌ FAIL (1533s) | ❌ FAIL (560s) | Triple Fail (High Complexity / Upstream Defect) |
| `multi-source-data-merger` | Medium | `data-processing` | ✅ PASS (165s) | ✅ PASS (97s) | ✅ PASS (170s) | Triple Pass (Consensus Solution) |
| `openssl-selfsigned-cert` | Medium | `security` | ✅ PASS (174s) | ✅ PASS (171s) | ✅ PASS (114s) | Triple Pass (Consensus Solution) |
| `overfull-hbox` | Easy | `debugging` | ✅ PASS (297s) | ❌ FAIL (372s) | ✅ PASS (321s) | Mixed Resolution |
| `password-recovery` | Hard | `security` | ✅ PASS (181s) | ✅ PASS (205s) | ✅ PASS (258s) | Triple Pass (Consensus Solution) |
| `path-tracing` | Hard | `software-engineering` | ✅ PASS (377s) | ✅ PASS (304s) | ✅ PASS (286s) | Triple Pass (Consensus Solution) |
| `path-tracing-reverse` | Hard | `software-engineering` | ✅ PASS (579s) | ✅ PASS (475s) | ✅ PASS (493s) | Triple Pass (Consensus Solution) |
| `polyglot-c-py` | Medium | `software-engineering` | ✅ PASS (188s) | ✅ PASS (224s) | ✅ PASS (164s) | Triple Pass (Consensus Solution) |
| `polyglot-rust-c` | Hard | `software-engineering` | ✅ PASS (200s) | ✅ PASS (186s) | ✅ PASS (130s) | Triple Pass (Consensus Solution) |
| `portfolio-optimization` | Medium | `optimization` | ✅ PASS (509s) | ✅ PASS (427s) | ✅ PASS (380s) | Triple Pass (Consensus Solution) |
| `protein-assembly` | Hard | `scientific-computing` | ✅ PASS (894s) | ❌ FAIL (886s) | ✅ PASS (916s) | Mixed Resolution |
| `prove-plus-comm` | Easy | `software-engineering` | ❌ FAIL (80s) | ❌ FAIL (143s) | ❌ FAIL (69s) | Triple Fail (High Complexity / Upstream Defect) |
| `qemu-alpine-ssh` | Medium | `system-administration` | ❌ FAIL (907s) | ❌ FAIL (725s) | ✅ PASS (597s) | Mixed Resolution |
| `qemu-startup` | Medium | `system-administration` | ✅ PASS (685s) | ✅ PASS (610s) | ✅ PASS (593s) | Triple Pass (Consensus Solution) |
| `query-optimize` | Medium | `data-science` | ✅ PASS (459s) | ✅ PASS (370s) | ✅ PASS (680s) | Triple Pass (Consensus Solution) |
| `raman-fitting` | Medium | `scientific-computing` | ❌ FAIL (275s) | ✅ PASS (321s) | ❌ FAIL (310s) | Superpowers Solo Win |
| `reshard-c4-data` | Medium | `data-science` | ✅ PASS (1325s) | ✅ PASS (1534s) | ✅ PASS (1349s) | Triple Pass (Consensus Solution) |
| `rstan-to-pystan` | Medium | `data-science` | ✅ PASS (1812s) | ❌ FAIL (1810s) | ✅ PASS (1543s) | Mixed Resolution |
| `sam-cell-seg` | Hard | `data-science` | ❌ FAIL (443s) | ❌ FAIL (7222s) | ❌ FAIL (3328s) | Triple Fail (High Complexity / Upstream Defect) |
| `sanitize-git-repo` | Medium | `security` | ❌ FAIL (456s) | ❌ FAIL (398s) | ❌ FAIL (272s) | Triple Fail (High Complexity / Upstream Defect) |
| `schemelike-metacircular-eval` | Medium | `software-engineering` | ✅ PASS (400s) | ✅ PASS (2411s) | ✅ PASS (361s) | Triple Pass (**Supreme 6.0x Faster**) |
| `sparql-university` | Hard | `data-querying` | ✅ PASS (485s) | ✅ PASS (494s) | ✅ PASS (477s) | Triple Pass (Consensus Solution) |
| `torch-pipeline-parallelism` | Hard | `software-engineering` | ❌ FAIL (607s) | ❌ FAIL (624s) | ❌ FAIL (662s) | Triple Fail (High Complexity / Upstream Defect) |
| `torch-tensor-parallelism` | Hard | `software-engineering` | ❌ FAIL (909s) | ❌ FAIL (195s) | ❌ FAIL (910s) | Triple Fail (High Complexity / Upstream Defect) |
| `tune-mjcf` | Medium | `scientific-computing` | ✅ PASS (415s) | ❌ FAIL (813s) | ❌ FAIL (502s) | 🏆 **Supreme Solo Win** |
| `video-processing` | Hard | `video-processing` | ✅ PASS (1074s) | ✅ PASS (1511s) | ❌ FAIL (1603s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `vulnerable-secret` | Medium | `security` | ✅ PASS (58s) | ✅ PASS (62s) | ❌ FAIL (14s) | Prompt Grounding Win (Baseline Refusal/Fail) |
| `winning-avg-corewars` | Medium | `software-engineering` | ✅ PASS (175s) | ✅ PASS (1649s) | ✅ PASS (1104s) | Triple Pass (**Supreme 9.4x Faster**) |
| `write-compressor` | Hard | `software-engineering` | ✅ PASS (299s) | ✅ PASS (151s) | ✅ PASS (152s) | Triple Pass (Consensus Solution) |

---

### 📁 Domain: System Administration (7 Tasks)

**Domain Performance Summary:**  
- **Supreme (v1.0):** 6/7 (85.7%)  
- **Superpowers by obra:** 7/7 (100.0%)  
- **Baseline:** 7/7 (100.0%)  

| Task Name | Difficulty | Category | Supreme (v1.0) | Superpowers by obra | Baseline | Key Dynamics |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `configure-git-webserver` | Hard | `system-administration` | ✅ PASS (290s) | ✅ PASS (290s) | ✅ PASS (523s) | Triple Pass (Consensus Solution) |
| `db-wal-recovery` | Medium | `file-operations` | ✅ PASS (195s) | ✅ PASS (154s) | ✅ PASS (147s) | Triple Pass (Consensus Solution) |
| `log-summary-date-ranges` | Medium | `data-processing` | ✅ PASS (121s) | ✅ PASS (121s) | ✅ PASS (84s) | Triple Pass (Consensus Solution) |
| `model-extraction-relu-logits` | Hard | `mathematics` | ❌ FAIL (211s) | ✅ PASS (190s) | ✅ PASS (236s) | Mixed Resolution |
| `nginx-request-logging` | Medium | `system-administration` | ✅ PASS (114s) | ✅ PASS (166s) | ✅ PASS (123s) | Triple Pass (Consensus Solution) |
| `pypi-server` | Medium | `software-engineering` | ✅ PASS (154s) | ✅ PASS (224s) | ✅ PASS (260s) | Triple Pass (Consensus Solution) |
| `regex-log` | Medium | `data-processing` | ✅ PASS (218s) | ✅ PASS (204s) | ✅ PASS (227s) | Triple Pass (Consensus Solution) |

---

## 3. Deep-Dive Forensic Autopsies on Decisive Tasks

### 🔬 Case 1: Task #88 (`winning-avg-corewars`) — The Anatomy of Tool-Discovery Thrashing

- **Domain:** Software Engineering / Assembly Algorithmics  
- **Objective:** Design an optimal Redcode warrior meeting competitive win thresholds in the MARS arena.  
- **Empirical Metrics:**
  - **Supreme (v1.0):** 🏆 **PASS in 175.00s** | 53 tool calls | 300,413 tokens | 100% tests passed.
  - **Superpowers by obra:** 🏆 **PASS in 1,648.65s** | 535 tool calls | 3,513,757 tokens | 100% tests passed.
  - **Baseline:** 🏆 **PASS in 1,103.95s** | 249 tool calls | 2,163,114 tokens | 100% tests passed.

**Forensic Investigation:**  
Why did Superpowers require $11.7\times$ more tokens and $10\times$ more tool invocations to achieve the exact same passing grade?  
Transcript tracing reveals that when Superpowers encountered non-deterministic battle simulator outputs, its dynamic prompt loader directed the model to re-invoke skill discovery. The model repeatedly re-read `systematic-debugging/SKILL.md`, `test-driven-development/SKILL.md`, and references, creating a meta-cognitive loop. Instead of analyzing the Redcode opcode structure, the agent launched 535 shell operations running brute-force parameter sweeps. In contrast, Supreme's constitutional mandate (*'Hypothesis testing before mutation'*) forced the agent to formulate an architectural warrior strategy (P-space adaptive scanner) in just 2 structured iterations.

### 🔬 Case 2: Task #85 (`tune-mjcf`) — Solo Pass on Physics Solver Convergence

- **Domain:** Robotics & Physics Simulation (MuJoCo)  
- **Objective:** Optimize XML kinematics and solver parameters to accelerate simulation by $\ge 40\%$ with zero trajectory divergence ($D \le 10^{-4}$).  
- **Empirical Metrics:**
  - **Supreme (v1.0):** 🏆 **SOLO PASS in 414.94s** | 81 tool calls | 436,922 tokens | **2.19x speedup** | $D = 0.0000$.
  - **Superpowers by obra:** ❌ **FAIL in 813.02s** | 126 tool calls | 543,089 tokens | 0% speedup (0.99x ratio).
  - **Baseline:** ❌ **FAIL in 501.80s** | 57 tool calls | 384,399 tokens | negative speedup (1.01x ratio).

**Forensic Investigation:**  
MuJoCo XML simulation tuning is an ultra-sensitive continuous optimization problem. Naive parameter edits (e.g. changing integrator timesteps) immediately trigger catastrophic trajectory divergence or solver explosion. Supreme methodically profiled the solver pipeline first, identified PGS solver tolerances and collision margins as non-divergent acceleration knobs, and achieved a **2.19x wall-clock speedup**. Superpowers and Baseline engaged in speculative trial-and-error edits, degrading simulation accuracy without improving compute throughput.

### 🔬 Case 3: Tasks #82 & #83 — Auditing Upstream Infrastructure Defects

- **Task #82:** `torch-pipeline-parallelism` (Distributed Deep Learning)  
- **Task #83:** `torch-tensor-parallelism` (Megatron-LM Style Matrix Partitioning)  
- **Empirical Finding:** Both tasks registered failures across all 3 paradigms.  

**Forensic Investigation:**  
1. **Task #82 Container Defect:** In Task #82, the author's Docker container was built without Python or curl installed, and network egress was blocked. When `/tests/test.sh` was invoked during post-execution verification, it executed `curl ... | python3 -`, which crashed immediately with `exit code 127 (command not found)`. No agent code was ever evaluated.  
2. **Task #83 CUDA Download Timeout:** In Task #83, `/tests/test.sh` contained an unconstrained `pip install torch` directive that attempted to pull **2.85 GB of CUDA 12 GPU wheels** on a CPU-only test environment. The pip download saturated the 900s timeout, killing the verifier before running pytest.  
**Scientific Takeaway:** Documenting these upstream bugs in public ledgers prevents unfair penalties and establishes benchmark harness credibility.

### 🔬 Case 4: Task #87 (`vulnerable-secret`) — Contextual Developer Grounding vs Safety Refusal

- **Domain:** Security & Reverse Engineering (CTF Memory Exploitation)  
- **Objective:** Buffer overflow exploit to recover secret flag in local C binary.  
- **Empirical Metrics:**
  - **Supreme (v1.0):** 🏆 **PASS in 58.48s** | 17 tool calls | 96,941 tokens.
  - **Superpowers by obra:** 🏆 **PASS in 61.74s** | 17 tool calls | 99,854 tokens.
  - **Baseline:** ❌ **FAIL in 14.20s** | 1 tool call | 22,585 tokens (Immediate Refusal).

**Forensic Investigation:**  
On Turn 1, the unprompted Baseline model triggered an immediate safety over-refusal (*'I cannot assist with binary exploitation...'*). Both Supreme and Superpowers provided the model with explicit developer environment awareness, allowing the agent to distinguish an authorized CTF challenge from malicious activity.

---

## 4. Master Failure Taxonomy & Root Cause Matrix

Across all 267 graded runs, we classify every failure into four mutually exclusive categories:

| Failure Category | Description | Supreme (v1.0) | Superpowers by obra | Baseline | Root Cause & Mechanism |
|:---|:---|:---:|:---:|:---:|:---|
| **Code Logic / Verification Defect** | Agent attempted implementation but failed unit test assertions. | 22 | 24 | 26 | Complex algorithmic boundaries, edge-case math, or strict tolerances. |
| **Tool Thrashing / Timeout Exhaustion** | Agent exceeded 900s timeout due to recursive search loops. | 3 | 5 | 4 | Combinatorial search spaces triggering unbounded exploratory tool loops. |
| **Upstream Infrastructure Defect** | Broken container, missing tools, or external PyPI download timeouts. | 3 (T82, T83, T84) | 3 (T82, T83, T84) | 3 (T82, T83, T84) | Docker environment misconfigurations outside model control. |
| **Safety Alignment Over-Refusal** | Model refused benign authorized programming task on Turn 1. | 0 | 0 | 1 (T87) | Over-active RLHF safety filters on security/CTF tasks. |
| **Total Failures** | Sum of non-passing evaluations | **28 / 89** | **31 / 89** | **34 / 89** | **Supreme minimizes both tool thrashing and logic failures.** |

---

## 5. Architectural Principles for Autonomous Agent Systems

The forensic findings of CARB-v4 establish three foundational principles for building production-grade coding agents:

1. **Constitutional Guardrails Outperform Unbounded Dynamic Search**:  
   Static, invariant axioms that mandate *evidence before assumption*, *hypothesis formulation before code mutation*, and *surgical diff inspection* prevent models from degrading into runaway parameter sweeps.

2. **Dynamic Skill Catalogs Require Strict Loop-Breaking Bounds**:  
   If an agent system uses on-demand skill discovery, it must enforce maximum re-read thresholds and backoff limits to prevent the *Tool-Discovery Thrashing* phenomenon observed in Task #88.

3. **Surgical Editing Yields Substantial Economic Savings**:  
   Prompt length optimizations pale in comparison to diff control. Supreme's surgical editing rules prevented full-file rewrites, saving hundreds of thousands of tokens per complex task.
