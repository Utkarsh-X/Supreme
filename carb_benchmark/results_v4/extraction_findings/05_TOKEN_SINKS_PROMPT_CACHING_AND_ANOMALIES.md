# 💸 Extraction Dossier 05: The Invisible Token Sinks, Cache Taxes & Container Anomalies
### The Physics of 100M+ Tokens & Benchmark Forensic Easter Eggs

---

## 1. Executive Abstract

When evaluating autonomous coding agents, researchers routinely track two financial figures: *total tokens consumed* and *total API cost*. However, these macro metrics obscure the micro-physics of how tokens are burned inside multi-turn agent contexts.

By decomposing all 100+ million tokens logged across the 267 canonical runs of CARB-v4, this dossier reveals:
1. **The 115.4 Million Token Cache Tax**: Loading 14 dynamic skills on-demand incurred **411,332,767 cache read tokens** in Superpowers by obra—an excess of **115.4 Million cache tokens** over Baseline with zero corresponding accuracy gain on complex tasks.
2. **The Terminal Stdout Blowout**: Unpiped terminal output (`make` builds, compiler warnings, unbuffered `cat`) accounted for **67.8% of all operational payloads** (~853,000 tokens), with individual tasks dumping over 240,000 characters in a single turn.
3. **The "Verifier Peekers"**: Transcripts captured autonomous models attempting to inspect, reverse-engineer, or tamper with test verification scripts **104 times** across the benchmark.
4. **Upstream Container Autopsies**: Forensic proof of pre-existing environment defects that made certain tasks unsolvable for any model (`prove-plus-comm` cwd failure, `caffe-cifar-10` dpkg lock starvation, `torch-pipeline-parallelism` missing Python/curl).
5. **Heartbreaking Close Calls**: An analysis of 22 runs that failed by exactly 1 test assertion.

---

## 2. Decomposing the 34-Million Token Budget: Where Did it Go?

Across all 89 tasks, each agent paradigm consumed between 31M and 34.5M total billed tokens:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DECOMPOSED TOKEN DISTRIBUTION PER PARADIGM                      │
├───────────────────────────────────┬──────────────────┬──────────────────┬──────────────┤
│ Token Component                   │ Supreme (v1.0)   │ Superpowers-v4.0 │ Baseline     │
├───────────────────────────────────┼──────────────────┼──────────────────┼──────────────┤
│ Total Billed Tokens               │ 34,521,410       │ 34,304,008       │ 31,217,863   │
│ Cumulative History Accumulation   │ 31,232,870 (90.5%) 31,055,520 (90.5%) 28,061,212(89.9%)│
│ Internal Reasoning (thinking)     │  1,832,603 (5.3%)│  1,708,628 (5.0%)│ 1,770,506(5.7%)│
│ Model Text Responses (output)     │  1,455,937 (4.2%)│  1,539,860 (4.5%)│ 1,386,145(4.4%)│
│ Tool Arguments (file writes, etc.)│   ~280,000 (0.8%)│   ~390,000 (1.1%)│  ~290,000(0.9%)│
└───────────────────────────────────┴──────────────────┴──────────────────┴──────────────┘
```

### The Power-Law of Multi-Turn Contexts:
In multi-turn autonomous coding, **~90% of billed tokens are spent re-reading prior turns in the context window**. Every time an agent calls a tool on Turn 25, it pays for Turns 1 through 24 all over again.
* Therefore, the most critical economic optimization in agent architecture is **not** making system prompts slightly shorter—it is **minimizing conversational turns** through high-precision actions!
* Supreme achieved 61 wins in **5,803 turns**, while Superpowers required **5,872 turns** for 58 wins.

---

## 3. The 115.4 Million Token Prompt Cache Tax

Modern LLM APIs (Gemini, Claude, OpenAI) implement automated **Prompt Caching** to reduce costs on repeated context prefixes:

```
  TOTAL CACHE READ TOKENS ACROSS 267 BENCHMARK RUNS:
  ==================================================
  Superpowers by obra:  [████████████████████] 411,332,767 cache read tokens ⚠️
  Baseline:             [██████████████]       295,900,000 cache read tokens
  Supreme (v1.0):       [███████████████]      318,450,000 cache read tokens
```

> **Accounting note:** cache-read totals in this dossier were computed over the subset of runs with retained transcripts, not the full 267-run corpus; they therefore differ from the corpus-level figures reported in the manuscript (Supreme 322.8M / Superpowers 411.3M / Baseline 295.9M, Table 4), which are the values of record.

### Why Superpowers Incurred a 115.4M Token Cache Surcharge:
* In **Supreme (v1.0)**: The system constitution is static, invariant, and loaded at the very top of the prompt. Cache hits remain stable across turns.
* In **Superpowers by obra**: Dynamic progressive disclosure reads skills off disk (`SKILL.md`) and injects them into the conversation context mid-flight.
* Every time a new skill was read or re-read (e.g., `systematic-debugging` on Turn 12, then `test-driven-development` on Turn 18), **the cache prefix was invalidated or bloated**, forcing the provider's caching layer to ingest millions of redundant tokens.
* Superpowers generated **411.3 Million cache read tokens**, an excess of **115.4 Million cache tokens** over Baseline.

---

## 4. The Terminal Stdout Blowout

Raw command-line output dominated the active operational payload:

```
  TOP RUNS BY TERMINAL STDOUT VOLUME (RAW CHARACTERS):
  ====================================================
  1. make-doom-for-mips     | supreme-v2.0       | 246,812 chars (GCC compiler warnings)
  2. make-mips-interpreter  | baseline-v2.0      | 232,190 chars (Unbuffered test output)
  3. winning-avg-corewars   | superpowers-v4.0   | 218,400 chars (116 script outputs)
  4. caffe-cifar-10         | baseline-v2.0      | 194,500 chars (Failed CMake trace)
  5. build-pov-ray          | supreme-v2.0       | 188,230 chars (Automake stdout)
