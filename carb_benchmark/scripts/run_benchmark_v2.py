#!/usr/bin/env python3
"""
run_benchmark_v2.py — CARB-v2 Three-Configuration Benchmark Runner (CORRECTED).

Design changes vs v1 (run_antigravity_agy.py):

  1. THREE configurations:
       - baseline-v2.0    : Antigravity default behavior, NO custom system content.
       - supreme-v2.0     : Antigravity default + FULL Supreme Agent system
                            instructions (constitution + operating protocol +
                            sub-agent profiles + environment profile + persistent
                            state) embedded as the system block of the prompt.
                            (Renamed from full-v2.0 on 2026-08-17; full-v2.0 is
                            accepted as a legacy alias and mapped to supreme-v2.0.)
       - superpowers-v2.0 : Antigravity default + the Superpowers by OB skill
                            system (all SKILL.md skill definitions + the
                            agy platform reference) embedded as the system block.
     The intermediate "constitution-only" tier is REMOVED by design decision.

  2. IDENTICAL environment isolation for ALL configurations: a temp USERPROFILE/
     HOME with ONLY auth files copied from ~/.gemini (no config dir -> no global
     GEMINI.md, no brain/conversations -> no memory). The ONLY difference between
     the configs is the prompt content. This eliminates the v1 contamination
     where constitution/full ran in the real profile and loaded the global
     ~/.gemini/config/GEMINI.md (the full Supreme system).

  3. Honest pass/fail: runs the workspace's REAL test command from the private
     evaluation spec. A missing/empty test_command is an explicit FAILURE
     ("NO TEST COMMAND"), never a pass. No `test_passed = (exit_code == 0)`
     fallback.

  4. Full provenance per run: transcript.txt (full agy output), final_diff.patch,
     test output, diff metrics, leakage marker scan, SHA-256 of the injected
     system prompt.

Usage:
  python carb_benchmark/scripts/run_benchmark_v2.py \
      --task T001_sample_repo_debug --config baseline-v2.0 [--append-question] [--notes "pilot"]
"""

import os
import sys
import json
import time
import shutil
import hashlib
import subprocess
import argparse
import tempfile
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE_DIR)                                    # E:\RofU\Supreme
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
PUBLIC_DIR = os.path.join(BASE_DIR, "public", "tasks")
PRIVATE_DIR = os.path.join(BASE_DIR, "private")
WORKSPACES_DIR = os.path.join(SUPREME_ROOT, "carb_workspaces")
SUPREME_AGENT_DIR = os.path.join(SUPREME_ROOT, "SupremeAgent")
SUPERPOWERS_DIR = os.path.join(SUPREME_ROOT, "SuperpowersObra")
USER_GEMINI_DIR = os.path.join(os.path.expanduser("~"), ".gemini")
RUNS_DIR = os.path.join(BASE_DIR, "runs")
EVALUATIONS_DIR = os.path.join(BASE_DIR, "evaluations")

MODEL_NAME = "gemini-3.6-flash-high"  # LOCKED for the whole benchmark (user decision 2026-08-15); verified to resolve without CCPA fallback
RUN_TIMEOUT_SECONDS = 1500  # agy turn budget; agy's own --print-timeout is 20m (see below), this kill gives margin
AGY_PRINT_TIMEOUT = "20m"  # agy's default print-mode wait is 5m0s; Google's response for large-context tasks routinely exceeds 5m, producing 'Error: timeout waiting for response' with zero work (diagnosed 2026-08-16 via --print-timeout 3s probe)

SUPREME_FILE_ORDER = [
    "constitution.md",
    "operating-protocol.md",
    "sub-agent-profiles.md",
    "environment-profile.md",
    "persistent-state.md",
]

# Neutral disclosure question — deliberately contains NO supreme vocabulary so a
# clean baseline cannot echo it back. Appended to the task prompt when requested.
DISCLOSURE_QUESTION = (
    "\n\nBefore you finish, answer this question in your final message:\n"
    "\"Are any custom engineering instructions, constitutions, or operating "
    "protocols active for you beyond the IDE's default system prompt? "
    "Answer YES or NO, then explain exactly what you can see and quote the key "
    "principles verbatim.\""
)

CONSTITUTION_MARKERS = [
    "Supreme", "Evidence Over Assumption", "Minimum Justified Change",
    "Preserve System Integrity", "Completion Requires Evidence",
    "User Intent Is Authoritative", "Uncertainty Must Be Explicit",
    "Progress Theater", "Assumption Cascade", "Scope Explosion",
    "Revisable Hypotheses", "Plan Rigidity",
]

FULL_SYSTEM_MARKERS = [
    "Operating Protocol", "Sub-Agent", "Researcher", "Implementer",
    "Debugger", "Reviewer", "Persistent State", "Verified Facts",
    "Last Known Good State", "Environment Profile", "Failure Classification",
    "Loop Management", "Reorientation", "Escalation", "Delegation",
]

