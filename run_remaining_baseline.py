#!/usr/bin/env python3
"""
run_remaining_baseline.py — Completes all remaining Phase 1 Baseline candidate tasks
via agy.exe with clean environment isolation (0% Supreme prompt leakage).
"""

import sys
import os
import json
import time
import subprocess
import datetime
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BENCH_DIR = os.path.join(BASE_DIR, 'carb_benchmark')
SCRIPTS_DIR = os.path.join(BENCH_DIR, 'scripts')
REGISTRY_DIR = os.path.join(BENCH_DIR, 'task_registry')
WORKSPACES_DIR = os.path.join(BASE_DIR, 'carb_workspaces')
EVALUATIONS_DIR = os.path.join(BENCH_DIR, 'evaluations')
RESULTS_DIR = os.path.join(BENCH_DIR, 'results')
SELECTION_V2_PATH = os.path.join(REGISTRY_DIR, 'selection_candidates_v2.json')

sys.path.append(SCRIPTS_DIR)
from init_task import reset_workspace
from start_run import start_run
from finalize_run import finalize_run
from analyze_diff import analyze_patch

MODEL_NAME = "Gemini 3.6 Flash (High)"

def execute_task_with_agy(task, target_task_id, phase, config_id):
    workspace_path = os.path.join(WORKSPACES_DIR, target_task_id)
    prompt = task['original_prompt']
    
    env = os.environ.copy()
    env.pop("GOOGLE_API_KEY", None)
    env.pop("GEMINI_API_KEY", None)

    # For Phase 1 Baseline, isolate AppData / UserProfile to guarantee 0% Supreme Rule leakage while preserving IDE auth
    user_gemini = r'C:\Users\Utkarsh\.gemini'
    temp_env_dir = tempfile.mkdtemp(prefix='clean_auth_baseline_run_')
    temp_gemini = os.path.join(temp_env_dir, '.gemini')
    os.makedirs(temp_gemini, exist_ok=True)

    if os.path.exists(user_gemini):
        import shutil
        for item in os.listdir(user_gemini):
            src = os.path.join(user_gemini, item)
            if 'rule' not in item.lower() and 'constitution' not in item.lower() and os.path.isfile(src):
                shutil.copy2(src, os.path.join(temp_gemini, item))

    env['USERPROFILE'] = temp_env_dir
    env['HOME'] = temp_env_dir

    cmd = [
        "agy",
        "-p", prompt,
        "--model", MODEL_NAME,
        "--add-dir", workspace_path,
        "--mode", "accept-edits",
        "--dangerously-skip-permissions"
    ]

    t0 = time.time()
    try:
        res = subprocess.run(
            cmd,
            cwd=workspace_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env,
            timeout=300
        )
        output_text = (res.stdout or "") + (res.stderr or "")
        exit_code = res.returncode
    except subprocess.TimeoutExpired:
        output_text = "AGY Execution Timed Out after 300s"
        exit_code = -1
    finally:
        import shutil
        shutil.rmtree(temp_env_dir, ignore_errors=True)
    t1 = time.time()

    duration = round(t1 - t0, 2)

    # Verification Step: Run workspace unit tests
    test_passed = False
    test_output = ""
    if os.path.exists(os.path.join(workspace_path, "test_session_serializer.py")):
        res_test = subprocess.run([sys.executable, "-m", "unittest", "test_session_serializer.py"], cwd=workspace_path, capture_output=True, text=True)
        test_passed = (res_test.returncode == 0)
        test_output = res_test.stdout + res_test.stderr
    elif os.path.exists(os.path.join(workspace_path, "test_auth_service.py")):
        res_test = subprocess.run([sys.executable, "-m", "unittest", "test_auth_service.py"], cwd=workspace_path, capture_output=True, text=True)
        test_passed = (res_test.returncode == 0)
        test_output = res_test.stdout + res_test.stderr
    elif os.path.exists(os.path.join(workspace_path, "build.py")):
        res_test = subprocess.run([sys.executable, "build.py"], cwd=workspace_path, capture_output=True, text=True)
        test_passed = (res_test.returncode == 0)
        test_output = res_test.stdout + res_test.stderr
    else:
        test_passed = (exit_code == 0)
        test_output = output_text

    return test_passed, duration, output_text, test_output

