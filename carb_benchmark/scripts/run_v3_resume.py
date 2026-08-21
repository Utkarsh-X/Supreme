#!/usr/bin/env python3
"""
run_v3_resume.py — resume script for the 8 remaining Superpowers tasks after internet reconnection.
Runs the 8 tasks and automatically compiles the finalized V3 findings report.
"""
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
RESULTS = os.path.join(BASE, "results")
RESUME_TASKS = os.path.join(RESULTS, "v3_superpowers_resume_tasks.txt")
PROGRESS = os.path.join(RESULTS, "v3_superpowers_resume_progress.json")


def main():
    print(f"CARB-v3 Resume Runner Started at {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"Resuming {RESUME_TASKS} under superpowers-v2.0 (8 tasks)...", flush=True)

    cmd = [
        sys.executable,
        os.path.join(SCRIPTS, "run_carb_v2_batch.py"),
        "--configs", "superpowers-v2.0",
        "--task-list-file", RESUME_TASKS,
        "--progress", PROGRESS,
    ]
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    proc.communicate()
    print(f"\nBatch completed with returncode {proc.returncode}\n", flush=True)

    print(f"=======================================================", flush=True)
    print(f"COMPILING FINAL V3 FINDINGS AND MASTER MATRIX", flush=True)
    print(f"=======================================================\n", flush=True)

    cmd_agg = [sys.executable, os.path.join(SCRIPTS, "aggregate_v3_results.py")]
    subprocess.run(cmd_agg)

    print(f"\nAll tasks finished and aggregated at {time.strftime('%Y-%m-%d %H:%M:%S')}!", flush=True)


if __name__ == "__main__":
    main()
