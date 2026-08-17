#!/usr/bin/env python3
"""
build_swe_workspaces.py — Materialize real SWE-bench Verified workspaces for CARB-v2.

For each instance in the selection file:
  1. Download the repo tarball at the exact base_commit from codeload.github.com.
  2. Extract into carb_workspaces/<instance_id>/ (stripping the tarball root dir).
  3. Write prompt.txt = the real problem statement (public).
  4. Write private/<instance_id>/{gold_patch.patch, test_patch.patch,
     evaluation_spec.json} (private — never exposed to the agent workspace).
  5. git init + initial commit (so run diffs can be extracted).
  6. Append to the task registry (task_registry/swe_tasks_v2.json).

Usage:
  python carb_benchmark/scripts/build_swe_workspaces.py [--selection <jsonl>] [--limit N]
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import tarfile
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE_DIR)
WORKSPACES_DIR = os.path.join(SUPREME_ROOT, "carb_workspaces")
PRIVATE_DIR = os.path.join(BASE_DIR, "private")
REGISTRY_DIR = os.path.join(BASE_DIR, "task_registry")
DATA_DIR = os.path.join(BASE_DIR, "sources", "data", "swebench_verified")
CACHE_DIR = os.path.join(DATA_DIR, "tarballs")

DEFAULT_SELECTION = os.path.join(DATA_DIR, "selected_30.jsonl")
REGISTRY_PATH = os.path.join(REGISTRY_DIR, "swe_tasks_v2.json")


def fetch_tarball(owner_repo, commit):
    """Download (and cache) the repo tarball at the exact commit."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    safe = owner_repo.replace("/", "__")
    cache = os.path.join(CACHE_DIR, f"{safe}_{commit[:12]}.tar.gz")
    if os.path.exists(cache) and os.path.getsize(cache) > 0:
        return cache
    url = f"https://codeload.github.com/{owner_repo}/tar.gz/{commit}"
    print(f"  downloading {owner_repo}@{commit[:10]} ...", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "CARB-v2-corpus"})
    with urllib.request.urlopen(req, timeout=120) as r, open(cache, "wb") as f:
        shutil.copyfileobj(r, f)
    return cache


def extract_tarball(tarball, dest):
    """Extract tarball, stripping the single root directory."""
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(tarball, "r:gz") as tf:
        members = tf.getmembers()
        root = None
        for m in members:
            parts = m.name.split("/")
            if root is None and parts:
                root = parts[0]
        for m in members:
            parts = m.name.split("/")
            if len(parts) <= 1:
                continue
            rel = "/".join(parts[1:])
            m.name = rel
            tf.extract(m, dest, filter="data")


def git_init_commit(workspace):
    subprocess.run(["git", "init"], cwd=workspace, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "config", "core.longpaths", "true"], cwd=workspace, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "add", "."], cwd=workspace, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "SWE-bench base commit snapshot"],
                   cwd=workspace, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", default=DEFAULT_SELECTION)
    parser.add_argument("--limit", type=int, default=0, help="0 = all")
    args = parser.parse_args()

    with open(args.selection, encoding="utf-8") as f:
        instances = [json.loads(l) for l in f if l.strip()]
    if args.limit:
        instances = instances[:args.limit]

    registry = []
    if os.path.exists(REGISTRY_PATH):
        registry = json.load(open(REGISTRY_PATH, encoding="utf-8"))
    seen = {r["instance_id"] for r in registry}

    print(f"Materializing {len(instances)} SWE-bench workspaces...")
    for idx, inst in enumerate(instances, 1):
        iid = inst["instance_id"]
        if iid in seen:
            print(f"[{idx}/{len(instances)}] {iid}: already exists, skip")
            continue
        owner_repo = inst["repo"]
        commit = inst["base_commit"]
        print(f"[{idx}/{len(instances)}] {iid} ({owner_repo}@{commit[:10]})")
        tarball = fetch_tarball(owner_repo, commit)

        workspace = os.path.join(WORKSPACES_DIR, iid)
        extract_tarball(tarball, workspace)

        # Public prompt = real problem statement
        with open(os.path.join(workspace, "prompt.txt"), "w", encoding="utf-8") as f:
            f.write(inst["problem_statement"].strip() + "\n")

        # Private artifacts
        priv = os.path.join(PRIVATE_DIR, iid)
        os.makedirs(priv, exist_ok=True)
        with open(os.path.join(priv, "gold_patch.patch"), "w", encoding="utf-8") as f:
            f.write(inst["patch"].strip() + "\n")
        with open(os.path.join(priv, "test_patch.patch"), "w", encoding="utf-8") as f:
            f.write(inst["test_patch"].strip() + "\n")
        with open(os.path.join(priv, "evaluation_spec.json"), "w", encoding="utf-8") as f:
            json.dump({
                "instance_id": iid,
                "repo": owner_repo,
                "base_commit": commit,
                "environment_setup_commit": inst.get("environment_setup_commit"),
                "FAIL_TO_PASS": inst["FAIL_TO_PASS"],
                "PASS_TO_PASS": inst["PASS_TO_PASS"],
                "test_command_hint": "pytest <FAIL_TO_PASS files>",
            }, f, indent=2, ensure_ascii=False)

        git_init_commit(workspace)
        registry.append({
            "instance_id": iid,
            "repo": owner_repo,
            "base_commit": commit,
            "source": "swebench_verified",
            "difficulty": inst.get("difficulty"),
            "workspace_path": os.path.join("carb_workspaces", iid),
            "prompt_file": os.path.join("carb_workspaces", iid, "prompt.txt"),
            "private_dir": os.path.join("private", iid),
        })
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"  -> done ({len(registry)} in registry)")

    print(f"\nRegistry: {len(registry)} tasks -> {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