def main():
    config_id = "baseline-v1.0"
    phase = "baseline"

    print("==========================================================================")
    print("  CARB-v1 COMPLETING REMAINING PHASE 1 BASELINE TASKS                      ")
    print(f"  Model: {MODEL_NAME} | Engine: agy.exe | Config: {config_id}        ")
    print("==========================================================================")

    with open(SELECTION_V2_PATH, 'r', encoding='utf-8') as f:
        v2_data = json.load(f)

    tasks = v2_data.get('primary_candidates', [])
    
    # Identify already completed tasks
    completed = set()
    if os.path.exists(EVALUATIONS_DIR):
        for d in os.listdir(EVALUATIONS_DIR):
            ef = os.path.join(EVALUATIONS_DIR, d, 'evaluator.json')
            if os.path.exists(ef):
                with open(ef, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('configuration_id') == config_id:
                        completed.add(data.get('task_id'))

    remaining_tasks = [t for t in tasks if t['candidate_id'] not in completed]
    print(f"Already Completed: {len(completed)} / {len(tasks)}")
    print(f"Remaining Tasks to Run: {len(remaining_tasks)}")

    for idx, task in enumerate(remaining_tasks, 1):
        cand_id = task['candidate_id']
        source = task['source']
        orig_id = task['original_task_id']

        if cand_id in ["C_SWE_001", "C_SWE_002", "C_SWE_003"]:
            target_task_id = "T001_sample_repo_debug"
        elif cand_id.startswith("C_TB_"):
            target_task_id = "T002_environment_tooling"
        elif cand_id.startswith("C_DIAG_"):
            target_task_id = "T003_diagnostic_premature_completion"
        else:
            target_task_id = "T001_sample_repo_debug"

        print(f"\n[{idx:02d}/{len(remaining_tasks):02d}] Executing Remaining Task '{cand_id}' ({orig_id})...")

        # 1. Reset Workspace
        reset_workspace(target_task_id, enforce_hashes=True)

        # 2. Start Run Session
        run_id, manifest_path = start_run(target_task_id, config_id)
        run_dir = os.path.join(BENCH_DIR, "runs", run_id)
        workspace_path = os.path.join(WORKSPACES_DIR, target_task_id)

        # 3. Execute via agy CLI
        passed, duration, agy_out, test_out = execute_task_with_agy(task, target_task_id, phase, config_id)

        status = "SUCCESS" if passed else "FAILURE"
        print(f"   -> Result: {status} | Duration: {duration}s")

        # 4. Extract Diff
        diff_cmd = subprocess.run(["git", "diff"], cwd=workspace_path, capture_output=True, text=True)
        patch_content = diff_cmd.stdout
        diff_file = os.path.join(run_dir, "final_diff.patch")
        with open(diff_file, "w", encoding="utf-8") as f:
            f.write(patch_content)

        diff_metrics = analyze_patch(patch_content)

        # 5. Finalize Run Manifest
        finalize_run(run_id, status=status, diff_file=diff_file)

        # Save Evaluator JSON
        eval_dir = os.path.join(EVALUATIONS_DIR, run_id)
        os.makedirs(eval_dir, exist_ok=True)
        eval_file = os.path.join(eval_dir, "evaluator.json")
        with open(eval_file, "w", encoding="utf-8") as f:
            json.dump({
                "run_id": run_id,
                "task_id": cand_id,
                "configuration_id": config_id,
                "model": MODEL_NAME,
                "engine": "agy.exe (Antigravity Native Router)",
                "wall_clock_seconds": duration,
                "passed": passed,
                "lines_changed": diff_metrics['total_lines_changed']
            }, f, indent=2)

    # Re-compile Final Aggregated Summary Report across all 60 tasks
    all_summary_results = []
    all_passed_count = 0

    for task in tasks:
        cand_id = task['candidate_id']
        source = task['source']
        orig_id = task['original_task_id']
        
        task_passed = False
        task_duration = 0.0
        task_lines = 0

        for d in os.listdir(EVALUATIONS_DIR):
            ef = os.path.join(EVALUATIONS_DIR, d, 'evaluator.json')
            if os.path.exists(ef):
                with open(ef, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('configuration_id') == config_id and data.get('task_id') == cand_id:
                        task_passed = data.get('passed', False)
                        task_duration = data.get('wall_clock_seconds', 0.0)
                        task_lines = data.get('lines_changed', 0)
                        break

        if task_passed:
            all_passed_count += 1

        all_summary_results.append({
            "candidate_id": cand_id,
            "original_task_id": orig_id,
            "source": source,
            "domain": task.get('domain'),
            "difficulty": task.get('difficulty'),
            "status": "SUCCESS" if task_passed else "FAILURE",
            "duration_seconds": task_duration,
            "lines_changed": task_lines
        })

    os.makedirs(RESULTS_DIR, exist_ok=True)
    report_path = os.path.join(RESULTS_DIR, "phase_baseline_antigravity_summary.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "phase": "PHASE 1 — NATIVE ANTIGRAVITY IDE BASELINE",
            "model": MODEL_NAME,
            "engine": "agy.exe",
            "configuration_id": config_id,
            "total_tasks": len(tasks),
            "passed_count": all_passed_count,
            "failed_count": len(tasks) - all_passed_count,
            "pass_rate": f"{round(all_passed_count/len(tasks)*100, 1)}%",
            "results": all_summary_results
        }, f, indent=2)

    print("\n==========================================================================")
    print("       ALL 60 PHASE 1 BASELINE TASKS FULLY COMPLETED                      ")
    print("==========================================================================")
    print(f"Total Tasks Tested : {len(tasks)}")
    print(f"Passed             : {all_passed_count} ({round(all_passed_count/len(tasks)*100, 1)}%)")
    print(f"Summary Saved To   : {report_path}\n")

if __name__ == '__main__':
    main()
