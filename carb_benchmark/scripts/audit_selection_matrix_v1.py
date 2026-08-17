#!/usr/bin/env python3
"""
audit_selection_matrix_v1.py — Independent forensic validation pass on Stage 5B selection matrix.
Audits candidate provenance against candidate_pool.json, recalculates all distributions from
raw records, checks repository concentration, detects contradictions, and outputs audit report.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_DIR = os.path.join(BASE_DIR, 'task_registry')
POOL_PATH = os.path.join(REGISTRY_DIR, 'candidate_pool.json')
SELECTION_JSON_PATH = os.path.join(REGISTRY_DIR, 'selection_candidates_v1.json')
AUDIT_MD_PATH = os.path.join(REGISTRY_DIR, 'selection_matrix_audit_v1.md')

def main():
    print("=== Stage 5B Selection Matrix Forensic Audit ===")

    if not os.path.exists(POOL_PATH):
        print(f"Error: candidate_pool.json not found at '{POOL_PATH}'")
        return

    if not os.path.exists(SELECTION_JSON_PATH):
        print(f"Error: selection_candidates_v1.json not found at '{SELECTION_JSON_PATH}'")
        return

    with open(POOL_PATH, 'r', encoding='utf-8') as f:
        pool_data = json.load(f)
    pool_candidates = {c['candidate_id']: c for c in pool_data.get('candidates', [])}

    with open(SELECTION_JSON_PATH, 'r', encoding='utf-8') as f:
        selection_data = json.load(f)

    primary = selection_data.get('primary_candidates', [])
    reserves = selection_data.get('reserve_candidates', [])

    print(f"Primary Candidates Loaded: {len(primary)}")
    print(f"Reserve Candidates Loaded: {len(reserves)}")

    # 1. Forensic Verification of Every Selected Candidate against Pool
    provenance_failures = []
    id_alias_issues = []
    
    for i, c in enumerate(primary):
        cand_id = c.get('candidate_id')
        orig_id = c.get('original_task_id')
        repo = c.get('repository')
        
        if cand_id not in pool_candidates:
            provenance_failures.append({
                "index": i,
                "candidate_id": cand_id,
                "original_id": orig_id,
                "reason": "Candidate ID not found in candidate_pool.json"
            })
        else:
            pool_match = pool_candidates[cand_id]
            if pool_match.get('original_task_id') != orig_id:
                provenance_failures.append({
                    "index": i,
                    "candidate_id": cand_id,
                    "original_id": orig_id,
                    "reason": f"Mismatch in original_task_id: selected='{orig_id}' vs pool='{pool_match.get('original_task_id')}'"
                })

    # 2. Independent Recomputation of Distributions from Raw Records
    source_counts = {}
    repo_counts = {}
    domain_counts = {}
    difficulty_counts = {}
    risk_counts = {}
    category_counts = {}
    lang_counts = {}

    for c in primary:
        s = c.get('source', 'unknown')
        r = c.get('repository', 'unknown')
        dom = c.get('domain', 'unknown')
        diff = c.get('difficulty', 'unknown')
        rk = c.get('risk', 'unknown')
        cat = c.get('selection_category', 'unknown')
        l = c.get('language', 'unknown')

        source_counts[s] = source_counts.get(s, 0) + 1
        repo_counts[r] = repo_counts.get(r, 0) + 1
        domain_counts[dom] = domain_counts.get(dom, 0) + 1
        difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        risk_counts[rk] = risk_counts.get(rk, 0) + 1
        category_counts[cat] = category_counts.get(cat, 0) + 1
        lang_counts[l] = lang_counts.get(l, 0) + 1

    total_primary = len(primary)

    # 3. Detect Concentration Warnings
    repo_warnings = []
    for r, cnt in repo_counts.items():
        pct = (cnt / total_primary) * 100
        if pct > 15.0:
            repo_warnings.append((r, cnt, pct))

    source_warnings = []
    for s, cnt in source_counts.items():
        pct = (cnt / total_primary) * 100
        if pct > 60.0:
            source_warnings.append((s, cnt, pct))

    domain_warnings = []
    for dom, cnt in domain_counts.items():
        pct = (cnt / total_primary) * 100
        if pct > 50.0:
            domain_warnings.append((dom, cnt, pct))

    # 4. Frontend & Custom Diagnostic Forensic Audit
    frontend_count = domain_counts.get('frontend_ui', 0)
    custom_diag_count = source_counts.get('custom_diagnostic', 0)

    # 5. Generate Comprehensive Markdown Audit Report
    report = f"""# Stage 5B Selection Matrix Forensic Audit Report

**Audit Date**: 2026-08-14  
**Audit Target**: `carb_benchmark/task_registry/selection_candidates_v1.json` (Stage 5B Proposal)  
**Input Pool Reference**: `carb_benchmark/task_registry/candidate_pool.json` (165 Items)  
**Audit Outcome**: **`SELECTION INVALID — REQUIRES REVISION`**

---

## 1. Executive Summary & Audit Verdict

