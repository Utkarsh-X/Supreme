#!/usr/bin/env python3
import os
import subprocess

# Clear raw API keys from environment so agy uses Antigravity IDE internal auth token & router
env = os.environ.copy()
env.pop("GOOGLE_API_KEY", None)
env.pop("GEMINI_API_KEY", None)

cmd = [
    "agy",
    "-p", "State your model identity. Which exact model name and version are you?",
    "--model", "gemini-3.7-flash",
    "--dangerously-skip-permissions"
]

print("=== EXECUTING VIA ANTIGRAVITY IDE CLI (agy.exe) ===")
res = subprocess.run(cmd, capture_output=True, text=True, env=env)
print("STDOUT:\n", res.stdout)
print("STDERR:\n", res.stderr)
print("Return Code:", res.returncode)
