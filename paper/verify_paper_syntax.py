#!/usr/bin/env python3
"""
verify_paper_syntax.py — Validates LaTeX syntax, figure paths, and citation keys for paper/
"""

import os
import re

PAPER_DIR = "paper"
SECTIONS_DIR = os.path.join(PAPER_DIR, "sections")
BIB_FILE = os.path.join(PAPER_DIR, "references.bib")

def verify():
    errors = []
    warnings = []

    # 1. Load BibTeX keys
    bib_keys = set()
    if os.path.exists(BIB_FILE):
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r'@\w+\s*\{\s*([^,]+),', content)
            bib_keys = set(m.strip() for m in matches)
        print(f"Loaded {len(bib_keys)} BibTeX keys: {sorted(bib_keys)}")
    else:
        errors.append(f"Missing {BIB_FILE}")

    # 2. Check all .tex files
    tex_files = [os.path.join(PAPER_DIR, "main.tex")]
    if os.path.exists(SECTIONS_DIR):
        for f in sorted(os.listdir(SECTIONS_DIR)):
            if f.endswith(".tex"):
                tex_files.append(os.path.join(SECTIONS_DIR, f))

    all_labels = set()
    all_refs = set()
    all_cites = set()
    all_figs = set()

    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            text = f.read()

        # Check environment balance
        begins = re.findall(r'\\begin\{([^}]+)\}', text)
        ends = re.findall(r'\\end\{([^}]+)\}', text)
        if begins != ends:
            # Check stack
            stack = []
            for token in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
                action, env = token
                if action == "begin":
                    stack.append(env)
                elif action == "end":
                    if stack and stack[-1] == env:
                        stack.pop()
                    else:
                        errors.append(f"Mismatched \\end{{{env}}} in {tf}")
            if stack:
                errors.append(f"Unclosed environments in {tf}: {stack}")

        # Extract labels, refs, cites, figs
        for l in re.findall(r'\\label\{([^}]+)\}', text):
            all_labels.add(l)
        for r in re.findall(r'\\ref\{([^}]+)\}', text):
            all_refs.add(r)
        for c in re.findall(r'\\cite\{([^}]+)\}', text):
            for single_c in c.split(","):
                all_cites.add(single_c.strip())
        for fig in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text):
            all_figs.add(fig)

    print(f"Verified {len(tex_files)} .tex files.")
    print(f"Total Labels: {len(all_labels)} | Total Refs: {len(all_refs)}")
    print(f"Total Citations: {len(all_cites)}")
    print(f"Total Figures Referenced: {len(all_figs)}")

    # Check dangling refs
    dangling_refs = all_refs - all_labels
    if dangling_refs:
        errors.append(f"Dangling \\ref targets (no matching \\label): {dangling_refs}")

    # Check dangling cites
    dangling_cites = all_cites - bib_keys
    if dangling_cites:
        errors.append(f"Dangling \\cite keys (not in references.bib): {dangling_cites}")

    # Check figures exist
    for fig_path in all_figs:
        full_fig = os.path.join(PAPER_DIR, fig_path)
        if not os.path.exists(full_fig):
            errors.append(f"Referenced figure not found on disk: {full_fig}")

    if errors:
        print("\n[FAIL] VALIDATION FAILED WITH ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\n[SUCCESS] VALIDATION PASSED: 100% Syntax Closure, Zero Dangling Refs/Cites, All Figures Exist!")
        return True


if __name__ == "__main__":
    verify()
