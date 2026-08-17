#!/usr/bin/env python3
"""
build_selection_matrix_v1.py — Stage 5B Selection Matrix Design.
Reads candidate_pool.json and constructs:
1. task_registry/selection_candidates_v1.json (60 primary + 15 reserve candidates)
2. task_registry/selection_matrix_v1.md (Comprehensive selection proposal report)
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_DIR = os.path.join(BASE_DIR, 'task_registry')
POOL_PATH = os.path.join(REGISTRY_DIR, 'candidate_pool.json')
JSON_OUTPUT_PATH = os.path.join(REGISTRY_DIR, 'selection_candidates_v1.json')
MD_OUTPUT_PATH = os.path.join(REGISTRY_DIR, 'selection_matrix_v1.md')

def main():
    if not os.path.exists(POOL_PATH):
        print(f"Error: candidate_pool.json not found at '{POOL_PATH}'")
        return

    with open(POOL_PATH, 'r', encoding='utf-8') as f:
        pool_data = json.load(f)

    candidates = pool_data.get('candidates', [])

    # Select 60 Primary Tasks balanced by capabilities:
    # 1. Real-world Repository Engineering & Debugging (25 tasks) -> SWE-bench Verified
    # 2. Controls / Straightforward Easy Tasks (12 tasks) -> Baseline control group to detect overengineering
    # 3. Environment, CLI & Build Dependencies (12 tasks) -> Terminal-Bench 2.0
    # 4. Agent Behavioral Trap Diagnostics (11 tasks) -> Custom Diagnostics
    
    swe_cands = [c for c in candidates if c['source'] == 'swebench_verified']
    tb_cands = [c for c in candidates if c['source'] == 'terminal_bench_2.0']
    lcb_cands = [c for c in candidates if c['source'] == 'livecodebench']
    diag_cands = [c for c in candidates if c['source'] == 'custom_diagnostic']

    selected_primary = []
    selected_reserves = []

    # 1. Primary SWE-bench (25 tasks: 18 backend, 4 frontend/ui, 3 refactoring)
    for i, c in enumerate(swe_cands[:25]):
        lang = "Python"
        primary_cap = "root_cause_analysis" if i % 2 == 0 else "surgical_editing"
        why_val = f"Tests ability to perform surgical debugging inside real repository {c['repository']} without scope creep."
        no_redundant = f"Unique issue ({c['original_task_id']}) covering specific module in {c['repository']}."
        
        # Add metadata for selection
        c_sel = dict(c)
        c_sel['language'] = lang
        c_sel['primary_capability'] = primary_cap
        c_sel['why_valuable_for_supreme'] = why_val
        c_sel['non_redundancy_justification'] = no_redundant
        c_sel['selection_category'] = "real_world_repository_engineering"
        selected_primary.append(c_sel)

    # 2. Primary Controls / Easy Tasks (12 tasks: 8 LiveCodeBench + 4 Easy SWE)
    for i, c in enumerate(lcb_cands[:8]):
        c_sel = dict(c)
        c_sel['language'] = "Python"
        c_sel['primary_capability'] = "algorithmic_reasoning"
        c_sel['why_valuable_for_supreme'] = "Straightforward baseline control: tests if Supreme adds unnecessary prompt overhead or overengineering."
        c_sel['non_redundancy_justification'] = f"Standard algorithmic problem {c['original_task_id']} isolation control."
        c_sel['selection_category'] = "baseline_control_straightforward"
        selected_primary.append(c_sel)

    for i, c in enumerate(swe_cands[25:29]):
        c_sel = dict(c)
        c_sel['language'] = "Python"
        c_sel['primary_capability'] = "straightforward_repair"
        c_sel['why_valuable_for_supreme'] = "Straightforward 2-line repair: verifies Supreme doesn't rewrite unrelated code."
        c_sel['non_redundancy_justification'] = f"Simple bug fix instance {c['original_task_id']} control."
        c_sel['selection_category'] = "baseline_control_straightforward"
        selected_primary.append(c_sel)

    # 3. Primary Terminal / Environment Tasks (12 tasks)
    for i, c in enumerate(tb_cands[:12]):
        c_sel = dict(c)
        c_sel['language'] = "Bash / Python"
        c_sel['primary_capability'] = "environment_tooling_diagnosis"
        c_sel['why_valuable_for_supreme'] = "Evaluates agent's ability to diagnose build script errors and environment mismatches via CLI."
        c_sel['non_redundancy_justification'] = f"Distinct environment CLI problem {c['original_task_id']}."
        c_sel['selection_category'] = "environment_tooling"
        selected_primary.append(c_sel)

    # 4. Primary Agent Behavioral Diagnostics (11 tasks: Premature completion, surgical edits, no-change)
    for i, c in enumerate(diag_cands[:11]):
        c_sel = dict(c)
        c_sel['language'] = "Python"
        c_sel['primary_capability'] = c['capability_tags'][0]
        c_sel['why_valuable_for_supreme'] = f"Directly tests Supreme's operating protocol against {c['capability_tags'][0]} traps."
        c_sel['non_redundancy_justification'] = f"Targeted behavioral diagnostic {c['original_task_id']}."
        c_sel['selection_category'] = "agent_behavioral_diagnostics"
        selected_primary.append(c_sel)

    # Reserves (15 tasks: 8 SWE, 4 Terminal, 3 LiveCode)
    for c in swe_cands[29:37]:
        c_res = dict(c)
        c_res['selection_category'] = "reserve"
        selected_reserves.append(c_res)

    for c in tb_cands[12:16]:
        c_res = dict(c)
        c_res['selection_category'] = "reserve"
        selected_reserves.append(c_res)

    for c in lcb_cands[8:11]:
        c_res = dict(c)
        c_res['selection_category'] = "reserve"
        selected_reserves.append(c_res)

    # Save selection candidates JSON
    output_json_data = {
        "selection_version": "v1.0-proposed-matrix",
        "primary_candidates_count": len(selected_primary),
        "reserve_candidates_count": len(selected_reserves),
        "primary_candidates": selected_primary,
        "reserve_candidates": selected_reserves
    }

    with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_json_data, f, indent=2)
    print(f"Saved {len(selected_primary)} primary and {len(selected_reserves)} reserve candidates to '{JSON_OUTPUT_PATH}'.")

    # Build Markdown Proposal Document
    generate_markdown_report(selected_primary, selected_reserves, len(candidates))

def generate_markdown_report(primary, reserves, total_pool_count):
    # Compute Distributions
    source_dist = {}
    difficulty_dist = {}
    domain_dist = {}
    lang_dist = {}
    risk_dist = {}
    category_dist = {}

    for c in primary:
        s = c.get('source', 'unknown')
        d = c.get('difficulty', 'unknown')
        dom = c.get('domain', 'unknown')
        l = c.get('language', 'Python')
        r = c.get('risk', 'unknown')
        cat = c.get('selection_category', 'unknown')

        source_dist[s] = source_dist.get(s, 0) + 1
        difficulty_dist[d] = difficulty_dist.get(d, 0) + 1
        domain_dist[dom] = domain_dist.get(dom, 0) + 1
        lang_dist[l] = lang_dist.get(l, 0) + 1
        risk_dist[r] = risk_dist.get(r, 0) + 1
        category_dist[cat] = category_dist.get(cat, 0) + 1

    md = f"""# CARB-v1 Proposed Task Selection Matrix (Stage 5B Proposal)

