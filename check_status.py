import os
import json

evals_dir = 'carb_benchmark/evaluations'
evals = sorted([d for d in os.listdir(evals_dir) if '2026-08-14-205' in d or '2026-08-14-21' in d])

print(f"Total Completed Sessions: {len(evals)}")
passed_count = 0
for idx, e in enumerate(evals, 1):
    fpath = os.path.join(evals_dir, e, 'evaluator.json')
    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
            passed = data.get('passed', False)
            if passed:
                passed_count += 1
            print(f"[{idx:02d}] Task: {data.get('task_id')} | Passed: {passed} | Lines: {data.get('lines_changed')} | Duration: {data.get('wall_clock_seconds')}s")

print(f"\nTotal Passed: {passed_count} / {len(evals)} ({round(passed_count/len(evals)*100, 1) if evals else 0}%)")
