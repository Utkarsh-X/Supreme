#!/usr/bin/env python3
"""
v3_propose_tasks.py — build the V3 candidate shortlist for a *discriminative*
benchmark arm.

Why V3 exists: the v2 50-task set is saturated (46/50 tasks solved by all
three configurations; McNemar p = 1.0 on every pair). Saturated tasks cannot
separate configurations, so V3 must target tasks on which the baseline
configuration empirically FAILS. This script produces the candidate pool from
which that calibrated set will be chosen (calibration itself is a baseline-only
run phase described in protocol/v3_discriminative_set_proposal.md).

Selection tiers (all data is public corpus metadata, not model output):

  SWE-bench Verified (500 instances, difficulty = human resolution time):
    - hard   : "1-4 hours" and ">4 hours" tiers, repositories we already
               support with era-appropriate venvs (django, sympy, sphinx,
               matplotlib, pytest, scikit-learn, astropy)
    - medium : "15 min - 1 hour" tier, same repos (fallback volume)
    Excludes every instance already used in v2 (never reuse exposed tasks).

  LiveCodeBench v5 (175 problems):
    - AtCoder-platform medium + hard tiers (our eval harness runs stdio
      main.py graders, so AtCoder problems are directly usable)
    Excludes the 20 v2 question ids.

  Never-used families (from the v1 candidate pool, no v2 exposure):
    - terminal_bench_2.0 (40 candidates)
    - custom_diagnostic (20 candidates)

Output: task_registry/v3_candidate_shortlist.json
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # carb_benchmark/
DATA = os.path.join(BASE, "sources", "data")
REGISTRY = os.path.join(BASE, "task_registry")

SUPPORTED_REPOS = {
    "django/django", "sympy/sympy", "sphinx-doc/sphinx",
    "matplotlib/matplotlib", "pytest-dev/pytest",
    "scikit-learn/scikit-learn", "astropy/astropy",
}
HARD_TIERS = ("1-4 hours", ">4 hours")
MEDIUM_TIERS = ("15 min - 1 hour",)

# Package-version prefixes for which an era-appropriate venv can be built on
# this machine (must mirror validate_swe_tasks.PY_MAP; unknown versions => the
# task cannot be evaluated and must not enter the calibration set).
SUPPORTED_VERSIONS = {
    "sympy": ("1.1", "1.4", "1.5", "1.7", "1.12"),
    "django": ("3.0", "3.1", "3.2", "4.0", "4.2", "5.0"),
    "pytest": ("4.5", "6.0"),
    "sphinx": ("3.5", "4.1", "4.3", "5.0"),
    "matplotlib": ("3.5", "3.6"),
    "scikit-learn": ("0.22",),
    "astropy": ("5.1",),
}


def version_supported(repo: str, version: str) -> bool:
    # LCB/platform entries have no repo path (e.g. "atcoder") — venv support
    # only applies to SWE-bench repos.
    if "/" not in repo:
        return True
    repo_name = repo.split("/")[1]
    return any(version.startswith(p) for p in SUPPORTED_VERSIONS.get(repo_name, ()))


def load_v2_ids():
    ids = set()
    f = os.path.join(REGISTRY, "final_tasks_v2.json")
    if os.path.exists(f):
        for t in json.load(open(f, encoding="utf-8")):
            ids.add(t["instance_id"])
    l = os.path.join(REGISTRY, "lcb_tasks_v2.json")
    if os.path.exists(l):
        for t in json.load(open(l, encoding="utf-8")):
            ids.add(t["instance_id"])
    return ids


def swe_instances():
    path = os.path.join(DATA, "swebench_verified", "verified.jsonl")
    out = {"hard": [], "medium": []}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            d = json.loads(line)
            if d.get("repo") not in SUPPORTED_REPOS:
                continue
            tier = d.get("difficulty")
            if tier in HARD_TIERS:
                out["hard"].append(d)
            elif tier in MEDIUM_TIERS:
                out["medium"].append(d)
    return out


def lcb_instances():
    path = os.path.join(DATA, "lcb_v5.jsonl")
    out = {"medium": [], "hard": []}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            d = json.loads(line)
            qid = str(d.get("question_id", ""))
            if not (qid.startswith("abc") or qid.startswith("arc")):
                continue
            diff = d.get("difficulty")
            if diff == "medium":
                out["medium"].append(d)
            elif diff == "hard":
                out["hard"].append(d)
    return out


def other_family_candidates():
    pool = json.load(open(os.path.join(REGISTRY, "candidate_pool.json"), encoding="utf-8"))
    by_src = {}
    for c in pool["candidates"]:
        by_src.setdefault(c["source"], []).append(c)
    return {
        "terminal_bench_2.0": by_src.get("terminal_bench_2.0", []),
        "custom_diagnostic": by_src.get("custom_diagnostic", []),
    }


def summarize(d):
    """Small metadata record for a candidate (no problem statements)."""
    version = d.get("version") or ""
    repo = d.get("repo") or ""
    return {
        "instance_id": d.get("instance_id") or d.get("question_id"),
        "repo": repo,
        "difficulty": d.get("difficulty"),
        "version": version,
        "venv_supported": version_supported(repo, version),
        "gold_patch_bytes": len(d.get("patch", "") or ""),
        "fail_to_pass_count": len(d.get("FAIL_TO_PASS", []) or []),
        "pass_to_pass_count": len(d.get("PASS_TO_PASS", []) or []),
    }


def main():
    v2_ids = load_v2_ids()
    print(f"v2 instances to exclude: {len(v2_ids)}")

    swe = swe_instances()
    lcb = lcb_instances()
    other = other_family_candidates()

    swe_hard = [summarize(d) for d in swe["hard"] if d["instance_id"] not in v2_ids]
    swe_medium = [summarize(d) for d in swe["medium"] if d["instance_id"] not in v2_ids]

    shortlist = {
        "v3_candidate_shortlist_version": "0.2",
        "generated_by": os.path.basename(__file__),
        "excludes": {"v2_instances": sorted(v2_ids)},
        "swe_bench_verified": {
            "hard_tier": swe_hard,
            "hard_tier_venv_supported": [c for c in swe_hard if c["venv_supported"]],
            "medium_tier": swe_medium,
            "medium_tier_venv_supported": [c for c in swe_medium if c["venv_supported"]],
        },
        "livecodebench_v5_atcoder": {
            "medium": [summarize(d) for d in lcb["medium"] if str(d["question_id"]) not in v2_ids],
            "hard": [summarize(d) for d in lcb["hard"] if str(d["question_id"]) not in v2_ids],
        },
        "never_used_families": {
            "terminal_bench_2.0": [summarize(c) for c in other["terminal_bench_2.0"]],
            "custom_diagnostic": [summarize(c) for c in other["custom_diagnostic"]],
        },
    }

    out_path = os.path.join(REGISTRY, "v3_candidate_shortlist.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(shortlist, fh, indent=1)

    print("\n--- SWE-bench Verified (supported repos, excluding v2) ---")
    print(f"  hard tier  (1-4h / >4h):     {len(shortlist['swe_bench_verified']['hard_tier'])}  (venv-supported: {len(shortlist['swe_bench_verified']['hard_tier_venv_supported'])})")
    print(f"  medium tier (15min-1h):      {len(shortlist['swe_bench_verified']['medium_tier'])}  (venv-supported: {len(shortlist['swe_bench_verified']['medium_tier_venv_supported'])})")
    print("\n--- LiveCodeBench v5 AtCoder (excluding v2) ---")
    print(f"  medium: {len(shortlist['livecodebench_v5_atcoder']['medium'])}   hard: {len(shortlist['livecodebench_v5_atcoder']['hard'])}")
    print("\n--- Never-used families ---")
    print(f"  terminal_bench_2.0: {len(shortlist['never_used_families']['terminal_bench_2.0'])}   custom_diagnostic: {len(shortlist['never_used_families']['custom_diagnostic'])}")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    sys.exit(main())
