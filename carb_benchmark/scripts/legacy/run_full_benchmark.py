#!/usr/bin/env python3
"""
run_full_benchmark.py — DEPRECATED (2026-08-17). Superseded by
run_carb_v2_batch.py (3-configuration support: baseline-v2.0, supreme-v2.0,
superpowers-v2.0, with full-v2.0 mapped to the supreme-v2.0 alias).
Kept for historical reference only — do not use for new runs.
"""
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
CONFIGS = ["baseline-v2.0", "full-v2.0"]
RUN_TIMEOUT = 2700  # per run (agy 1500s with 20m print-timeout + SWE test/venv + overhead + margin)

os.makedirs(RESULTS, exist_ok=True)


def run_already_done(task_id, config_id):
    """A (task, config) is done iff a run dir with a FINALIZED manifest exists.
    Dir-based (robust to driver restarts; progress file is informational)."""
    prefix = f"{task_id}-{config_id}"
    if not os.path.isdir(RUNS):
        return False
    for d in os.listdir(RUNS):
        if not d.endswith(prefix):
            continue
        mp = os.path.join(RUNS, d, "run_manifest.yaml")
        if not os.path.exists(mp):
            continue
        try:
            txt = open(mp, encoding="utf-8").read()
        except Exception:
            continue
        if "status: SUCCESS" in txt:
            return "SUCCESS"
        if "status: FAILURE" in txt:
            return "FAILURE"
    return False


def main():
    registry = json.load(open(REGISTRY, encoding="utf-8"))
    print(f"registry: {len(registry)} tasks; configs: {CONFIGS}")
    progress_path = os.path.join(RESULTS, "benchmark_v2_progress.json")
    progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}

    total = len(registry) * len(CONFIGS)
    done = 0
    passed = 0
    failed = 0
    skipped = 0
    errors = []

    for task in registry:
        task_id = task["instance_id"]
        for config_id in CONFIGS:
            key = f"{task_id}::{config_id}"
            prior = run_already_done(task_id, config_id)
            if prior:
                done += 1
                if prior == "SUCCESS":
                    passed += 1
                else:
                    failed += 1
                skipped += 1
                continue
            print(f"\n[{done + 1 - skipped}/{total}] {task_id} | {config_id} "
                  f"({time.strftime('%H:%M:%S')})")
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
            except subprocess.TimeoutExpired:
                output = "RUN TIMED OUT"
                status = "TIMEOUT"
                # kill the whole process tree so agy.exe doesn't survive
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
                   "tail": output[-800:]}
            progress[key] = rec
            json.dump(progress, open(progress_path, "w", encoding="utf-8"), indent=1)
            done += 1
            if status == "SUCCESS":
                passed += 1
            else:
                failed += 1
                errors.append((key, status, output[-500:]))
            print(f"  -> {status}")

    print("\n===== BENCHMARK COMPLETE =====")
    print(f"total: {total} | passed: {passed} | failed: {failed} | skipped: {skipped}")
    if errors:
        print("\n--- failures ---")
        for key, status, tail in errors:
            print(f"{key}: {status}")
    json.dump({"summary": {"total": total, "passed": passed, "failed": failed,
                           "skipped": skipped}, "runs": progress},
              open(progress_path, "w", encoding="utf-8"), indent=1)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
