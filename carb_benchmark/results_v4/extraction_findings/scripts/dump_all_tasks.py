import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('carb_benchmark/results_v4/v4_task_taxonomy.json', 'r', encoding='utf-8') as f:
    tax = json.load(f)

with open('carb_benchmark/results_v4/FORENSIC_AUDIT_LEDGER.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

task_results = {}
for r in ledger:
    task_results.setdefault(r['task_name'], {})[r['config_id']] = r['status']

all_tasks = []
for i, t in enumerate(tax['tasks'], 1):
    res = task_results.get(t['task_name'], {})
    all_tasks.append({
        'num': i,
        'name': t['task_name'],
        'domain': t.get('domain'),
        'category': t.get('category'),
        'difficulty': t.get('difficulty'),
        'snippet': t.get('instruction_snippet', ''),
        'vfiles': t.get('verifier_files', []),
        'results': res
    })

# Write this out as a json for detailed analysis
with open('carb_benchmark/results_v4/extraction_findings/all_89_tasks_annotated.json', 'w', encoding='utf-8') as f:
    json.dump(all_tasks, f, indent=2)

print(f"Dumped {len(all_tasks)} annotated tasks to json.")
