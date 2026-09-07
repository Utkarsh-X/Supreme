#!/usr/bin/env python3
"""
extract_all_deep_findings.py
Performs an exhaustive multi-dimensional forensic extraction across all 267 canonical benchmark runs.

Extracts:
1. Tool call distributions & proportions (read vs write vs exec vs manage)
2. Thinking token dynamics (thinking tokens, output tokens, thinking-to-output ratios)
3. Turn counts and conversation depth
4. Editing methods: surgical edits (replace_file_content) vs destructive rewrites (write_to_file)
5. Time & tool count to first modification
6. Error indicators: commands resulting in failures/exceptions
7. Domain & difficulty performance breakdowns
8. Extreme cases: top token consumers, top tool callers, fastest solvers, longest sessions
"""

import os
import json
import re
from collections import defaultdict
from typing import Dict, Any, List

BENCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BENCH_DIR, "results_v4")
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(RESULTS_DIR, "FORENSIC_AUDIT_LEDGER.json")
TAXONOMY_JSON = os.path.join(RESULTS_DIR, "v4_task_taxonomy.json")
OUT_DIR = os.path.join(RESULTS_DIR, "extraction_findings")
OUT_DATASET = os.path.join(OUT_DIR, "canonical_267_deep_telemetry.json")


def load_canonical_ledger() -> List[Dict[str, Any]]:
    with open(LEDGER_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_taxonomy() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(TAXONOMY_JSON):
        return {}
    with open(TAXONOMY_JSON, "r", encoding="utf-8") as f:
        tax = json.load(f)
    return {t["task_name"]: t for t in tax.get("tasks", [])}


def parse_run_transcript(run_id: str) -> Dict[str, Any]:
    trans_path = os.path.join(RUNS_DIR, run_id, "transcript.txt")
    metrics = {
        "turn_count": 0,
        "thinking_tokens_total": 0,
        "output_tokens_total": 0,
        "input_tokens_total": 0,
        "tools_breakdown": defaultdict(int),
        "first_edit_tool_idx": None,
        "read_tools_count": 0,
        "write_tools_count": 0,
        "exec_tools_count": 0,
        "manage_tools_count": 0,
        "command_error_count": 0,
        "edited_files": set(),
        "read_files": set(),
        "unique_files_edited_count": 0,
        "unique_files_read_count": 0,
        "tool_sequence": []
    }


    if not os.path.exists(trans_path):
        del metrics["edited_files"]
        del metrics["read_files"]
        return metrics


    READ_TOOLS = {"view_file", "list_dir", "grep_search", "find_by_name", "read_url_content"}
    WRITE_TOOLS = {"write_to_file", "replace_file_content"}
    EXEC_TOOLS = {"run_command"}
    MANAGE_TOOLS = {"manage_task", "schedule"}

    tool_counter = 0

    try:
        with open(trans_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or not (line.startswith("{") and line.endswith("}")):
                    continue
                try:
                    event_data = json.loads(line)
                    su = event_data.get("step_update", {})
                    stype = su.get("step_type")
                    state = su.get("state")

                    # Parse LLM response usage
                    if stype == "agent_response" and state == "DONE":
                        metrics["turn_count"] += 1
                        usage = su.get("usage", {})
                        metrics["thinking_tokens_total"] += usage.get("thinking_tokens", 0)
                        metrics["output_tokens_total"] += usage.get("output_tokens", 0)
                        metrics["input_tokens_total"] += usage.get("input_tokens", 0)

                    # Parse tool executions
                    elif stype == "tool" and state == "DONE":
                        tool_counter += 1
                        tname = su.get("tool_name", "unknown")
                        metrics["tools_breakdown"][tname] += 1
                        metrics["tool_sequence"].append(tname)

                        # Classify category
                        if tname in READ_TOOLS:
                            metrics["read_tools_count"] += 1
                            params = su.get("tool_info", {}).get("parameters", {})
                            fp = params.get("AbsolutePath") or params.get("SearchPath")
                            if fp:
                                metrics["read_files"].add(fp)
                        elif tname in WRITE_TOOLS:
                            metrics["write_tools_count"] += 1
                            if metrics["first_edit_tool_idx"] is None:
                                metrics["first_edit_tool_idx"] = tool_counter
                            params = su.get("tool_info", {}).get("parameters", {})
                            tf = params.get("TargetFile")
                            if tf:
                                metrics["edited_files"].add(tf)
                        elif tname in EXEC_TOOLS:
                            metrics["exec_tools_count"] += 1
                            output_str = str(su.get("tool_info", {}).get("output", ""))
                            if "exited with code" in output_str and not "exited with code 0" in output_str:
                                metrics["command_error_count"] += 1
                            elif "command failed" in output_str.lower() or "error:" in output_str.lower():
                                metrics["command_error_count"] += 1
                        elif tname in MANAGE_TOOLS:
                            metrics["manage_tools_count"] += 1

                except Exception:
                    pass
    except Exception:
        pass

    # Convert sets to serializable formats
    metrics["unique_files_edited_count"] = len(metrics["edited_files"])
    metrics["unique_files_read_count"] = len(metrics["read_files"])
    del metrics["edited_files"]
    del metrics["read_files"]

    return metrics


def extract_all():
    ledger = load_canonical_ledger()
    taxonomy = load_taxonomy()

    print(f"Extracting deep forensic metrics across {len(ledger)} canonical runs...")
    extracted_dataset = []

    # Aggregators by configuration
    cfg_stats = defaultdict(lambda: {
        "runs": 0,
        "passes": 0,
        "fails": 0,
        "total_wall_sec": 0.0,
        "total_tokens": 0,
        "total_thinking_tokens": 0,
        "total_output_tokens": 0,
        "total_input_tokens": 0,
        "total_turns": 0,
        "total_tools": 0,
        "read_tools": 0,
        "write_tools": 0,
        "exec_tools": 0,
        "manage_tools": 0,
        "command_errors": 0,
        "tools_by_name": defaultdict(int),
        "ttfe_list": [],
        "unique_files_edited_total": 0
    })

    # Domain aggregators
    domain_stats = defaultdict(lambda: defaultdict(lambda: {"passes": 0, "runs": 0, "tokens": 0, "time": 0.0}))

    for idx, r in enumerate(ledger, 1):
        run_id = r["run_id"]
        t_name = r["task_name"]
        cfg = r["config_id"]
        status = r["status"]
        wall_sec = r.get("wall_clock_seconds", 0.0)
        tokens = r.get("total_tokens", 0)

        tax_meta = taxonomy.get(t_name, {})
        domain = tax_meta.get("domain", "General Engineering")
        difficulty = tax_meta.get("difficulty", "medium")

        # Parse transcript
        t_metrics = parse_run_transcript(run_id)

        record = {
            "task_num": r.get("task_num"),
            "task_name": t_name,
            "config_id": cfg,
            "run_id": run_id,
            "status": status,
            "domain": domain,
            "difficulty": difficulty,
            "wall_clock_seconds": wall_sec,
            "total_tokens": tokens,
            "sha256_verifier": r.get("sha256_verifier"),
            "verifier_summary": r.get("verifier_summary", {}),
            "transcript_metrics": t_metrics
        }
        extracted_dataset.append(record)

        # Aggregate cfg stats
        cs = cfg_stats[cfg]
        cs["runs"] += 1
        if status == "SUCCESS":
            cs["passes"] += 1
        else:
            cs["fails"] += 1
        cs["total_wall_sec"] += wall_sec
        cs["total_tokens"] += tokens
        cs["total_thinking_tokens"] += t_metrics["thinking_tokens_total"]
        cs["total_output_tokens"] += t_metrics["output_tokens_total"]
        cs["total_input_tokens"] += t_metrics["input_tokens_total"]
        cs["total_turns"] += t_metrics["turn_count"]
        cs["total_tools"] += sum(t_metrics["tools_breakdown"].values())
        cs["read_tools"] += t_metrics["read_tools_count"]
        cs["write_tools"] += t_metrics["write_tools_count"]
        cs["exec_tools"] += t_metrics["exec_tools_count"]
        cs["manage_tools"] += t_metrics["manage_tools_count"]
        cs["command_errors"] += t_metrics["command_error_count"]
        cs["unique_files_edited_total"] += t_metrics["unique_files_edited_count"]
        if t_metrics["first_edit_tool_idx"] is not None:
            cs["ttfe_list"].append(t_metrics["first_edit_tool_idx"])

        for tname, cnt in t_metrics["tools_breakdown"].items():
            cs["tools_by_name"][tname] += cnt

        # Aggregate domain stats
        ds = domain_stats[domain][cfg]
        ds["runs"] += 1
        if status == "SUCCESS":
            ds["passes"] += 1
        ds["tokens"] += tokens
        ds["time"] += wall_sec

        if idx % 50 == 0:
            print(f"Processed {idx}/{len(ledger)} runs...")

    # Save full JSON dataset
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_DATASET, "w", encoding="utf-8") as f:
        json.dump(extracted_dataset, f, indent=2)

    print(f"Successfully saved full deep telemetry dataset to: {OUT_DATASET}")
    return extracted_dataset, cfg_stats, domain_stats


if __name__ == "__main__":
    extract_all()
