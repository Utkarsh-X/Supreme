# Supreme Agent Guidance

Supreme is a five-document engineering skill for coding agents. Together, the documents describe core principles, an operating protocol, optional specialist roles, environment grounding, and state management. They are intended to be adapted as project-level guidance or agent instructions.

## Documents

1. [Engineering constitution](constitution.md) — nine principles for evidence-led, bounded, responsible engineering work.
2. [Operating protocol](operating-protocol.md) — task planning, editing boundaries, verification, failure classification, and loop management.
3. [Specialist roles](sub-agent-profiles.md) — bounded responsibilities for research, implementation, debugging, and review.
4. [Environment profile](environment-profile.md) — host, tool, shell, and execution context.
5. [Persistent state](persistent-state.md) — maintaining fresh plans, hypotheses, and verification evidence across turns.

## Using the guidance

Start with the constitution and operating protocol. Add the other documents when their guidance fits your agent and workflow. Adapt host-specific commands, permissions, and repository conventions before use; these documents provide guidance rather than runtime enforcement.

The project-level [AGENTS.md](../AGENTS.md) shows one integrated application of the principles. For the complete study context, see the [research paper](../paper/main.pdf).

## Evaluation context

The paper reports an evaluation across all 89 Terminal-Bench 2.1 tasks, with three configurations and 267 isolated evaluations. It provides the methods and aggregate findings. The task corpus, run-level traces, and full evaluation pipeline are not included in this release.

Supreme is released under the repository's [MIT License](../LICENSE).
