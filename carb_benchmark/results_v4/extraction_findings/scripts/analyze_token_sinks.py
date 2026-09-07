import os
import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

configs = ['supreme-v2.0', 'superpowers-v4.0', 'baseline-v2.0']

# Metrics per config
metrics = {cfg: {
    "runs": 0,
    "total_billed_tokens": 0,
    "input_tokens_turn_sum": 0,
    "output_tokens_turn_sum": 0,
    "thinking_tokens_total": 0,
    "generation_tokens_total": 0, # output - thinking
    
    # Character metrics for content breakdown
    "stdout_stderr_chars": 0,
    "view_file_content_chars": 0,
    "manage_task_output_chars": 0,
    "other_tool_output_chars": 0,
    
    "write_to_file_content_chars": 0,
    "run_command_line_chars": 0,
    "other_tool_input_chars": 0,
    
    "final_response_chars": 0,
    "first_turn_input_tokens": [],
    "cache_read_tokens_total": 0
} for cfg in configs}

# Track top stdout blowouts
top_stdout_runs = []

for r in ledger:
    run_id = r["run_id"]
    cfg = r["config_id"]
    tname = r["task_name"]
    trans_path = os.path.join(RUNS_DIR, run_id, "transcript.txt")
    if not os.path.exists(trans_path):
        continue

    m = metrics[cfg]
    m["runs"] += 1
    m["total_billed_tokens"] += r.get("total_tokens", 0)

    run_stdout_chars = 0
    first_turn = True

    with open(trans_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
                evt = ev.get("event")
                
                if evt == "step_update":
                    su = ev.get("step_update", {})
                    stype = su.get("step_type")
                    state = su.get("state")

                    if stype == "agent_response" and state == "DONE":
                        u = su.get("usage", {})
                        inp = u.get("input_tokens", 0)
                        out = u.get("output_tokens", 0)
                        th = u.get("thinking_tokens", 0)
                        gen = max(0, out - th)
                        cache = u.get("cache_read_tokens", 0)

                        m["input_tokens_turn_sum"] += inp
                        m["output_tokens_turn_sum"] += out
                        m["thinking_tokens_total"] += th
                        m["generation_tokens_total"] += gen
                        m["cache_read_tokens_total"] += cache

                        if first_turn:
                            m["first_turn_input_tokens"].append(inp)
                            first_turn = False

                    elif stype == "tool" and state == "ACTIVE":
                        tname_tool = su.get("tool_name")
                        params = su.get("tool_info", {}).get("parameters", {})
                        if tname_tool == "write_to_file":
                            m["write_to_file_content_chars"] += len(str(params.get("CodeContent", "")))
                        elif tname_tool == "replace_file_content":
                            m["write_to_file_content_chars"] += len(str(params.get("ReplacementContent", "")))
                        elif tname_tool == "run_command":
                            m["run_command_line_chars"] += len(str(params.get("CommandLine", "")))
                        else:
                            m["other_tool_input_chars"] += len(json.dumps(params))

                    elif stype == "tool" and state == "DONE":
                        tname_tool = su.get("tool_name")
                        out_str = str(su.get("tool_info", {}).get("output", ""))
                        c_len = len(out_str)
                        if tname_tool == "run_command":
                            m["stdout_stderr_chars"] += c_len
                            run_stdout_chars += c_len
                        elif tname_tool == "view_file":
                            m["view_file_content_chars"] += c_len
                        elif tname_tool == "manage_task":
                            m["manage_task_output_chars"] += c_len
                        else:
                            m["other_tool_output_chars"] += c_len

                elif evt == "result":
                    res = ev.get("result", {})
                    resp = res.get("response", "")
                    m["final_response_chars"] += len(str(resp))

            except Exception:
                pass

    top_stdout_runs.append({
        "run_id": run_id,
        "config_id": cfg,
        "task_name": tname,
        "stdout_chars": run_stdout_chars,
        "stdout_est_tokens": run_stdout_chars // 4
    })

print("=== TOKEN CONSUMPTION & COMPONENT BREAKDOWN ===")
for cfg in configs:
    m = metrics[cfg]
    print(f"\n==================================================")
    print(f"CONFIGURATION: {cfg.upper()} ({m['runs']} runs)")
    print(f"==================================================")
    tot_billed = m["total_billed_tokens"]
    print(f"Total Billed Tokens: {tot_billed:,}")
    print(f"Turn-Level Input Tokens Sum: {m['input_tokens_turn_sum']:,}")
    print(f"Turn-Level Output Tokens Sum: {m['output_tokens_turn_sum']:,}")
    print(f"  - Thinking Tokens: {m['thinking_tokens_total']:,} ({m['thinking_tokens_total']/tot_billed*100:.2f}% of total billed)")
    print(f"  - Generation Tokens: {m['generation_tokens_total']:,} ({m['generation_tokens_total']/tot_billed*100:.2f}% of total billed)")
    print(f"Turn-Level Cache Read Tokens: {m['cache_read_tokens_total']:,}")
    
    # Initial turn input tokens (System prompt + user instruction)
    ft = m["first_turn_input_tokens"]
    avg_ft = sum(ft)/len(ft) if ft else 0
    print(f"First-Turn Input Tokens (System + Task Prompt): Avg = {avg_ft:.1f}, Min = {min(ft) if ft else 0}, Max = {max(ft) if ft else 0}")
    
    # Character breakdowns
    tot_chars = (m["stdout_stderr_chars"] + m["view_file_content_chars"] + 
                 m["manage_task_output_chars"] + m["other_tool_output_chars"] + 
                 m["write_to_file_content_chars"] + m["run_command_line_chars"] + 
                 m["other_tool_input_chars"] + m["final_response_chars"])
    
    print(f"\nOperational Payload Volume (Characters & Est. Tokens @ ~4 chars/token):")
    print(f"  1. Terminal stdout/stderr:        {m['stdout_stderr_chars']:11,d} chars (~{m['stdout_stderr_chars']//4:8,d} tokens) | {m['stdout_stderr_chars']/tot_chars*100:5.2f}%")
    print(f"  2. File Content Viewed (Read):    {m['view_file_content_chars']:11,d} chars (~{m['view_file_content_chars']//4:8,d} tokens) | {m['view_file_content_chars']/tot_chars*100:5.2f}%")
    print(f"  3. File Content Written (Writes): {m['write_to_file_content_chars']:11,d} chars (~{m['write_to_file_content_chars']//4:8,d} tokens) | {m['write_to_file_content_chars']/tot_chars*100:5.2f}%")
    print(f"  4. Commands Issued:               {m['run_command_line_chars']:11,d} chars (~{m['run_command_line_chars']//4:8,d} tokens) | {m['run_command_line_chars']/tot_chars*100:5.2f}%")
    print(f"  5. Task Polling Outputs:          {m['manage_task_output_chars']:11,d} chars (~{m['manage_task_output_chars']//4:8,d} tokens) | {m['manage_task_output_chars']/tot_chars*100:5.2f}%")
    print(f"  6. Final Explanation Text:        {m['final_response_chars']:11,d} chars (~{m['final_response_chars']//4:8,d} tokens) | {m['final_response_chars']/tot_chars*100:5.2f}%")
    print(f"  Total Operational Payload:        {tot_chars:11,d} chars (~{tot_chars//4:8,d} tokens)")

print("\n=== TOP 10 LARGEST TERMINAL STDOUT/STDERR BLOWOUT RUNS ===")
top_stdout_runs.sort(key=lambda x: x["stdout_chars"], reverse=True)
for o in top_stdout_runs[:10]:
    print(f"{o['config_id']:16} | {o['task_name']:30} | Stdout: {o['stdout_chars']:,} chars (~{o['stdout_est_tokens']:,} tokens)")
