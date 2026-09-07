import os
import json
import re
import sys
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

def is_command_error(out_str: str) -> bool:
    if not out_str:
        return False
    low = out_str.lower()
    # Check powershell / bash exit code lines
    if "exited with code" in low and "exited with code 0" not in low:
        return True
    if "command failed" in low:
        return True
    if "traceback (most recent call last):" in low:
        return True
    if "syntaxerror" in low or "importerror" in low or "modulenotfounderror" in low:
        return True
    if "error: " in low or "fatal: " in low or "err!" in low or "compilation terminated" in low:
        return True
    if "oci runtime exec failed" in low or "unable to start container" in low:
        return True
    if "is not recognized as the name of a cmdlet" in low:
        return True
    return False

# Analyze each run
results_by_config = defaultdict(lambda: {
    "total_commands": 0,
    "total_errors": 0,
    "streak_lengths": [],
    "recovery_at_next_cmd": 0,
    "fail_at_next_cmd": 0,
    "runs_analyzed": 0
})

deepest_loops = []

for item in ledger:
    run_id = item["run_id"]
    cfg = item["config_id"]
    tname = item["task_name"]
    trans_path = os.path.join(RUNS_DIR, run_id, "transcript.txt")
    if not os.path.exists(trans_path):
        continue

    results_by_config[cfg]["runs_analyzed"] += 1
    
    # Extract chronological list of run_command executions
    cmd_events = []
    with open(trans_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip() or not line.strip().startswith("{"):
                continue
            try:
                ev = json.loads(line)
                su = ev.get("step_update", {})
                if su.get("step_type") == "tool" and su.get("state") == "DONE":
                    tname_tool = su.get("tool_name")
                    if tname_tool == "run_command":
                        cmd_line = su.get("tool_info", {}).get("parameters", {}).get("CommandLine", "")
                        out = str(su.get("tool_info", {}).get("output", ""))
                        err = is_command_error(out)
                        cmd_events.append({
                            "cmd": cmd_line,
                            "out": out,
                            "is_err": err,
                            "step_index": su.get("step_index", 0)
                        })
            except Exception:
                pass

    total_cmds = len(cmd_events)
    results_by_config[cfg]["total_commands"] += total_cmds

    # Calculate streaks of consecutive errors
    current_streak = 0
    streak_cmds = []
    
    for i, c in enumerate(cmd_events):
        if c["is_err"]:
            results_by_config[cfg]["total_errors"] += 1
            current_streak += 1
            streak_cmds.append(c)
            
            # Check next command if exists
            if i + 1 < len(cmd_events):
                if not cmd_events[i+1]["is_err"]:
                    results_by_config[cfg]["recovery_at_next_cmd"] += 1
                else:
                    results_by_config[cfg]["fail_at_next_cmd"] += 1
        else:
            if current_streak > 0:
                results_by_config[cfg]["streak_lengths"].append(current_streak)
                if current_streak >= 5:
                    deepest_loops.append({
                        "run_id": run_id,
                        "task_name": tname,
                        "config_id": cfg,
                        "streak": current_streak,
                        "sample_cmd": streak_cmds[0]["cmd"][:80],
                        "sample_err": streak_cmds[0]["out"][:150].strip().replace('\n', ' '),
                        "final_cmd": streak_cmds[-1]["cmd"][:80]
                    })
                current_streak = 0
                streak_cmds = []

    if current_streak > 0:
        results_by_config[cfg]["streak_lengths"].append(current_streak)
        if current_streak >= 5:
            deepest_loops.append({
                "run_id": run_id,
                "task_name": tname,
                "config_id": cfg,
                "streak": current_streak,
                "sample_cmd": streak_cmds[0]["cmd"][:80],
                "sample_err": streak_cmds[0]["out"][:150].strip().replace('\n', ' '),
                "final_cmd": streak_cmds[-1]["cmd"][:80]
            })

print("=== ERROR SPIRALING & RESILIENCE METRICS ===")
for cfg, data in results_by_config.items():
    tot_cmds = data["total_commands"]
    tot_errs = data["total_errors"]
    rec = data["recovery_at_next_cmd"]
    fail = data["fail_at_next_cmd"]
    tot_eval = rec + fail
    p_rec = (rec / tot_eval * 100) if tot_eval else 0.0
    streaks = data["streak_lengths"]
    max_streak = max(streaks) if streaks else 0
    avg_streak = sum(streaks) / len(streaks) if streaks else 0.0
    s_counts = Counter(streaks)
    
    print(f"\n[{cfg.upper()}] (Runs: {data['runs_analyzed']})")
    print(f"  Total Commands: {tot_cmds:,}")
    print(f"  Total Errored Commands: {tot_errs:,} ({tot_errs/tot_cmds*100:.2f}%)")
    print(f"  Immediate Recovery P(Success at t+1 | Error at t): {p_rec:.2f}% ({rec}/{tot_eval})")
    print(f"  Multi-turn Failure Spiral P(Error at t+1 | Error at t): {100 - p_rec:.2f}% ({fail}/{tot_eval})")
    print(f"  Average Error Streak Length: {avg_streak:.2f}")
    print(f"  Max Consecutive Error Streak: {max_streak}")
    print(f"  Streak Length Distribution:")
    print(f"    Length 1 (Immediate Recovery): {s_counts[1]} ({s_counts[1]/len(streaks)*100:.1f}%)" if streaks else "N/A")
    print(f"    Length 2: {s_counts[2]} ({s_counts[2]/len(streaks)*100:.1f}%)" if streaks else "N/A")
    print(f"    Length 3-4: {sum(s_counts[k] for k in [3,4])} ({sum(s_counts[k] for k in [3,4])/len(streaks)*100:.1f}%)" if streaks else "N/A")
    print(f"    Length 5+: {sum(s_counts[k] for k in s_counts if k >= 5)} ({sum(s_counts[k] for k in s_counts if k >= 5)/len(streaks)*100:.1f}%)" if streaks else "N/A")

print("\n=== TOP 10 DEEPEST ERROR LOOPS IN BENCHMARK ===")
deepest_loops.sort(key=lambda x: x["streak"], reverse=True)
for d in deepest_loops[:10]:
    print(f"Streak {d['streak']:2d} | {d['config_id']:16} | {d['task_name']:30} | First cmd: {d['sample_cmd']}")
    print(f"   Err sample: {d['sample_err']}")
