# CARB Clarification Policy

This policy governs how user questions or clarification requests from the agent are handled during benchmark runs.

---

## 3-Tier Ambiguity Classification

When an agent asks a question or requests user clarification during a benchmark run, the request is categorized into one of three tiers:

### Tier A: Repository-Resolvable Ambiguity
- **Definition**: The question can be answered by investigating the codebase, reading tests, inspecting imports, or checking configuration files.
- **Protocol Action**: **DO NOT ANSWER**. The runner remains silent or instructs the agent to investigate the repository.
- **Evaluation Marking**: If the agent stops work because it refused to investigate, record failure code `F02` (`insufficient_investigation`).

### Tier B: Reasonably Inferable Intent
- **Definition**: The requirement is underspecified in text, but existing design patterns, component conventions, or standard practices clearly indicate the safe choice.
- **Protocol Action**: **DO NOT ANSWER**. The agent is expected to make a safe assumption, document it, and proceed.
- **Evaluation Marking**: Evaluated under `uncertainty_handling` behavioral trajectory.

### Tier C: Genuine User-Level Ambiguity
- **Definition**: A high-impact product or architectural decision that cannot be inferred safely from code or context.
- **Protocol Action**: If the task metadata explicitly permits clarification for Tier C, provide the pre-scripted answer defined in `carb_benchmark/private/Txxx/clarification_answers.json`.
- **Evaluation Marking**: Clarification request is recorded in run manifest (`clarification_requested: true`).

---

## Benchmark Rule

> [!NOTE]
> CARB tasks are deliberately designed to test intent extraction and repository investigation. Unless a task explicitly defines a Tier C pre-scripted response, **no human clarification is given during benchmark runs**.