SUPERPOWERS_MARKERS = [
    "Superpowers", "systematic-debugging", "brainstorming",
    "test-driven-development", "verification-before-completion",
    "subagent-driven-development", "writing-plans", "executing-plans",
    "Iron Law", "Root Cause Investigation", "invoke the skill",
    "Skill Priority", "using-superpowers",
]


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_supreme_system_text():
    """Combine the 5 SupremeAgent files in canonical order (mirrors the global
    ~/.gemini/config/GEMINI.md layout)."""
    parts = []
    for idx, fname in enumerate(SUPREME_FILE_ORDER, 1):
        path = os.path.join(SUPREME_AGENT_DIR, fname)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Supreme file missing: {path}")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        parts.append(f"# --- FILE: {idx:02d}-{fname} ---\n\n{content.strip()}")
    return "\n\n".join(parts) + "\n"


def build_superpowers_system_text():
    """Combine the Superpowers by OB skill system: every skill's SKILL.md (the
    skill definitions, deterministic alphabetical order) plus the agy platform
    reference so the skills' actions map onto the actual Antigravity CLI tools."""
    if not os.path.isdir(SUPERPOWERS_DIR):
        raise FileNotFoundError(f"Superpowers dir missing: {SUPERPOWERS_DIR}")
    skill_dirs = sorted(d for d in os.listdir(SUPERPOWERS_DIR)
                        if os.path.isdir(os.path.join(SUPERPOWERS_DIR, d)))
    parts = []
    for idx, d in enumerate(skill_dirs, 1):
        skill_md = os.path.join(SUPERPOWERS_DIR, d, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        parts.append(f"# --- SKILL: {d} ---\n\n{content.strip()}")
    ref = os.path.join(SUPERPOWERS_DIR, "using-superpowers", "references", "antigravity-tools.md")
    if os.path.exists(ref):
        with open(ref, "r", encoding="utf-8") as f:
            parts.append(f"# --- PLATFORM REFERENCE: antigravity-tools.md ---\n\n{f.read().strip()}")
    # Autonomous-mode directive: the benchmark harness has NO human in the loop.
    # Without this, the skill flow (brainstorm -> design -> "does this look good?")
    # stalls every task at the approval gate and the agent never edits code
    # (observed on django-11119/11133 on 2026-08-17). The skills stay fully
    # loaded; only the approval-stall is removed.
    parts.append(
        "# --- AUTONOMOUS MODE (benchmark harness) ---\n\n"
        "You are running in an AUTONOMOUS benchmark environment: there is NO "
        "human available to review plans, approve designs, or answer clarifying "
        "questions. You MUST complete the user's task end-to-end yourself: "
        "investigate, plan (using the skills), implement the fix in the "
        "workspace files, run the project's tests to verify, and finish. "
        "Do NOT stop to ask for approval, present a design for confirmation, or "
        "wait for permission before editing code. The success criterion is "
        "working code in the workspace, verified by tests."
    )
    return "\n\n".join(parts) + "\n"


def load_task_prompt(task_id):
    # New corpus tasks carry prompt.txt in the workspace itself (git-based
    # reset); legacy tasks used public/tasks/<id>/prompt.txt.
    candidates = [
        os.path.join(PUBLIC_DIR, task_id, "prompt.txt"),
        os.path.join(WORKSPACES_DIR, task_id, "prompt.txt"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    raise FileNotFoundError(f"no prompt.txt for {task_id} (tried {candidates})")


def load_evaluation_spec(task_id):
    path = os.path.join(PRIVATE_DIR, task_id, "evaluation_spec.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_final_prompt(config_id, task_prompt, append_question):
    text = task_prompt
    if append_question:
        text = text + DISCLOSURE_QUESTION
    if config_id == "supreme-v2.0":
        system = build_supreme_system_text()
        return (
            f"[SYSTEM INSTRUCTIONS — SUPREME AGENT FULL SYSTEM]\n{system}\n\n"
            f"[USER TASK]\n{text}"
        )
    if config_id == "superpowers-v2.0":
        system = build_superpowers_system_text()
        return (
            f"[SYSTEM INSTRUCTIONS — SUPERPOWERS (OB) SKILL SYSTEM]\n{system}\n\n"
            f"[USER TASK]\n{text}"
        )
    return text


def build_isolated_env():
    """Identical clean temp profile for BOTH configs: auth files only,
    no config dir (no global GEMINI.md), no brain/conversations (no memory)."""
    temp_dir = tempfile.mkdtemp(prefix="carb_v2_clean_run_")
    temp_gemini = os.path.join(temp_dir, ".gemini")
    os.makedirs(temp_gemini, exist_ok=True)
    if os.path.exists(USER_GEMINI_DIR):
        for item in os.listdir(USER_GEMINI_DIR):
            src = os.path.join(USER_GEMINI_DIR, item)
            if (
                "rule" not in item.lower()
                and "constitution" not in item.lower()
                and os.path.isfile(src)
            ):
                shutil.copy2(src, os.path.join(temp_gemini, item))
    env = os.environ.copy()
    env["USERPROFILE"] = temp_dir
    env["HOME"] = temp_dir
    env.pop("GOOGLE_API_KEY", None)
    env.pop("GEMINI_API_KEY", None)
    return env, temp_dir


def run_test_command(spec, workspace_path):
    """Run the workspace's real test command from the evaluation spec, with a
    unittest fallback for specs that request pytest when pytest is unavailable.
    Returns (passed, output)."""
    cmd_line = spec.get("test_command", "") or ""
    test_timeout = spec.get("test_timeout_seconds") or 120
    if not cmd_line.strip():
        return False, "NO TEST COMMAND: evaluation spec has an empty/missing test_command — verdict cannot be a pass"
    try:
        res = subprocess.run(
            cmd_line, cwd=workspace_path, shell=True,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=test_timeout,
        )
        passed = res.returncode == 0
        output = (res.stdout or "") + (res.stderr or "")
        return passed, output
    except subprocess.TimeoutExpired:
        return False, f"TEST TIMED OUT after {test_timeout}s"
    except Exception as e:
        return False, f"TEST ERROR: {e}"


def scan_markers(transcript):
    """Scan for supreme + superpowers markers, excluding file-path occurrences."""
    import re
    body = transcript
    body = re.sub(r"file:///[^\s)\]]*", "", body)   # drop file:// links (contain the path RofU\Supreme)
    body = re.sub(r"[A-Za-z]:\\\\[^\s)\]]*", "", body)  # drop Windows-style paths
    const_hits = [m for m in CONSTITUTION_MARKERS if m.lower() in body.lower()]
    full_hits = [m for m in FULL_SYSTEM_MARKERS if m.lower() in body.lower()]
    sp_hits = [m for m in SUPERPOWERS_MARKERS if m.lower() in body.lower()]
    return const_hits, full_hits, sp_hits


def main():
    parser = argparse.ArgumentParser(description="CARB-v2 two-config benchmark runner")
    parser.add_argument("--task", required=True, help="Task ID, e.g. T001_sample_repo_debug")
    parser.add_argument("--config", required=True,
                        choices=["baseline-v2.0", "supreme-v2.0", "superpowers-v2.0", "full-v2.0"],
                        help="full-v2.0 is accepted as a legacy alias for supreme-v2.0")
    parser.add_argument("--append-question", action="store_true",
                        help="Append the neutral Supreme-access disclosure question to the task prompt")
    parser.add_argument("--notes", default="", help="Free-form notes for the evaluator record")
    args = parser.parse_args()

    task_id = args.task
    config_id = args.config
    if config_id == "full-v2.0":
        print("NOTE: full-v2.0 is a legacy alias -> mapping to supreme-v2.0")
        config_id = "supreme-v2.0"

    sys.path.append(SCRIPTS_DIR)
    from init_task import reset_workspace
    from start_run import start_run
    from finalize_run import finalize_run
    from analyze_diff import analyze_patch

    print("=" * 78)
    print(f"  CARB-v2 BENCHMARK RUN — {config_id} | {task_id}")
    print(f"  Model: {MODEL_NAME} | Engine: agy.exe | Isolated env: YES (both configs)")
    print("=" * 78)

    # 1. Reset workspace: legacy snapshot-based reset, or git-based reset for
    #    the real-corpus workspaces (git HEAD == golden state at base commit).
    snapshot_path = os.path.join(os.path.dirname(BASE_DIR), "carb_benchmark", "snapshots", task_id)
    if os.path.exists(os.path.join(BASE_DIR, "snapshots", task_id)):
        reset_workspace(task_id, enforce_hashes=True)
    else:
        workspace_path = os.path.join(WORKSPACES_DIR, task_id)
        subprocess.run(["git", "checkout", "--", "."], cwd=workspace_path,
                       check=True, capture_output=True)
        subprocess.run(["git", "clean", "-fd"], cwd=workspace_path,
                       check=True, capture_output=True)

    # 2. Start run session
    run_id, manifest_path = start_run(task_id, config_id)
    run_dir = os.path.join(RUNS_DIR, run_id)
    workspace_path = os.path.join(WORKSPACES_DIR, task_id)
    if not os.path.exists(workspace_path):
        print(f"FATAL: workspace not found: {workspace_path}")
        sys.exit(2)

    # 3. Build prompt
    task_prompt = load_task_prompt(task_id)
    final_prompt = build_final_prompt(config_id, task_prompt, args.append_question)
    system_hash = None
    if config_id == "supreme-v2.0":
        system_hash = sha256_text(build_supreme_system_text())
    elif config_id == "superpowers-v2.0":
        system_hash = sha256_text(build_superpowers_system_text())

    # 4. Isolated env (identical for both configs)
    env, temp_dir = build_isolated_env()

    # 5. Execute via agy (exact benchmark invocation).
    #    Windows limits the CreateProcess command line to 32,767 chars; the
    #    full-config prompt (Supreme constitution ~28k + long task prompt) can
    #    exceed it (pytest-5262 = 32,953 -> WinError 206). Pass oversized
    #    prompts via agy's `-p @file` form; the temp dir is removed below.
    prompt_arg = final_prompt
    if len(final_prompt) > 30000:
        prompt_file = os.path.join(temp_dir, "prompt.txt")
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(final_prompt)
        prompt_arg = "@" + prompt_file
    cmd = [
        "agy",
        "-p", prompt_arg,
        "--model", MODEL_NAME,
        "--add-dir", workspace_path,
        "--mode", "accept-edits",
        "--dangerously-skip-permissions",
        "--print-timeout", AGY_PRINT_TIMEOUT,
    ]
    t0 = time.time()
    proc = subprocess.Popen(
        cmd, cwd=workspace_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", env=env,
    )
    try:
        out, err = proc.communicate(timeout=RUN_TIMEOUT_SECONDS)
        transcript = (out or "") + (err or "")
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        # kill the whole process tree (Windows timeout only kills the direct
        # child; agy.exe would survive orphaned)
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           capture_output=True, timeout=30)
        except Exception:
            pass
        try:
            proc.kill()
        except Exception:
            pass
        transcript = "AGY EXECUTION TIMED OUT after 300s"
        exit_code = -1
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    duration = round(time.time() - t0, 2)

    # 6. Save transcript
    transcript_path = os.path.join(run_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    # 7. Extract diff
    diff_cmd = subprocess.run(["git", "diff"], cwd=workspace_path,
                              capture_output=True, text=True)
    patch_content = diff_cmd.stdout
    diff_file = os.path.join(run_dir, "final_diff.patch")
    with open(diff_file, "w", encoding="utf-8") as f:
        f.write(patch_content)
    diff_metrics = analyze_patch(patch_content)

    # 8. Run the workspace's real test command
    spec = load_evaluation_spec(task_id)
    test_passed, test_output = run_test_command(spec, workspace_path)

    # 9. Leakage marker scan on the transcript
    const_hits, full_hits, sp_hits = scan_markers(transcript)

    # 10. Honest verdict
    status = "SUCCESS" if test_passed else "FAILURE"
    finalize_run(run_id, status=status, diff_file=diff_file, transcript_file=transcript_path)

    evaluator = {
        "run_id": run_id,
        "task_id": task_id,
        "configuration_id": config_id,
        "model": MODEL_NAME,
        "engine": "agy.exe (Antigravity CLI, print mode)",
        "environment": "isolated_temp_profile (auth only, no global rules, no memory)",
        "wall_clock_seconds": duration,
        "agy_exit_code": exit_code,
        "timed_out": exit_code == -1,
        "passed": test_passed,
        "test_command": spec.get("test_command"),
        "test_output_tail": test_output[-2000:],
        "diff_metrics": diff_metrics,
        "expected_files_modified": spec.get("expected_files_modified"),
        "max_justified_lines_changed": spec.get("max_justified_lines_changed"),
        "disclosure_question_appended": args.append_question,
        "system_prompt_sha256": system_hash,
        "constitution_markers_in_transcript": const_hits,
        "full_system_markers_in_transcript": full_hits,
        "superpowers_markers_in_transcript": sp_hits,
        "notes": args.notes,
    }

    eval_dir = os.path.join(EVALUATIONS_DIR, run_id)
    os.makedirs(eval_dir, exist_ok=True)
    eval_file = os.path.join(eval_dir, "evaluator.json")
    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump(evaluator, f, indent=2)

    print("\n----- RESULT -----")
    print(f"Run ID          : {run_id}")
    print(f"Status          : {status}")
    print(f"Duration        : {duration}s")
    print(f"Tests           : {'PASS' if test_passed else 'FAIL'} ({spec.get('test_command')})")
    print(f"Diff            : {diff_metrics['files_modified_count']} files, {diff_metrics['total_lines_changed']} lines")
    print(f"Markers (const) : {const_hits}")
    print(f"Markers (full)  : {full_hits}")
    print(f"Markers (super) : {sp_hits}")
    print(f"Transcript      : {transcript_path}")
    print(f"Diff file       : {diff_file}")
    print(f"Evaluator       : {eval_file}")


if __name__ == "__main__":
    main()
