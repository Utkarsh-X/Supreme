#!/usr/bin/env python3
"""
generate_carb_v2_report.py — build the final comparative CARB-v2 report.

Reads the authoritative per-run manifests + evaluator records and writes
carb_benchmark/results/carb_v2_final_report.md with:
  - methodology recap (3 configurations, locked model, isolated envs)
  - overall + per-source pass rates
  - per-task results table with diff + duration + marker-scan flags
  - explicit caveat section (quarantined invalid runs, superseded runners)

Run AFTER scripts/aggregate_results.py (it consumes benchmark_v2_final.json).
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(BASE, "runs")
RESULTS = os.path.join(BASE, "results")
FINAL_JSON = os.path.join(RESULTS, "benchmark_v2_final.json")
REPORT = os.path.join(RESULTS, "carb_v2_final_report.md")

CONFIGS = ["baseline-v2.0", "supreme-v2.0", "superpowers-v2.0"]
LEGACY = {"full-v2.0": "supreme-v2.0"}
MODEL = "gemini-3.6-flash-high"


def latest_run_manifests():
    """task -> config -> run dir (latest finalized per (task, config))."""
    best = {}
    for f in glob.glob(os.path.join(RUNS, "*v2.0", "run_manifest.yaml")):
        txt = open(f, encoding="utf-8").read()
        fields = {}
        for line in txt.splitlines():
            for key in ("status", "task_id", "configuration_id"):
                if line.startswith(key + ":"):
                    fields[key] = line.split(":", 1)[1].strip()
        if fields.get("status") not in ("SUCCESS", "FAILURE"):
            continue
        cfg = LEGACY.get(fields.get("configuration_id"), fields.get("configuration_id"))
        task = fields.get("task_id")
        if not task or not cfg:
            continue
        key = (task, cfg)
        d = os.path.dirname(f)
        if key not in best or os.path.basename(d) > os.path.basename(best[key]):
            best[key] = d
    return best


def load_evaluator(run_dir):
    ev = os.path.join(os.path.dirname(run_dir), "..", "evaluations",
                      os.path.basename(run_dir), "evaluator.json")
    ev = os.path.normpath(ev)
    if not os.path.exists(ev):
        return {}
    with open(ev, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    summary = json.load(open(FINAL_JSON, encoding="utf-8"))
    counts = summary["counts"]
    per_task = summary["per_task"]

    best = latest_run_manifests()

    # per-task detail: duration + diff from evaluator records
    detail = {}
    for (task, cfg), run_dir in best.items():
        e = load_evaluator(run_dir)
        detail[(task, cfg)] = {
            "seconds": e.get("wall_clock_seconds"),
            "files": (e.get("diff_metrics") or {}).get("files_modified_count"),
            "lines": (e.get("diff_metrics") or {}).get("total_lines_changed"),
            "const_markers": e.get("constitution_markers_in_transcript") or [],
            "full_markers": e.get("full_system_markers_in_transcript") or [],
            "sp_markers": e.get("superpowers_markers_in_transcript") or [],
        }

    def src(t):
        return "LCB" if t.startswith("lcb__") else "SWE"

    lines = []
    A = lines.append
    A("# CARB-v2 Final Report — System-Prompt Effectiveness Benchmark")
    A("")
    A(f"**Generated**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    A(f"**Model (locked)**: `{MODEL}` via agy (Antigravity CLI)  ")
    A("**Corpus**: 50 real tasks — 30 SWE-bench Verified + 20 LiveCodeBench v5")
    A("")
    A("## 1. Configurations (identical environment, only prompt content differs)")
    A("")
    A("| Config | System content injected |")
    A("|---|---|")
    A("| `baseline-v2.0` | None (default IDE behavior) |")
    A("| `supreme-v2.0` | Supreme Agent system (constitution + operating protocol + sub-agents + environment profile + persistent state) — renamed from `full-v2.0` (2026-08-17) |")
    A("| `superpowers-v2.0` | Superpowers by OB skill system (14 SKILL.md definitions + agy platform reference) — new arm (2026-08-17) |")
    A("")
    A("## 2. Overall results")
    A("")
    A("| Config | PASS | FAIL | PENDING | Pass rate (finalized) |")
    A("|---|---|---|---|---|")
    for cfg in CONFIGS:
        k = counts[cfg]
        fin = k["pass"] + k["fail"]
        rate = f"{k['pass'] / fin:.1%}" if fin else "n/a"
        A(f"| {cfg} | {k['pass']} | {k['fail']} | {k['missing']} | {rate} |")
    A("")
    for src_name in ("SWE", "LCB"):
        A(f"### {src_name} breakdown")
        A("")
        A("| Config | PASS | FAIL | PENDING | Pass rate |")
        A("|---|---|---|---|---|")
        for cfg in CONFIGS:
            sub = [t for t in per_task if src(t) == src_name]
            p = sum(1 for t in sub if per_task[t].get(cfg) == "SUCCESS")
            f_ = sum(1 for t in sub if per_task[t].get(cfg) == "FAILURE")
            pend = len(sub) - p - f_
            fin = p + f_
            rate = f"{p / fin:.1%}" if fin else "n/a"
            A(f"| {cfg} | {p} | {f_} | {pend} | {rate} |")
        A("")

    A("## 3. Per-task results")
    A("")
    hdr = "| Task | Source | " + " | ".join(CONFIGS) + " | Diff (files/lines) | Seconds |"
    A(hdr)
    A("|" + "---|" * (hdr.count("|") - 1))
    for task in per_task:
        row = f"| {task} | {src(task)} |"
        for cfg in CONFIGS:
            st = per_task[task].get(cfg, "PENDING")
            row += f" {st} |"
        d = detail.get((task, cfg))
        if d:
            row += f" {d['files']}/{d['lines']} | {d['seconds']:.0f} |"
        else:
            row += " — | — |"
        A(row)
    A("")

    A("## 4. Leakage / isolation flags")
    A("")
    leak_rows = []
    for (task, cfg), d in detail.items():
        flags = []
        if d["const_markers"]:
            flags.append("const:" + ",".join(d["const_markers"]))
        if d["full_markers"]:
            flags.append("full:" + ",".join(d["full_markers"]))
        if d["sp_markers"]:
            flags.append("super:" + ",".join(d["sp_markers"]))
        if flags:
            leak_rows.append((task, cfg, "; ".join(flags)))
    if leak_rows:
        A("| Task | Config | Markers seen in transcript |")
        A("|---|---|---|")
        for task, cfg, flags in leak_rows:
            A(f"| {task} | {cfg} | {flags} |")
    else:
        A("None — no configuration markers leaked into any final transcript.")
    A("")

    A("## 5. Integrity & corrections log")
    A("")
    A("- **2026-08-17 harness corrections**: 7 tasks had `test_command: null` in")
    A("  their evaluation specs (false `PASS` verdicts — no real test ran). They were")
    A("  re-wired to the real `eval_swe.py` hidden-test harness and re-run on")
    A("  baseline & supreme. `pytest-5262` supreme (previously crashed with")
    A("  `WinError 206` on the 32k Windows command-line limit) was re-run via the")
    A("  `-p @file` prompt path. The 14 invalid runs are quarantined in")
    A("  `runs/_invalid_quarantine_no_test_cmd/`.")
    A("- **v1 contamination (2026-08-15)**: v1 harness isolated only the baseline;")
    A("  constitution/full ran with the real profile loading the global Supreme")
    A("  `GEMINI.md`. v1 results (3.3%/8.3%/96.7%) are NOT trustworthy and are NOT")
    A("  included here. All v2.0 runs use identical temp-profile isolation.")
    A("- **Runner**: `scripts/run_benchmark_v2.py` (authoritative); batch driver")
    A("  `scripts/run_carb_v2_batch.py`. `run_full_benchmark.py` and")
    A("  `run_retry_batch.py` are superseded/deprecated.")
    A("")
    A("## 6. Reproducibility")
    A("")
    A("- Registry: `task_registry/final_tasks_v2.json` (50 tasks).")
    A("- Run artifacts: `carb_benchmark/runs/<ts>-<task>-<config>-v2.0/` — transcript,")
    A("  diff, run_manifest.yaml, evaluator.json.")
    A("- Evaluation: `scripts/eval_swe.py` / `scripts/eval_lcb.py` (hidden tests).")
    A("- Configurations: `carb_benchmark/configurations/config_{baseline,supreme,superpowers}.yaml`.")

    open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
