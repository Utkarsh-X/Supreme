#!/usr/bin/env python3
"""
run_retry_batch.py — DEPRECATED (2026-08-17). Historical infra-retry driver;
superseded by run_carb_v2_batch.py (3-configuration support). Kept for
reference only — do not use for new runs.

Original purpose: re-run the infra-failed CARB-v2 runs.

The first full pass (run_full_benchmark.py) had 25 runs invalidated by
infrastructure, not by model quality:
  - agy API "timeout waiting for response" (Google-side latency)
  - network/DNS drop ("Eligibility check failed", dial tcp unreachable, no such host)
  - agy re-authentication timeout ("authentication timed out")
  - generic "Agent execution terminated due to error"
  - one stale run (pytest-5262-full) whose manifest stuck at IN_PROGRESS

The original run dirs were moved to runs/_retry_quarantine/ so the evidence is
preserved. This driver re-runs each (task, config) pair through the identical
runner (same model, same prompts, same eval) and records fresh run dirs.
arc191_a-baseline is NOT re-run: its transcript shows a complete, genuine
(incorrect) solution attempt with no infra error — that failure stands.
"""
import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
RESULTS = os.path.join(BASE, "results")
RUN_TIMEOUT = 2700  # agy 1500s (with 20m print-timeout) + SWE test/venv + margin

RETRY_RUNS = [
    ("matplotlib__matplotlib-23299", "baseline-v2.0"),
    ("matplotlib__matplotlib-23299", "full-v2.0"),
    ("matplotlib__matplotlib-23476", "baseline-v2.0"),
    ("matplotlib__matplotlib-23476", "full-v2.0"),
    ("matplotlib__matplotlib-24627", "baseline-v2.0"),
    ("matplotlib__matplotlib-24627", "full-v2.0"),
    ("pytest-dev__pytest-5262", "baseline-v2.0"),
    ("pytest-dev__pytest-5262", "full-v2.0"),
    ("pytest-dev__pytest-7521", "baseline-v2.0"),
    ("pytest-dev__pytest-7521", "full-v2.0"),
    ("sphinx-doc__sphinx-10435", "baseline-v2.0"),
    ("sphinx-doc__sphinx-10435", "full-v2.0"),
    ("sphinx-doc__sphinx-9367", "baseline-v2.0"),
    ("sphinx-doc__sphinx-9367", "full-v2.0"),
    ("sphinx-doc__sphinx-9698", "baseline-v2.0"),
    ("sphinx-doc__sphinx-9698", "full-v2.0"),
    ("sympy__sympy-15875", "baseline-v2.0"),
    ("sympy__sympy-15875", "full-v2.0"),
    ("sympy__sympy-23950", "baseline-v2.0"),
    ("sympy__sympy-23950", "full-v2.0"),
    ("lcb__abc387_b", "full-v2.0"),
    ("lcb__abc388_c", "baseline-v2.0"),
    ("lcb__abc390_c", "baseline-v2.0"),
    ("lcb__abc390_c", "full-v2.0"),
    ("lcb__abc391_d", "baseline-v2.0"),
]


def main():
    os.makedirs(RESULTS, exist_ok=True)
    progress_path = os.path.join(RESULTS, "benchmark_v2_retry_progress.json")
    progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}
    log_path = os.path.join(RESULTS, "benchmark_v2_retry.log")

    total = len(RETRY_RUNS)
    done = passed = failed = 0
    errors = []
    with open(log_path, "a", encoding="utf-8") as log:
        for i, (task_id, config_id) in enumerate(RETRY_RUNS, 1):
            key = f"{task_id}::{config_id}"
            if key in progress and progress[key].get("status") in ("SUCCESS", "FAILURE"):
                done += 1
                if progress[key]["status"] == "SUCCESS":
                    passed += 1
                else:
                    failed += 1
                continue
            line = f"\n[{i}/{total}] {key} ({time.strftime('%H:%M:%S')})"
            print(line, flush=True)
            log.write(line + "\n")
            log.flush()
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
            line2 = f"  -> {status}"
            print(line2, flush=True)
            log.write(line2 + "\n")
            log.flush()

    summary = f"\n===== RETRY COMPLETE =====\ntotal: {total} | passed: {passed} | failed: {failed}"
    print(summary, flush=True)
    log.write(summary + "\n")
    if errors:
        print("\n--- remaining failures ---")
        log.write("\n--- remaining failures ---\n")
        for key, status, tail in errors:
            print(f"{key}: {status}")
            log.write(f"{key}: {status}\n")
    json.dump({"summary": {"total": total, "passed": passed, "failed": failed},
               "runs": progress},
              open(progress_path, "w", encoding="utf-8"), indent=1)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
