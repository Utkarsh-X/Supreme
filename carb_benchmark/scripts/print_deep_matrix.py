#!/usr/bin/env python3
import json
from collections import defaultdict

with open("carb_benchmark/results_v4/extraction_findings/canonical_267_deep_telemetry.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cfg_agg = defaultdict(lambda: {
    "runs": 0, "passes": 0, "wall_time": 0.0,
    "total_tokens": 0, "thinking_tokens": 0, "output_tokens": 0, "input_tokens": 0,
    "turns": 0, "read_tools": 0, "write_tools": 0, "exec_tools": 0, "manage_tools": 0,
    "command_errors": 0, "ttfe_sum": 0, "ttfe_count": 0, "files_edited": 0,
    "write_to_file_count": 0, "replace_file_content_count": 0
})

for r in data:
    cfg = r["config_id"]
    tm = r["transcript_metrics"]
    ca = cfg_agg[cfg]
    ca["runs"] += 1
    if r["status"] == "SUCCESS":
        ca["passes"] += 1
    ca["wall_time"] += r["wall_clock_seconds"]
    ca["total_tokens"] += r["total_tokens"]
    ca["thinking_tokens"] += tm.get("thinking_tokens_total", 0)
    ca["output_tokens"] += tm.get("output_tokens_total", 0)
    ca["input_tokens"] += tm.get("input_tokens_total", 0)
    ca["turns"] += tm.get("turn_count", 0)
    ca["read_tools"] += tm.get("read_tools_count", 0)
    ca["write_tools"] += tm.get("write_tools_count", 0)
    ca["exec_tools"] += tm.get("exec_tools_count", 0)
    ca["manage_tools"] += tm.get("manage_tools_count", 0)
    ca["command_errors"] += tm.get("command_error_count", 0)
    ca["files_edited"] += tm.get("unique_files_edited_count", 0)
    
    tb = tm.get("tools_breakdown", {})
    ca["write_to_file_count"] += tb.get("write_to_file", 0)
    ca["replace_file_content_count"] += tb.get("replace_file_content", 0)
    
    ttfe = tm.get("first_edit_tool_idx")
    if ttfe is not None:
        ca["ttfe_sum"] += ttfe
        ca["ttfe_count"] += 1

print("\n=== GRAND ARCHITECTURAL COMPARISON MATRIX (267 CANONICAL RUNS) ===\n")
header = f"{'Metric':<38} | {'Supreme (v1.0)':<18} | {'Superpowers by obra':<20} | {'Baseline':<18}"
print(header)
print("-" * len(header))

sup = cfg_agg["supreme-v2.0"]
sp = cfg_agg["superpowers-v4.0"]
base = cfg_agg["baseline-v2.0"]

def row(title, v_sup, v_sp, v_b):
    print(f"{title:<38} | {str(v_sup):<18} | {str(v_sp):<20} | {str(v_b):<18}")

row("Solved / Total Runs", f"{sup['passes']}/89 ({sup['passes']/89*100:.1f}%)", f"{sp['passes']}/89 ({sp['passes']/89*100:.1f}%)", f"{base['passes']}/89 ({base['passes']/89*100:.1f}%)")
row("Total Wall-Clock Latency", f"{sup['wall_time']/3600:.2f} hrs", f"{sp['wall_time']/3600:.2f} hrs", f"{base['wall_time']/3600:.2f} hrs")
row("Total Thinking Tokens (Gemini)", f"{sup['thinking_tokens']:,}", f"{sp['thinking_tokens']:,}", f"{base['thinking_tokens']:,}")
row("Total Output Tokens", f"{sup['output_tokens']:,}", f"{sp['output_tokens']:,}", f"{base['output_tokens']:,}")
row("Thinking / Output Ratio", f"{sup['thinking_tokens']/sup['output_tokens']:.2f}", f"{sp['thinking_tokens']/sp['output_tokens']:.2f}", f"{base['thinking_tokens']/base['output_tokens']:.2f}")
row("Total Conversational Turns", f"{sup['turns']:,}", f"{sp['turns']:,}", f"{base['turns']:,}")
row("Avg Turns / Task", f"{sup['turns']/89:.1f}", f"{sp['turns']/89:.1f}", f"{base['turns']/89:.1f}")
row("Read Tools (view/grep/list)", f"{sup['read_tools']:,}", f"{sp['read_tools']:,}", f"{base['read_tools']:,}")
row("Write Tools (modifications)", f"{sup['write_tools']:,}", f"{sp['write_tools']:,}", f"{base['write_tools']:,}")
row("Read-to-Write Ratio", f"{sup['read_tools']/sup['write_tools']:.2f}", f"{sp['read_tools']/sp['write_tools']:.2f}", f"{base['read_tools']/base['write_tools']:.2f}")
row("Full Overwrites (write_to_file)", f"{sup['write_to_file_count']:,}", f"{sp['write_to_file_count']:,}", f"{base['write_to_file_count']:,}")
row("Surgical Edits (replace_content)", f"{sup['replace_file_content_count']:,}", f"{sp['replace_file_content_count']:,}", f"{base['replace_file_content_count']:,}")
row("Avg Tools Before First Edit", f"{sup['ttfe_sum']/sup['ttfe_count']:.1f}", f"{sp['ttfe_sum']/sp['ttfe_count']:.1f}", f"{base['ttfe_sum']/base['ttfe_count']:.1f}")
row("Command Errors Encountered", f"{sup['command_errors']:,}", f"{sp['command_errors']:,}", f"{base['command_errors']:,}")
row("Avg Unique Files Edited / Task", f"{sup['files_edited']/89:.2f}", f"{sp['files_edited']/89:.2f}", f"{base['files_edited']/89:.2f}")
