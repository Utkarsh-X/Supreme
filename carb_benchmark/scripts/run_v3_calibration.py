#!/usr/bin/env python3
"""
run_v3_calibration.py — V3 Phase A calibration: run the BASELINE configuration
on the candidate hard set and record per-task pass/fail, so the locked V3 set
can be built from tasks the baseline empirically FAILS.

Protocol (see protocol/v3_discriminative_set_proposal.md):
  - baseline only; challenger configs never run in this phase
  - a task is kept for V3 iff baseline fails it (target baseline pass 30-60%)
  - results land in results/v3_calibration.json, appended per task
  - idempotent: tasks already in the progress file are skipped

Usage:
  python carb_benchmark/scripts/run_v3_calibration.py \
      --tasks-file task_registry/v3_calibration_tasks.txt \
      [--config baseline-v2.0] [--notes "v3 calibration"]
"""
import glob
import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE)
RUNNER = os.path.join(BASE, "scripts", "run_benchmark_v2.py")
EVALS = os.path.join(BASE, "evaluations")
PROGRESS = os.path.join(BASE, "results", "v3_calibration.json")


def load_tasks(path):
    tasks = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                tasks.append(line)
    return tasks


def load_progress():
    if os.path.exists(PROGRESS):
        return json.load(open(PROGRESS, encoding="utf-8"))
    return {"config": None, "notes": "", "results": {}, "started_at": None}


def save_progress(p):
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)


def find_new_eval(task_id, after):
    pat = os.path.join(EVALS, f"*{task_id}*", "evaluator.json")
    best, best_m = None, 0.0
    for p in glob.glob(pat):
        m = os.path.getmtime(p)
        if m > after and m > best_m:
            best, best_m = p, m
    return best


def main():
    args = sys.argv[1:]
    tasks_file = None
    config = "baseline-v2.0"
    notes = "v3 calibration"
    if "--tasks-file" in args:
        tasks_file = args[args.index("--tasks-file") + 1]
    if "--config" in args:
        config = args[args.index("--config") + 1]
    if "--notes" in args:
        notes = args[args.index("--notes") + 1]
    if not tasks_file or not os.path.exists(tasks_file):
        print(f"usage: --tasks-file <path> (missing: {tasks_file})")
        return 1

    tasks = load_tasks(tasks_file)
    prog = load_progress()
    if prog["config"] is None:
        prog["config"] = config
        prog["notes"] = notes
        prog["started_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    results = prog["results"]

    print(f"V3 calibration: {len(tasks)} tasks | config={config} | "
          f"{len(results)} already recorded", flush=True)

    for i, task in enumerate(tasks, 1):
        if task in results:
            print(f"[{i}/{len(tasks)}] {task}: already done -> skip", flush=True)
            continue
        print(f"[{i}/{len(tasks)}] {task}: running baseline...", flush=True)
        t0 = time.time()
        rc = subprocess.run(
            [sys.executable, RUNNER, "--task", task, "--config", config,
             "--notes", notes],
            cwd=SUPREME_ROOT,
        ).returncode
        wall = round(time.time() - t0, 1)
        ev_file = find_new_eval(task, t0 - 5)
        if ev_file is None:
            results[task] = {"run_id": None, "passed": None, "error": f"no eval record (rc={rc})"}
        else:
            d = json.load(open(ev_file, encoding="utf-8"))
            results[task] = {
                "run_id": d.get("run_id"),
                "passed": d.get("passed"),
                "wall_clock_seconds": d.get("wall_clock_seconds"),
                "diff": (d.get("diff_metrics") or {}).get("total_lines_changed"),
                "timed_out": d.get("timed_out"),
                "note": (d.get("notes") or "")[:200],
            }
            print(f"    -> {'PASS' if d.get('passed') else 'FAIL'} "
                  f"({wall}s wall, {results[task]['diff']} lines) {d.get('run_id')}", flush=True)
        prog["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_progress(prog)

    passed = sum(1 for r in results.values() if r.get("passed"))
    failed = sum(1 for r in results.values() if r.get("passed") is False)
    print(f"\nDone. recorded={len(results)} passed={passed} failed={failed} "
          f"baseline pass rate={passed/(passed+failed)*100:.1f}% "
          f"(of graded)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
