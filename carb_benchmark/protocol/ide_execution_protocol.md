# CARB Manual IDE Execution Protocol

This protocol defines the step-by-step procedure for executing benchmark runs inside an IDE coding agent session.

---

## Environment Security Classification

> [!IMPORTANT]
> **Cooperative Isolation**: This execution protocol operates under **non-adversarial/cooperative isolation**. The host environment does not enforce OS container sandboxing between `carb_workspaces/` and `carb_benchmark/private/`. Experimental validity relies on folder separation, prompt hashes, non-intervention execution, and automated verification checks.

---

## Pre-Run Checklists & Mandatory Hash Enforcement

Before launching any benchmark run:

1. **Reconstruct Workspace from Immutable Golden Snapshot**: Run `python carb_benchmark/scripts/init_task.py --task Txxx`. This completely purges the previous workspace and recreates `carb_workspaces/Txxx` fresh from `carb_benchmark/snapshots/Txxx/`.
2. **Mandatory Hash Gate**: `init_task.py` validates the SHA-256 prompt hash and snapshot tree hash against `metadata.yaml`. If a mismatch is detected, initialization **aborts**.
3. **Automated Manifest Session Start**: Run `python carb_benchmark/scripts/start_run.py --task Txxx --config <config-id>`. This creates `carb_benchmark/runs/<run_id>/run_manifest.yaml` recording model ID, environment specs, hashes, and ISO timestamps.

---

## Step-by-Step Execution Workflow

```text
[Step 1: Reconstruct Workspace]
  └── Run `python carb_benchmark/scripts/init_task.py --task Txxx`.

[Step 2: Initialize Run Session]
  └── Run `python carb_benchmark/scripts/start_run.py --task Txxx --config baseline-v1.0`.

[Step 3: Open Fresh Session]
  └── Open fresh IDE chat session in workspace `carb_workspaces/Txxx/`.

[Step 4: Inject Task Prompt]
  └── Copy standardized `prompt.txt` verbatim into chat textbox. Do NOT add extra instructions or hints.

[Step 5: Non-Intervention Execution]
  └── Allow the coding agent to execute normally.
  └── DO NOT rescue, hint, steer, or answer questions unless permitted by Clarification Policy.

[Step 6: Finalize Run Session]
  └── Run `python carb_benchmark/scripts/finalize_run.py --run-id <run_id> --status SUCCESS --diff-file <path>`.

[Step 7: Layered Evaluation]
  └── Run automated test scripts and analyze diff via `python carb_benchmark/scripts/analyze_diff.py`.
```

---

## Non-Intervention Rule

> [!CAUTION]
> **Strict Non-Intervention**: Human runners must **never** assist the agent during a benchmark session. If the agent makes a mistake, gets stuck in a loop, or edits the wrong file, let it fail. The benchmark measures agent autonomy and reliability, not human-agent pair performance.
