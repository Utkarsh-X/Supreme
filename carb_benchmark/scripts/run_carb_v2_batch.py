#!/usr/bin/env python3
"""
run_carb_v2_batch.py — resumable batch driver for CARB-v2 runs.

Runs a set of (task, config) pairs through run_benchmark_v2.py with the locked
model gemini-3.6-flash-high. Resumable: a (task, config) pair whose run dir has
a FINALIZED manifest is skipped, so the driver can be killed and restarted at
any time without losing progress. Writes a live progress JSON.

Usage:
  python carb_benchmark/scripts/run_carb_v2_batch.py --configs superpowers-v2.0
  python carb_benchmark/scripts/run_carb_v2_batch.py --configs baseline-v2.0,supreme-v2.0 --tasks django__django-11179,pytest-dev__pytest-5262
  python carb_benchmark/scripts/run_carb_v2_batch.py --configs superpowers-v2.0 --task-list-file /tmp/tasks.txt
"""
import argparse
import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
RUNS = os.path.join(BASE, "runs")
RESULTS = os.path.join(BASE, "results")
REGISTRY = os.path.join(BASE, "task_registry", "final_tasks_v2.json")
RUN_TIMEOUT = 3000  # per run: agy 1500s (20m print-timeout) + SWE test/venv + margin

LEGACY_ALIASES = {"full-v2.0": "supreme-v2.0"}


def run_already_done(task_id, config_id):
    """A (task, config) is done iff a run dir with a FINALIZED manifest exists
    (dir-based, robust to driver restarts)."""
    if not os.path.isdir(RUNS):
        return False
    for d in os.listdir(RUNS):
        if task_id not in d:
            continue
        mp = os.path.join(RUNS, d, "run_manifest.yaml")
        if not os.path.exists(mp):
            continue
        try:
            txt = open(mp, encoding="utf-8").read()
        except Exception:
            continue
        cfg_line = next((ln for ln in txt.splitlines() if ln.startswith("configuration_id:")), "")
        cfg = LEGACY_ALIASES.get(cfg_line.split(":", 1)[1].strip(), cfg_line.split(":", 1)[1].strip()) \
            if cfg_line else None
        if cfg != config_id:
            continue
        if "status: SUCCESS" in txt:
            return "SUCCESS"
        if "status: FAILURE" in txt:
            return "FAILURE"
    return False


def main():
    parser = argparse.ArgumentParser(description="Resumable CARB-v2 batch runner")
    parser.add_argument("--configs", required=True, help="comma-separated config ids")
    parser.add_argument("--tasks", default="", help="comma-separated task ids (default: all registry tasks)")
    parser.add_argument("--task-list-file", default="", help="file with one task id per line")
    parser.add_argument("--progress", default="", help="progress json name (default auto)")
    args = parser.parse_args()

    configs = [c.strip() for c in args.configs.split(",") if c.strip()]
    if args.tasks:
        task_ids = [t.strip() for t in args.tasks.split(",") if t.strip()]
    elif args.task_list_file:
        task_ids = [ln.strip() for ln in open(args.task_list_file, encoding="utf-8")
                    if ln.strip() and not ln.startswith("#")]
    else:
        registry = json.load(open(REGISTRY, encoding="utf-8"))
        task_ids = [t["instance_id"] for t in registry]

    print(f"tasks: {len(task_ids)} | configs: {configs}")
    progress_path = args.progress or os.path.join(
        RESULTS, f"benchmark_v2_batch_{'_'.join(configs)}.json")
    progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}

    total = len(task_ids) * len(configs)
    done = passed = failed = skipped = 0
    errors = []

    for task_id in task_ids:
        for config_id in configs:
            key = f"{task_id}::{config_id}"
            prior = run_already_done(task_id, config_id)
            if prior:
                done += 1
                skipped += 1
                if prior == "SUCCESS":
                    passed += 1
                else:
                    failed += 1
                continue
            print(f"\n[{done + 1 - skipped}/{total}] {key} ({time.strftime('%H:%M:%S')})", flush=True)
            proc = subprocess.Popen(
                [sys.executable, os.path.join(SCRIPTS, "run_benchmark_v2.py"),
                 "--task", task_id, "--config", config_id],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace",
            )
            try:
                out, err = proc.communicate(timeout=RUN_TIMEOUT)
                output = (out or "") + (err or "")
                status = "FAILURE"
                if "Status     : SUCCESS" in output:
                    status = "SUCCESS"
                elif "Status          : SUCCESS" in output:
                    status = "SUCCESS"
            except subprocess.TimeoutExpired:
                output = "RUN TIMED OUT"
                status = "TIMEOUT"
                try:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                                   capture_output=True, timeout=30)
                except Exception:
                    pass
                try:
                    proc.kill()
                except Exception:
                    pass
            except Exception as e:
                output = f"DRIVER ERROR: {e}"
                status = "ERROR"

            rec = {"status": status, "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "tail": output[-600:]}
            progress[key] = rec
            json.dump(progress, open(progress_path, "w", encoding="utf-8"), indent=1)
            done += 1
            if status == "SUCCESS":
                passed += 1
            else:
                failed += 1
                errors.append((key, status, output[-400:]))
            print(f"  -> {status}", flush=True)

    print("\n===== BATCH COMPLETE =====")
    print(f"total: {total} | passed: {passed} | failed: {failed} | skipped: {skipped}")
    if errors:
        print("\n--- remaining failures ---")
        for key, status, tail in errors:
            print(f"{key}: {status}")
    json.dump({"summary": {"total": total, "passed": passed, "failed": failed,
                           "skipped": skipped}, "runs": progress},
              open(progress_path, "w", encoding="utf-8"), indent=1)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
