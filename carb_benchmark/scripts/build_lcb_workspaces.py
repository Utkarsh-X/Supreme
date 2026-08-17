#!/usr/bin/env python3
"""
build_lcb_workspaces.py — materialize real LiveCodeBench tasks (v5, Jan-Apr 2025).

Each task becomes:
  carb_workspaces/lcb__<question_id>/          (what the agent sees)
      prompt.txt          real problem statement + public samples + I/O instruction
      main.py             empty starter
  carb_benchmark/private/lcb__<question_id>/   (never exposed to the agent)
      evaluation_spec.json      test_command -> shared LCB runner
      private_test_cases.json   hidden I/O pairs (the real grading set)
      public_test_cases.json    public I/O pairs (also embedded in prompt.txt)
      reference_solution.py     written in a later pass; verified against ALL private tests

Selection: 15 AtCoder problems, spread across contests (one per contest where
possible) to avoid same-contest contamination, easy+medium mix, all fresh
(contest_date Jan-Apr 2025 — outside any plausible training corpus cutoff for
the models under test).
"""
import json
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # carb_benchmark/
SUPREME_ROOT = os.path.dirname(BASE)
LCB_JSONL = os.path.join(BASE, "sources", "data", "lcb_v5.jsonl")
WORKSPACES = os.path.join(SUPREME_ROOT, "carb_workspaces")
PRIVATE = os.path.join(BASE, "private")
TARGET_COUNT = 20

# One task per contest, in chronological order, mixing easy/medium.
# question_id -> (difficulty preference)
PREFERRED = [
    "abc387_b",  # easy   9x9 Sum
    "abc388_c",  # medium Various Kagamimochi
    "abc389_d",  # medium Squares in Circle
    "abc390_c",  # medium Paint to make a rectangle
    "abc391_d",  # medium Gravity
    "abc392_b",  # easy   Who is Missing?
    "abc393_b",  # easy   Emptiness
    "abc394_b",  # easy   cat
    "abc395_b",  # easy   Make Target
    "abc396_b",  # easy   Card Pile
    "abc397_c",  # medium Variety Split Easy
    "abc398_b",  # medium Full House 3
    "abc399_b",  # easy   Ranking with Ties
    "abc400_c",  # medium 2^a b^2
    "arc191_a",  # medium ARC (harder contest type for diversity)
    # --- round 2 additions (2026-08-15, distinct contests, difficulty spread) ---
    "arc192_a",  # medium ARC
    "arc194_a",  # medium ARC
    "arc195_a",  # medium ARC
    "arc190_a",  # hard ARC
    "arc193_a",  # hard ARC
]


def load_rows():
    rows = []
    with open(LCB_JSONL, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def decode_cases(raw):
    import base64, zlib, pickle
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str) and raw.lstrip().startswith("["):
        return json.loads(raw)
    return json.loads(pickle.loads(zlib.decompress(base64.b64decode(raw))))


def normalize_content(text):
    # dataset uses \r\n; convert to \n and collapse runs of blank lines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_prompt(question, pub_cases):
    parts = []
    parts.append(normalize_content(question["question_content"]))
    if pub_cases:
        parts.append("\nPublic test cases:\n")
        for i, tc in enumerate(pub_cases, 1):
            parts.append(f"Example {i} input:\n{tc['input'].strip()}\n")
            parts.append(f"Example {i} expected output:\n{tc['output'].strip()}\n")
    parts.append(
        "\n---\n"
        "Write a single Python 3 program in the file main.py that reads the input "
        "from standard input (stdin) and writes the answer to standard output "
        "(stdout). Do not print anything other than the answer. "
        "The solution will be graded against hidden test cases with the same "
        "format as the examples above."
    )
    return "\n".join(parts)


def main():
    rows = load_rows()
    by_id = {r["question_id"]: r for r in rows}

    selected = []
    seen_contests = set()
    for qid in PREFERRED:
        if qid not in by_id:
            print(f"  skip {qid}: not in dataset")
            continue
        r = by_id[qid]
        contest = r["contest_id"]
        if contest in seen_contests:
            print(f"  skip {qid}: duplicate contest {contest}")
            continue
        seen_contests.add(contest)
        selected.append(r)
        if len(selected) == TARGET_COUNT:
            break

    print(f"selected {len(selected)} tasks:")
    for r in selected:
        print(f"  {r['question_id']:12s} {r['difficulty']:7s} {r['contest_date'][:10]} {r['question_title']}")

    os.makedirs(WORKSPACES, exist_ok=True)
    os.makedirs(PRIVATE, exist_ok=True)

    for r in selected:
        task_id = f"lcb__{r['question_id']}"
        ws = os.path.join(WORKSPACES, task_id)
        priv = os.path.join(PRIVATE, task_id)
        shutil.rmtree(ws, ignore_errors=True)
        shutil.rmtree(priv, ignore_errors=True)
        os.makedirs(ws, exist_ok=True)
        os.makedirs(priv, exist_ok=True)

        pub = decode_cases(r["public_test_cases"])
        priv_cases = decode_cases(r["private_test_cases"])

        # workspace (agent-visible)
        prompt = build_prompt(r, pub)
        with open(os.path.join(ws, "prompt.txt"), "w", encoding="utf-8") as f:
            f.write(prompt)
        with open(os.path.join(ws, "main.py"), "w", encoding="utf-8") as f:
            f.write("# Write your solution here. Read from stdin, print the answer to stdout.\n")

        # private (agent-hidden)
        with open(os.path.join(priv, "private_test_cases.json"), "w", encoding="utf-8") as f:
            json.dump(priv_cases, f, indent=1)
        with open(os.path.join(priv, "public_test_cases.json"), "w", encoding="utf-8") as f:
            json.dump(pub, f, indent=1)
        spec = {
            "task_id": task_id,
            "source": "livecodebench_v5",
            "question_id": r["question_id"],
            "question_title": r["question_title"],
            "contest_id": r["contest_id"],
            "contest_date": r["contest_date"],
            "platform": r["platform"],
            "difficulty": r["difficulty"],
            "test_command": "python ../../carb_benchmark/scripts/eval_lcb.py "
                            f"{task_id}",
            "test_timeout_seconds": 300,
            "test_type": "io_exact_match",
            "private_test_count": len(priv_cases),
            "public_test_count": len(pub),
            "expected_files_modified": ["main.py"],
            "max_justified_lines_changed": 400,
        }
        with open(os.path.join(priv, "evaluation_spec.json"), "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2)

    print("\nDone. Workspaces + private dirs created for", len(selected), "tasks.")


if __name__ == "__main__":
    main()
