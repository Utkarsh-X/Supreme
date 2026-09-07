import json
import os
import re

with open('carb_benchmark/results_v4/v4_task_taxonomy.json', 'r', encoding='utf-8') as f:
    tax = json.load(f)

with open('carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

# Build a lookup of task results by config
task_results = {}
for r in ledger:
    tname = r['task_name']
    cfg = r['config_id']
    st = r['status']
    task_results.setdefault(tname, {})[cfg] = st

print(f"Total tasks in taxonomy: {len(tax['tasks'])}")

# Let's inspect each task and classify its primary language / environment
tasks_meta = []
for t in tax['tasks']:
    tname = t['task_name']
    cat = t.get('category', '')
    instr = t.get('instruction_snippet', '')
    desc = t.get('description', '')
    vfiles = t.get('verifier_files', [])
    combined_text = f"{tname} {cat} {instr} {desc}".lower()
    
    # We can also check files in the benchmark task directory if available
    tasks_meta.append({
        'task_name': tname,
        'category': cat,
        'domain': t.get('domain', ''),
        'difficulty': t.get('difficulty', ''),
        'snippet': instr[:200],
        'results': task_results.get(tname, {})
    })

print("Sample 10 tasks and snippets:")
for tm in tasks_meta[:10]:
    print(f"{tm['task_name']:30} | {tm['category']:20} | {tm['results']}")
