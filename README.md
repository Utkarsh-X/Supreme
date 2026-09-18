<p align="center">
  <img src="assets/banner.png" width="800" alt="Supreme">
</p>

<h3 align="center">For agents that should know better.</h3>

<p align="center">
  <em>A lean engineering constitution. Minimal by design. Nothing to install, nothing to load mid-turn.</em>
</p>

<p align="center">
  <strong>Five Markdown Files</strong> &nbsp;&bull;&nbsp;
  <strong>Zero Runtime</strong> &nbsp;&bull;&nbsp;
  <strong>Terminal-Bench 2.1 · 267 Graded Runs</strong> &nbsp;&bull;&nbsp;
  <strong>MIT License</strong>
</p>

---

You ask an agent to fix an off-by-one error in a parser.

It inspects nothing. It rewrites three files from scratch, wipes out your error handling, runs `ls -la` twenty times, launches background compilation loops it forgets about, and then proudly announces:

> *"Task complete! I have improved your architecture and verified everything works."*

It did not run the test suite. It did not check the exit code. It simply declared victory and went to sleep.

Every developer using agents has been there. Agents do not fail because they lack intelligence—they fail because they lack basic engineering discipline. When left unconstrained, they guess instead of investigating, rewrite entire files to tweak one line, spin in infinite polling loops, and declare tasks finished without checking.

**Supreme** gives your agent an engineering constitution: evidence instead of panic, surgical line diffs instead of file overwrites, verification instead of victory laps.

---

## What Supreme Actually Is

**Five markdown files.** No runtime, no hooks, no framework to adopt. Concatenated, they form one static prefix at the front of your agent's context—and it never moves. No mid-turn document loads. No on-demand skill ingestion. No context churn.

The benchmark put a number on that design choice. Measured as cache-read token volume across all 267 runs, the dynamic skill-loading arm accumulated **411.3M tokens** of documentation traffic—a **+39% context-churn tax** over the unprompted baseline. Supreme's static prefix ran **322.8M (+9%)**: **21.5% less context churn than dynamic skill loading**, with zero document loads mid-turn.

What it is not: not a framework. Not a fine-tune. Not a tool. Not dynamic documentation. Five files and the discipline to read them.

---

## Start Here. Make It Yours.

The standard reaction to an agent making mistakes is to pile on more: fifty-page operating manuals, orchestration frameworks, thousands of lines of procedural instructions. The result drowns in its own context and becomes slower and more confused.

Supreme goes the other way: **nine principles, one operating protocol, five files.** If you remember nothing else, the nine distill into four instincts:

1. **Evidence over assumption** &mdash; Read the file. Run the compiler. Look at the stack trace. Never guess when the environment can tell you the truth.
2. **Surgical diffs** &mdash; Touch only what is broken. If you are fixing line 42, leave lines 1&ndash;41 and 43&ndash;400 completely untouched.
3. **Proactive loop breaking** &mdash; If a command stalls or an approach fails twice, stop. Do not spin in polling loops or retry the exact same failing command.
4. **Proof mandatory** &mdash; Code generated is not task complete. Tests passing is not system correct. Prove it works before claiming it is done.

Start here. Treat this as your baseline. Understand what your workflow actually requires, prune what you do not need, and make it your own.

---

## The Behavioral Contrast

| The Unconstrained Trap | The Supreme Grounding |
|---|---|
| **Whole-File Blast Radius**: Overwrites hundreds of lines of working code to modify a single boolean, introducing silent regressions and breaking git history. | **Surgical Line Diffs**: Requires line-targeted edits (`replace_file_content`). If you are fixing line 42, the rest of the file stays untouched. |
| **The Polling Spin Trap**: Launches background tasks and repeatedly polls status hundreds of times without doing any meaningful work. | **Proactive Loop Breaking**: Detects stalling early, checks exit codes immediately, and halts circular tool loops. |
| **Trial-and-Error Scripting**: Authors 100+ disposable exploration scripts on open-ended combinatorial tasks—one documented benchmark task burned 3.51M tokens where 300k sufficed. | **Hypothesis-Driven Deliberation**: Forms a grounded hypothesis before executing. Solves the same task in 55 turns and 300k tokens—verified, then stopped. |
| **Premature Victory**: Assumes that because code was generated without a syntax crash, the task is complete. | **Proof Mandatory**: Code generated &ne; task complete. Tests passing &ne; system correct. Explicit verification evidence is required. |

---

## Three Runs That Explain the Whole Benchmark

Receipts from the audit ledger—every number below is verifiable in the [paper](paper/main.pdf) and the [cryptographic ledger](carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.md).

