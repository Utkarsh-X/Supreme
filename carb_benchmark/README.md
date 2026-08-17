# CARB — Coding Agent Reliability Benchmark

CARB (Coding Agent Reliability Benchmark) is an internal, reproducible, IDE-based experimental framework designed to evaluate whether custom coding-agent architectures (system prompts, constitutions, operating protocols, skill architectures, sub-agent delegation, and state tracking) genuinely improve software-engineering performance and reliability over base model baselines.

---

## 1. System Architecture & Physical Isolation

To ensure absolute experimental fairness and prevent benchmark contamination, CARB enforces a strict **three-tier physical isolation model**:

```text
e:/RofU/Supreme/
│
├── SupremeAgent/                  ← System Under Test (IMMUTABLE during benchmark)
│
├── carb_benchmark/                ← Benchmark Control Plane
│   ├── README.md                  ← This file
│   ├── design_reference/          ← Immutable design conversation reference
│   ├── methodology/               ← Methodology, evaluation layers, failure taxonomy
│   ├── protocol/                  ← Execution, reset, clarification, & pilot protocols
│   ├── sources/                   ← Dataset acquisition specs (SWE-bench, Terminal-Bench, etc.)
│   ├── task_registry/             ← Candidate pool, selection matrix, master task list
│   ├── configurations/            ← Declarative, versioned agent configurations
│   ├── public/                    ← Agent-visible task prompts & public metadata
│   ├── private/                   ← Evaluator-private data (patches, hidden tests, evaluation specs)
│   ├── runs/                      ← Run trajectory logs and execution manifests
│   ├── evaluations/               ← Multi-layer evaluation outputs
│   ├── results/                   ← Comparative analytical reports
│   └── scripts/                   ← Verification, diff analysis, and hashing tools
│
└── carb_workspaces/              ← Clean Task Workspaces for IDE Agent Runs
    ├── T001/                      ← Fresh task workspace for T001
    ├── T002/                      ← Fresh task workspace for T002
    └── T003/                      ← Fresh task workspace for T003
```

> [!IMPORTANT]
> **Anti-Contamination Rule**: The coding agent operates strictly inside `carb_workspaces/Txxx/`. It has **zero access** to `carb_benchmark/private/` (which contains expected solution patches, hidden tests, and evaluator instructions) or `carb_benchmark/task_registry/`.

---

## 2. Experimental Configurations

CARB v2 compares **three** standardized configurations (the intermediate constitution-only tier was removed by design decision):

1. **`BASELINE` (`baseline-v2.0`)**: Default Antigravity/Gemini behavior. NO custom system instructions anywhere.
2. **`SUPREME` (`supreme-v2.0`)**: Default behavior + the FULL Supreme Agent system (constitution + operating protocol + sub-agent profiles + environment profile + persistent state) embedded as the system block of the prompt. *(Renamed from `full-v2.0` on 2026-08-17; `full-v2.0` remains a legacy alias.)*
3. **`SUPERPOWERS` (`superpowers-v2.0`)**: Default behavior + the **Superpowers by OB** skill system (every skill's `SKILL.md` definition + the `antigravity-tools.md` platform reference) embedded as the system block of the prompt. Introduced 2026-08-17 as the third CARB-v2 arm.

All three configurations run with **identical environment isolation** (temp profile, auth files only — no global `~/.gemini/config` rules, no memory). The ONLY difference between them is the prompt content.

> **IMPORTANT — v1 contamination discovered on 2026-08-15**: the v1 harness isolated only the baseline; constitution/full ran in the real profile where the global `~/.gemini/config/GEMINI.md` (the full Supreme system) was loaded. This collapsed the intended gradient to *clean → full → full*. See [`results/carb_v2_pilot_proof_report.md`](file:///e:/RofU/Supreme/carb_benchmark/results/carb_v2_pilot_proof_report.md) for the probe evidence. v1 result summaries (3.3% / 8.3% / 96.7%) are **not trustworthy** and should not be reported.

---

## 3. Evaluation Framework

CARB evaluates runs using a 4-layer methodology:
- **Layer 1: Functional Correctness** (Automated build, test suite, and hidden tests).
- **Layer 2: Regression Safety** (Preservation of existing test suite behavior).
- **Layer 3: Engineering Quality** (Minimum justified change, surgical editing, structural integrity).
- **Layer 4: Behavioral Trajectory** (Investigation, planning, uncertainty handling, verification, premature completion prevention).

---

## 4. Quick Start & Execution Workflow

### Running a Benchmark Task (CARB v2 — authoritative runner)
Runs one task in one configuration with identical isolation, transcripts, real test commands, and leakage marker scan:
```bash
python carb_benchmark/scripts/run_benchmark_v2.py --task T001_sample_repo_debug --config baseline-v2.0 [--append-question]
python carb_benchmark/scripts/run_benchmark_v2.py --task T001_sample_repo_debug --config supreme-v2.0 [--append-question]
python carb_benchmark/scripts/run_benchmark_v2.py --task T001_sample_repo_debug --config superpowers-v2.0 [--append-question]
```

> The v1 runners (`run_antigravity_agy.py`, root-level `run_remaining_baseline.py`) are **deprecated** — they contain the isolation bug and the exit-code-0 pass fallback.

### Initializing a Task Workspace
To reset and set up a clean task workspace for testing:
```bash
python carb_benchmark/scripts/init_task.py --task T001
```

### Running an Integrity & Isolation Check
To verify that private evaluation files are hidden and workspace snapshots are deterministic:
```bash
python carb_benchmark/scripts/verify_isolation.py
```

### Analyzing a Run Diff
To analyze the surgical editing characteristics of a completed run diff:
```bash
python carb_benchmark/scripts/analyze_diff.py --run-dir carb_benchmark/runs/2026-08-13-T001-baseline-v1.0-001
```

---

## 5. Provenance & References

- **Design Reference**: [`carb_benchmark/design_reference/architecture_conversation.md`](file:///e:/RofU/Supreme/carb_benchmark/design_reference/architecture_conversation.md)
- **Supreme Agent Specs**: [`SupremeAgent/`](file:///e:/RofU/Supreme/SupremeAgent/)
