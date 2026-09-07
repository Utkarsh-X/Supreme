import os
import json
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BENCH_DIR = "carb_benchmark"
RUNS_DIR = os.path.join(BENCH_DIR, "runs_v4")
LEDGER_JSON = os.path.join(BENCH_DIR, "results_v4", "FORENSIC_AUDIT_LEDGER.json")

with open(LEDGER_JSON, "r", encoding="utf-8") as f:
    ledger = json.load(f)

# Track interesting anomalies
verifier_peekers = []
rare_commands = defaultdict(list)
weird_tool_calls = []
close_calls = []
creative_workarounds = []

RARE_TOOLS_OR_CMDS = [
    'objdump', 'readelf', 'strace', 'gdb', 'hexdump', 'xxd', 'ghc', 'ocamlopt', 
    'cobc', 'pmars', 'qemu-system', 'chroot', 'LD_PRELOAD', 'ptrace', 'dmesg',
    'base64 -d', 'sed -i', 'nasm', 'as ', 'gcc -shared', 'eval', 'test.sh'
]

for r in ledger:
    run_id = r["run_id"]
    cfg = r["config_id"]
    tname = r["task_name"]
    st = r["status"]
    trans_path = os.path.join(RUNS_DIR, run_id, "transcript.txt")
    vlog_path = os.path.join(RUNS_DIR, run_id, "verifier_output.log")
    
    # Check verifier log for close calls (e.g. 8/9 tests passed, or 1 failed)
    if os.path.exists(vlog_path):
        try:
            with open(vlog_path, "r", encoding="utf-8", errors="ignore") as vf:
                vtext = vf.read()
                # Check for test summary patterns
                m_tests = re.findall(r'(\d+)\s*(?:passed|failed|errors|of|\/)', vtext.lower())
                vsum = r.get("verifier_summary", {})
                passed = vsum.get("passed_tests")
                failed = vsum.get("failed_tests")
                total = vsum.get("total_tests")
                if total and total > 1 and failed == 1 and st != "SUCCESS":
                    close_calls.append({
                        "run_id": run_id, "cfg": cfg, "task": tname, 
                        "passed": passed, "failed": failed, "total": total
                    })
        except Exception:
            pass

    if not os.path.exists(trans_path):
        continue

    with open(trans_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip() or not line.strip().startswith("{"):
                continue
            try:
                ev = json.loads(line)
                su = ev.get("step_update", {})
                if su.get("step_type") == "tool":
                    tname_tool = su.get("tool_name")
                    params = su.get("tool_info", {}).get("parameters", {})
                    
                    # Check for unknown / hallucinated tools
                    KNOWN_TOOLS = {
                        "run_command", "view_file", "write_to_file", "replace_file_content",
                        "list_dir", "grep_search", "find_by_name", "manage_task",
                        "schedule", "send_message", "read_url_content", "search_web",
                        "generate_image", "notebook_edit", "manage_subagents"
                    }
                    if tname_tool not in KNOWN_TOOLS:
                        weird_tool_calls.append({
                            "run_id": run_id, "cfg": cfg, "task": tname,
                            "tool_name": tname_tool, "params": params
                        })

                    if tname_tool == "run_command":
                        cmd = params.get("CommandLine", "")
                        
                        # Verifier inspection check
                        if "test.sh" in cmd or "test_outputs" in cmd or "eval" in cmd:
                            if any(x in cmd for x in ["cat ", "less ", "view ", "head ", "grep ", "find "]):
                                verifier_peekers.append({
                                    "run_id": run_id, "cfg": cfg, "task": tname,
                                    "cmd": cmd
                                })
                        
                        # Rare commands check
                        for rc in RARE_TOOLS_OR_CMDS:
                            if rc in cmd:
                                rare_commands[rc].append({
                                    "run_id": run_id, "cfg": cfg, "task": tname,
                                    "cmd": cmd[:100]
                                })
                                
                        # Creative workarounds
                        if any(k in cmd for k in ["apt-get install", "pip install", "patch ", "LD_PRELOAD", "compile", "make install", "git clone"]):
                            if any(k2 in cmd for k2 in ["source", "build", "tar -x", "make -j"]):
                                creative_workarounds.append({
                                    "run_id": run_id, "cfg": cfg, "task": tname,
                                    "cmd": cmd[:120]
                                })
            except Exception:
                pass

print("=== FORENSIC ANOMALIES & EASTER EGGS ===")
print(f"\n1. Hallucinated / Unknown Tool Calls: {len(weird_tool_calls)}")
for wt in weird_tool_calls[:5]:
    print(f"   {wt['cfg']} on {wt['task']}: tool='{wt['tool_name']}'")

print(f"\n2. Verifier Peeking / Reverse Engineering Attempts: {len(verifier_peekers)}")
for vp in verifier_peekers[:10]:
    print(f"   {vp['cfg']:16} | {vp['task']:25} | Cmd: {vp['cmd'][:80]}")

print(f"\n3. Rare / Advanced Terminal Commands Usage:")
for rc, instances in rare_commands.items():
    cfgs = Counter(x['cfg'] for x in instances)
    print(f"   '{rc:15}': Total={len(instances):3d} | By config: {dict(cfgs)}")

print(f"\n4. Heartbreaking Close Calls (Failed by exactly 1 test): {len(close_calls)}")
for cc in close_calls[:10]:
    print(f"   {cc['cfg']:16} | {cc['task']:25} | Passed: {cc['passed']}/{cc['total']} (Failed 1!)")

print(f"\n5. Complex Creative Workarounds (Compilation/Patches/Builds): {len(creative_workarounds)}")
for cw in creative_workarounds[:8]:
    print(f"   {cw['cfg']:16} | {cw['task']:25} | Cmd: {cw['cmd']}")
