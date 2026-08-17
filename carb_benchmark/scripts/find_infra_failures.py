#!/usr/bin/env python3
"""find_infra_failures.py — list runs that failed for infrastructure reasons.

An INFRA failure = status FAILURE AND (transcript contains agy's internal
'timeout waiting for response' OR our 'AGY EXECUTION TIMED OUT') AND the final
diff is empty (the agent did no work before the API timed out).

These runs get deleted and re-run after the main driver completes.
"""
import glob
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(BASE, "runs")

INFRA_TAILS = ("timeout waiting for response", "AGY EXECUTION TIMED OUT")


def main():
    infra = []
    kept_failures = []
    for d in sorted(glob.glob(os.path.join(RUNS, "*v2.0"))):
        mp = os.path.join(d, "run_manifest.yaml")
        if not os.path.exists(mp):
            continue
        txt = open(mp, encoding="utf-8", errors="replace").read()
        status = None
        for line in txt.splitlines():
            if line.strip().startswith("status:"):
                status = line.split(":", 1)[1].strip()
                break
        if status != "FAILURE":
            continue
        tr = os.path.join(d, "transcript.txt")
        tail = ""
        if os.path.exists(tr):
            tail = open(tr, encoding="utf-8", errors="replace").read()[-200:].strip()
        diff = os.path.join(d, "final_diff.patch")
        diff_size = os.path.getsize(diff) if os.path.exists(diff) else 0
        rec = {"dir": os.path.basename(d), "transcript_tail": tail,
               "diff_bytes": diff_size}
        if any(k in tail for k in INFRA_TAILS) and diff_size == 0:
            infra.append(rec)
        else:
            kept_failures.append(rec)

    print("### INFRA FAILURES (re-run after driver completes):")
    for r in infra:
        print(f"- {r['dir']} | {r['transcript_tail'][:60]}")
    print("\n### Other failures (need manual review):")
    for r in kept_failures:
        print(f"- {r['dir']} | diff={r['diff_bytes']}B | {r['transcript_tail'][:60]}")

    json.dump({"infra": infra, "other": kept_failures},
              open(os.path.join(BASE, "results", "infra_failures.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
