import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

other_unsolved = [
    'break-filter-js-from-html', 'caffe-cifar-10', 'compile-compcert', 
    'dna-assembly', 'dna-insert', 'extract-elf'
]

for name in other_unsolved:
    print(f"\nTask: {name}")
    t_runs = [r for r in ledger if r["task_name"] == name]
    for r in t_runs:
        cfg = r["config_id"]
        sec = r["wall_clock_seconds"]
        tok = r["total_tokens"]
        vsum = r.get("verifier_summary", {})
        p = vsum.get("passed_tests")
        tot = vsum.get("total_tests")
        log_snip = str(vsum.get("key_assertion_log", ""))[:140].strip().replace("\n", " ")
        print(f"  {cfg:16}: Passed: {p}/{tot} | Sec: {sec:6.1f}s | Tok: {tok:8,d} | Log: {log_snip}")
