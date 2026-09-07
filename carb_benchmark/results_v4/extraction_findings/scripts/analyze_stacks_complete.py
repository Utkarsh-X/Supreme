import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('carb_benchmark/results_v4/extraction_findings/all_89_tasks_annotated.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

STACK_MAPPING = {
    # 1. Systems & Low-Level Languages: C, C++, Assembly, MIPS, Redcode, OCaml, Rust
    'Systems & Low-Level (C, C++, Asm, Rust, OCaml)': [
        'build-pmars', 'build-pov-ray', 'caffe-cifar-10', 'circuit-fibsqrt',
        'compile-compcert', 'custom-memory-heap-crash', 'extract-elf',
        'feal-linear-cryptanalysis', 'fix-ocaml-gc', 'gpt2-codegolf',
        'make-doom-for-mips', 'make-mips-interpreter', 'path-tracing',
        'path-tracing-reverse', 'polyglot-c-py', 'polyglot-rust-c',
        'sqlite-db-truncate', 'sqlite-with-gcov', 'winning-avg-corewars',
        'write-compressor'
    ],
    # 2. Esoteric & Symbolic: Scheme, R, COBOL, LaTeX, SPARQL, Stan, Formal Logic
    'Esoteric & Symbolic (Scheme, R, COBOL, Stan, LaTeX, SPARQL)': [
        'adaptive-rejection-sampler', 'bn-fit-modify', 'cobol-modernization',
        'feal-differential-cryptanalysis', 'gcode-to-text', 'largest-eigenval',
        'mcmc-sampling-stan', 'overfull-hbox', 'portfolio-optimization',
        'prove-plus-comm', 'raman-fitting', 'rstan-to-pystan',
        'schemelike-metacircular-eval', 'sparql-university'
    ],
    # 3. Systems Administration, OS, Networking & DevOps: Linux, QEMU, Nginx, Git, SSH, OpenSSL
    'SysAdmin, OS & DevOps (Linux, Git, QEMU, Nginx, SSH, SSL)': [
        'configure-git-webserver', 'db-wal-recovery', 'fix-git', 'git-leak-recovery',
        'git-multibranch', 'install-windows-3.11', 'kv-store-grpc',
        'nginx-request-logging', 'openssl-selfsigned-cert', 'password-recovery',
        'pypi-server', 'qemu-alpine-ssh', 'qemu-startup', 'sanitize-git-repo',
        'vulnerable-secret'
    ],
    # 4. ML, Deep Learning & Robotics: PyTorch, HuggingFace, MuJoCo, Embeddings
    'ML, Deep Learning & Robotics (PyTorch, HF, MuJoCo)': [
        'count-dataset-tokens', 'distribution-search', 'hf-model-inference',
        'llm-inference-batching-scheduler', 'model-extraction-relu-logits',
        'mteb-leaderboard', 'mteb-retrieve', 'mujoco-physics',
        'pytorch-model-cli', 'pytorch-model-recovery', 'sam-cell-seg',
        'torch-pipeline-parallelism', 'torch-tensor-parallelism', 'train-fasttext',
        'tune-mjcf'
    ],
    # 5. Core Software Engineering, Python & Data Pipeline
    'Software Engineering & Data Processing (Python, DB, Vim)': [
        'break-filter-js-from-html', 'build-cython-ext', 'cancel-async-tasks',
        'chess-best-move', 'code-from-image', 'constraints-scheduling',
        'crack-7z-hash', 'dna-assembly', 'dna-insert', 'extract-moves-from-video',
        'filter-js-from-html', 'financial-document-processor', 'fix-code-vulnerability',
        'headless-terminal', 'large-scale-text-editing', 'log-summary-date-ranges',
        'mailman', 'merge-diff-arc-agi-task', 'modernize-scientific-stack',
        'multi-source-data-merger', 'protein-assembly', 'query-optimize',
        'regex-chess', 'regex-log', 'reshard-c4-data', 'video-processing'
    ]
}

# Verify coverage of all 89 tasks
all_assigned = []
for k, v in STACK_MAPPING.items():
    all_assigned.extend(v)
all_task_names = set(t['name'] for t in tasks)
missing = all_task_names - set(all_assigned)
extra = set(all_assigned) - all_task_names
print(f"Total tasks mapped: {len(all_assigned)} / {len(all_task_names)} (Missing: {len(missing)}, Extra: {len(extra)})")

print("\n=== COMPREHENSIVE 89-TASK PERFORMANCE BY TECHNICAL STACK ===")
for stack, task_list in STACK_MAPPING.items():
    tot = len(task_list)
    sup_wins = sum(1 for t in tasks if t['name'] in task_list and t['results'].get('supreme-v2.0') == 'SUCCESS')
    obra_wins = sum(1 for t in tasks if t['name'] in task_list and t['results'].get('superpowers-v4.0') == 'SUCCESS')
    base_wins = sum(1 for t in tasks if t['name'] in task_list and t['results'].get('baseline-v2.0') == 'SUCCESS')
    
    print(f"\n{stack} (N={tot} tasks):")
    print(f"  Supreme (v1.0)     : {sup_wins:2d}/{tot:2d} ({sup_wins/tot*100:5.1f}%)")
    print(f"  Superpowers by obra: {obra_wins:2d}/{tot:2d} ({obra_wins/tot*100:5.1f}%)")
    print(f"  Baseline           : {base_wins:2d}/{tot:2d} ({base_wins/tot*100:5.1f}%)")
    
    # Show diffs
    sup_adv = [t for t in task_list if any(t == x['name'] and x['results'].get('supreme-v2.0') == 'SUCCESS' and x['results'].get('superpowers-v4.0') != 'SUCCESS' for x in tasks)]
    obra_adv = [t for t in task_list if any(t == x['name'] and x['results'].get('superpowers-v4.0') == 'SUCCESS' and x['results'].get('supreme-v2.0') != 'SUCCESS' for x in tasks)]
    if sup_adv:
        print(f"    -> Supreme Win / Superpowers Loss: {sup_adv}")
    if obra_adv:
        print(f"    -> Superpowers Win / Supreme Loss: {obra_adv}")
