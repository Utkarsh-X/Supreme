<p align="center">
  <img src="assets/banner.png" width="800" alt="Supreme">
</p>

<h1 align="center">Supreme</h1>

<p align="center"><strong>A practical engineering playbook for coding agents.</strong></p>

<p align="center">Inspect first · Change deliberately · Verify before done</p>

---

Supreme is a compact engineering skill for coding agents working in existing software projects. It gives agents a disciplined way to inspect a system, plan in proportion to risk, make justified changes, verify outcomes, and report uncertainty clearly.

The guidance is written in five Markdown documents. Use it as project-level agent guidance or adapt it to the instruction format of your agent. It requires no runtime, hooks, or benchmark framework.

## Start using Supreme

Begin with the [engineering constitution](SupremeAgent/constitution.md) and [operating protocol](SupremeAgent/operating-protocol.md). The remaining documents cover [specialist roles](SupremeAgent/sub-agent-profiles.md), [environment grounding](SupremeAgent/environment-profile.md), and [persistent state](SupremeAgent/persistent-state.md). The [SupremeAgent guide](SupremeAgent/README.md) explains how the pieces fit together.

Adapt the instructions to your repository, tools, and host environment. The project-level [AGENTS.md](AGENTS.md) shows how Supreme is applied in this repository.

## Evaluation snapshot

The research study compared Supreme, Superpowers by obra, and an unprompted baseline on all 89 Terminal-Bench 2.1 tasks: 267 isolated evaluations, with one run per task and configuration. All configurations used Gemini 3.6 Flash High through Google's API, Claude Code as the execution client, and zero temperature.

| Measure | Supreme | Superpowers by obra | Baseline |
|---|---:|---:|---:|
| Tasks completed (89) | **61 (68.5%)** | 58 (65.2%) | 55 (61.8%) |
| Adjusted completion¹ (86) | **61 (70.9%)** | 58 (67.4%) | 55 (64.0%) |
| Hard tasks completed (30) | **20 (66.7%)** | 16 (53.3%) | 17 (56.7%) |
| Aggregate wall-clock time | **15.15 h** | 18.30 h | 16.92 h |
| Modeled cost per successful task² | **$0.489** | $0.506 | $0.497 |

<p align="center">
  <img src="assets/macro_benchmark_summary.png" width="980" alt="Comparison of task completion, aggregate wall-clock time, modeled cost per successful task, and hard-task results">
</p>

¹ Adjusted completion excludes three tasks with verified upstream environment defects. ² Cost is estimated using the recorded OpenRouter rate schedule; it is not a reported transaction charge.

Paired tests did not distinguish aggregate completion differences at conventional significance levels (all p-values above 0.05). The hard-task result is directional (paired p = 0.22). The evaluation compares complete configurations with different guidance content and delivery, so it does not isolate the effect of any single design choice. Findings are limited to this model and one run per task/configuration.

## Research paper and release scope

The [research paper](paper/main.pdf) describes the study, methods, aggregate results, confidence intervals, statistical analysis, and limitations. The benchmark is an evaluation study, not a released benchmark framework. This release does not include the task corpus, run-level traces, or full evaluation pipeline.

## License

Supreme is released under the [MIT License](LICENSE).
