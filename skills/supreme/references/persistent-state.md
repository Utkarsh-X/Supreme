# Persistent State

For non-trivial tasks, externalize this snapshot through the host's task or session state mechanism when available. Otherwise, keep it in active context; create a workspace scratch file such as `.supreme/state.md` only when the user or repository explicitly permits it and the file is excluded from version control. Never commit the state file unless requested. Update it at meaningful boundaries — after investigation, after planning, after each major implementation step, after verification, after discovery of new requirements, and after reorientation.

This is a snapshot, not a log. Keep it compact. Its purpose is context recovery — not documentation.

---

## Objective

[What are we trying to accomplish? One clear statement.]

## Requirements & Acceptance Criteria

- [ ] [Observable success condition derived from the objective]
- [ ] [Additional criteria discovered during investigation]

## Constraints

- [What must not change or be violated]
- [Explicit boundaries on the work]

## Verified Facts

- [Fact] — Source: [file / command / observation]
- [Fact] — Source: [file / command / observation]

## Assumptions

- [Assumption] — Rationale: [why this is reasonable]

## Unknowns

- [What remains uncertain and may affect the work]

## Risks

- [Risk description] — Severity: [LOW / MEDIUM / HIGH] — Status: [open / mitigated]

## Active Plan

[Current high-level approach — what are the major steps?]

### Active Subplan

[Current detailed work — what specific step are we executing?]

## Decisions

- [Decision] — Confidence: [HIGH / MEDIUM / LOW] — Reason: [evidence or rationale]

## Interpretations

- [Interpretation] — Confidence: [HIGH / MEDIUM / LOW] — Evidence: [source]

## Completed Work

- [x] [What has been verified as done — not just attempted]

## Discovered Work

- [ ] [Additional necessary work found during implementation — must be resolved or explicitly deferred]

## Failed Approaches

- [What was tried] → [Why it didn't work] → [What was learned]

## Next Justified Action

[What should happen next and why it is the right next step.]

## Last Known Good State

[Description of the last verified working state — what can we safely return to if something goes wrong.]

---

## Integrated guide

Return to the [Supreme Skill entrypoint](../SKILL.md), which loads all five components together.
