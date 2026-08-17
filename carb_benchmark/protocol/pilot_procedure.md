# CARB Pilot Execution Procedure

Before running the full 60-task benchmark suite across all configurations, CARB requires a 3-task pilot run to validate benchmark protocol mechanics, isolation boundaries, script utilities, and evaluation pipelines.

---

## Pilot Task Suite

The pilot suite comprises 3 representative tasks across real-world repository debugging, environment interaction, and custom behavioral diagnostics:

1. **`T001_sample_repo_debug`**: Real repository bug fix (Python/JS repo task adapted from SWE-bench Lite).
2. **`T002_environment_tooling`**: Terminal & environment task (CLI tool / package fix adapted from Terminal-Bench 2.0).
3. **`T003_diagnostic_premature_completion`**: Diagnostic premature-completion trap (Visible request looks simple, but acceptance criteria require multi-component changes).

---

## Pilot Validation Steps

### Step 1: Pre-Pilot Isolation Test
Run automated isolation check:
```bash
python carb_benchmark/scripts/verify_isolation.py
```
*Expected Result*: PASS. Confirms `carb_workspaces/` cannot read `carb_benchmark/private/` files.

### Step 2: Task Workspace Initialization
Initialize workspace for T001, T002, T003:
```bash
python carb_benchmark/scripts/init_task.py --task T001
python carb_benchmark/scripts/init_task.py --task T002
python carb_benchmark/scripts/init_task.py --task T003
```

### Step 3: Experimental Configuration Runs
Execute each task under `BASELINE`, `CONSTITUTION`, and `FULL` configurations following `ide_execution_protocol.md`:
- Record run manifests and transcripts in `carb_benchmark/runs/`.
- Ensure clean workspace resets between runs.

### Step 4: Analytical Verification
Run diff analysis and hashing:
```bash
python carb_benchmark/scripts/generate_hashes.py
python carb_benchmark/scripts/analyze_diff.py --run-dir carb_benchmark/runs/<pilot-run-id>
```

### Step 5: Protocol Refinement
Identify any workflow glitches, script errors, or isolation gaps. Fix benchmark infrastructure before launching the full 60-task set.
