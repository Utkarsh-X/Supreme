#!/usr/bin/env python3
"""
start_run.py — Programmatically initializes a benchmark run session and creates run_manifest.yaml.
Automates complete provenance capture (hashes, environment specs, configuration version, timestamps).
"""

import sys
import os
import hashlib
import json
import yaml
import datetime
import argparse
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS_DIR = os.path.join(BASE_DIR, 'runs')

def hash_file(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def hash_directory_tree(dirpath):
    if not os.path.exists(dirpath):
        return None
    hasher = hashlib.sha256()
    for root, dirs, files in os.walk(dirpath):
        if '.git' in dirs:
            dirs.remove('.git')
        dirs.sort()
        for file in sorted(files):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, dirpath).replace('\\', '/')
            hasher.update(rel_path.encode('utf-8'))
            with open(full_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
    return hasher.hexdigest()

def start_run(task_id, config_id):
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    run_id = f"{timestamp_str}-{task_id}-{config_id}"
    run_dir = os.path.join(RUNS_DIR, run_id)
    os.makedirs(run_dir, exist_ok=True)

    config_path = os.path.join(BASE_DIR, 'configurations', f"config_{config_id.split('-')[0]}.yaml")
    if not os.path.exists(config_path):
        config_path = os.path.join(BASE_DIR, 'configurations', f"{config_id}.yaml")

    prompt_path = os.path.join(BASE_DIR, 'public', 'tasks', task_id, 'prompt.txt')
    snapshot_path = os.path.join(BASE_DIR, 'snapshots', task_id)

    config_hash = hash_file(config_path) if os.path.exists(config_path) else None
    prompt_hash = hash_file(prompt_path) if os.path.exists(prompt_path) else None
    snapshot_hash = hash_directory_tree(snapshot_path) if os.path.exists(snapshot_path) else None

    manifest_data = {
        "run_id": run_id,
        "task_id": task_id,
        "configuration_id": config_id,
        "status": "IN_PROGRESS",
        "started_at": datetime.datetime.now().isoformat(),
        "finished_at": None,
        "model": {
            "provider": "Gemini",
            "identifier": "gemini-3.6-flash-high",  # LOCKED model for the whole benchmark; agy is invoked with --model gemini-3.6-flash-high
            "temperature": 0.0
        },
        "environment": {
            "os": platform.platform(),
            "python_version": sys.version.split()[0],
            "ide": "Antigravity IDE Agent",
            "isolation_mode": "non_adversarial_cooperative"
        },
        "provenance_hashes": {
            "configuration_hash": config_hash,
            "prompt_hash": prompt_hash,
            "snapshot_hash": snapshot_hash
        },
        "artifacts": {
            "transcript_file": None,
            "diff_file": None,
            "evaluator_output": None
        },
        "resource_metrics": {
            "tool_iterations": 0,
            "wall_clock_seconds": 0
        }
    }

    manifest_path = os.path.join(run_dir, "run_manifest.yaml")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        yaml.dump(manifest_data, f, sort_keys=False)

    print(f"=== Programmatic Run Session Initialized ===")
    print(f"Run ID        : {run_id}")
    print(f"Manifest Path : {manifest_path}")
    print(f"Config Hash   : {config_hash[:12] if config_hash else 'N/A'}")
    print(f"Prompt Hash   : {prompt_hash[:12] if prompt_hash else 'N/A'}")
    return run_id, manifest_path

def main():
    parser = argparse.ArgumentParser(description="Programmatically initialize CARB run session and provenance manifest.")
    parser.add_argument("--task", required=True, help="Task ID")
    parser.add_argument("--config", required=True, help="Configuration ID (e.g. baseline-v1.0)")
    args = parser.parse_args()
    start_run(args.task, args.config)

if __name__ == '__main__':
    main()