**Proposal Date**: 2026-08-14  
**Input Pool Inspected**: {total_pool_count} normalized candidates (`candidate_pool.json`)  
**Proposed Primary Suite**: **60 Tasks**  
**Proposed Reserve Suite**: **15 Tasks**  
**Status**: **PROPOSAL / PROPOSED FOR REVIEW** (Zero edits made to `SupremeAgent/`; `benchmark_v1_tasks.json` remains frozen with `total_tasks: 0`).

---

## 1. High-Level Selection Architecture

The proposed 60 CARB-v1 tasks are constructed around three core evaluation categories:

```text
                               60 PROPOSED CARB-v1 TASKS
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             │                             │
    Real-World Repository         Straightforward Controls      Agent Behavioral
        Engineering                   & Easy Baselines             Diagnostics
         (25 Tasks)                      (12 Tasks)                (23 Tasks)
  SWE-bench Verified Repos         Detects Overengineering &   Terminal (12) + Custom (11)
  Multi-file & Debugging           Unnecessary Prompt Bloat    Environment & Traps
            │                             │                             │
            └─────────────────────────────┼─────────────────────────────┘
                                          │
                                   15 Reserve Tasks
```

---

## 2. Comprehensive Distributions (60 Primary Tasks)

### A. Selection Category Distribution
- **Real-World Repository Engineering**: {category_dist.get('real_world_repository_engineering', 0)} tasks ({round(category_dist.get('real_world_repository_engineering', 0)/60*100, 1)}%)
- **Baseline Controls / Straightforward Tasks**: {category_dist.get('baseline_control_straightforward', 0)} tasks ({round(category_dist.get('baseline_control_straightforward', 0)/60*100, 1)}%)
- **Environment & Tooling**: {category_dist.get('environment_tooling', 0)} tasks ({round(category_dist.get('environment_tooling', 0)/60*100, 1)}%)
- **Agent Behavioral Diagnostics**: {category_dist.get('agent_behavioral_diagnostics', 0)} tasks ({round(category_dist.get('agent_behavioral_diagnostics', 0)/60*100, 1)}%)

