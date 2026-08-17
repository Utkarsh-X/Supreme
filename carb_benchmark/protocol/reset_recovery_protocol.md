# CARB Reset & Clean-State Recovery Protocol

This protocol enforces clean repository restoration between experimental benchmark runs.

---

## Workspace Reset Procedure

To reset task `Txxx` to its exact golden snapshot:

1. **Remove Unversioned & Generated Artifacts**:
   Delete all temporary, compiled, or agent-created files in `carb_workspaces/Txxx/` that were not in the initial clean commit.

2. **Hard Git Reset**:
   Execute `git reset --hard HEAD` and `git clean -fd` inside `carb_workspaces/Txxx/`.

3. **Verify SHA-256 Snapshot Hash**:
   Compute tree hash of `carb_workspaces/Txxx/` and verify equality with `task_snapshot_hash` recorded in `carb_benchmark/public/tasks/Txxx/metadata.yaml`.

4. **Fresh Session Verification**:
   Verify that any local session cache, IDE context history, or agent memory files are cleared.

---

## Recovery Protocol on Interrupted / Corrupted Runs

If a benchmark run is interrupted (power loss, tool crash, workspace corruption):

1. Mark the run status in `run_manifest.yaml` as `interrupted`.
2. Do **not** overwrite the partial run directory; preserve it in `carb_benchmark/runs/<run_id>/` for diagnostic analysis.
3. Execute `python carb_benchmark/scripts/init_task.py --task Txxx` to restore a clean workspace.
4. Re-run the task session with a new unique run ID (e.g. `2026-08-13-Txxx-full-v1.0-002`).
