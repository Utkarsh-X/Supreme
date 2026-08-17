#!/usr/bin/env python3
"""
prepare_phase_b.py — generate the Phase B run plan from the locked V3 set.

Phase B runs supreme + superpowers on the baseline-failing tasks locked in
task_registry/final_tasks_v3.json (produced by build_v3_final_set.py).
Per the protocol (§6) the task order is randomized and configurations are
interleaved per task (run_carb_v2_batch.py already interleaves configs inner-
loop) so no configuration runs to completion first and no day-level latency
bias can attach to a config.

Usage:
  python carb_benchmark/scripts/prepare_phase_b.py [--seed 42]

Outputs:
  results/v3_phase_b_tasks.txt   — shuffled task ids (one per line)
  prints the exact batch command
"""
import json
import os
import random
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(BASE, "task_registry", "final_tasks_v3.json")
OUT = os.path.join(BASE, "results", "v3_phase_b_tasks.txt")


def main():
    seed = 42
    if "--seed" in sys.argv:
        seed = int(sys.argv[sys.argv.index("--seed") + 1])

    if not os.path.exists(REGISTRY):
        print(f"FATAL: {REGISTRY} does not exist — run build_v3_final_set.py "
              f"after calibration completes.")
        return 1

    data = json.load(open(REGISTRY, encoding="utf-8"))
    tasks = [t["instance_id"] for t in data.get("tasks", [])]
    random.Random(seed).shuffle(tasks)

    with open(OUT, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(t + "\n")

    print(f"locked set: {len(tasks)} tasks (seed={seed})")
    print(f"wrote {OUT}")
    print(f"\nPhase B command:")
    print(f"  python carb_benchmark/scripts/run_carb_v2_batch.py \\")
    print(f"      --configs supreme-v2.0,superpowers-v2.0 \\")
    print(f"      --task-list-file {OUT} \\")
    print(f"      --progress v3_phase_b_progress.json")
    print(f"\nBaseline cells for these tasks already exist (Phase A); "
          f"run_carb_v2_batch.py skips any (task, config) whose run dir is "
          f"already finalized, so baseline is not re-run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
