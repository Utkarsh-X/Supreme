#!/usr/bin/env python3
"""
eval_swe.py — grade a SWE-bench workspace after the agent has edited it.

Runs the instance's REAL hidden tests (FAIL_TO_PASS) against the agent's
workspace state:

  1. apply the hidden test patch (private/test_patch.patch) ON TOP of the
     agent's changes (the workspace is NOT reset — the agent's fix must stay),
  2. run the FAIL_TO_PASS tests in the era-appropriate venv (same machinery
     as validation: per-repo Python + pinned deps + compiled overlay),
  3. exit 0 iff every F2P test passes.

The test patch + F2P list live only in carb_benchmark/private/<task_id>/,
never in the agent-visible workspace.
"""
import importlib.util
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE)
PRIVATE = os.path.join(BASE, "private")
WORKSPACES = os.path.join(SUPREME_ROOT, "carb_workspaces")

# load validate_swe_tasks as a module without running its main()
spec = importlib.util.spec_from_file_location(
    "vst", os.path.join(BASE, "scripts", "validate_swe_tasks.py"))
vst = importlib.util.module_from_spec(spec)
sys.modules["vst"] = vst
spec.loader.exec_module(vst)


def grade_task(task_id: str) -> int:
    workspace = vst.WORKSPACES / task_id
    private = vst.PRIVATE / task_id
    spec_path = private / "evaluation_spec.json"
    if not spec_path.exists():
        print(f"ERROR: no evaluation_spec.json for {task_id}")
        return 1
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    f2p = json.loads(spec.get("FAIL_TO_PASS", "[]"))
    if not f2p:
        print(f"ERROR: no FAIL_TO_PASS in spec for {task_id}")
        return 1

    # repo + package version from the verified dataset
    verified = {}
    with vst.VERIFIED.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                verified[r["instance_id"]] = r
    v = verified.get(task_id)
    if v is None:
        print(f"ERROR: {task_id} not in verified dataset")
        return 1
    repo = v["repo"].split("/")[1]
    pkg_version = v["version"]

    venv = vst.ensure_venv(repo, pkg_version)
    if venv is None:
        print(f"ERROR: venv setup failed for {task_id}")
        return 1
    vst.overlay_compiled(venv, repo, pkg_version, workspace)
    if repo == "pytest":
        vst.prepare_pytest_version(workspace, vst.get_install_root(workspace, repo), pkg_version)
    if repo == "scikit-learn":
        vst.write_sklearn_compat(venv)
        vst.write_sklearn_shims(workspace)

    # --- evaluation semantics (mirrors official SWE-bench) ---
    # 1. capture the agent's changes,
    # 2. reset the workspace to the base commit,
    # 3. re-apply ONLY the agent's non-test-file changes (test-file edits are
    #    discarded: the hidden tests are applied from the clean test patch, so
    #    an agent that "fixes" by weakening visible tests still fails, while a
    #    correct source fix is not penalized for a benign test-file touch),
    # 4. apply the hidden test patch, run FAIL_TO_PASS.
    import subprocess

    def git(*args):
        return subprocess.run(["git"] + list(args), cwd=str(workspace),
                              capture_output=True, text=True, encoding="utf-8")

    agent_diff = git("diff").stdout
    if not agent_diff.strip():
        print(f"FAIL: no changes made by agent in {task_id}")
        return 1

    # filter the agent diff to non-test files: split into per-file blocks and
    # drop whole blocks whose path is a test file (robust against hunk mangles)
    #
    # NOTE: test-file detection is by exact segment / filename pattern, NOT by
    # substring search — a substring match for "test" misclassifies package
    # dirs like src/_pytest ("pytest" contains "test") and silently discards
    # every pytest source fix during evaluation (observed 2026-08-17: all six
    # pytest-5262 / pytest-7521 sessions graded against unfixed base code).
    TEST_DIRS = {"test", "tests", "testing"}
    TEST_FILES = {"conftest.py", "runtests.py", "tests.py", "test.py"}

    def _is_test_path(target: str) -> bool:
        for seg in target.split("/"):
            s = seg.lower()
            if s in TEST_DIRS or s in TEST_FILES:
                return True
            if s.startswith("test_") or s.endswith("_test.py"):
                return True
        return False

    blocks = agent_diff.split("\ndiff --git ")
    kept = []
    for i, blk in enumerate(blocks):
        if i == 0:
            header = blk
        else:
            header = "diff --git " + blk
        path_line = header.split("\n", 1)[0]
        target = path_line.split(" b/", 1)[-1] if " b/" in path_line else ""
        if not _is_test_path(target):
            # block must end with exactly one newline or git apply rejects the
            # last hunk as corrupt (the split consumed the trailing newline)
            kept.append(header.rstrip("\n") + "\n")
    filtered = "".join(kept)

    git("checkout", "--", ".")
    git("clean", "-fd")
    if filtered:
        r = subprocess.run(["git", "apply", "--recount", "-"], cwd=str(workspace),
                           input=filtered, capture_output=True, text=True,
                           encoding="utf-8")
        if r.returncode != 0:
            print(f"FAIL: agent source patch could not be re-applied: {r.stderr[-400:]}")
            return 1

    test_patch = private / "test_patch.patch"
    if not vst.apply_patch(workspace, test_patch):
        print(f"FAIL: hidden test patch could not be applied for {task_id}")
        return 1

    args = vst.resolve_test_args(f2p, test_patch, workspace, repo)
    unresolvable = [a for a in args if a.startswith("__UNRESOLVABLE__")]
    if unresolvable:
        print(f"FAIL: F2P labels not mappable: {unresolvable}")
        return 1

    rc, out = vst.run_tests(venv, workspace, repo, args, "EVAL")
    print(out[-2500:])
    if rc == 0:
        print(f"PASS: {task_id} — all FAIL_TO_PASS tests passed")
        return 0
    print(f"FAIL: {task_id} — FAIL_TO_PASS rc={rc}")
    return 1


if __name__ == "__main__":
    task_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not task_id:
        print("usage: eval_swe.py <task_id>")
        sys.exit(2)
    sys.exit(grade_task(task_id))
