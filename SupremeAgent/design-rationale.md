# Supreme — Design Rationale

This document explains why the Supreme system is structured the way it is, how the components connect, and what failure modes remain. It is written for the human who maintains the system, not for the model that operates within it.

---

## Core Insight

The Supreme system does not attempt to make a model smarter. It creates conditions under which the model's existing intelligence is used deliberately, responsibly, and effectively.

### Design Invariant: Intelligence Preservation

The system must constrain harmful behavior without unnecessarily constraining useful reasoning, creativity, or legitimate initiative. Harness constraints exist to unlock intelligence, not to enforce bureaucracy.

The fundamental approach is to **convert knowledge problems into verification problems**. A weak model may not know the correct API signature — but it can inspect the repository and find it. A weak model may not recognize a subtle regression — but it can run tests and analyze failures. The system forces investigation where the model's instinct would be to guess.

The second insight is that **the harness matters independently of the model**. Research consistently shows that agent scaffolding — planning, verification, tool use, retry logic — can materially change outcomes even when the underlying model is held constant. This system is that scaffold, formalized as an engineering discipline.

---

## Why Six Components

The system is separated into six files because they serve different purposes and change at different rates:

| Component | Purpose | Audience | Stability |
|---|---|---|---|
| **Constitution** | Behavioral laws | Model (permanent) | Never changes |
| **Operating Protocol** | Decision framework | Model (reference) | Rarely changes |
| **Environment Profile** | Capabilities and tools | Model (permanent) | Changes per environment |
| **Persistent State** | Working memory | Model (read/write) | Changes per task |
| **Sub-Agent Profiles** | Specialist definitions | Model (when delegating) | Rarely changes |
| **Design Rationale** | Architecture explanation | Human (reference) | Updated with architecture |

This separation achieves several important properties:

- **The constitution never changes.** It contains zero environment-specific, domain-specific, or task-specific content. Moving between IDEs, languages, or projects requires no constitution changes.
- **The environment profile is swappable.** When moving from one IDE to another, only this file changes.
- **The persistent state is disposable per task.** It carries no architectural weight.
- **The protocol can evolve.** Improved procedures don't require rewriting behavioral principles.

### Why not fewer files?

Merging constitution + protocol would create a single document too large for a weak model to reliably retain as permanent context. Separation allows loading the protocol on demand.

### Why not more files?

The original conversation proposed separate files for planning, execution, verification, risk, and completion protocols, plus separate critic files. This fragments context unnecessarily. The operating protocol contains all of these as sections — a weak model can navigate to the relevant section without needing agent hops between files.

---

## Why Nine Principles

The source conversation contains approximately 68 distinct ideas about how the agent should behave. Many are duplicates or near-duplicates (e.g., "don't rush," "kill the completion reflex," and "anti-premature-closure" all express Principle 5).

The nine principles were derived as the **minimal generative set** — the smallest collection from which every desired behavior follows. The test: for every specific behavior mentioned in the source conversation, at least one principle directly generates it.

Verification of coverage:

| Desired Behavior | Generating Principle(s) |
|---|---|
| Explicit acceptance criteria | 5 (completion requires evidence) |
| Surgical / minimum-justified editing | 4 (minimum justified change) |
| Action-risk assessment | 8 (scrutiny scales with risk) |
| External side-effect gates | 9 (consequential actions require accountability) |
| State freshness | 1 (evidence over assumption — stale state is an assumption) |
| Escalation / blocking | 9 + 6 (accountability + explicit uncertainty) |
| Context reorientation | 1 + 6 (evidence + explicit uncertainty) |
| Provenance | 1 (evidence — know where facts come from) |
| Decision reversal | 7 (plans and decisions are revisable) |
| Required vs. valuable vs. optional | 2 (user intent is authoritative) |
| Bounded delegation | 9 (consequential actions require accountability) |
| System integrity | 3 (preserve system integrity) |
| Environment / tool awareness | 1 (evidence) + environment profile |
| Discovered work tracking | 5 (completion requires evidence) + protocol |
| Compute allocation | 1 (evidence over assumption — spend compute on evidence) |

No behavior is orphaned. All nine principles earn their place.

### Why six anti-patterns?

The six anti-patterns address the specific, predictable failure modes of weak coding models. They are not derivable from the principles alone — a model could theoretically follow all nine principles and still fall into "progress theater" or "environment confusion" because those are failure modes of model behavior, not violations of engineering principle. Making them explicit gives the model concrete patterns to watch for in its own behavior.

---

## How the Components Connect

### Normal Task Flow

```
User Request
     │
     ▼
Constitution (permanent behavioral laws)
     │
     ▼
Operating Protocol → Risk Assessment → Depth Selection
     │
     ▼
Environment Profile (what tools and capabilities exist)
     │
     ▼
Investigation / Planning / Execution / Verification
     │
     ▼
Persistent State (updated at meaningful boundaries)
     │
     ▼
Sub-Agents (when delegation is beneficial)
     │
     ▼
Completion Audit
```

### Sub-Agent Invocation

```
Parent identifies bounded task for delegation
     │
     ▼
Select profile: Researcher / Implementer / Debugger / Reviewer
     │
     ▼
Construct task packet:
  - Constitution
  - Relevant protocol section
  - Role profile
  - Bounded task description
  - Necessary context and evidence
     │
     ▼
Sub-agent executes within bounds
     │
     ▼
Sub-agent returns evidence-rich output
     │
     ▼
Parent evaluates result
     │
     ▼
Parent makes consequential decisions
```

### State Lifecycle

1. **Created** when a non-trivial task begins.
2. **Updated** after investigation, planning, implementation, verification, or discovery.
3. **Read** during reorientation or after context compaction.
4. **Discarded** when the task is complete.