**Same task, same model, same arena.** On the Core Wars task, Supreme formed one hypothesis—a Silk/Replicator warrior—implemented it, verified the win rates, and left in **175 seconds and 300k tokens**. The dynamic skill arm authored **116 exploration scripts** over 27 minutes and 3.51 million tokens. Both passed. One of them read the problem first.

**44 minutes, nobody watching.** Windows 3.11 for Workgroups, installed autonomously inside headless QEMU—disks partitioned, FAT16 formatted, floppy images swapped, network drivers installed. **307 turns.** It finished.

**The polling gap.** Waiting on a background task, the unprompted agent immediately re-polls it **50.1%** of the time. Supreme: **28.6%**. That difference is one paragraph of protocol.

---

## The Receipt: 89 Environments, 267 Containers

We did not write these rules because they sound nice on paper. We wanted to see what actually happens when you put a disciplined agent into real, messy terminal environments against unconstrained agents.

We evaluated Supreme against an unprompted **Baseline** and the dynamic skill system **Superpowers by obra** across all 89 tasks of **Terminal-Bench 2.1** (267 containerized executions) under locked **Gemini 3.6 Flash High** (temperature = 0.0):

| Metric | Supreme (v1.0) | Superpowers by obra | Baseline (Unprompted) | Comparison |
|---|:---:|:---:|:---:|---|
| **Tasks Solved (N=89)** | **61 / 89 (68.5%)** | 58 / 89 (65.2%) | 55 / 89 (61.8%) | Highest observed completion rate |
| **Adjusted Pass Rate\*** | **70.9%** (61/86) | 67.4% (58/86) | 64.0% (55/86) | Adjusted for 3 upstream container defects |
| **Hard Tasks (N=30)** | **20 / 30 (66.7%)** | 16 / 30 (53.3%) | 17 / 30 (56.7%) | +13.4 pts over dynamic skill loading (p = 0.22, directional) |
| **Aggregate Runtime** | **15.15 Hours** | 18.30 Hours | 16.92 Hours | 17.2% lower latency than Superpowers |
| **Cost / Solved Task** | **$0.489** | $0.506 | $0.497 | Lowest modeled cost per successful solution |
| **Surgical Line Edits** | **42 diffs** | 9 diffs | &mdash; | 300 vs. 471 whole-file rewrites |

<sub>Note: Aggregate pass rate differences are not statistically significant (paired McNemar p > 0.05). Evaluated on Gemini 3.6 Flash High. Economic figures modeled on OpenRouter paid rates.</sub>

<p align="center">
  <img src="assets/macro_benchmark_summary.png" width="980" alt="Master Benchmark Overview">
</p>

### Master Scoreboard (89 Tasks &times; 3 Paradigms = 267 Evaluated Runs)

| Configuration | Raw Pass (N=89) | Raw Pass (95% CI) | Adjusted Pass (N=86)* | Total Compute Time | Thinking Tokens / Task |
|---|:---:|:---:|:---:|:---:|:---:|
| **Supreme (v1.0)** | **61 / 89** | **68.5%** [58.3%, 77.2%] | **70.9%** [60.6%, 79.5%] | **15.15h** | **20,591** |
| Superpowers by obra | 58 / 89 | 65.2% [54.8%, 74.3%] | 67.4% [57.0%, 76.4%] | 18.30h | 19,198 |
| Baseline (Unprompted) | 55 / 89 | 61.8% [51.4%, 71.2%] | 64.0% [53.4%, 73.3%] | 16.92h | 19,893 |

<sub>*Adjusted scores exclude three tasks with verified upstream container defects (<code>prove-plus-comm</code>, <code>caffe-cifar-10</code>, <code>torch-pipeline-parallelism</code>). Brackets report Wilson 95% score confidence intervals.</sub>

*One model, one run per task, temperature zero. The 3-task margin between Supreme and Superpowers is within run-to-run noise—the McNemar tests say so, and we say so too. What held up across all 267 runs was the behavior: deliberation, tool discipline, polling, context churn.*

<p align="center">
  <img src="assets/fig2_markov_tool_state_transitions.png" width="880" alt="Markov Tool State Transitions">
</p>

### What the Data Actually Showed

