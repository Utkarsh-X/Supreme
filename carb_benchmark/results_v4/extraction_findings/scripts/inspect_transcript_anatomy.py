import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('carb_benchmark/runs_v4/2026-08-22-025802-adaptive-rejection-sampler-supreme-v2.0/transcript.txt', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if i > 25:
            break
        ev = json.loads(line)
        evt = ev.get("event")
        su = ev.get("step_update", {})
        stype = su.get("step_type")
        state = su.get("state")
        keys = list(su.keys())
        print(f"Line {i:2d}: event={evt} | type={stype} | state={state} | keys={keys}")
        if stype == 'agent_response' and state == 'DONE':
            print("   Agent response sample:", str(su)[:200])
        elif stype == 'tool' and state == 'ACTIVE':
            print("   Tool active sample:", str(su)[:200])
        elif stype == 'tool' and state == 'DONE':
            print("   Tool done sample:", str(su)[:200])
