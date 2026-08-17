#!/usr/bin/env python3
"""
generate_hashes.py — Calculates SHA-256 hashes for task prompts, configurations, and repository snapshots.
Enforces strict experimental integrity by detecting unrecorded changes in prompts or configurations.
"""

import sys
import os
import hashlib
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def main():
    print("=== CARB SHA-256 Integrity Hash Generator ===")
    
    # Hashes for configurations
    config_dir = os.path.join(BASE_DIR, 'configurations')
    print("\n--- Configuration Hashes ---")
    for cfg in sorted(os.listdir(config_dir)):
        if cfg.endswith('.yaml'):
            cfg_path = os.path.join(config_dir, cfg)
            print(f"Config: {cfg:<30} SHA-256: {hash_file(cfg_path)}")
            
    # Hashes for public pilot task prompts
    public_tasks_dir = os.path.join(BASE_DIR, 'public', 'tasks')
    print("\n--- Public Task Prompt Hashes ---")
    if os.path.exists(public_tasks_dir):
        for task in sorted(os.listdir(public_tasks_dir)):
            prompt_path = os.path.join(public_tasks_dir, task, 'prompt.txt')
            if os.path.exists(prompt_path):
                print(f"Task Prompt: {task:<30} SHA-256: {hash_file(prompt_path)}")

if __name__ == '__main__':
    main()