The state is always a compact snapshot — never a full history.

### Reorientation Flow

```
Uncertainty or context loss detected
     │
     ▼
Read persistent state
     │
     ▼
Reconstruct: objective, constraints, plan, progress, unknowns
     │
     ▼
Verify reconstruction against available evidence
     │
     ▼
Resume or replan
```

---

## Architectural Provenance

Three mechanisms from the source conversation required formalization beyond their original discussion. These are not new ideas — they are operationalizations of ideas that were discussed but not yet given concrete form:

1. **Environment-independent constitution**: The conversation proposed separating environment from behavior but did not make the separation architecturally explicit. The current system ensures the constitution contains zero environment-specific references.

2. **Failure classification**: The conversation discussed the danger of confusing environment failures with code bugs but did not provide a classification framework. The current system includes a concrete taxonomy (CODE / ENVIRONMENT / TOOL / EXTERNAL / UNKNOWN) in both the protocol and the environment profile.

3. **Loop-stopping criteria**: The conversation acknowledged the risk of infinite self-review but did not provide operational stopping conditions. The current system defines concrete criteria: stop when repeated work produces no meaningful new information.

---

## Known Failure Modes

### Mitigated Risks

| Failure Mode | Mitigation | Residual Risk |
|---|---|---|
| Premature completion | Acceptance criteria + discovered work tracking + completion audit + anti-premature-closure question | Model may satisfy the audit superficially |
| Assumption cascade | Explicit uncertainty tracking (unknown / assumed / inferred / verified) | Model may not update uncertainty state diligently |
| Scope explosion | Work classification (required / valuable / optional / out of scope) | Model may misclassify "interesting" as "required" |
| Plan rigidity | Plans-as-hypotheses principle + decision reversal | Sunk-cost reasoning is deeply ingrained |
| Environment confusion | Failure classification taxonomy | Model may not correctly classify ambiguous failures |
| Infinite loops | Loop-stopping criteria in every recursive mechanism | Model may not recognize diminishing returns |
| Timid behavior | Risk scaling + explicit permission to skip procedures + trivial-task collapse | Overemphasis on caution could still slow simple tasks |
| Context loss | Persistent state + reorientation protocol | State may drift from reality if not updated consistently |
| Stale information | State freshness checks before consequential actions | Model may skip freshness checks |

### Accepted Risks

| Failure Mode | Why Accepted |
|---|---|
| Model ignores principles in very long contexts | Mitigated by persistent state and reorientation. Cannot fully prevent without model-level changes. |
| Sub-agent draws wrong conclusion from limited context | Mitigated by evidence-rich output requirements. Parent can investigate. Cannot guarantee without giving full context (which defeats context compression). |
| Model treats protocol as rigid checklist | Mitigated by explicit anti-proceduralism language and behavioral balance clause. Cannot fully prevent; this is a model-level tendency. |
| Correlated hallucination across planning passes | Partially mitigated by adversarial review perspective. Full mitigation requires perspective-separation techniques that add significant complexity. |

### Deliberately Excluded

| Idea from Source Conversation | Why Excluded |
|---|---|
| Domain-specific instructions | Violates "general-purpose" design goal. The principles apply to all domains. |
| Personality / persona simulation | Engineering discipline, not character acting. Personas add no reliability. |
| Formal compute budgets | Too rigid. "Scale with risk" is more adaptive and model-friendly. |
| Self-awareness / meta-reflection layers | Adds complexity without proportional benefit. Risk of infinite self-review. |
| More than four sub-agent types | Insufficient evidence they are needed. Can be added later if benchmarking shows a bottleneck. |
| Elaborate transaction / rollback framework | Host environment typically provides checkpointing. Agent needs only basic recovery awareness. |
| Benchmarking system | Valuable but separate project. Not part of the behavioral system itself. |

---

## Design Tests Performed

Before implementation, the architecture was evaluated against three critical questions:

### 1. Could a weak model follow every instruction perfectly and still produce worse work?

**Finding**: Yes, if it treats the protocol as a rigid checklist for trivial tasks. **Mitigation**: The constitution's behavioral balance clause explicitly permits skipping irrelevant procedures. The protocol opens with "For trivial tasks, collapse to: understand → execute → verify." Risk scaling ensures light treatment for simple work.

### 2. Could the agent use this architecture to justify stopping too early?

**Finding**: A model could derive shallow acceptance criteria and then declare them met. **Mitigation**: The anti-premature-closure question ("if this were falsely claiming to be complete, what would I have overlooked?") directly targets shallow criteria. The discovered-work mechanism prevents ignoring requirements that emerged during investigation.

### 3. Could the system make the agent too timid?

**Finding**: Nine principles emphasizing caution could create paralysis. **Mitigation**: Principle 8 (scrutiny scales with risk) is the primary defense, explicitly stating "no more cautious than necessary." The behavioral balance clause gives explicit permission to finish quickly when tasks are trivial. The anti-patterns do not include "making changes" — they target specific bad behaviors, not the act of editing code.

---

## Compression Analysis

The final system was evaluated for removability:

> *Could 20% be removed without materially reducing behavioral guarantees?*

**Finding**: No. Each component serves a distinct purpose:
- Removing any principle orphans at least one important behavior.
- Removing any anti-pattern loses explicit defense against a known failure mode.
- Removing any protocol section loses operational guidance for a critical decision moment.
- Removing any sub-agent profile eliminates a fundamental engineering activity.
- Removing the environment profile re-contaminates the constitution with environment specifics.
- Removing persistent state eliminates the primary context-recovery mechanism.

The system is at or near its minimal viable size for the behavioral guarantees it provides.
