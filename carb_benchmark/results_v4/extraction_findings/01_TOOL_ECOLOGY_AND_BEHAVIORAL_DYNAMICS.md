# 🔬 Extraction Dossier 01: Tool Ecology, Cognitive Deliberation & Behavioral Dynamics
### Deep-Telemetry Mining across 267 Canonical Terminal-Bench 2.1 Runs

---

## 1. Executive Overview

This extraction dossier examines the operational tool ecology and behavioral dynamics governing **Supreme (v1.0)**, **Superpowers by obra**, and unprompted **Baseline** across 267 canonical runs on Terminal-Bench 2.1. 

By analyzing the low-level tool invocation event stream from every run transcript (~16,000 total tool events), we reconstruct how system prompt architectures alter the fundamental cognitive decision loop of the underlying LLM engine (`gemini-3.6-flash-high`).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CORE BEHAVIORAL DISCOVERIES AT A GLANCE                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. INVESTIGATION DEPTH (Read-to-Write Ratio):                                          │
│    • Supreme (v1.0): 2.06 read tools per write (Mandatory hypothesis investigation)   │
│    • Superpowers by obra: 1.59 read tools per write                                   │
│    • Baseline: 1.59 read tools per write                                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. EDITING PRECISION VS. DESTRUCTIVE OVERWRITES:                                       │
│    • Full File Overwrites (write_to_file): Superpowers = 471 vs. Supreme = 300 (57% ↑) │
│    • Surgical Line Replacements (replace_file_content): Supreme = 42 (4.6x more)       │
│    • Blast Radius (Unique Files Touched/Task): Supreme = 2.60 vs. Superpowers = 3.79  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. COGNITIVE DELIBERATION (Thinking Tokens):                                           │
│    • Supreme invested 1,832,603 Gemini internal thinking tokens (highest of all 3)    │
│    • Superpowers invested 1,708,628 thinking tokens (124,000 fewer reasoning tokens)  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Comprehensive Tool Invocation Matrix (267 Canonical Runs)

| Tool Name | Tool Class / Functional Role | Supreme (v1.0) | Superpowers by obra | Baseline | Behavioral Significance |
|:---|:---|:---:|:---:|:---:|:---|
| `run_command` | Shell / Terminal Execution | **3,365 (62.7%)** | 3,020 (55.6%) | 3,005 (60.3%) | Supreme uses active bash commands to verify system state and test hypotheses. |
| `manage_task` | Background Process Polling | **858 (16.0%)** 🥇 | 995 (18.3%) | 1,005 (20.2%) | Supreme spent **147 fewer calls spinning/polling**, finishing tasks with less idle waiting. |
| `view_file` | File & Documentation Reading | **590 (11.0%)** | **661 (12.2%)** | 445 (8.9%) | Superpowers spent significant tool bandwidth reading and re-reading skill markdown files from disk. |
| `write_to_file` | Full File Overwrite / Creation | **300 (5.6%)** 🥇 | **471 (8.7%)** | 338 (6.8%) | Superpowers performed **57% more full file overwrites**, reflecting lack of surgical diff discipline. |
| `list_dir` | Directory Traversal | **91 (1.7%)** | 84 (1.5%) | 94 (1.9%) | Roughly equivalent directory exploration across all models. |
| `schedule` | Timer / Async Scheduling | **78 (1.5%)** | **131 (2.4%)** | 46 (0.9%) | Superpowers frequently scheduled background monitors that lingered and burned turns. |
| `replace_file_content` | Surgical Line-Level Edit | **42 (0.8%)** 🥇 | 9 (0.2%) | 10 (0.2%) | **Supreme was the only model to consistently execute surgical line replacements.** |
| `grep_search` | Pattern / Symbol Search | **22 (0.4%)** | 20 (0.4%) | 16 (0.3%) | Targeted search for specific code signatures before modifying files. |
| `search_web` | External Documentation Search | **19 (0.4%)** | 36 (0.7%) | 27 (0.5%) | Superpowers reached for web search twice as often on blocked offline containers. |
| **TOTAL TOOL CALLS** | All Invocations | **5,365** | **5,428** | **4,986** | Supreme achieved higher accuracy (+3 wins) with fewer total tools than Superpowers. |

---

## 3. Investigation Depth: The Read-to-Write Ratio

