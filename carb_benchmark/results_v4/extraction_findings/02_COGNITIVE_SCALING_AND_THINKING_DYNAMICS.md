# 🧠 Extraction Dossier 02: The Cognitive Scaling Frontier & Thinking Dynamics
### Empirical Chain-of-Thought Allocation Across 267 Canonical Terminal-Bench 2.1 Runs

---

## 1. Executive Abstract

Frontier reasoning models (such as Google Gemini 3.6 Flash High) do not merely emit code; they generate structured internal chain-of-thought tokens (`thinking_tokens`) preceding every tool execution and text response. Across the 267 canonical runs of CARB-v4, the underlying model invested a cumulative **5,311,737 thinking tokens**.

This dossier investigates how system prompt architectures modulate the model's internal reasoning budget:
1. **The Hard-Task Scaling Law**: Supreme v1.0 scaled thinking tokens by **+66.0%** on Hard tasks, achieving a **+13.4 percentage point win-rate advantage (66.7% vs. 53.3%)** over Superpowers by obra.
2. **Context Window Starvation**: Progressive skill loading (Superpowers by obra) constrained available reasoning context, capping thinking on Hard tasks at 23,196 tokens/task.
3. **The "Overthinking Trap" vs. "Breakthrough Deliberation"**: We establish the empirical boundary where deep thinking yields correct algorithmic breakthroughs versus where it degenerates into ungrounded speculation.
4. **The CoreWars Divergence**: A turn-by-turn case study of the largest cognitive efficiency contrast in the benchmark (300k tokens vs. 3.51M tokens on Task #88).

---

## 2. Macro Thinking Token Distribution (All 267 Runs)

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

### Key Statistical Inferences:
* **Controlled Deliberation Variance**: Supreme exhibited the lowest standard deviation ($\sigma = 13,545$), reflecting disciplined, predictable thinking allocation across all tasks.
* **Unconstrained Variance in Baseline**: Baseline swung wildly between zero thinking on quick refusals ($\text{Min} = 0$) and massive cognitive lockups ($\text{Max} = 199,582$), demonstrating a lack of cognitive pacing.
* **The Aggregate Thinking Lead**: Supreme invested **123,975 more total thinking tokens** than Superpowers, dedicating its context window to algorithmic deduction rather than markdown documentation parsing.

---

## 3. Cognitive Allocation Across Difficulty Strata

We stratified all 89 tasks into official difficulty tiers: **Easy** ($N=4$), **Medium** ($N=55$), and **Hard** ($N=30$).

```
  HARD-TASK WIN RATE (30 TASKS)
  =============================
  Supreme (v1.0):       [████████████████████] 66.7% (20/30) 🏆
  Baseline:             [█████████████████]    56.7% (17/30)
  Superpowers by obra:  [████████████████]     53.3% (16/30)
```

| Difficulty Strata | Metric | Supreme (v1.0) | Superpowers by obra | Baseline | Cognitive Interpretation |
|:---|:---|:---:|:---:|:---:|:---|
| **EASY** ($N=4$) | Pass Rate | **75.0% (3/4)** 🏆 | 25.0% (1/4) ⚠️ | 50.0% (2/4) | Superpowers collapsed on simple tasks due to skill prompt distraction. |
| | Mean Thinking | 11,885.8 | 14,618.0 | 10,688.5 | Superpowers burned +23% more thinking tokens but failed 3 of 4. |
| | Median Thinking | 7,288.0 | 13,393.0 | 8,281.0 | Supreme needed fewer tokens to solve Easy tasks accurately. |
| **MEDIUM** ($N=55$) | Pass Rate | 69.1% (38/55) | **74.5% (41/55)** 🥇 | 65.5% (36/55) | Superpowers peaked on Medium tasks where standard recipes fit. |
| | Mean Thinking | 17,035.1 | 17,350.3 | 18,090.2 | Balanced deliberation across all three paradigms (~17k tokens). |
| | Median Thinking | 16,055.0 | 15,431.0 | 14,306.0 | Consistent reasoning footprint. |
| **HARD** ($N=30$) | Pass Rate | **66.7% (20/30)** 🏆 | 53.3% (16/30) | 56.7% (17/30) | **Supreme achieves a +13.4 percentage point lead on Hard tasks.** |
| | Mean Thinking | **28,271.0** 🥇 | 23,196.2 | 24,426.3 | Supreme scaled thinking by **+66.0%** over Medium tasks. |
| | Median Thinking | **21,710.0** | 20,104.0 | 22,073.5 | Supreme invested **5,075 more thinking tokens per task** than Superpowers. |

> [!IMPORTANT]
> **The Hard-Task Scaling Law**: As task complexity escalates from Medium to Hard, Supreme's constitutional grounding encourages deep, bounded reasoning (+66.0% increase in thinking tokens). In contrast, Superpowers' available context was crowded by on-demand skill documentation, starving the model of internal reasoning space and suppressing its Hard-task pass rate to 53.3%.

---

## 4. "Overthinking Traps": When High Deliberation Induces Paralysis

High thinking token investment is not an absolute guarantee of success. In several notable tasks, models generated massive thinking traces but became trapped in ungrounded speculative loops:

| Paradigm | Task Name | Difficulty | Thinking Tokens | Turns | Seconds | The Failure Mechanism |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| `superpowers-v4.0` | `regex-chess` | Hard | **76,457** | 105 | 1,154.1s | Model wrote deeply nested regexes to validate chess moves, constantly rethinking lookahead assertions without running quick unit tests. |
| `supreme-v2.0` | `regex-chess` | Hard | **63,348** | 82 | 675.9s | Combinatorial regex explosion; attempted to encode knight/bishop moves into single patterns instead of modular logic. |
| `supreme-v2.0` | `make-doom-for-mips` | Hard | **62,381** | 177 | 901.8s | Cross-compiling Doom for MIPS; overthought C macro rewrites while missing a simple link library flag. |
| `baseline-v2.0` | `make-mips-interpreter` | Hard | **58,900** | 199 | 1,812.5s | Spent 199 turns debugging MIPS opcode decoding; lost track of endianness in register load. |
| `superpowers-v4.0` | `gpt2-codegolf` | Hard | **47,746** | 108 | 902.7s | Deliberated extensively on BPE tokenization tables in pure C, but failed matrix multiplication stride calculation. |
| `baseline-v2.0` | `fix-ocaml-gc` | Hard | **45,483** | 82 | 568.7s | Analyzed OCaml garbage collection run-length compression, but corrupted the allocation header format. |

---

## 5. "Breakthrough Deliberations": High Deliberation Unlocking Complex Passes

Conversely, deep deliberation was decisive in solving several of the most difficult engineering tasks in the benchmark:

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

### Case Study 1: `write-compressor` (Supreme's Maximum Deliberation Solve)
* **Task**: Implement a custom lossless data compressor in C that achieves a high compression ratio on specific binary inputs.
* **Cognitive Profile**: Supreme invested **64,932 thinking tokens** (its benchmark maximum) across 66 turns in just 299.2 seconds.
* **Why it Succeeded**: Supreme spent the first 18 turns in pure algorithmic derivation, formulating a custom Huffman + Run-Length-Encoding (RLE) scheme with optimal frequency table packing, then wrote the entire C implementation and verified it in one pass.

### Case Study 2: `install-windows-3.11` (Supreme's 44-Minute Autonomous Marathon)
* **Task**: Install Windows 3.11 for Workgroups inside QEMU, configure networking, and boot into desktop.
* **Cognitive Profile**: **58,010 thinking tokens**, 307 turns, 2,648.7s (44.1 minutes).
* **Execution**: Supreme navigated MS-DOS setup prompts, disk partitioning (`fdisk`), format, floppy image swapping, and VESA graphics driver installation entirely through headless QEMU serial/monitor inputs, passing 4/4 assertions. Superpowers and Baseline both failed.

---

## 6. The Extreme Divergence: Task #88 (`winning-avg-corewars`)

The most dramatic efficiency contrast across all 267 runs occurred in `winning-avg-corewars` (implementing a Mars / Redcode warrior that outperforms standard competitors):

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

### Forensic Reconstruction:
* **Supreme's Strategy (175 seconds)**: Supreme inspected existing benchmark warriors (`cat warriors/*.red`), ran 100 test rounds with `pmars -b -r 100`, deduced that a Silk/Replicator warrior would dominate the test pool, wrote `my_warrior.red` (17 writes), validated win rates, and terminated.
* **Superpowers' Trajectory (1,648 seconds, 3.51 Million Tokens)**: Superpowers fell into a massive trial-and-error loop. It wrote **116 separate Python exploration scripts** (`find_snake_and_g2_winners.py`, `explore_coprime_silks.py`, `test_pspace_warrior.py`), repeatedly copied them into Docker with `docker cp`, watched them fail or time out, and took **563 turns** before finally achieving the pass threshold.
* **The Architectural Lesson**: Supreme achieved a **9.4x wall-clock speedup** and consumed **11.7x fewer tokens** by utilizing structured empirical hypothesis testing rather than unconstrained script generation.

---

## 7. Architectural Takeaways for Agent System Designers

1. **Thinking Token Elasticity**: Agent architectures must allow internal reasoning tokens to scale dynamically with task difficulty. Rigid prompt formats that force quick tool calls suppress cognitive deliberation on Hard tasks.
2. **Context Preservation for Reasoning**: On-demand skill catalogs that inject multi-thousand-token markdown files mid-task directly compete with the model's internal reasoning cache, causing cognitive degradation on complex problems.
3. **Loop-Breaking Guardrails**: When a model accumulates over 40,000 thinking tokens across multiple failing turns without state progress, the harness must intervene with an architectural reorientation prompt to prevent the "Overthinking Trap".
