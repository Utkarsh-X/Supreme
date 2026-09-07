import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

with open('carb_benchmark/results_v4/extraction_findings/all_89_tasks_annotated.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# Find unsolved
unsolved = [t for t in tasks if not any(v == 'SUCCESS' for v in t['results'].values())]

print(f"=== THE 18 UNSOLVED FRONTIER TASKS (0% PASS RATE ACROSS ALL PARADIGMS) ===")
for t in unsolved:
    name = t['name']
    diff = t['difficulty']
    dom = t['domain']
    cat = t['category']
    print(f"\nTask: {name} | Diff: {diff} | Domain: {dom} | Cat: {cat}")
    t_runs = [r for r in ledger if r["task_name"] == name]
    for r in t_runs:
        cfg = r["config_id"]
        sec = r["wall_clock_seconds"]
        tok = r["total_tokens"]
        vsum = r.get("verifier_summary", {})
        p = vsum.get("passed_tests")
        tot = vsum.get("total_tests")
        log_snip = str(vsum.get("key_assertion_log", ""))[:120].strip().replace("\n", " ")
        print(f"  {cfg:16}: Passed: {p}/{tot} | Sec: {sec:6.1f}s | Tok: {tok:8,d} | Log: {log_snip}")
