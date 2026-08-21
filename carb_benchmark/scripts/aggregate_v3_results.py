#!/usr/bin/env python3
"""aggregate_v3_results.py — comprehensive aggregator for CARB-v3 (39 tasks) and CARB-v2+v3 Master Matrix."""
import json
import os
import glob
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(BASE, "runs")
REG_V3 = os.path.join(BASE, "task_registry", "final_tasks_v3.json")
REG_V2 = os.path.join(BASE, "task_registry", "final_tasks_v2.json")
RESULTS = os.path.join(BASE, "results")


def load_v3_tasks():
    d = json.load(open(REG_V3, encoding="utf-8"))
    return [t["instance_id"] for t in d["tasks"]]


def get_runs():
    all_runs = sorted(os.listdir(RUNS))
    records = {}
    for d in all_runs:
        mf = os.path.join(RUNS, d, "run_manifest.yaml")
        if not os.path.exists(mf):
            continue
        try:
            txt = open(mf, encoding="utf-8", errors="ignore").read()
            status, tid, cfg = None, None, None
            for ln in txt.splitlines():
                if ln.startswith("status:"):
                    status = ln.split(":", 1)[1].strip()
                if ln.startswith("task_id:"):
                    tid = ln.split(":", 1)[1].strip()
                if ln.startswith("configuration_id:"):
                    cfg = ln.split(":", 1)[1].strip()
            if status in ("SUCCESS", "FAILURE") and tid and cfg:
                if cfg == "full-v2.0":
                    cfg = "supreme-v2.0"

                tel_path = os.path.join(RUNS, d, "telemetry.json")
                tools, wall, tokens = 0, 0.0, 0
                if os.path.exists(tel_path):
                    try:
                        tdata = json.load(open(tel_path, encoding="utf-8", errors="ignore"))
                        tools = len(tdata.get("tool_calls", []))
                        wall = float(tdata.get("wall_clock_seconds", 0.0))
                        tokens = tdata.get("usage", {}).get("total_tokens", 0)
                    except Exception:
                        pass

                key = (tid, cfg)
                is_valid = (tools > 0 and wall >= 10.0) or (status == "SUCCESS")

                rec = {
                    "run_id": d,
                    "status": status,
                    "tools": tools,
                    "wall": wall,
                    "tokens": tokens,
                    "is_valid": is_valid,
                }

                if key not in records:
                    records[key] = rec
                else:
                    cur = records[key]
                    if (is_valid and not cur["is_valid"]) or (is_valid == cur["is_valid"] and d > cur["run_id"]):
                        records[key] = rec
        except Exception:
            continue
    return records


def generate_v3_report():
    tasks = load_v3_tasks()
    runs = get_runs()

    summary = {
        "total_tasks": len(tasks),
        "baseline": {"pass": 0, "fail": len(tasks), "pending": 0},
        "supreme": {"pass": 0, "fail": 0, "pending": 0},
        "superpowers": {"pass": 0, "fail": 0, "pending": 0},
        "matrix": [],
    }

    table_lines = [
        "| Task ID | Baseline | Supreme | Superpowers | Notes |",
        "|---|:---:|:---:|:---:|---|",
    ]

    for t in tasks:
        b_res = "❌ FAIL"

        s_rec = runs.get((t, "supreme-v2.0"))
        if not s_rec or not s_rec["is_valid"]:
            s_res = "⚠️ PENDING"
            summary["supreme"]["pending"] += 1
        elif s_rec["status"] == "SUCCESS":
            s_res = "✅ PASS"
            summary["supreme"]["pass"] += 1
        else:
            s_res = "❌ FAIL"
            summary["supreme"]["fail"] += 1

        p_rec = runs.get((t, "superpowers-v2.0"))
        if not p_rec or not p_rec["is_valid"]:
            p_res = "⚠️ PENDING"
            summary["superpowers"]["pending"] += 1
        elif p_rec["status"] == "SUCCESS":
            p_res = "✅ PASS"
            summary["superpowers"]["pass"] += 1
        else:
            p_res = "❌ FAIL"
            summary["superpowers"]["fail"] += 1

        notes = []
        if s_res == "✅ PASS" and p_res == "✅ PASS":
            notes.append("Both challengers win")
        elif s_res == "✅ PASS":
            notes.append("Supreme win")
        elif p_res == "✅ PASS":
            notes.append("Superpowers win")

        table_lines.append(f"| `{t}` | {b_res} | {s_res} | {p_res} | {', '.join(notes)} |")
        summary["matrix"].append({
            "task_id": t,
            "baseline": "FAILURE",
            "supreme": s_rec["status"] if s_rec and s_rec["is_valid"] else "PENDING",
            "superpowers": p_rec["status"] if p_rec and p_rec["is_valid"] else "PENDING",
        })

    s_done = summary["supreme"]["pass"] + summary["supreme"]["fail"]
    p_done = summary["superpowers"]["pass"] + summary["superpowers"]["fail"]
    s_rate = (summary["supreme"]["pass"] / s_done * 100) if s_done else 0
    p_rate = (summary["superpowers"]["pass"] / p_done * 100) if p_done else 0

    md = f"# CARB-v3 Discriminative Benchmark Summary (39 Tasks)\n\n"
    md += f"**Status Summary:**\n"
    md += f"- **Baseline-v2.0:** 0 / {len(tasks)} (0.0%)\n"
    md += f"- **Supreme-v2.0:** {summary['supreme']['pass']} PASS / {s_done} valid ({s_rate:.1f}%) | {summary['supreme']['pending']} pending\n"
    md += f"- **Superpowers-v2.0:** {summary['superpowers']['pass']} PASS / {p_done} valid ({p_rate:.1f}%) | {summary['superpowers']['pending']} pending\n\n"
    md += "\n".join(table_lines) + "\n"

    out_md = os.path.join(RESULTS, "v3_live_summary.md")
    out_json = os.path.join(RESULTS, "v3_live_summary.json")
    open(out_md, "w", encoding="utf-8").write(md)
    open(out_json, "w", encoding="utf-8").write(json.dumps(summary, indent=2))
    print(f"Wrote live summary to {out_md} and {out_json}")
    print(f"Supreme: {summary['supreme']['pass']} pass, {summary['supreme']['fail']} fail, {summary['supreme']['pending']} pending")
    print(f"Superpowers: {summary['superpowers']['pass']} pass, {summary['superpowers']['fail']} fail, {summary['superpowers']['pending']} pending")


if __name__ == "__main__":
    generate_v3_report()