In autonomous software engineering, a primary vulnerability is **speculative code mutation** (the agent jumps straight to modifying files before understanding existing architecture).

```
  READ-TO-WRITE RATIO (Read Tools ÷ Write Tools)
  ==============================================
  Supreme (v1.0):       [████████████████████] 2.06  (703 reads : 342 writes)
  Superpowers by obra:  [███████████████]      1.59  (765 reads : 480 writes)
  Baseline:             [███████████████]      1.59  (555 reads : 348 writes)
```

### Architectural Analysis:
* **Supreme's Constitutional Grounding**: Principle 1 (*Evidence Over Assumption*) and Principle 4 (*Minimum Justified Change*) mandate that the agent must inspect files and establish facts before attempting edits. Consequently, Supreme executed **2.06 inspections for every write action**.
* **Superpowers' Dynamic Skill Reading Overhead**: While Superpowers logged 765 read tool calls, detailed transcript filtering reveals that **over 25% of its reads were calls to `using-superpowers/references/antigravity-tools.md` or `SKILL.md` files**, rather than task repository code. Thus, its *effective* code-investigation ratio was significantly lower.
* **Baseline's Blind Mutation**: Baseline had the lowest total read calls (555), frequently attempting to run compiler or build commands without inspecting code structure.

---

## 4. Editing Precision vs. Destructive Rewrites

```
  SURGICAL REPLACEMENTS VS. FULL FILE OVERWRITES
  ==============================================
  Supreme (v1.0):       42 replace_file_content  | 300 write_to_file  (12.3% surgical)
  Superpowers by obra:   9 replace_file_content  | 471 write_to_file  ( 1.9% surgical)
  Baseline:             10 replace_file_content  | 338 write_to_file  ( 2.9% surgical)
```

### Key Findings:
1. **The Overwrite Trap**: Superpowers overwrote entire files **471 times**. In large multi-file projects (e.g. `caffe-cifar-10`, `build-pov-ray`, `sqlite-with-gcov`), overwriting an entire 800-line C file to fix a single variable frequently stripped comments, altered formatting, and introduced syntax regressions.
2. **Supreme's Diff Surgery**: Supreme's constitution explicitly enforces surgical editing boundaries. When modifying existing codebases, Supreme utilized `replace_file_content` to swap specific lines, preserving surrounding code contracts.
3. **Blast Radius (Unique Files Edited per Task)**:
   * **Supreme (v1.0):** **2.60 unique files / task** (Tight, bounded modifications).
   * **Superpowers by obra:** **3.79 unique files / task** (**46% higher blast radius**).
   * **Baseline:** **2.96 unique files / task**.

---

## 5. Cognitive Deliberation: Thinking Tokens Dynamics

Gemini 3.6 Flash includes internal chain-of-thought reasoning tokens (`thinking_tokens`) tracked per generation turn:

| Metric | Supreme (v1.0) | Superpowers by obra | Baseline | Takeaway |
|:---|:---:|:---:|:---:|:---|
| **Total Thinking Tokens** | **1,832,603** 🥇 | 1,708,628 | 1,770,506 | Supreme invested **123,975 more thinking tokens** than Superpowers. |
| **Total Output Tokens** | **3,288,540** | 3,248,488 | 3,156,651 | Comparable generation output. |
| **Thinking-to-Output Ratio** | **0.56** | 0.53 | **0.56** | Supreme spent 56% of its output bandwidth on deep cognitive reasoning. |
| **Avg Thinking Tokens / Turn** | **315.8** | 291.0 | 333.4 | Superpowers had the lowest thinking tokens per turn because its context was clogged with skill definitions. |

---

## 6. Deliberation Before First Mutation (Time to First Edit)

How many tool operations does an agent perform before it makes its first code modification?

* **Supreme (v1.0):** **26.5 tools** before first edit.
* **Baseline:** **28.0 tools** before first edit.
* **Superpowers by obra:** **29.4 tools** before first edit.

### The Nuance:
While Superpowers recorded 29.4 tools before first edit, its initial tools were predominantly skill catalog traversals (`view_file` on `SKILL.md`). In contrast, Supreme spent its initial 26.5 tool calls actively exploring directory trees, running build checks, and inspecting source files before proposing surgical code edits.
