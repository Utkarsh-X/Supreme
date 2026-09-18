# 📑 CARB-v4 Executive Findings Index: The Empirical Dossier Suite
### Deep-Telemetry Mining Across 267 Canonical Terminal-Bench 2.1 Runs

---

## Welcome to the CARB-v4 Forensic Investigation Suite

This directory contains the complete, unredacted forensic findings excavated from the **267 canonical runs of CARB-v4 (Terminal-Bench 2.1)** evaluated on **Gemini 3.6 Flash High**. 

Across 32.3 MB of step-by-step execution transcripts, 16,000+ tool invocations, and 100+ million cumulative tokens, we examine the true behavioral, cognitive, and economic differences between:
* **Supreme (v1.0)**: Constitutional Agent Architecture (Static principles, hierarchical planning, surgical edits, verification guardrails).
* **Superpowers by obra**: Dynamic Skill Loading System authored by Jesse Vincent (`obra/superpowers`).
* **Baseline**: Unprompted Gemini 3.6 Flash High foundation.

---

## 🧭 Master Navigation: The 5 Specialized Dossiers

| Dossier | Core Focus & Scientific Scope | Key Quantitative Takeaway |
|:---|:---|:---|
| 📄 **[Dossier 01: Tool Ecology & Behavioral Dynamics](01_TOOL_ECOLOGY_AND_BEHAVIORAL_DYNAMICS.md)** | Tool frequencies, Read-to-Write ratios, surgical line edits vs. destructive rewrites. | **Supreme read 2.06 tools per write** (investigation before mutation), performed **42 surgical line edits** (`replace_file_content`), and cut destructive overwrites by 57%. |
| 📄 **[Dossier 02: Cognitive Scaling & Thinking Dynamics](02_COGNITIVE_SCALING_AND_THINKING_DYNAMICS.md)** | Gemini internal chain-of-thought (`thinking_tokens`), Hard-task scaling, overthinking traps, and breakthrough passes. | **Hard-Task Deliberation Pattern**: Supreme scaled thinking by **+66%** on Hard tasks, achieving a **+13.4-point win-rate advantage (66.7% vs 53.3%; McNemar p = 0.22, directional)** over Superpowers. |
| 📄 **[Dossier 03: Polyglot Stacks & Low-Level Systems](03_POLYGLOT_STACKS_AND_LOW_LEVEL_SYSTEMS.md)** | Evaluation across 5 technical stacks (C/C++, QEMU, Python, Scheme, COBOL, PyTorch) and the 89-Task Venn Partition. | **Low-Level Dominance**: Supreme led Low-Level Systems (**70.0% vs 60.0%**) and SysAdmin (**86.7% vs 73.3%**). **The Esoteric Anomaly**: Baseline led in COBOL/Scheme (85.7%). |
| 📄 **[Dossier 04: Error Spiraling & Resilience](04_ERROR_SPIRALING_AND_COGNITIVE_RESILIENCE.md)** | Post-failure Markov transitions ($P(\text{Next} \mid \text{Error})$), the "Task Polling Spin Trap", and recovery rates. | **Resilience**: Supreme converted errors to PASS **76.91% of the time**. Cut passive background task polling from 50.1% down to 28.6% (saving 179 wasted turns). |
| 📄 **[Dossier 05: Token Sinks, Cache Taxes & Anomalies](05_TOKEN_SINKS_PROMPT_CACHING_AND_ANOMALIES.md)** | Token decomposition, 115M prompt cache tax, terminal stdout blowouts, 104 verifier peekers, and container bugs. | **Cache Tax**: Dynamic skill loading cost **411.3M cache read tokens** (+115.4M over Baseline). Transcripts captured 104 verifier reverse-engineering attempts. |

---

## 📊 Grand Master Comparison Matrix

```
┌─────────────────────────────────────┬──────────────────┬──────────────────┬──────────────┐
│ Metric                              │ Supreme (v1.0)   │ Superpowers-v4.0 │ Baseline     │
├─────────────────────────────────────┼──────────────────┼──────────────────┼──────────────┤
│ 🏆 Benchmark Pass Rate              │ **61/89 (68.5%)**│ 58/89 (65.2%)    │ 55/89 (61.8%)│
│ ⏱️ Total Wall-Clock Latency         │ **15.15 hrs** 🥇 │ 18.30 hrs        │ 16.92 hrs    │
│ 🧠 Total Thinking Tokens (Gemini)   │ **1,832,603** 🥇 │ 1,708,628        │ 1,770,506    │
│ 📈 Hard-Task Win Rate (N=30)        │ **66.7% (20/30)**│ 53.3% (16/30)    │ 56.7% (17/30)│
│ 🔍 Read-to-Write Ratio              │ **2.06** 🥇      │ 1.59             │ 1.59         │
│ ✂️ Surgical Edits (replace_content) │ **42** 🥇        │ 8                │ 10           │
│ 📝 Full File Overwrites (write_to)  │ **300** 🥇       │ 471 (57% higher) │ 338          │
│ 🔄 Task Polling Re-poll Probability │ **28.6%** 🥇     │ 42.7% (299 loops)│ 50.1%        │
│ 🛠️ Low-Level Systems Pass Rate      │ **70.0% (14/20)**│ 60.0% (12/20)    │ 65.0% (13/20)│
│ 🖥️ SysAdmin & OS Pass Rate          │ **86.7% (13/15)**│ 73.3% (11/15)    │ 73.3% (11/15)│
│ 💰 Cache Read Tokens Incurred       │ 318.4 Million    │ **411.3 Million**│ 295.9 Million│
└─────────────────────────────────────┴──────────────────┴──────────────────┴──────────────┘
```

---

## 📁 Source Datasets
* **Machine-Readable Telemetry**: [`canonical_267_deep_telemetry.json`](canonical_267_deep_telemetry.json) (789 KB, all 267 runs structured).
* **Comprehensive Mining Report**: [`UNEARTHED_SIGNALS_AND_LATENT_PATTERNS.md`](UNEARTHED_SIGNALS_AND_LATENT_PATTERNS.md) (50 KB, raw excavation findings).
* **Cryptographic Verification Ledger**: [`../FORENSIC_AUDIT_LEDGER.md`](../FORENSIC_AUDIT_LEDGER.md) (SHA-256 verifier hashes for all runs).
