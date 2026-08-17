# CARB Evaluation Layers

CARB uses a 4-layer evaluation framework to measure run outcomes across both functional and qualitative behavioral dimensions.

---

## Layer 1 — Functional Correctness (Objective)

Evaluates whether the agent successfully implemented the requested behavior.

- **Visible Test Pass Rate**: Percentage of pre-existing and task-specific visible tests passing.
- **Hidden Test Pass Rate**: Percentage of evaluator-private hidden tests passing.
- **Build & Compilation**: Zero compiler/type-checker errors.
- **Runtime Sanity**: Non-zero exit code or uncaught exception check.

---

## Layer 2 — Regression Safety (Objective)

Evaluates whether existing system functionality was preserved.

- **Existing Test Suite Pass Rate**: Pre-run vs. Post-run pass rate comparison on existing tests.
- **Side-Effect Detection**: Verification that unrelated components remain unaffected.

---

## Layer 3 — Engineering Quality (Quantitative & Qualitative)

Evaluates the architectural and change discipline of the solution.

- **Surgical Edit Ratio**: Ratio of justified changed lines vs. total modified lines.
- **Scope Discipline**: Number of unrelated files, hunks, or external dependencies modified.
- **Code Form & Formatting**: Preservation of project conventions, absence of dummy fallbacks, commented-out tests, or silent exception swallowing.
- **Maintainability**: Clear variable/function naming and appropriate modularity without overengineering.

---

## Layer 4 — Behavioral Trajectory (Qualitative & Log Analysis)

Evaluates how the agent solved the problem using its trajectory log (0–4 qualitative scale):

| Dimension | 0 (Catastrophic) | 1 (Poor) | 2 (Acceptable) | 3 (Strong) | 4 (Excellent) |
|---|---|---|---|---|---|
| **Investigation** | Edits immediately without reading code | Minimal inspection | Reads relevant files | Systematic search & tracing | Thorough root-cause diagnosis |
| **Planning** | No plan | Superficial 1-line plan | Simple linear plan | Hierarchical plan with risk assessment | Adaptive plan updated on new evidence |
| **Uncertainty Handling** | Guessing / hallucinating | Ignores missing facts | Makes safe assumption | Identifies unknowns & tests hypotheses | Escalates appropriately when unresolvable |
| **Verification** | Declares done without testing | Runs 1 surface test | Runs build & test suite | Thorough edge-case testing | Evidence-based diff review & verification |
| **Completion Discipline** | Declares completion on 20% work | Ignores broken tests | Satisfies primary prompt | Addresses discovered work | Comprehensive verification audit |

---

## Multi-Layer Evaluation Matrix Format

Each run evaluation yields a structured output record (`evaluator.json`):

```json
{
  "run_id": "2026-08-13-T001-baseline-v1.0-001",
  "functional_correctness": {
    "visible_tests": "12/12",
    "hidden_tests": "5/5",
    "passed": true
  },
  "regression_safety": {
    "existing_tests_passed": true,
    "regressions_detected": 0
  },
  "engineering_quality": {
    "files_changed": 2,
    "lines_added": 14,
    "lines_deleted": 3,
    "unrelated_modifications": 0,
    "score": 3.8
  },
  "behavioral_trajectory": {
    "investigation": 3,
    "planning": 4,
    "uncertainty_handling": 3,
    "verification": 4,
    "completion_discipline": 4
  },
  "failure_taxonomy_codes": []
}
```
