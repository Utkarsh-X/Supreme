#!/usr/bin/env python3
"""
run_v3_final_expansion.py — Run baseline calibration on 67 new tasks
(9 VALIDATED SWE + 20 existing LCB + 38 new hard LCB) to push the
baseline-fail count toward 50.

This covers every remaining materialized workspace in carb_workspaces/.

Idempotent: reads v3_calibration.json and only runs tasks not yet graded.

Usage:
  python carb_benchmark/scripts/run_v3_final_expansion.py [--timeout-minutes 40]
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

FINAL_TASKS = [
    # ---- 9 VALIDATED SWE (all untested, validated via validate_swe_tasks.py) ----
    "django__django-11179",
    "django__django-12965",
    "django__django-14089",
    "django__django-14493",
    "django__django-16082",
    "django__django-16485",
    "sympy__sympy-15875",
    "sympy__sympy-16886",
    "sympy__sympy-19637",
    # ---- 20 existing LCB (medium _c/_d + easy _a/_b variants) ----
    "lcb__abc387_b",
    "lcb__abc388_c",
    "lcb__abc389_d",
    "lcb__abc390_c",
    "lcb__abc391_d",
    "lcb__abc392_b",
    "lcb__abc393_b",
    "lcb__abc394_b",
    "lcb__abc395_b",
    "lcb__abc396_b",
    "lcb__abc397_c",
    "lcb__abc398_b",
    "lcb__abc399_b",
    "lcb__abc400_c",
    "lcb__arc190_a",
    "lcb__arc191_a",
    "lcb__arc192_a",
    "lcb__arc193_a",
    "lcb__arc194_a",
    "lcb__arc195_a",
    # ---- 38 new hard LCB (materialized 2026-08-19) ----
    "lcb__abc397_g",
    "lcb__abc398_f",
    "lcb__abc398_g",
    "lcb__abc399_f",
    "lcb__abc400_g",
    "lcb__arc190_d",
    "lcb__arc191_d",
    "lcb__arc192_e",
    "lcb__arc192_d",
    "lcb__arc193_d",
    "lcb__arc194_c",
    "lcb__arc194_e",
    "lcb__arc194_d",
    "lcb__arc195_e",
    "lcb__arc195_c",
    "lcb__arc195_d",
    "lcb__arc196_c",
    "lcb__arc196_d",
    "lcb__3674",
    "lcb__3725",
    "lcb__3697",
    "lcb__3696",
    "lcb__3762",
    "lcb__3733",
    "lcb__3781",
    "lcb__3770",
    "lcb__3789",
    "lcb__3801",
    "lcb__3744",
    "lcb__3717",
    "lcb__3777",
    "lcb__3687",
    "lcb__3739",
    "lcb__3701",
    "lcb__3692",
    "lcb__3783",
    "lcb__3784",
    "lcb__3765",
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
    notes = "v3 final expansion (all remaining workspaces)"
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

    already_done = sum(1 for t in FINAL_TASKS if t in results and results[t].get("passed") is not None)
    to_run = [t for t in FINAL_TASKS if t not in results or results[t].get("passed") is None]

    print(f"V3 final expansion: {len(FINAL_TASKS)} tasks | "
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
    print(f"\nFinal expansion complete. Total graded: {total_graded} | "
          f"passed={passed} failed={failed} | pass rate={rate:.1f}%", flush=True)
    print(f"Target: 50 failing tasks | Current: {failed}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
