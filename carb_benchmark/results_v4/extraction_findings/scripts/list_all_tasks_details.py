import json

with open('carb_benchmark/results_v4/v4_task_taxonomy.json', 'r', encoding='utf-8') as f:
    tax = json.load(f)

print(f"Total tasks: {len(tax['tasks'])}")
for i, t in enumerate(tax['tasks'], 1):
    print(f"[{i:02d}] {t['task_name']} | Domain: {t.get('domain')} | Cat: {t.get('category')} | Image: {t.get('docker_image')}")
    print(f"     Prompt snippet: {t.get('instruction_snippet', '')[:120].strip()}...")
