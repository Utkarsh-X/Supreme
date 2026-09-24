# Supreme Agent Guidance

Supreme is a five-document engineering skill for coding agents. The documents describe core principles, an operating protocol, specialist roles, environment grounding, and state management. Use the complete set together; do not treat the later documents as optional add-ons when applying Supreme as a skill.

## Documents

1. [Engineering constitution](constitution.md) — nine principles for evidence-led, bounded, responsible engineering work.
2. [Operating protocol](operating-protocol.md) — task planning, editing boundaries, verification, failure classification, and loop management.
3. [Specialist roles](sub-agent-profiles.md) — bounded responsibilities for research, implementation, debugging, and review.
4. [Environment profile](environment-profile.md) — host, tool, shell, and execution context.
5. [Persistent state](persistent-state.md) — maintaining fresh plans, hypotheses, and verification evidence across turns.

## Using the guidance

For the installable Agent Skill, start at [`skills/supreme/SKILL.md`](../skills/supreme/SKILL.md). Its load protocol instructs the agent to read all five packaged documents in full before acting. The packaged documents retain their full text and link back to the entrypoint for navigation. Adapt host-specific commands, permissions, and repository conventions before use; these documents provide guidance rather than runtime enforcement.

For single-file use, load [`supreme.md`](../supreme.md), the complete integrated guide.

The project-level [AGENTS.md](../AGENTS.md) shows one integrated application of the principles. For the complete study context, see the [research paper](../paper/main.pdf).

## Evaluation context

The paper reports an evaluation across all 89 Terminal-Bench 2.1 tasks, with three configurations and 267 isolated evaluations. It provides the methods and aggregate findings. The task corpus, run-level traces, and full evaluation pipeline are not included in this release.

Supreme is released under the repository's [MIT License](../LICENSE).
