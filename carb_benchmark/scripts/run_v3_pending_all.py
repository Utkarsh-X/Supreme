#!/usr/bin/env python3
"""
run_v3_pending_all.py — master runner for all pending CARB-v3 tasks followed by automatic aggregation.
Runs 7 Supreme tasks, then 10 Superpowers tasks, and finally compiles the full findings.
"""
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
RESULTS = os.path.join(BASE, "results")

SUPREME_TASKS = os.path.join(RESULTS, "v3_supreme_pending_tasks.txt")
SUPERPOWERS_TASKS = os.path.join(RESULTS, "v3_superpowers_pending_tasks.txt")


def run_batch(config_id, task_file, progress_file):
    print(f"\n=======================================================", flush=True)
    print(f"STARTING BATCH: {config_id} ({time.strftime('%Y-%m-%d %H:%M:%S')})", flush=True)
    print(f"Task list: {task_file}", flush=True)
    print(f"=======================================================\n", flush=True)

    cmd = [
        sys.executable,
        os.path.join(SCRIPTS, "run_carb_v2_batch.py"),
        "--configs", config_id,
        "--task-list-file", task_file,
        "--progress", progress_file,
    ]
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    proc.communicate()
    print(f"\nBatch {config_id} finished with code {proc.returncode}\n", flush=True)
    return proc.returncode


def main():
    print(f"CARB-v3 Master Runner Started at {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

    # 1. Run Supreme Pending
    run_batch(
        "supreme-v2.0",
        SUPREME_TASKS,
        os.path.join(RESULTS, "v3_supreme_pending_progress.json")
    )

    # 2. Run Superpowers Pending
    run_batch(
        "superpowers-v2.0",
        SUPERPOWERS_TASKS,
        os.path.join(RESULTS, "v3_superpowers_pending_progress.json")
    )

    # 3. Aggregate Results
    print(f"\n=======================================================", flush=True)
    print(f"COMPILING FINAL V3 FINDINGS AND MASTER MATRIX", flush=True)
    print(f"=======================================================\n", flush=True)

    cmd_agg = [sys.executable, os.path.join(SCRIPTS, "aggregate_v3_results.py")]
    subprocess.run(cmd_agg)

    print(f"\nAll tasks and aggregation completed at {time.strftime('%Y-%m-%d %H:%M:%S')}!", flush=True)


if __name__ == "__main__":
    main()
