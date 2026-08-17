#!/usr/bin/env python3
"""aggregate_results.py — build the final CARB-v2 results table from run dirs.

Authoritative source: finalized run_manifest.yaml files under carb_benchmark/runs/
(one per (task, config)). Prints a markdown table + summary JSON.

Three configurations since 2026-08-17: baseline-v2.0, supreme-v2.0 (renamed
from full-v2.0), superpowers-v2.0. Legacy full-v2.0 manifests are counted under
supreme-v2.0.
"""
import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(BASE, "runs")
REGISTRY = os.path.join(BASE, "task_registry", "final_tasks_v2.json")
CONFIGS = ["baseline-v2.0", "supreme-v2.0", "superpowers-v2.0"]
LEGACY_CONFIG_ALIASES = {"full-v2.0": "supreme-v2.0"}


def finalized_runs():
    out = []
    for f in glob.glob(os.path.join(RUNS, "*v2.0", "run_manifest.yaml")):
        try:
            txt = open(f, encoding="utf-8").read()
        except Exception:
            continue
        status = None
        task_id = None
        cfg = None
        for line in txt.splitlines():
            if line.startswith("status:"):
                status = line.split(":", 1)[1].strip()
            if line.startswith("task_id:"):
                task_id = line.split(":", 1)[1].strip()
            if line.startswith("configuration_id:"):
                cfg = line.split(":", 1)[1].strip()
        if status in ("SUCCESS", "FAILURE") and task_id and cfg:
            cfg = LEGACY_CONFIG_ALIASES.get(cfg, cfg)
            out.append({"dir": os.path.dirname(f), "task": task_id, "config": cfg,
                        "status": status})
    return out


def main():
    registry = json.load(open(REGISTRY, encoding="utf-8"))
    tasks = [t["instance_id"] for t in registry]
    runs = finalized_runs()

    # newest run per (task, config) — probe duplicates share outcome, pick latest
    best = {}
    for r in runs:
        key = (r["task"], r["config"])
        if key not in best or os.path.basename(r["dir"]) > os.path.basename(best[key]["dir"]):
            # attach extra detail: transcript size + wall time + tail marker
            tr = os.path.join(r["dir"], "transcript.txt")
            try:
                r["transcript_bytes"] = os.path.getsize(tr)
                tail_txt = open(tr, encoding="utf-8", errors="replace").read()[-120:].strip()
            except Exception:
                r["transcript_bytes"] = 0
                tail_txt = ""
            r["transcript_tail"] = tail_txt
            try:
                txt = open(os.path.join(r["dir"], "run_manifest.yaml"), encoding="utf-8").read()
                for line in txt.splitlines():
                    if line.strip().startswith("wall_clock_seconds:") and "seconds" not in r:
                        r["seconds"] = line.split(":", 1)[1].strip()
            except Exception:
                pass
            best[key] = r

    rows = []
    counts = {c: {"pass": 0, "fail": 0, "missing": 0} for c in CONFIGS}
    for task in tasks:
        row = {"task": task}
        for c in CONFIGS:
            r = best.get((task, c))
            if r is None:
                row[c] = "PENDING"
                counts[c]["missing"] += 1
            else:
                row[c] = r["status"]
                row[f"{c}_detail"] = {
                    "seconds": r.get("seconds"),
                    "transcript_bytes": r.get("transcript_bytes", 0),
                    "transcript_tail": r.get("transcript_tail", ""),
                }
                counts[c]["pass" if r["status"] == "SUCCESS" else "fail"] += 1
        rows.append(row)

    print("\n### Transcript-quality flags (thin transcripts = infra timeouts, not failures)\n")
    for row in rows:
        for c in CONFIGS:
            d = row.get(f"{c}_detail")
            if d and d.get("transcript_bytes", 0) < 200:
                print(f"- {row['task']} | {c} | {d.get('seconds')}s | {d['transcript_bytes']}B | {d.get('transcript_tail','')[:80]}")

    # split by source
    def src(task_id):
        return "LCB" if task_id.startswith("lcb__") else "SWE"

    print("# CARB-v2 Results — 50 tasks x 3 configs (gemini-3.6-flash-high, locked)\n")
    print("| Task | baseline-v2.0 | supreme-v2.0 | superpowers-v2.0 |")
    print("|---|---|---|---|")
    for row in rows:
        print(f"| {row['task']} | {row['baseline-v2.0']} | {row['supreme-v2.0']} | {row['superpowers-v2.0']} |")

    print("\n## Summary\n")
    print("| Config | PASS | FAIL | PENDING | Pass rate (finalized) |")
    print("|---|---|---|---|---|")
    for c in CONFIGS:
        k = counts[c]
        fin = k["pass"] + k["fail"]
        rate = f"{k['pass'] / fin:.1%}" if fin else "n/a"
        print(f"| {c} | {k['pass']} | {k['fail']} | {k['missing']} | {rate} |")

    for src_name in ("SWE", "LCB"):
        print(f"\n### {src_name} breakdown")
        for c in CONFIGS:
            sub = [r for r in rows if src(r["task"]) == src_name]
            p = sum(1 for r in sub if r[c] == "SUCCESS")
            f_ = sum(1 for r in sub if r[c] == "FAILURE")
            pend = sum(1 for r in sub if r[c] == "PENDING")
            print(f"- {c}: {p} PASS / {f_} FAIL / {pend} PENDING (of {len(sub)})")

    summary = {"tasks": len(tasks), "counts": counts,
               "per_task": {r["task"]: {c: r[c] for c in CONFIGS} for r in rows}}
    json.dump(summary, open(os.path.join(BASE, "results", "benchmark_v2_final.json"), "w"),
              indent=1, default=str)
    print("\nwrote carb_benchmark/results/benchmark_v2_final.json")


if __name__ == "__main__":
    main()