1. **Deliberation on Hard Tasks**: On the 30 hardest tasks in the suite, Supreme prompted **+66% higher internal deliberation** (28,271 thinking tokens/task vs. 17,035 on Medium), holding a 66.7% pass rate (20/30) compared to 53.3% (16/30) for Superpowers and 56.7% (17/30) for Baseline—a directional lead, not a confirmed one (McNemar p = 0.22).
2. **Evaluated Unit Economics**: Supreme achieved the lowest modeled cost per successful task (**$0.489**), roughly **3.4% below Superpowers ($0.506)**, while solving three additional tasks (61 vs. 58). In absolute terms, Baseline spent the least overall ($27.33) and had the lowest cost per attempt ($0.307).
3. **Surgical Editing in Practice**: Supreme performed 42 targeted surgical line replacements versus 9 for Superpowers, with 300 whole-file overwrites against Superpowers' 471 across the benchmark.
4. **Escaping the Polling Spin Trap**: While Baseline fell into command-polling spin traps 50.1% of the time and Superpowers logged 299 repetitive polling loops (42.7%), Supreme reduced uninformative polling loops to **28.6%**.
5. **Context Economics**: Dynamically loading procedural documentation on demand accumulated **411.3 Million cache-read tokens** under Superpowers—a **+39% context-churn tax** over the unprompted baseline. Supreme's static prefix: **322.8 Million (+9%)**. No mid-turn document loads, no documentation thrashing.

<details>
<summary><strong>How we measured—and what we'd do differently</strong></summary>

Supreme went through two earlier benchmark generations before this one. CARB-v2 (50 tasks) hit a ceiling—the model solved 92–94% of everything across all configurations, so the architecture didn't matter (paired McNemar p = 1.0). CARB-v3 pre-selected tasks the baseline had already failed—a circular design we abandoned. CARB-v4 evaluates the complete, unmodified 89-task corpus of Terminal-Bench 2.1 with no selection.

Known limits, stated plainly: one foundation model (Gemini 3.6 Flash High, &tau; = 0.0), one run per task, and structure confounded with content—Supreme and Superpowers differ in delivery mechanism <em>and</em> in what they teach. Multi-model replication and controlled ablations are Iteration 2.

Three tasks with verified upstream container defects (<code>prove-plus-comm</code>, <code>caffe-cifar-10</code>, <code>torch-pipeline-parallelism</code>) are excluded from the adjusted cohort (N = 86); a fourth (<code>torch-tensor-parallelism</code>) is additionally excluded in the conservative cohort (N = 85).

</details>

---

## The Constitution in Practice

The complete engineering constitution lives in [`SupremeAgent/constitution.md`](SupremeAgent/constitution.md): **nine invariant principles**, from *Evidence Over Assumption* to *Consequential Actions Require Proportional Accountability*, plus six named anti-patterns (*progress theater*, *assumption cascade*, *scope explosion*&hellip;).

The [operating protocol](SupremeAgent/operating-protocol.md) carries the machinery: risk-scaled planning, failure classification (CODE / ENVIRONMENT / TOOL / EXTERNAL / UNKNOWN), and loop management—the source of instinct #3 above. It ends with the best rule in the file:

> **"BLOCK is a valid, successful outcome. It is better than guessing."**

---

## Universal Agent Integration

Supreme runs anywhere your agent reads a rule file or a system prompt—**Claude Code**, **Cursor**, **Codex**, **Zed**, **Gemini / Antigravity**, and anything that speaks `AGENTS.md`.

```bash
# Option A — the distilled digest (what this repository itself runs)
cp AGENTS.md /path/to/your/project/

# Option B — the full five-file engine (the configuration the benchmark measured)
cat SupremeAgent/constitution.md SupremeAgent/operating-protocol.md \
    SupremeAgent/sub-agent-profiles.md SupremeAgent/environment-profile.md \
    SupremeAgent/persistent-state.md > SUPREME.md
```

Drop `AGENTS.md` into your repository root (auto-discovered by most hosts), or point your host's global rule file at `SUPREME.md`.

---

## Research Paper & Cryptographic Ledgers

Every graded run carries a SHA-256 verifier hash, a telemetry record, and a written dossier. The scoreboard is re-derivable from the committed artifacts:

* **Research Paper:** [`paper/main.pdf`](paper/main.pdf) &mdash; 10-page academic manuscript with full statistical analysis, Wilson confidence intervals, paired McNemar tests, cost economics&mdash;and the null results.
* **Cryptographic Ledger:** [`carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.md`](carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.md) &mdash; SHA-256 verifier logs and execution timestamps for all 267 container sessions.
* **Deep Telemetry Dossiers:** Located in [`carb_benchmark/results_v4/extraction_findings/`](carb_benchmark/results_v4/extraction_findings/) covering Markov transitions, polyglot performance, thinking token dynamics, and token sinks.

---

## FAQ

**Is this a framework?**
No. It is five markdown files. There is nothing to build, import, or update.

**Does it work with other models?**
Untested. The benchmark locked one model at temperature zero. The constitution is model-agnostic prose—if you run it elsewhere, you now know exactly how to measure it.

**Why not just write my own rules?**
You should. Supreme is a baseline you prune, not a gospel you obey.

**Why "Supreme"?**
Because somewhere between *please be careful* and *verify everything*, the agent needed to hear it from an authority.

---

## License

[MIT](LICENSE). The constitution is yours to amend.
