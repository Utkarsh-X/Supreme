#!/usr/bin/env python3
"""
analyze_diff.py — Analyzes run diffs to measure surgical editing metrics.
Generates empirical evidence (files modified, lines added/deleted, hunks, scope discipline) for Layer 3 evaluation.
"""

import sys
import os
import argparse
import re

def analyze_patch(patch_content):
    files_modified = set()
    lines_added = 0
    lines_deleted = 0
    hunks = 0

    current_file = None
    for line in patch_content.splitlines():
        if line.startswith('--- a/') or line.startswith('+++ b/'):
            filename = line[6:].strip()
            if filename != '/dev/null':
                files_modified.add(filename)
        elif line.startswith('@@'):
            hunks += 1
        elif line.startswith('+') and not line.startswith('+++'):
            lines_added += 1
        elif line.startswith('-') and not line.startswith('---'):
            lines_deleted += 1

    return {
        "files_modified_count": len(files_modified),
        "files_modified_list": sorted(list(files_modified)),
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "total_lines_changed": lines_added + lines_deleted,
        "hunks_count": hunks
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze git diff patch for surgical editing metrics.")
    parser.add_argument("--patch-file", help="Path to patch file")
    parser.add_argument("--run-dir", help="Path to run output directory containing final_diff.patch")
    args = parser.parse_args()

    patch_path = args.patch_file
    if not patch_path and args.run_dir:
        patch_path = os.path.join(args.run_dir, "final_diff.patch")

    if not patch_path or not os.path.exists(patch_path):
        print(f"Error: Patch file not found at '{patch_path}'")
        sys.exit(1)

    with open(patch_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    metrics = analyze_patch(content)
    print("=== Surgical Edit & Diff Analysis Metrics ===")
    print(f"Files Modified Count : {metrics['files_modified_count']}")
    print(f"Files Modified List  : {', '.join(metrics['files_modified_list'])}")
    print(f"Lines Added          : {metrics['lines_added']}")
    print(f"Lines Deleted        : {metrics['lines_deleted']}")
    print(f"Total Lines Changed  : {metrics['total_lines_changed']}")
    print(f"Hunks Count          : {metrics['hunks_count']}")

if __name__ == '__main__':
    main()
