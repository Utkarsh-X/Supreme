import json
import re

with open('carb_benchmark/results_v4/extraction_findings/all_89_tasks_annotated.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# Let's inspect keywords in snippets and names
for t in tasks:
    name = t['name']
    snip = t['snippet'].lower()
    vf = " ".join(t['vfiles']).lower()
    
    langs = []
    if 'cobol' in name or 'cobol' in snip:
        langs.append('COBOL')
    if 'ocaml' in name or 'ocaml' in snip:
        langs.append('OCaml')
    if 'mips' in name or 'assembly' in snip or 'pmars' in snip or 'corewars' in name or 'redcode' in snip:
        langs.append('Assembly/MIPS/Redcode')
    if 'c++' in snip or 'cpp' in snip or 'pov-ray' in name or 'caffe' in name or 'cmake' in snip:
        langs.append('C++')
    if re.search(r'\b\.c\b', snip) or 'c program' in snip or 'in c ' in snip or 'c binary' in snip or 'dependency-free c' in snip or 'sqlite' in name:
        langs.append('C')
    if 'rscript' in snip or 'in r ' in snip or 'in r.' in snip or 'r language' in snip or 'sampler' in name:
        langs.append('R')
    if 'sparql' in name or 'sparql' in snip or 'wikidata' in name:
        langs.append('SPARQL/SQL')
    if 'javascript' in snip or 'node' in snip or '.js' in snip:
        langs.append('JavaScript/Node')
    if 'rust' in snip or 'cargo' in snip:
        langs.append('Rust')
    if 'lean' in snip or 'coq' in snip or 'prove' in name or 'isabelle' in snip:
        langs.append('Formal Proof (Coq/Lean)')
    if 'latex' in snip or 'tex' in snip or 'overfull' in name:
        langs.append('LaTeX')
    if 'bash' in snip or 'shell' in snip or 'script' in snip or 'git' in name or 'linux' in snip or 'qemu' in snip:
        langs.append('Shell/SysAdmin')
    if 'python' in snip or '.py' in snip or 'pytorch' in snip or 'torch' in snip or 'scipy' in snip or 'numpy' in snip:
        langs.append('Python')

    t['detected_langs'] = langs

# Print non-Python tasks
print("Detected polyglot/non-python tasks:")
for t in tasks:
    if any(l not in ['Python', 'Shell/SysAdmin'] for l in t['detected_langs']):
        print(f"[{t['num']:02d}] {t['name']:30} -> {t['detected_langs']} | Sup: {t['results'].get('supreme-v2.0')} | Obra: {t['results'].get('superpowers-v4.0')} | Base: {t['results'].get('baseline-v2.0')}")
