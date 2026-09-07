import json
from collections import Counter, defaultdict
import numpy as np

with open('carb_benchmark/results_v4/extraction_findings/canonical_267_deep_telemetry.json', 'r', encoding='utf-8') as f:
    runs = json.load(f)

configs = ['supreme-v2.0', 'superpowers-v4.0', 'baseline-v2.0']

for cfg in configs:
    cfg_runs = [r for r in runs if r['config_id'] == cfg]
    bigrams = Counter()
    trigrams = Counter()
    transitions = defaultdict(Counter)
    tool_counts = Counter()

    for r in cfg_runs:
        seq = r['transcript_metrics']['tool_sequence']
        for t in seq:
            tool_counts[t] += 1
        for i in range(len(seq) - 1):
            bg = (seq[i], seq[i+1])
            bigrams[bg] += 1
            transitions[seq[i]][seq[i+1]] += 1
        for i in range(len(seq) - 2):
            tg = (seq[i], seq[i+1], seq[i+2])
            trigrams[tg] += 1

    print(f"\n=======================================================")
    print(f"CONFIGURATION: {cfg.upper()}")
    print(f"Total tool invocations: {sum(tool_counts.values())}")
    print(f"=======================================================")
    
    print("\n--- TOP 10 TOOL 2-GRAMS (Transitions) ---")
    tot_bg = sum(bigrams.values())
    for bg, c in bigrams.most_common(10):
        pct = (c / tot_bg) * 100
        print(f"  {bg[0]:20} -> {bg[1]:20} : {c:5d} ({pct:5.2f}%)")

    print("\n--- TOP 10 TOOL 3-GRAMS (Action Loops) ---")
    tot_tg = sum(trigrams.values())
    for tg, c in trigrams.most_common(10):
        pct = (c / tot_tg) * 100
        print(f"  {tg[0]:15} -> {tg[1]:15} -> {tg[2]:15} : {c:5d} ({pct:5.2f}%)")

    print("\n--- CONDITIONAL PROBABILITIES P(Next | Current) ---")
    for curr in ['run_command', 'write_to_file', 'replace_file_content', 'view_file', 'manage_task']:
        if curr in transitions:
            tot_from = sum(transitions[curr].values())
            print(f"  Given {curr} (N={tot_from}):")
            for nxt, c in transitions[curr].most_common(3):
                p = (c / tot_from) * 100
                print(f"    -> {nxt:20}: {p:5.1f}% ({c})")
