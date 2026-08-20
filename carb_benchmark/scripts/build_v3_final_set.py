#!/usr/bin/env python3
"""
build_v3_final_set.py — Phase A -> Phase B handoff: lock the final V3 task set.

Phase A (calibration) ran the BASELINE configuration only on the candidate
pool and recorded pass/fail per task in results/v3_calibration.json. Per the
pre-registered protocol (protocol/v3_discriminative_set_proposal.md §4), a
task is kept for the V3 experiment **if and only if baseline FAILED it**.
Challenger configurations never influence selection; the set is frozen here,
before any supreme/superpowers cell exists.

Usage:
  python carb_benchmark/scripts/build_v3_final_set.py [--min-keep N] [--dry-run]

Outputs:
  task_registry/final_tasks_v3.json   — the locked set (registry records only)
  results/v3_final_set_report.md      — human-readable summary
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # carb_benchmark/
REGISTRY = os.path.join(BASE, "task_registry")
RESULTS = os.path.join(BASE, "results")

SWE_REGISTRY = os.path.join(REGISTRY, "swe_tasks_v3.json")
SWE_MEDIUM_REGISTRY = os.path.join(REGISTRY, "swe_tasks_v3_medium.json")
LCB_REGISTRY = os.path.join(REGISTRY, "v3_lcb_calibration.jsonl")
V2_REGISTRY = os.path.join(REGISTRY, "final_tasks_v2.json")
CALIBRATION = os.path.join(RESULTS, "v3_calibration.json")
OUT = os.path.join(REGISTRY, "final_tasks_v3.json")
REPORT = os.path.join(RESULTS, "v3_final_set_report.md")


def load_calibration():
    d = json.load(open(CALIBRATION, encoding="utf-8"))
    return d.get("results", {}), d.get("config"), d.get("notes")


def load_registries():
    by_id = {}
    for t in json.load(open(SWE_REGISTRY, encoding="utf-8")):
        by_id[t["instance_id"]] = {**t, "family": "SWE", "tier": "hard"}
    medium = json.load(open(SWE_MEDIUM_REGISTRY, encoding="utf-8"))
    items = medium if isinstance(medium, list) else medium.get("instances", medium.get("tasks", []))
    for t in items:
        by_id[t["instance_id"]] = {**t, "family": "SWE", "tier": "medium"}
    with open(LCB_REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            by_id[r["instance_id"]] = {**r, "family": "LCB"}
    return by_id


def main():
    dry = "--dry-run" in sys.argv
    min_keep = 10
    min_wall = 10  # exclude infrastructure failures (agy crashed in <10s)
    if "--min-keep" in sys.argv:
        min_keep = int(sys.argv[sys.argv.index("--min-keep") + 1])
    if "--min-wall" in sys.argv:
        min_wall = int(sys.argv[sys.argv.index("--min-wall") + 1])

    results, config, notes = load_calibration()
    registry = load_registries()

    # Build v2 exclusion set (no cross-version contamination)
    v2_raw = json.load(open(V2_REGISTRY, encoding="utf-8"))
    if isinstance(v2_raw, list):
        v2_ids = set(t.get("instance_id", t.get("id", "")) for t in v2_raw) if v2_raw and isinstance(v2_raw[0], dict) else set(v2_raw)
    else:
        v2_ids = set(v2_raw.keys()) if "tasks" not in v2_raw else set(t.get("instance_id", "") for t in v2_raw["tasks"])
    print(f"v2 exclusion set: {len(v2_ids)} tasks")

    kept, dropped, excluded = [], [], []
    for tid, rec in sorted(results.items()):
        passed = rec.get("passed")
        err = rec.get("error")
        meta = registry.get(tid, {})
        entry = {
            "instance_id": tid,
            "family": meta.get("family", "UNKNOWN"),
            "tier": meta.get("tier"),
            "repo": meta.get("repo"),
            "difficulty": meta.get("difficulty"),
            "workspace_path": meta.get("workspace_path"),
            "prompt_file": meta.get("prompt_file"),
            "private_dir": meta.get("private_dir"),
            "calibration": {
                "passed": passed,
                "wall_clock_seconds": rec.get("wall_clock_seconds"),
                "diff_lines": rec.get("diff"),
                "run_id": rec.get("run_id"),
                "note": (rec.get("note") or "")[:200],
            },
        }
        if tid in v2_ids:
            excluded.append(entry)
            continue
        wall = rec.get("wall_clock_seconds") or 0
        if wall < min_wall:
            excluded.append({**entry, "exclusion_reason": f"infra-fail ({wall:.1f}s < {min_wall}s)"})
            continue
        if passed is False:
            kept.append(entry)
        else:
            dropped.append(entry)

    n_kept = len(kept)
    n_graded = n_kept + len(dropped)
    baseline_pass = sum(1 for e in kept + dropped if e["calibration"]["passed"] is True)
    baseline_pass_rate = baseline_pass / n_graded * 100 if n_graded else 0

    print(f"calibration: {n_graded} graded cells | config={config}")
    print(f"excluded: {len(excluded)} (v2: {sum(1 for e in excluded if e.get('exclusion_reason','').startswith('infra'))} infra-fails, rest v2)")
    print(f"baseline pass rate: {baseline_pass}/{n_graded} = {baseline_pass_rate:.1f}%")
    print(f"kept for V3 (baseline FAILED): {n_kept}")
    print(f"dropped (baseline passed):     {len(dropped)}")

    if n_kept < min_keep:
        print(f"\nWARNING: only {n_kept} tasks calibrate as hard (min_keep={min_keep}).")
        print("The protocol's mitigation: enlarge the pool (medium SWE/LCB) or use "
              "multi-seed runs. Do NOT weaken the keep rule (baseline-fail only) — "
              "that would re-introduce the v2 ceiling.")

    if not dry:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump({"v3_final_set_version": "1.0", "config": config,
                       "selection_rule": "baseline FAILED in Phase A calibration",
                       "notes": notes, "tasks": kept}, f, indent=2)

        fam = {}
        for e in kept:
            fam[e["family"]] = fam.get(e["family"], 0) + 1
        with open(REPORT, "w", encoding="utf-8") as f:
            f.write(f"# V3 Final Task Set (locked after Phase A)\n\n")
            f.write(f"- Locked: {len(kept)} tasks where baseline FAILED in Phase A calibration.\n")
            f.write(f"- Baseline pass rate on the candidate pool: {baseline_pass_rate:.1f}% "
                    f"({baseline_pass}/{n_graded}).\n")
            f.write(f"- Families: {json.dumps(fam)}.\n")
            f.write(f"- Selection rule: baseline-fail only (pre-registered); challengers "
                    f"never influenced selection.\n\n")
            f.write("| Task | Family | Difficulty | Baseline wall (s) | Diff lines |\n")
            f.write("|---|---|---|---|---|\n")
            for e in sorted(kept, key=lambda x: x["instance_id"]):
                c = e["calibration"]
                f.write(f"| `{e['instance_id']}` | {e['family']} | {e.get('difficulty')} | "
                        f"{c.get('wall_clock_seconds')} | {c.get('diff_lines')} |\n")
        print(f"\nwrote {OUT}")
        print(f"wrote {REPORT}")
    else:
        print("\n[dry-run] no files written")
        for e in kept:
            print(f"  KEEP {e['instance_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
