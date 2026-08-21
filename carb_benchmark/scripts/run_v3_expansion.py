#!/usr/bin/env python3
"""
run_v3_expansion.py — Run baseline calibration on the 21 additional tasks
to expand the baseline pool from 29 (v3_calibration.json) to 50 total.

This script is idempotent: it reads v3_calibration.json and only runs tasks
that haven't been graded yet (passed=None or missing).

Usage:
  python carb_benchmark/scripts/run_v3_expansion.py [--timeout-minutes 40]
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

# The 21 new tasks for the expansion
EXPANSION_TASKS = [
    # Django (15min-1h, medium difficulty)
    "django__django-11119",
    "django__django-11133",
    "django__django-11880",
    "django__django-12419",
    "django__django-15851",
    "django__django-17029",
    # Matplotlib (15min-1h)
    "matplotlib__matplotlib-23299",
    "matplotlib__matplotlib-23476",
    "matplotlib__matplotlib-24177",
    "matplotlib__matplotlib-24627",
    # Sphinx (<15min fix)
    "sphinx-doc__sphinx-8595",
    "sphinx-doc__sphinx-9230",
    "sphinx-doc__sphinx-9367",
    "sphinx-doc__sphinx-9698",
    "sphinx-doc__sphinx-10435",
    # Pytest (<15min fix)
    "pytest-dev__pytest-5262",
    "pytest-dev__pytest-7521",
    # SymPy (mixed difficulty)
    "sympy__sympy-13480",
    "sympy__sympy-14711",
    "sympy__sympy-23950",
    # Scikit-learn (<15min fix)
    "scikit-learn__scikit-learn-14141",
]


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
    config = "baseline-v2.0"
    notes = "v3 expansion (50-task baseline)"
    timeout_minutes = 40
    if "--config" in args:
        config = args[args.index("--config") + 1]
    if "--timeout-minutes" in args:
        timeout_minutes = int(args[args.index("--timeout-minutes") + 1])

    prog = load_progress()
    if prog["config"] is None:
        prog["config"] = config
        prog["notes"] = notes
        prog["started_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    results = prog["results"]

    already_done = sum(1 for t in EXPANSION_TASKS if t in results and results[t].get("passed") is not None)
    to_run = [t for t in EXPANSION_TASKS if t not in results or results[t].get("passed") is None]

    print(f"V3 expansion: {len(EXPANSION_TASKS)} tasks | "
          f"{already_done} already graded | {len(to_run)} to run", flush=True)

    for i, task in enumerate(to_run, 1):
        rec = results.get(task)
        if rec is not None:
            print(f"[{i}/{len(to_run)}] {task}: incomplete ({rec.get('error')}) -> re-run", flush=True)
        else:
            print(f"[{i}/{len(to_run)}] {task}: running baseline...", flush=True)
        t0 = time.time()
        rc = subprocess.run(
            [sys.executable, RUNNER, "--task", task, "--config", config,
             "--notes", notes, "--timeout-minutes", str(timeout_minutes)],
            cwd=SUPREME_ROOT,
        ).returncode
        wall = round(time.time() - t0, 1)
        ev_file = find_new_eval(task, t0 - 5)
        if ev_file is None:
            results[task] = {"run_id": None, "passed": None, "error": f"no eval record (rc={rc})"}
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
            print(f"    -> {'PASS' if d.get('passed') else 'FAIL'} "
                  f"({wall}s wall, {results[task]['diff']} lines) {d.get('run_id')}", flush=True)
        prog["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_progress(prog)

    # Summary
    all_results = results
    total_graded = sum(1 for r in all_results.values() if r.get("passed") is not None)
    passed = sum(1 for r in all_results.values() if r.get("passed"))
    failed = sum(1 for r in all_results.values() if r.get("passed") is False)
    rate = passed / (passed + failed) * 100 if (passed + failed) else 0
    print(f"\nExpansion complete. Total graded: {total_graded} | "
          f"passed={passed} failed={failed} | pass rate={rate:.1f}%", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
