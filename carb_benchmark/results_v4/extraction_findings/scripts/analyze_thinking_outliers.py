import json
import numpy as np

with open('carb_benchmark/results_v4/extraction_findings/canonical_267_deep_telemetry.json', 'r', encoding='utf-8') as f:
    runs = json.load(f)

print('=== EASY TASKS AUDIT ===')
easy_runs = [r for r in runs if r['difficulty'].lower() == 'easy']
tasks_easy = sorted(list(set(r['task_name'] for r in easy_runs)))
for t in tasks_easy:
    print(f'Task: {t}')
    for cfg in ['supreme-v2.0', 'superpowers-v4.0', 'baseline-v2.0']:
        r = next(x for x in easy_runs if x['task_name'] == t and x['config_id'] == cfg)
        th = r['transcript_metrics']['thinking_tokens_total']
        status = r['status']
        tc = r['transcript_metrics']['turn_count']
        print(f"  {cfg:16}: {status:7} | Thinking: {th:6d} | Tools: {tc:2d}")

print('\n=== TOP 10 OVERTHINKING TRAPS (FAILED RUNS WITH HIGHEST THINKING) ===')
failed_runs = [r for r in runs if r['status'] != 'SUCCESS']
failed_runs.sort(key=lambda x: x['transcript_metrics']['thinking_tokens_total'], reverse=True)
for r in failed_runs[:10]:
    th = r['transcript_metrics']['thinking_tokens_total']
    turns = r['transcript_metrics']['turn_count']
    cfg = r['config_id']
    tname = r['task_name']
    diff = r['difficulty']
    secs = r['wall_clock_seconds']
    print(f"{cfg:16} | {tname:35} | Diff: {diff:6} | Thinking: {th:6d} | Turns: {turns:2d} | Secs: {secs:6.1f}")

print('\n=== TOP 10 BREAKTHROUGH HIGH-THINKING PASSES (SUCCESS RUNS) ===')
succ_runs = [r for r in runs if r['status'] == 'SUCCESS']
succ_runs.sort(key=lambda x: x['transcript_metrics']['thinking_tokens_total'], reverse=True)
for r in succ_runs[:10]:
    th = r['transcript_metrics']['thinking_tokens_total']
    turns = r['transcript_metrics']['turn_count']
    cfg = r['config_id']
    tname = r['task_name']
    diff = r['difficulty']
    secs = r['wall_clock_seconds']
    print(f"{cfg:16} | {tname:35} | Diff: {diff:6} | Thinking: {th:6d} | Turns: {turns:2d} | Secs: {secs:6.1f}")
