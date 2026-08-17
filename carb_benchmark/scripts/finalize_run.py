#!/usr/bin/env python3
"""
finalize_run.py — Programmatically seals a benchmark run session manifest upon completion.
Updates status, timestamps, diff artifact paths, and surgical editing metrics.
"""

import sys
import os
import yaml
import datetime
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS_DIR = os.path.join(BASE_DIR, 'runs')

def finalize_run(run_id, status, diff_file=None, transcript_file=None):
    run_dir = os.path.join(RUNS_DIR, run_id)
    manifest_path = os.path.join(run_dir, "run_manifest.yaml")

    if not os.path.exists(manifest_path):
        print(f"Error: Manifest for run '{run_id}' not found at '{manifest_path}'")
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = yaml.safe_load(f)

    start_time = datetime.datetime.fromisoformat(manifest['started_at'])
    end_time = datetime.datetime.now()
    wall_clock = (end_time - start_time).total_seconds()

    manifest['status'] = status
    manifest['finished_at'] = end_time.isoformat()
    manifest['resource_metrics']['wall_clock_seconds'] = round(wall_clock, 2)

    if diff_file:
        manifest['artifacts']['diff_file'] = diff_file
    if transcript_file:
        manifest['artifacts']['transcript_file'] = transcript_file

    with open(manifest_path, 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, sort_keys=False)

    print(f"=== Programmatic Run Session Finalized ===")
    print(f"Run ID     : {run_id}")
    print(f"Status     : {status}")
    print(f"Duration   : {round(wall_clock, 2)}s")
    print(f"Manifest   : {manifest_path}")

def main():
    parser = argparse.ArgumentParser(description="Finalize CARB run session manifest.")
    parser.add_argument("--run-id", required=True, help="Run ID")
    parser.add_argument("--status", choices=["SUCCESS", "FAILURE", "TIMEOUT", "CANCELLED"], default="SUCCESS")
    parser.add_argument("--diff-file", help="Path to diff file")
    parser.add_argument("--transcript-file", help="Path to transcript file")
    args = parser.parse_args()
    finalize_run(args.run_id, args.status, args.diff_file, args.transcript_file)

if __name__ == '__main__':
    main()
