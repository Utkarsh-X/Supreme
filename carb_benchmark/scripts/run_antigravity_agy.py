#!/usr/bin/env python3
"""
run_antigravity_agy.py — CARB-v1 Native Antigravity IDE Runner.
Executes benchmark tasks using local `agy.exe` CLI, routing through the 
Antigravity IDE internal engine & model router (Gemini 3.6 Flash High).
Enforces 0% Prompt Leakage Isolation for Phase 1 Baseline runs.
"""

import sys
import os
import json
import time
import subprocess
import argparse
import datetime
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
REGISTRY_DIR = os.path.join(BASE_DIR, 'task_registry')
WORKSPACES_DIR = os.path.join(os.path.dirname(BASE_DIR), 'carb_workspaces')
EVALUATIONS_DIR = os.path.join(BASE_DIR, 'evaluations')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
SELECTION_V2_PATH = os.path.join(REGISTRY_DIR, 'selection_candidates_v2.json')
CONSTITUTION_PATH = os.path.join(os.path.dirname(BASE_DIR), 'SupremeAgent', 'constitution.md')

sys.path.append(SCRIPTS_DIR)
from init_task import reset_workspace
from start_run import start_run
from finalize_run import finalize_run
from analyze_diff import analyze_patch

MODEL_NAME = "Gemini 3.6 Flash (High)"

def load_constitution():
    if os.path.exists(CONSTITUTION_PATH):
        with open(CONSTITUTION_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return "Supreme Engineering Constitution."

def build_prompt_for_phase(task, phase):
    orig_prompt = task['original_prompt']
    
    if phase == "baseline":
        return orig_prompt
    elif phase == "constitution":
        constitution = load_constitution()
        return f"""[SYSTEM CONSTITUTION INSTRUCTION]
{constitution}

[USER TASK REQUIREMENT]
{orig_prompt}"""
    elif phase == "full":
        constitution = load_constitution()
        return f"""[SYSTEM ARCHITECTURE: SUPREME AGENT FULL SYSTEM]
{constitution}

[OPERATING PROTOCOL & STATE TRACKING]
- Core Objective: Produce correct, verified, justified progress while preserving system integrity.
- Surgical Editing Rule: Identify exact region of behavior, minimum justified change.
- Verification Rule: Mandatory evidence before completing (compiler, unit tests, runtime output).
- Decision Framework: Observe -> Simulate -> Modify local code -> Verify acceptance criteria.

[USER TASK REQUIREMENT]
{orig_prompt}"""
    else:
        raise ValueError(f"Unknown phase: {phase}")

def execute_task_with_agy(task, target_task_id, phase, config_id):
    workspace_path = os.path.join(WORKSPACES_DIR, target_task_id)
    prompt = build_prompt_for_phase(task, phase)
    
    env = os.environ.copy()
    env.pop("GOOGLE_API_KEY", None)
    env.pop("GEMINI_API_KEY", None)

    # For Phase 1 Baseline, isolate AppData / UserProfile to guarantee 0% Supreme Rule leakage while preserving IDE auth
    if phase == "baseline":
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
    parser = argparse.ArgumentParser(description="Run CARB-v1 phase via Antigravity agy CLI")
    parser.add_argument("--phase", required=True, choices=["baseline", "constitution", "full"], help="Phase to execute")
    args = parser.parse_args()

    phase = args.phase
    config_id = f"{phase}-v1.0"

    print("==========================================================================")
    print(f"  CARB-v1 NATIVE ANTIGRAVITY AGY BENCHMARK RUNNER ({phase.upper()})        ")
    print(f"  Model: {MODEL_NAME} | Engine: agy.exe | Config: {config_id}        ")
    print("==========================================================================")

    if not os.path.exists(SELECTION_V2_PATH):
        print(f"Error: {SELECTION_V2_PATH} not found.")
        sys.exit(1)

    with open(SELECTION_V2_PATH, 'r', encoding='utf-8') as f:
        v2_data = json.load(f)

    tasks = v2_data.get('primary_candidates', [])
    total_tasks = len(tasks)
    print(f"\nLoaded {total_tasks} primary tasks for {phase.upper()} execution.\n")

    summary_results = []
    passed_count = 0

    start_time_all = datetime.datetime.now()

    for idx, task in enumerate(tasks, 1):
        cand_id = task['candidate_id']
        source = task['source']
        orig_id = task['original_task_id']

        if cand_id in ["C_SWE_001", "C_SWE_002", "C_SWE_003"]:
            target_task_id = "T001_sample_repo_debug"
        elif cand_id in ["C_TB_001", "C_TB_002"]:
            target_task_id = "T002_environment_tooling"
        elif cand_id in ["C_DIAG_001", "C_DIAG_002"]:
            target_task_id = "T003_diagnostic_premature_completion"
        else:
            target_task_id = "T001_sample_repo_debug"

        print(f"[{idx:02d}/{total_tasks:02d}] Antigravity CLI Execution: Task '{cand_id}' ({orig_id})...")

        # 1. Reset Workspace to Golden Snapshot
        reset_workspace(target_task_id, enforce_hashes=True)

        # 2. Start Run Session
        run_id, manifest_path = start_run(target_task_id, config_id)
        run_dir = os.path.join(BASE_DIR, "runs", run_id)
        workspace_path = os.path.join(WORKSPACES_DIR, target_task_id)

        # 3. Execute via agy CLI inside workspace
        passed, duration, agy_out, test_out = execute_task_with_agy(task, target_task_id, phase, config_id)

        status = "SUCCESS" if passed else "FAILURE"
        if passed:
            passed_count += 1

        print(f"   -> Result: {status} | Duration: {duration}s")

        # 4. Extract Diff
        diff_cmd = subprocess.run(["git", "diff"], cwd=workspace_path, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace")
        patch_content = diff_cmd.stdout or ""
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

        summary_results.append({
            "task_index": idx,
            "candidate_id": cand_id,
            "original_task_id": orig_id,
            "source": source,
            "domain": task.get('domain'),
            "difficulty": task.get('difficulty'),
            "status": status,
            "duration_seconds": duration,
            "lines_changed": diff_metrics['total_lines_changed']
        })

    end_time_all = datetime.datetime.now()
    total_duration_secs = (end_time_all - start_time_all).total_seconds()

    # Save Aggregated Summary Report
    os.makedirs(RESULTS_DIR, exist_ok=True)
    report_path = os.path.join(RESULTS_DIR, f"phase_{phase}_antigravity_summary.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "phase": f"PHASE — NATIVE ANTIGRAVITY IDE {phase.upper()}",
            "model": MODEL_NAME,
            "engine": "agy.exe",
            "configuration_id": config_id,
            "total_tasks": total_tasks,
            "passed_count": passed_count,
            "failed_count": total_tasks - passed_count,
            "pass_rate": f"{round(passed_count/total_tasks*100, 1)}%",
            "total_duration_seconds": total_duration_secs,
            "results": summary_results
        }, f, indent=2)

    print("\n==========================================================================")
    print(f"       NATIVE ANTIGRAVITY AGY {phase.upper()} SUITE COMPLETE               ")
    print("==========================================================================")
    print(f"Total Tasks Tested : {total_tasks}")
    print(f"Passed             : {passed_count} ({round(passed_count/total_tasks*100, 1)}%)")
    print(f"Total Duration     : {round(total_duration_secs, 2)} seconds")
    print(f"Summary Saved To   : {report_path}\n")

if __name__ == '__main__':
    main()
