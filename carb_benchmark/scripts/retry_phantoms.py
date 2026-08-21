#!/usr/bin/env python3
"""Re-run the 12 remaining phantom arc tasks from v3_calibration.json.
Saves results after each task so crashes don't lose progress.
"""
import glob
import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPREME_ROOT = os.path.dirname(BASE)
RUNNER = os.path.join(BASE, "scripts", "run_benchmark_v2.py")
EVALS = os.path.join(BASE, "evaluations")
PROGRESS = os.path.join(BASE, "results", "v3_calibration.json")

# Only the 12 remaining arc phantom tasks
REMAINING = [
    "lcb__arc191_d", "lcb__arc192_d", "lcb__arc192_e", "lcb__arc193_d",
    "lcb__arc194_c", "lcb__arc194_d", "lcb__arc194_e", "lcb__arc195_c",
    "lcb__arc195_d", "lcb__arc195_e", "lcb__arc196_c", "lcb__arc196_d",
]


def load_progress():
    with open(PROGRESS, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(p):
    tmp = PROGRESS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)
    os.replace(tmp, PROGRESS)


def find_new_eval(task_id, after):
    pat = os.path.join(EVALS, f"*{task_id}*", "evaluator.json")
    best, best_m = None, 0.0
    for p in glob.glob(pat):
        m = os.path.getmtime(p)
        if m > after and m > best_m:
            best, best_m = p, m
    return best


def main():
    config = "baseline-v2.0"
    notes = "phantom retry (arc tasks)"
    timeout_minutes = 40

    prog = load_progress()
    results = prog["results"]

    # Filter to tasks not yet graded
    to_run = [t for t in REMAINING if t not in results or results[t].get("passed") is None]
    print(f"Phantom retry: {len(REMAINING)} targets | {len(to_run)} to run", flush=True)

    for i, task in enumerate(to_run, 1):
        print(f"[{i}/{len(to_run)}] {task}: running...", end=" ", flush=True)
        t0 = time.time()
        try:
            rc = subprocess.run(
                [sys.executable, RUNNER, "--task", task, "--config", config,
                 "--notes", notes, "--timeout-minutes", str(timeout_minutes)],
                cwd=SUPREME_ROOT,
                timeout=(timeout_minutes * 60) + 60,
            ).returncode
        except subprocess.TimeoutExpired:
            rc = -1
            print("HARDCAP TIMEOUT", flush=True)
        wall = round(time.time() - t0, 1)

        ev_file = find_new_eval(task, t0 - 5)
        if ev_file is None:
            results[task] = {"run_id": None, "passed": None, "wall_clock_seconds": wall, "error": f"no eval (rc={rc})"}
            print(f"NO EVAL (rc={rc})", flush=True)
        else:
            d = json.load(open(ev_file, encoding="utf-8"))
            tele = d.get("telemetry") or {}
            results[task] = {
                "run_id": d.get("run_id"),
                "passed": d.get("passed"),
                "wall_clock_seconds": d.get("wall_clock_seconds"),
                "diff": (d.get("diff_metrics") or {}).get("total_lines_changed"),
                "timed_out": d.get("timed_out"),
                "tool_calls_total": tele.get("tool_calls_total"),
                "usage_total_tokens": (tele.get("usage") or {}).get("total_tokens"),
                "time_to_first_edit": tele.get("time_to_first_edit_seconds"),
                "note": (d.get("notes") or "")[:200],
            }
            status = "PASS" if d.get("passed") else "FAIL"
            print(f"{status} ({wall}s, {results[task]['diff']} lines)", flush=True)

        # Save after EVERY task
        prog["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_progress(prog)

    # Summary
    total = sum(1 for r in results.values() if r.get("passed") is not None)
    passed = sum(1 for r in results.values() if r.get("passed") == True)
    failed = sum(1 for r in results.values() if r.get("passed") == False)
    print(f"\nDone. Total graded: {total} | PASS: {passed} | FAIL: {failed}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
