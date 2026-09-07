import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

tasks = ['fix-git', 'gpt2-codegolf', 'install-windows-3.11', 'tune-mjcf']

for t in tasks:
    print(f"\n=======================================================")
    print(f"DEEP DIVE: {t.upper()}")
    print(f"=======================================================")
    t_runs = [r for r in ledger if r["task_name"] == t]
    for r in t_runs:
        cfg = r["config_id"]
        st = r["status"]
        run_id = r["run_id"]
        sec = r["wall_clock_seconds"]
        tok = r["total_tokens"]
        vsum = r.get("verifier_summary", {})
        
        vlog_path = os.path.join(RUNS_DIR, run_id, "verifier_output.log")
        vlog_snip = ""
        if os.path.exists(vlog_path):
            with open(vlog_path, "r", encoding="utf-8", errors="ignore") as vf:
                vlog_snip = vf.read()[:300].strip().replace("\n", " ")

        print(f"\n  [{cfg.upper()}] Status: {st} | Time: {sec:.1f}s | Tokens: {tok:,}")
        print(f"    Verifier Summary: {vsum}")
        print(f"    Verifier Log Snip: {vlog_snip[:160]}...")
