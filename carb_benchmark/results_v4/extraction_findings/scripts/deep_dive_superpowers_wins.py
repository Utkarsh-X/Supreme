import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

tasks = ['hf-model-inference', 'mailman', 'mteb-leaderboard', 'raman-fitting']

for t in tasks:
    print(f"\n=======================================================")
    print(f"DEEP DIVE (SUPERPOWERS EXCLUSIVE): {t.upper()}")
    print(f"=======================================================")
    t_runs = [r for r in ledger if r["task_name"] == t]
    for r in t_runs:
        cfg = r["config_id"]
        st = r["status"]
        run_id = r["run_id"]
        sec = r["wall_clock_seconds"]
        tok = r["total_tokens"]
        vsum = r.get("verifier_summary", {})
        print(f"  [{cfg.upper()}] Status: {st:7} | Time: {sec:6.1f}s | Tokens: {tok:9,d} | Verifier: {vsum.get('passed_tests')}/{vsum.get('total_tests')} passed")
