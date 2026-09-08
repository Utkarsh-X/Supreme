# Supreme Agent Architecture

Supreme is a constitutional, static-grounding framework for autonomous AI software engineering agents. Rather than dynamically paging procedural documentation in and out of the prompt, Supreme establishes an invariant engineering constitution, structured operating protocols, and specialized sub-agent profiles in the system prompt.

---

## 🏛 Architectural Structure

The Supreme agent architecture consists of five core components:

1. **[`constitution.md`](constitution.md) — Engineering Constitution**  
   The foundational behavioral contract defining the 9 invariant principles:
   - *Evidence Over Assumption*
   - *User Intent Is Authoritative*
   - *Preserve System Integrity*
   - *Minimum Justified Change*
   - *Completion Requires Evidence*
   - *Uncertainty Must Be Explicit*
   - *Plans and Decisions Are Revisable Hypotheses*
   - *Scrutiny Scales With Risk*
   - *Consequential Actions Require Proportional Accountability*

2. **[`operating-protocol.md`](operating-protocol.md) — Operational Decision Framework**  
   Guidance for task decomposition, risk-scaled planning, surgical code editing boundaries, failure classification, debugging discipline, and completion criteria.

3. **[`sub-agent-profiles.md`](sub-agent-profiles.md) — Specialist Delegation Profiles**  
   Formal contracts for bounded sub-agents:
   - `Researcher`: Fact-finding, codebase reconnaissance, and dependency inspection.
   - `Implementer`: Bounded, surgical execution of an approved plan.
   - `Debugger`: Root-cause diagnosis without speculative edits.
   - `Reviewer`: Adversarial review and falsification of completed work.

4. **[`environment-profile.md`](environment-profile.md) — Runtime Grounding**  
   Definitions of the host system, tool environment, terminal shells, and execution boundaries.

5. **[`persistent-state.md`](persistent-state.md) — State Freshness & Memory Model**  
   Structured discipline for managing plans, hypotheses, and verification evidence across multi-turn sessions.

---

## 🚀 Usage

### 1. Universal Instruction File (`AGENTS.md` / `CLAUDE.md`)
In environments that read project-level instructions automatically (e.g. Antigravity, Claude Code, Cursor, Windsurf), you can link or embed the Supreme constitution directly in your repository's root [`AGENTS.md`](../AGENTS.md).

### 2. Direct System Prompt Integration
To embed Supreme into an API harness or custom runner:
```python
import os

SUPREME_FILES = [
    "constitution.md",
    "operating-protocol.md",
    "sub-agent-profiles.md",
    "environment-profile.md",
    "persistent-state.md"
]

def load_supreme_system_prompt(base_dir="SupremeAgent"):
    sections = []
    for fname in SUPREME_FILES:
        fpath = os.path.join(base_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            sections.append(f.read().strip())
    return "\n\n---\n\n".join(sections)
```

---

## 🔬 Benchmark Validation (Terminal-Bench 2.1 / CARB-v4)
Supreme was rigorously evaluated on **Terminal-Bench 2.1** across 89 diverse engineering, systems, and algorithmic tasks (267 total graded container runs). Full empirical results, audit logs, and comparative telemetry are documented in [`carb_benchmark/results_v4/`](../carb_benchmark/results_v4/).
