# X (Twitter) Viral Launch Thread: The Micro-Physics of Autonomous Coding

**Target Account:** Highly technical, data-driven AI engineering post  
**Tone:** Technical, punchy, honest, backed by 267 Docker evaluations.  
**Visual Attachments:** 6 high-resolution PNG charts from `paper/figures/`.

---

### Tweet 1 (The Hook):
Everyone assumes dynamic skill loading saves tokens and beats static prompts. 

We ran a controlled 267-run Docker benchmark across all 89 tasks of Terminal-Bench 2.1 evaluating Jesse Vincent's @obra Superpowers against our Constitutional Supreme architecture on Gemini 3.6 Flash.

The data shocked us. 🧵👇  
[ATTACH: paper/figures/fig1_cognitive_scaling_by_difficulty.png]

---

### Tweet 2 (The Setup):
The evaluation standard:
• 89 complex multi-turn CLI tasks (Linux sysadmin, C transformers, QEMU hypervisors, MuJoCo physics, Scheme, COBOL)
• Identical LLM engine: Gemini 3.6 Flash High @ temp 0.0
• Anti-Contamination: Test verifiers were injected via `docker cp` ONLY AFTER agent processes terminated
• Multi-signal cryptographic SHA-256 grading

---

### Tweet 3 (The Grand Scoreboard & Venn Partition):
The certified results across 267 graded evaluations:

🥇 1. Supreme (v1.0): 61/89 (68.5%) | 15.15h | 565k tokens/pass 🏆
🥈 2. Superpowers by obra: 58/89 (65.2%) | 18.30h | 591k tokens/pass
🥉 3. Baseline: 55/89 (61.8%) | 16.92h | 567k tokens/pass

Supreme won +3 tasks AND completed 3.15 hours faster. But the real story is in the 89-task mutual exclusion partition:  
[ATTACH: paper/figures/fig6_euler_venn_solvability_89tasks.png]

---

### Tweet 4 (The Hard-Task Cognitive Scaling Law):
Gemini 3.6 Flash outputs internal chain-of-thought (`thinking_tokens`).

On Hard tasks ($N=30$), Supreme scaled reasoning to **28,271 thinking tokens/task** (+66% over Medium), winning **66.7% vs 53.3%** (+13.4% lead over Superpowers).

Why did Superpowers stall? Because loading 14 skill markdown files mid-task starved the context window of reasoning space.

---

### Tweet 5 (The 3.5 Million Token Disaster — Task #88):
Look at Task #88 (Redcode warrior algorithmics):

• Supreme (v1.0): 175 seconds | 55 turns | 300,413 tokens ⚡
• Superpowers: 1,648 seconds | 563 turns | 3,513,757 tokens ⚠️

Superpowers wrote 116 custom Python exploration scripts inside Docker, thrashing in a skill-discovery loop. Supreme solved it via structured hypothesis testing with 11.7x fewer tokens.  
[ATTACH: paper/figures/fig5_task88_corewars_trajectory.png]

---

### Tweet 6 (The "Task Polling Spin Trap" & Destructive Rewrites):
We analyzed 16,000+ tool call transitions ($P(\text{Next} \mid \text{Current})$):

• The Spin Trap: Superpowers had a 42.7% chance of calling `manage_task` immediately after `manage_task` (299 triple-polling cycles).
• Destructive Rewrites: Superpowers logged 471 full file rewrites (`write_to_file`). Supreme made 42 surgical line edits (`replace_file_content`), cutting destructive file churn.  
[ATTACH: paper/figures/fig2_markov_tool_state_transitions.png]

---

### Tweet 7 (The 115.4 Million Token Cache Tax):
Think dynamic skill loading is cheap? Look at prompt caching physics:

Loading 14 skills on-demand cost Superpowers **411.3 Million cache read tokens**—an excess of **115.4 Million cache tokens** over Baseline!

Dynamic markdown injection invalidates cache prefixes, creating a massive hidden infrastructure bill.  
[ATTACH: paper/figures/fig4_token_sink_waterfall.png]

---

### Tweet 8 (Polyglot Systems & The Esoteric Anomaly):
We split all 89 tasks across 5 technical stacks:

• Low-Level Systems (C/Rust/OCaml): Supreme 70.0% vs Superpowers 60.0% (Supreme uniquely solved `gpt2-codegolf`, pure C GPT-2 inference).
• SysAdmin/DevOps: Supreme 86.7% vs 73.3% (Supreme solo-passed `install-windows-3.11`, a 44-min QEMU marathon).
• The Esoteric Anomaly: Baseline won COBOL & Scheme (85.7%) because unprompted Gemini answered without modern TDD recipe overhead!  
[ATTACH: paper/figures/fig3_polyglot_5stack_radar.png]

---

### Tweet 9 (The Verifier Peekers & Broken Containers):
Transcripts caught models attempting to reverse-engineer tests 104 times (`find / -name "*test*"`). Because tests were temporally isolated, 0 leaks occurred.

We also caught 3 broken upstream Docker images:
• `prove-plus-comm`: broken `chdir /app` (0% across all models)
• `caffe-cifar-10`: apt lock held by PID 168
• `torch-tensor-parallelism`: 2.85 GB CUDA PyPI download timeout

---

### Tweet 10 (Open Source Release):
The entire benchmark evaluation is 100% open-source and reproducible:

✅ Complete SHA-256 cryptographic audit ledger (all 267 runs)
✅ 5 deep extraction research dossiers
✅ Reproduce any task in 1 command: `python carb.py run -t <ID>`
✅ Apache 2.0 License

GitHub Repo: [github.com/your-username/Supreme]  
Full Research Report & Dossiers: [link]

What patterns have you seen in your agent setups? Drop your thoughts below! 💬👇
