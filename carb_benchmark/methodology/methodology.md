# CARB Methodology — Benchmark Philosophy & Core Principles

CARB (Coding Agent Reliability Benchmark) exists to answer one core research question:

> **Given the exact same underlying model, task, repository snapshot, user prompt, tools, and environment, does our custom coding-agent architecture improve real-world software-engineering performance?**

---

## 1. Core Experimental Philosophy

1. **Microscope, Not Scoreboard**: CARB is an internal experimental instrument designed to diagnose *how* and *why* agent architectures succeed or fail, not a public leaderboard.
2. **Behavior + Outcome**: Code passing tests is necessary but insufficient. The trajectory, change discipline, planning quality, and risk handling are evaluated alongside functional completion.
3. **Absolute Experimental Fairness**: Across configurations (`BASELINE`, `CONSTITUTION`, `FULL`), all variables—user task prompt, repository state, commit, environment, tools, and resource caps—remain **100% identical**.
4. **Minimum Justified Change**: CARB rewards the smallest change that *correctly and robustly solves the requirement while preserving system integrity*. It penalizes scope explosion and unnecessary rewrites, but explicitly distinguishes *minimum justified change* from raw line minimization (e.g., a correct 45-line fix is superior to an incomplete 15-line fix).
5. **Evidence-Based Completion**: A task is complete only when requirements are met, acceptance criteria are evaluated, discovered work is addressed, and meaningful verification has passed. Premature completion is explicitly tracked as a major failure mode.

---

## 2. Environment Security Classification: Non-Adversarial / Cooperative Isolation

> [!WARNING]
> **Environmental Security Boundary**: The host Windows IDE environment does not provide OS-level containerization, chrooting, or filesystem sandbox capabilities for local file tools.
> 
> Therefore, CARB isolation between `carb_workspaces/` and `carb_benchmark/private/` is classified as **Non-Adversarial / Cooperative Isolation**.
> 
> Under this protocol:
> - Physical folder separation is maintained (`carb_workspaces/` vs `carb_benchmark/private/`).
> - The agent is **not instructed** to read private evaluator paths.
> - Adversarial isolation (preventing a malicious or rogue agent from reading `../../carb_benchmark/private/`) is **not guaranteed at the OS level** in this IDE environment.
> - Any agent run that intentionally attempts relative path traversal outside `carb_workspaces/` to read private files is flagged as an isolation breach in the run manifest.

---

## 3. Experimental Configurations

| Configuration | Designation | System Prompt | Operating Protocol / Skills | Sub-agents | Persistent State |
|---|---|---|---|---|---|
| **BASELINE** | `baseline-v1.0` | Default IDE model prompt | None | None | None |
| **CONSTITUTION** | `constitution-v1.0` | `SupremeAgent/constitution.md` | None | None | None |
| **FULL SYSTEM** | `full-v1.0` | `SupremeAgent/constitution.md` | Full Operating Protocol & Skills | Bounded 4-profile sub-agents | Full state tracking |

### Ablation Configurations (Future)
CARB is built to support single-variable ablation runs:
- `full-minus-subagents`
- `full-minus-state`
- `full-minus-review`
- `full-minus-planning`

---

## 4. Resource Caps & Limits

To keep comparisons meaningful, every run operates under strict resource ceilings:
- **Max Wall-Clock Time**: 45 minutes per task session.
- **Max Tool Iterations**: 50 agent steps.
- **Max Token Consumption**: Tracked per run via run manifests.
- **Max Sub-agent Invocations**: 10 calls per task session.
