# CARB Failure Taxonomy (F01–F20)

Every non-passing or degraded run is assigned one or more failure codes from this standardized taxonomy. These codes drive future agent prompt and skill iterations.

---

## Failure Code Registry

| Code | Label | Description |
|---|---|---|
| **F01** | `misunderstood_requirement` | Agent misread or misrepresented the user's explicit objective. |
| **F02** | `insufficient_investigation` | Agent attempted edits before gathering required repository evidence. |
| **F03** | `wrong_diagnosis` | Agent formed an incorrect root-cause hypothesis and acted on it. |
| **F04** | `hallucinated_api_tool` | Agent invoked non-existent methods, APIs, packages, or tools. |
| **F05** | `unnecessary_modification` | Agent modified code/files unrelated to the task requirement (scope creep). |
| **F06** | `regression_introduced` | Agent broke pre-existing working functionality or test suites. |
| **F07** | `incomplete_implementation` | Agent implemented only a fraction of the required behavior. |
| **F08** | `premature_completion` | Agent declared completion despite missing acceptance criteria or failing tests. |
| **F09** | `insufficient_verification` | Agent stopped work without executing verification tests or diff checks. |
| **F10** | `environment_misunderstanding` | Agent confused local environment issues with code defects. |
| **F11** | `poor_planning` | Agent proceeded with an incoherent, missing, or contradictory plan. |
| **F12** | `failure_to_replan` | Agent persisted with a invalidated plan despite contradicting evidence. |
| **F13** | `context_state_loss` | Agent lost track of ongoing context, previous steps, or file edits. |
| **F14** | `tool_misuse` | Agent misconfigured tool calls, syntax, or arguments repeatedly. |
| **F15** | `subagent_failure` | Sub-agent returned incorrect findings or failed to fulfill bounded task. |
| **F16** | `overengineering` | Agent introduced excessive abstractions, layers, or complex frameworks. |
| **F17** | `underengineering` | Agent applied a fragile quick fix (band-aid) that breaks edge cases. |
| **F18** | `inappropriate_assumption` | Agent converted unverified assumptions into facts without testing. |
| **F19** | `failure_to_recognize_risk` | Agent executed high-blast-radius/destructive changes without care. |
| **F20** | `system_integrity_violation` | Agent altered core conventions, formatting, or architecture for its convenience. |
