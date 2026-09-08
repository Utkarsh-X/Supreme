#!/usr/bin/env python3
import json

data = json.load(open('carb_benchmark/results_v4/extraction_findings/canonical_267_deep_telemetry.json', encoding='utf-8'))

by_cfg = {}
by_cfg_hard = {}

for r in data:
    cfg = r['config_id']
    if cfg not in by_cfg:
        by_cfg[cfg] = {'solved': 0, 'runs': 0, 'inp': 0, 'out': 0, 'think': 0, 'tot': 0, 'wall': 0.0}
        by_cfg_hard[cfg] = {'solved': 0, 'runs': 0, 'inp': 0, 'out': 0, 'think': 0, 'tot': 0, 'wall': 0.0}
    
    by_cfg[cfg]['runs'] += 1
    if r['status'] == 'SUCCESS': by_cfg[cfg]['solved'] += 1
    by_cfg[cfg]['tot'] += r.get('total_tokens', 0)
    by_cfg[cfg]['wall'] += r.get('wall_clock_seconds', 0.0)
    tm = r.get('transcript_metrics', {})
    by_cfg[cfg]['inp'] += tm.get('input_tokens_total', 0)
    by_cfg[cfg]['out'] += tm.get('output_tokens_total', 0)
    by_cfg[cfg]['think'] += tm.get('thinking_tokens_total', 0)
    
    if r.get('difficulty') == 'hard':
        by_cfg_hard[cfg]['runs'] += 1
        if r['status'] == 'SUCCESS': by_cfg_hard[cfg]['solved'] += 1
        by_cfg_hard[cfg]['tot'] += r.get('total_tokens', 0)
        by_cfg_hard[cfg]['wall'] += r.get('wall_clock_seconds', 0.0)
        by_cfg_hard[cfg]['inp'] += tm.get('input_tokens_total', 0)
        by_cfg_hard[cfg]['out'] += tm.get('output_tokens_total', 0)
        by_cfg_hard[cfg]['think'] += tm.get('thinking_tokens_total', 0)

print("=== FULL BENCHMARK (N=89) ===")
total_think = 0
for cfg in sorted(by_cfg):
    d = by_cfg[cfg]
    total_think += d['think']
    cost_paid = (d['inp']/1e6 * 0.5598) + (d['out']/1e6 * 3.745)
    cost_list = (d['inp']/1e6 * 0.75) + (d['out']/1e6 * 3.75)
    cps_paid = cost_paid / d['solved']
    cpa_paid = cost_paid / d['runs']
    print(f"\n{cfg}:")
    print(f"  Solved: {d['solved']}/{d['runs']} ({d['solved']/d['runs']:.3%})")
    print(f"  Input Tokens: {d['inp']:,} ({d['inp']/1e6:.2f}M)")
    print(f"  Output Tokens: {d['out']:,} ({d['out']/1e6:.2f}M)")
    print(f"  Thinking Tokens: {d['think']:,} ({d['think']/1e6:.3f}M)")
    print(f"  Total Tokens: {d['tot']:,} ({d['tot']/1e6:.2f}M)")
    print(f"  Cost Paid: ${cost_paid:.4f} (rounds to ${cost_paid:.2f})")
    print(f"  Cost/Solved (Paid): ${cps_paid:.4f} (rounds to ${cps_paid:.3f})")
    print(f"  Cost/Attempted (Paid): ${cpa_paid:.4f} (rounds to ${cpa_paid:.3f})")
    print(f"  Cost List: ${cost_list:.4f} (rounds to ${cost_list:.2f})")
    print(f"  Cost/Solved (List): ${cost_list/d['solved']:.4f} (rounds to ${cost_list/d['solved']:.3f})")

print(f"\nTotal Thinking Tokens Across All 267 Runs: {total_think:,}")

print("\n=== HARD SUBSET (N=30) ===")
for cfg in sorted(by_cfg_hard):
    d = by_cfg_hard[cfg]
    cost_paid = (d['inp']/1e6 * 0.5598) + (d['out']/1e6 * 3.745)
    cps_paid = cost_paid / d['solved']
    cpa_paid = cost_paid / d['runs']
    print(f"\n{cfg}:")
    print(f"  Solved: {d['solved']}/{d['runs']} ({d['solved']/d['runs']:.3%})")
    print(f"  Input Tokens: {d['inp']:,} ({d['inp']/1e6:.2f}M)")
    print(f"  Output Tokens: {d['out']:,} ({d['out']/1e6:.2f}M)")
    print(f"  Thinking Tokens: {d['think']:,} ({d['think']/1e6:.3f}M)")
    print(f"  Cost Paid: ${cost_paid:.4f} (rounds to ${cost_paid:.2f})")
    print(f"  Cost/Solved (Paid): ${cps_paid:.4f} (rounds to ${cps_paid:.3f})")
    print(f"  Cost/Attempted (Paid): ${cpa_paid:.4f} (rounds to ${cpa_paid:.3f})")

# Calculate exact relative reduction between Superpowers and Supreme:
sp_cps = (by_cfg['superpowers-v4.0']['inp']/1e6 * 0.5598 + by_cfg['superpowers-v4.0']['out']/1e6 * 3.745) / by_cfg['superpowers-v4.0']['solved']
sup_cps = (by_cfg['supreme-v2.0']['inp']/1e6 * 0.5598 + by_cfg['supreme-v2.0']['out']/1e6 * 3.745) / by_cfg['supreme-v2.0']['solved']
rel_red = (sp_cps - sup_cps) / sp_cps * 100
print(f"\nRelative reduction (Superpowers vs Supreme Cost/Solved): ({sp_cps:.6f} - {sup_cps:.6f}) / {sp_cps:.6f} = {rel_red:.4f}%")

# Using rounded numbers from prompt:
sp_p = 29.35 / 58
sup_p = 29.80 / 61
rel_red_prompt = (sp_p - sup_p) / sp_p * 100
print(f"Using $29.35/58 and $29.80/61: ({sp_p:.6f} - {sup_p:.6f}) / {sp_p:.6f} = {rel_red_prompt:.4f}%")