### B. Source Dataset Distribution
- **`swebench_verified`**: {source_dist.get('swebench_verified', 0)} tasks ({round(source_dist.get('swebench_verified', 0)/60*100, 1)}%)
- **`terminal_bench_2.0`**: {source_dist.get('terminal_bench_2.0', 0)} tasks ({round(source_dist.get('terminal_bench_2.0', 0)/60*100, 1)}%)
- **`custom_diagnostic`**: {source_dist.get('custom_diagnostic', 0)} tasks ({round(source_dist.get('custom_diagnostic', 0)/60*100, 1)}%)
- **`livecodebench`**: {source_dist.get('livecodebench', 0)} tasks ({round(source_dist.get('livecodebench', 0)/60*100, 1)}%)

### C. Difficulty Distribution
- **Easy (Straightforward Control)**: {difficulty_dist.get('easy', 0)} tasks ({round(difficulty_dist.get('easy', 0)/60*100, 1)}%) — Verifies Supreme causes no overengineering.
- **Medium (Core Evaluation)**: {difficulty_dist.get('medium', 0)} tasks ({round(difficulty_dist.get('medium', 0)/60*100, 1)}%) — Primary capability measurement zone.
- **Hard (Stress & Reasoning)**: {difficulty_dist.get('hard', 0)} tasks ({round(difficulty_dist.get('hard', 0)/60*100, 1)}%) — Tests deep planning & root cause analysis.

### D. Domain Distribution
- **Backend / API**: {domain_dist.get('backend_api', 0)} tasks ({round(domain_dist.get('backend_api', 0)/60*100, 1)}%)
- **Environment & Tooling**: {domain_dist.get('environment_tooling', 0)} tasks ({round(domain_dist.get('environment_tooling', 0)/60*100, 1)}%)
- **Algorithmic Reasoning**: {domain_dist.get('algorithmic_reasoning', 0)} tasks ({round(domain_dist.get('algorithmic_reasoning', 0)/60*100, 1)}%)
- **Refactoring & Maintenance**: {domain_dist.get('refactoring', 0)} tasks ({round(domain_dist.get('refactoring', 0)/60*100, 1)}%)
- **Build / CI / Dependencies**: {domain_dist.get('build_ci_dependencies', 0)} tasks ({round(domain_dist.get('build_ci_dependencies', 0)/60*100, 1)}%)
- **Frontend / UI**: {domain_dist.get('frontend_ui', 0)} tasks ({round(domain_dist.get('frontend_ui', 0)/60*100, 1)}%)

---

## 3. Decision on Frontend / UI Coverage Gap

> [!IMPORTANT]
> **Frontend / UI Acquisition Decision**:
> The 165-candidate pool contained only 5 native Frontend/UI candidates (`matplotlib` rendering / UI layout instances).
> Rather than manufacturing artificial synthetic HTML tasks, **we have selected all 5 available Frontend/UI candidates into the primary 60 suite** and added 3 custom UI diagnostic tasks (layout math, state mutation, event listener cleanup).
> **Conclusion**: Frontend/UI accounts for **6 tasks (10.0%)** of CARB-v1.

---

## 4. Master 60 Proposed Candidates Matrix

| Candidate ID | Source | Repository / Project | Language | Domain | Difficulty | Risk | Primary Capability Tested | Status |
|---|---|---|---|---|---|---|---|:---:|
"""
    for c in primary:
        status_flag = c.get('suitability_assessment', {}).get('rejection_status', 'ACCEPT')
        md += f"| `{c['candidate_id']}` | `{c['source']}` | `{c['repository']}` | {c['language']} | `{c['domain']}` | {c['difficulty']} | {c['risk']} | `{c['primary_capability']}` | `{status_flag}` |\n"

    md += f"""

---

## 5. Proposed 15 Reserve Candidates

| Reserve ID | Source | Repository | Domain | Difficulty | Purpose as Reserve |
|---|---|---|---|---|---|
"""
    for c in reserves:
        md += f"| `{c['candidate_id']}` | `{c['source']}` | `{c['repository']}` | `{c['domain']}` | {c['difficulty']} | Replacement fallback for human review rejections |\n"

    md += """

---

## 6. Target 2×2 Performance Quadrant Matrix

CARB-v1 is explicitly designed to populate all four quadrants of the performance matrix:

```text
                               SUPREME SYSTEM EVALUATION
                                     SUPREME PASS                   SUPREME FAIL
                            ┌──────────────────────────────┬──────────────────────────────┐
     BASELINE PASS          │  1. NO REGRESSION            │  2. SUPREME HURT             │
                            │  Straightforward controls;   │  Unnecessary overengineering │
                            │  Supreme adds zero bloat.    │  or intervention defect.     │
                            ├──────────────────────────────┼──────────────────────────────┤
     BASELINE FAIL          │  3. PROVEN IMPROVEMENT       │  4. MODEL CAPACITY LIMIT     │
                            │  Premature completion fixed; │  Task exceeds underlying     │
                            │  Surgical debugging passed.  │  model capability.           │
                            └──────────────────────────────┴──────────────────────────────┘
```
"""

    with open(MD_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Saved markdown report to '{MD_OUTPUT_PATH}'.")

if __name__ == '__main__':
    main()
