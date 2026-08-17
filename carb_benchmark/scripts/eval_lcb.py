#!/usr/bin/env python3
"""
eval_lcb.py — grade a LiveCodeBench task workspace.

Runs the agent's main.py against EVERY private test case and compares output
using the official LiveCodeBench semantics (lcb_runner testing_util.grade_stdio):

  1. strip the full output; split into lines; strip each line
  2. line counts must match
  3. per line: exact string equality, else if both lines fully parse as
     Decimal numbers, Decimal equality

Exit code 0  -> all private tests passed
Exit code 1  -> at least one private test failed (report written to
                ../.. (BASE)/evaluations or printed)
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from decimal import Decimal, InvalidOperation

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE)
WORKSPACES = os.path.join(SUPREME_ROOT, "carb_workspaces")
PRIVATE = os.path.join(BASE, "private")

TIMEOUT_SECONDS = 5  # per test case (AtCoder limits are 2s; margin for slow machines)


def get_stripped_lines(val: str):
    val = val.strip()
    return [ln.strip() for ln in val.split("\n") if val]


def line_equal(prediction_line: str, gt_line: str) -> bool:
    if prediction_line == gt_line:
        return True
    try:
        d1 = [Decimal(e) for e in prediction_line.split()]
        d2 = [Decimal(e) for e in gt_line.split()]
    except InvalidOperation:
        return False
    return d1 == d2


# ---------------------------------------------------------------------------
# Checker for lcb__arc190_a (ARC190 A - Inside or Outside).
# The problem asks for ANY optimal operation assignment, so exact-string
# comparison against a single stored assignment is not a valid grade.
# Official semantics (per the problem statement): the printed assignment must
# (a) parse as K + M op types in {0,1,2},
# (b) have total cost exactly K and achieve full coverage of [1,N],
# (c) have K equal to the TRUE minimum cost.
# The true minimum is computed with the same (brute-force-verified) algorithm
# used by the reference solution.
# ---------------------------------------------------------------------------

_ARC190_SOLVER = None


def _arc190_solver():
    global _ARC190_SOLVER
    if _ARC190_SOLVER is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_arc190_ref", os.path.join(PRIVATE, "lcb__arc190_a", "reference_solution.py"))
        _ARC190_SOLVER = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_ARC190_SOLVER)
    return _ARC190_SOLVER


def _check_arc190a(inp: str, out: str):
    """Return (ok: bool, reason: str)."""
    lines = inp.strip().splitlines()
    try:
        n, m = map(int, lines[0].split())
        L, R = [], []
        for ln in lines[1:1 + m]:
            a, b = map(int, ln.split())
            L.append(a)
            R.append(b)
    except Exception:
        return False, "unparseable input"

    olines = [ln.strip() for ln in out.strip().splitlines() if ln.strip()]
    # unreachable answer: single line "-1"
    if len(olines) == 1 and olines[0] == "-1":
        true_min, _ = _arc190_solver().solve(n, m, L, R)
        if true_min is None:
            return True, None
        return False, f"not_minimal: printed -1 but goal IS achievable (min={true_min})"
    if len(olines) < 2:
        return False, "format_error: need K line + ops line"
    try:
        k = int(olines[0])
        ops = [int(x) for x in olines[1].split()]
    except ValueError:
        return False, "format_error: non-integer token"
    if len(ops) != m or any(x not in (0, 1, 2) for x in ops):
        return False, f"format_error: expected {m} op types in {{0,1,2}}, got {len(ops)}"

    covered = [False] * (n + 1)
    cost = 0
    for i, t in enumerate(ops):
        if t == 1:
            cost += 1
            for j in range(L[i], R[i] + 1):
                covered[j] = True
        elif t == 2:
            cost += 1
            for j in range(1, n + 1):
                if not (L[i] <= j <= R[i]):
                    covered[j] = True
    if cost != k:
        return False, f"cost_mismatch: printed K={k} but assignment cost={cost}"
    if not all(covered[1:]):
        return False, "not_covering: assignment leaves positions uncovered"

    true_min, _ = _arc190_solver().solve(n, m, L, R)
    if true_min is None:
        return False, "unreachable: goal not achievable"
    if k != true_min:
        return False, f"not_minimal: printed K={k} but true minimum is {true_min}"
    return True, None


USE_CHECKER = {"lcb__arc190_a": _check_arc190a}


def grade_task(task_id: str) -> int:
    ws = os.path.join(WORKSPACES, task_id)
    priv = os.path.join(PRIVATE, task_id)
    cases_path = os.path.join(priv, "private_test_cases.json")
    main_py = os.path.join(ws, "main.py")
    if not os.path.exists(cases_path):
        print(f"ERROR: no private test cases at {cases_path}")
        return 1
    if not os.path.exists(main_py):
        print(f"ERROR: no main.py at {main_py}")
        return 1
    with open(cases_path, encoding="utf-8") as f:
        cases = json.load(f)

    checker = USE_CHECKER.get(task_id)
    results = []
    passed = 0
    for idx, tc in enumerate(cases, 1):
        inp = tc["input"]
        expected = tc["output"]
        record = {"index": idx}
        try:
            t0 = time.time()
            res = subprocess.run(
                [sys.executable, "main.py"],
                cwd=ws,
                input=inp,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_SECONDS,
            )
            dt = time.time() - t0
            prediction = (res.stdout or "")
            if res.returncode != 0:
                record.update({"ok": False, "reason": "runtime_error",
                               "stderr_tail": (res.stderr or "")[-500:]})
            elif checker is not None:
                ok, reason = checker(inp, prediction)
                if ok:
                    record.update({"ok": True, "elapsed_s": round(dt, 3)})
                else:
                    record.update({"ok": False, "reason": reason,
                                   "got": prediction[:400]})
            else:
                pred_lines = get_stripped_lines(prediction)
                gt_lines = get_stripped_lines(expected)
                if len(pred_lines) != len(gt_lines):
                    record.update({"ok": False, "reason": "output_length_mismatch",
                                   "got_lines": len(pred_lines),
                                   "expected_lines": len(gt_lines)})
                else:
                    bad = None
                    for i, (p, g) in enumerate(zip(pred_lines, gt_lines)):
                        if not line_equal(p, g):
                            bad = (i, p[:200], g[:200])
                            break
                    if bad is None:
                        record.update({"ok": True, "elapsed_s": round(dt, 3)})
                    else:
                        record.update({"ok": False, "reason": "wrong_answer",
                                       "line": bad[0], "got": bad[1], "expected": bad[2]})
        except subprocess.TimeoutExpired:
            record.update({"ok": False, "reason": "timeout",
                           "timeout_s": TIMEOUT_SECONDS})
        except Exception as e:
            record.update({"ok": False, "reason": f"harness_error: {e}"})
        results.append(record)
        if record["ok"]:
            passed += 1

    all_ok = passed == len(cases)
    print(f"LCB {task_id}: {passed}/{len(cases)} private tests passed")
    if not all_ok:
        for r in results:
            if not r["ok"]:
                print(f"  FAIL #{r['index']}: {r.get('reason')} "
                      f"got={r.get('got','')!r} expected={r.get('expected','')!r}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    task_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not task_id:
        print("usage: eval_lcb.py <task_id>")
        sys.exit(2)
    sys.exit(grade_task(task_id))