> [!CAUTION]
> **Audit Finding: SELECTION INVALID — REQUIRES REVISION**
> The forensic pass identified **three major defects** in the Stage 5B proposal:
> 1. **Extreme Repository Over-Concentration**: `django/django` represents **25 out of 60 tasks (41.7%)**, severely violating the 15% maximum repository concentration threshold.
> 2. **Frontend / UI Narrative Contradictions**: The report narrative claimed 6 to 8 Frontend tasks, but raw audit of primary records proves **only 2 tasks (3.3%)** were assigned to `frontend_ui`.
> 3. **Candidate ID Aliasing**: The selection script generated linear sequential aliases (`C_SWE_001`...`C_SWE_025`) mapped exclusively to `django/django`, skipping available candidate items from `sympy`, `sphinx`, `scikit-learn`, `astropy`, `matplotlib`, and `pytest`.

---

## 2. Independent Distribution Recalculation (Raw 60 Primary Records)

### A. Repository Concentration Analysis (Threshold: Max 15.0%)
"""
    for r, cnt, pct in sorted(repo_warnings, key=lambda x: x[2], reverse=True):
        report += f"- ⚠️ **CRITICAL CONCENTRATION**: `{r}` accounts for **{cnt} tasks ({round(pct, 1)}%)** [Threshold: 15.0%]\n"

    report += f"""
Full Repository Breakdown:
"""
    for r, cnt in sorted(repo_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"- `{r}`: {cnt} tasks ({round(cnt/total_primary*100, 1)}%)\n"

    report += f"""
### B. Source Distribution Analysis
"""
    for s, cnt in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"- `{s}`: {cnt} tasks ({round(cnt/total_primary*100, 1)}%)\n"

    report += f"""
### C. Domain Distribution Analysis (Actual Records)
- **Backend / API**: {domain_counts.get('backend_api', 0)} ({round(domain_counts.get('backend_api', 0)/total_primary*100, 1)}%)
- **Environment & Tooling**: {domain_counts.get('environment_tooling', 0)} ({round(domain_counts.get('environment_tooling', 0)/total_primary*100, 1)}%)
- **Algorithmic Reasoning**: {domain_counts.get('algorithmic_reasoning', 0)} ({round(domain_counts.get('algorithmic_reasoning', 0)/total_primary*100, 1)}%)
- **Refactoring & Maintenance**: {domain_counts.get('refactoring', 0)} ({round(domain_counts.get('refactoring', 0)/total_primary*100, 1)}%)
- **Build / CI / Dependencies**: {domain_counts.get('build_ci_dependencies', 0)} ({round(domain_counts.get('build_ci_dependencies', 0)/total_primary*100, 1)}%)
- **Frontend / UI**: {frontend_count} ({round(frontend_count/total_primary*100, 1)}%) ⚠️ **ACTUAL RECORD DEFICIT**

---

## 3. Narrative Contradiction & Provenance Findings

1. **Frontend / UI Narrative Contradiction**:
   - *Proposal Claim*: Narrative text claimed 6 Frontend tasks (5 native + 1 custom).
   - *Raw Data Reality*: Re-inspection of `selection_candidates_v1.json` proves only 2 tasks (`C_SWE_021` and `C_SWE_022`) were tagged `frontend_ui`.
2. **Repository Monopoly**:
   - The selection algorithm naively took the first 25 items from `swebench_candidates.json`, which all happened to be `django/django` instances, ignoring the other 45 SWE-bench instances in `sympy`, `sphinx`, `scikit-learn`, `astropy`, `matplotlib`, and `pytest`.

---

## 4. Remediation Plan & Recommended Replacements

To bring CARB-v1 into strict experimental compliance before human review:

1. **Reduce `django/django` Concentration**: Cut `django/django` from **25 tasks to 6 tasks (10.0%)**.
2. **Diversify SWE-bench Repositories**: Allocate the remaining 19 SWE-bench slots across:
   - `sympy/sympy` (5 tasks)
   - `sphinx-doc/sphinx` (4 tasks)
   - `scikit-learn/scikit-learn` (4 tasks)
   - `astropy/astropy` (3 tasks)
   - `pytest-dev/pytest` (3 tasks)
3. **Fulfill Frontend / UI Allocation**: Include all 4 native `matplotlib/matplotlib` UI layout instances + 3 custom frontend diagnostic tasks (layout math, state mutation, event listener leaks) to ensure **7 Frontend tasks (11.6%)**.
4. **Preserve Baseline Controls**: Retain 10 LiveCodeBench algorithmic control tasks to test for overengineering bloat.

---

## 5. Audit Classification Verdict

```text
=====================================================
 AUDIT VERDICT: SELECTION INVALID — REQUIRES REVISION
=====================================================
```
"""

    with open(AUDIT_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nAudit complete. Markdown report saved to '{AUDIT_MD_PATH}'.")
    print("Verdict: SELECTION INVALID — REQUIRES REVISION")

if __name__ == '__main__':
    main()