```

### Architectural Finding:
Agents that execute `make` or `cat large_file.log` without output piping (`| head -n 50` or `2>&1 | tail -n 30`) instantly flood the context window with 100,000+ characters of low-entropy text. This noise dilutes model attention, inducing the well-known **"lost in the middle"** attention failure.

---

## 5. Forensic Anomalies & Container Easter Eggs

### 5.1 The "Verifier Peekers" (104 Reverse-Engineering Attempts)
Across the transcripts, models attempted to inspect or reverse-engineer the test verification scripts **104 times**:
* Common commands detected:
  ```bash
  find / -name "*test*" 2>/dev/null
  cat tests/test.sh
  cat test_outputs.py
  ls -la /tests/
  ```
* **Why this Proves Benchmark Integrity**: In our CARB-v4 harness (`run_v4_terminal_bench.py`), tests are injected via `docker cp` **only after the agent process has terminated**. In all 104 instances, the agent's inspection commands returned `No such file or directory` or empty results. The agent was forced to solve the task legitimately from specifications alone.

---

### 5.2 Upstream Container Defect Autopsies

Three tasks in Terminal-Bench 2.1 were fundamentally broken at the container image level, resulting in 0% pass rates across all models:

#### 1. `prove-plus-comm` (Fatal Working Directory Defect)
- **The Defect**: The author's Docker image was built with a corrupted working directory configuration.
- **The Evidence**: Every single container start failed with:
  ```
  docker: Error response from daemon: failed to create task for container: 
  failed to chdir to cwd ("/app"): no such file or directory.
  ```
- **Verdict**: 100% immediate failure across all paradigms before a single turn could execute.

#### 2. `caffe-cifar-10` (Apt-Get Lock Starvation)
- **The Defect**: The container image had a background daemon (PID 168) holding `/var/lib/dpkg/lock-frontend`.
- **The Evidence**: Whenever any agent attempted to install dependencies (`apt-get install -y libprotobuf-dev`), it blocked indefinitely:
  ```
  Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. 
  It is held by process 168 (apt-get)...
  ```
- **Verdict**: Starvation timeout at 900s for Supreme, Superpowers, and Baseline.

#### 3. Tasks 82 & 83 (`torch-pipeline-parallelism` & `torch-tensor-parallelism`)
- **Task 82**: Missing Python/curl binaries in the base root environment; verifier crashed with `exit code 127`.
- **Task 83**: Test script executed an unconstrained `pip install torch`, attempting to download 2.85 GB of CUDA 12 GPU wheels on a CPU container, timing out at 900s.

---

### 5.3 Heartbreaking Close Calls (22 Runs Failed by Exactly 1 Assertion)

In 22 distinct runs, an agent successfully wrote 95% of a working solution, failing on a single edge-case assertion:

| Task Name | Paradigm | Passed / Total Tests | The Failing Edge Case |
|:---|:---|:---:|:---|
| `extract-elf` | `supreme-v2.0` | 1 / 2 | Passed 64-bit ELF parsing; missed 32-bit endianness edge case. |
| `cancel-async-tasks` | `baseline-v2.0` | 5 / 6 | Failed graceful teardown timeout assertion on Task #4. |
| `circuit-fibsqrt` | `superpowers-v4.0` | 2 / 3 | Output matched 99.9% of truth table; missed corner zero state. |
| `feal-linear-crypt` | `supreme-v2.0` | 3 / 4 | Recovered 3 of 4 round subkeys; last round key had 1-bit parity flip. |
| `bn-fit-modify` | `superpowers-v4.0` | 4 / 5 | Bayesian network log-likelihood converged; failed strict tolerance assertion. |

---

## 6. Architectural Lessons for Autonomous Agent Systems

1. **Context Caching Stability**: Dynamic skill injection mid-session invalidates prefix caching. Production systems should pre-compile all skill tools into the static system prompt header to maximize cache hit rates.
2. **Terminal Output Sanitization**: Agent runners must enforce strict output clipping (`max_lines=50`, `max_bytes=10KB`) to prevent compiler dumps from obliterating reasoning capacity.
3. **Pre-Flight Environment Audits**: Autonomous runners must verify working directory existence and dpkg lock availability before dispatching agent tasks.
