import json

with open('carb_benchmark/results_v4/extraction_findings/all_89_tasks_annotated.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# Group tasks into sets
sup_pass = set(t['name'] for t in tasks if t['results'].get('supreme-v2.0') == 'SUCCESS')
obra_pass = set(t['name'] for t in tasks if t['results'].get('superpowers-v4.0') == 'SUCCESS')
base_pass = set(t['name'] for t in tasks if t['results'].get('baseline-v2.0') == 'SUCCESS')

all_three = sup_pass & obra_pass & base_pass
sup_only = sup_pass - obra_pass - base_pass
obra_only = obra_pass - sup_pass - base_pass
base_only = base_pass - sup_pass - obra_pass

sup_and_obra_not_base = (sup_pass & obra_pass) - base_pass
sup_and_base_not_obra = (sup_pass & base_pass) - obra_pass
obra_and_base_not_sup = (obra_pass & base_pass) - sup_pass

none_passed = set(t['name'] for t in tasks) - sup_pass - obra_pass - base_pass

print("=== VENN DIAGRAM BREAKDOWN (89 TASKS) ===")
print(f"All 3 Passed: {len(all_three)} tasks")
print(f"Supreme ONLY (Exclusive Wins): {len(sup_only)} tasks -> {sorted(list(sup_only))}")
print(f"Superpowers ONLY (Exclusive Wins): {len(obra_only)} tasks -> {sorted(list(obra_only))}")
print(f"Baseline ONLY (Exclusive Wins): {len(base_only)} tasks -> {sorted(list(base_only))}")
print(f"Supreme + Superpowers (Baseline Failed): {len(sup_and_obra_not_base)} tasks -> {sorted(list(sup_and_obra_not_base))}")
print(f"Supreme + Baseline (Superpowers Failed): {len(sup_and_base_not_obra)} tasks -> {sorted(list(sup_and_base_not_obra))}")
print(f"Superpowers + Baseline (Supreme Failed): {len(obra_and_base_not_sup)} tasks -> {sorted(list(obra_and_base_not_sup))}")
print(f"None Passed (Unsolved Frontier): {len(none_passed)} tasks -> {sorted(list(none_passed))}")

print(f"\nTotals:")
print(f"Supreme Total: {len(sup_pass)}/89 ({len(sup_pass)/89*100:.1f}%)")
print(f"Superpowers Total: {len(obra_pass)}/89 ({len(obra_pass)/89*100:.1f}%)")
print(f"Baseline Total: {len(base_pass)}/89 ({len(base_pass)/89*100:.1f}%)")
