#!/usr/bin/env python3
"""
init_task.py — Initializes or resets a clean task workspace directory from immutable golden snapshots.
Performs SHA-256 hash enforcement against metadata gates and enforces clean Git repository state.
"""

import sys
import os
import shutil
import argparse
import subprocess
import hashlib
import stat
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPREME_ROOT = os.path.dirname(BASE_DIR)
WORKSPACES_DIR = os.path.join(SUPREME_ROOT, 'carb_workspaces')
SNAPSHOTS_DIR = os.path.join(BASE_DIR, 'snapshots')

def handle_remove_readonly(func, path, exc_info):
    """
    Error handler for shutil.rmtree to handle read-only files (e.g. .git objects on Windows).
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

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

def reset_workspace(task_id, enforce_hashes=True):
    workspace_path = os.path.join(WORKSPACES_DIR, task_id)
    snapshot_path = os.path.join(SNAPSHOTS_DIR, task_id)
    metadata_path = os.path.join(BASE_DIR, 'public', 'tasks', task_id, 'metadata.yaml')

    if not os.path.exists(snapshot_path):
        print(f"Error: Golden snapshot for '{task_id}' not found at '{snapshot_path}'")
        sys.exit(1)

    print(f"=== CARB Task Workspace Reset & Snapshot Reconstruction ===")
    print(f"Task ID        : {task_id}")
    print(f"Snapshot Path  : {snapshot_path}")
    print(f"Workspace Path : {workspace_path}")

    # Step 1: Pre-run SHA-256 Hash Enforcement Gate
    if enforce_hashes and os.path.exists(metadata_path):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            meta = yaml.safe_load(f)
        
        expected_prompt_hash = meta.get('expected_prompt_hash')
        expected_snapshot_hash = meta.get('expected_snapshot_hash')

        actual_prompt_hash = hash_file(os.path.join(snapshot_path, 'prompt.txt'))
        actual_snapshot_hash = hash_directory_tree(snapshot_path)

        print("\n--- Mandatory Pre-Run Hash Integrity Gate ---")
        if expected_prompt_hash:
            if actual_prompt_hash != expected_prompt_hash:
                print(f"CRITICAL ERROR: Prompt hash mismatch for {task_id}!")
                print(f"  Expected : {expected_prompt_hash}")
                print(f"  Actual   : {actual_prompt_hash}")
                sys.exit(1)
            print(f"PASS: Prompt SHA-256 Hash Verified ({actual_prompt_hash[:12]}...)")

        if expected_snapshot_hash:
            if actual_snapshot_hash != expected_snapshot_hash:
                print(f"CRITICAL ERROR: Snapshot tree hash mismatch for {task_id}!")
                print(f"  Expected : {expected_snapshot_hash}")
                print(f"  Actual   : {actual_snapshot_hash}")
                sys.exit(1)
            print(f"PASS: Snapshot Tree SHA-256 Hash Verified ({actual_snapshot_hash[:12]}...)")

    # Step 2: Complete Destruction of Existing Workspace
    if os.path.exists(workspace_path):
        print(f"Purging existing workspace directory...")
        shutil.rmtree(workspace_path, onerror=handle_remove_readonly)

    # Step 3: Fresh Workspace Copy from Immutable Golden Snapshot
    print(f"Copying immutable golden snapshot...")
    shutil.copytree(snapshot_path, workspace_path)

    # Step 4: Initialize Fresh Local Git Repository in Workspace
    try:
        subprocess.run(['git', 'init'], cwd=workspace_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'add', '.'], cwd=workspace_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'commit', '-m', 'CARB Golden Task Snapshot Initialized'], cwd=workspace_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Initialized clean Git repository in workspace.")
    except Exception as e:
        print(f"Warning: Git initialization failed in workspace: {e}")

    print(f"SUCCESS: Task workspace '{task_id}' fully reconstructed and verified.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Initialize clean CARB task workspace from golden snapshot.")
    parser.add_argument("--task", required=True, help="Task ID (e.g. T001_sample_repo_debug)")
    parser.add_argument("--no-hash-check", action="store_true", help="Bypass hash integrity gate")
    args = parser.parse_args()
    reset_workspace(args.task, enforce_hashes=not args.no_hash_check)

if __name__ == '__main__':
    main()
