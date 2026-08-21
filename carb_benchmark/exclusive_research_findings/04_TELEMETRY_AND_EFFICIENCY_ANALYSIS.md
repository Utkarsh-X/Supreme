# CARB-v3: Telemetry, Speed & Cognitive Efficiency Metrics

This document analyzes the computational and behavioral dynamics across all 39 tasks in CARB-v3.

---

## 1. Summary Distribution Table

| Metric | Baseline (`baseline-v2.0`) | Superpowers (`superpowers-v2.0`) | Supreme (`supreme-v2.0`) |
|---|:---:|:---:|:---:|
| **Pass Rate (Accuracy)** | 0.0% (0 / 39) | 17.9% (7 / 39) | **23.1% (9 / 39)** |
| **Median Wall-Clock Time** | 182.9 s | **244.2 s** | 264.3 s |
| **Mean Wall-Clock Time** | 390.4 s | **363.9 s** | 530.6 s |
| **Median Tool Iterations** | 12.0 | **33.0** | 40.0 |
| **Mean Tool Iterations** | 18.5 | 45.0 | 44.4 |
| **Median Token Usage** | 120,400 | 262,634 | **255,647** |
| **Mean Token Usage** | 185,200 | 344,560 | **317,205** |

---

## 2. Speed vs. Accuracy Trade-Offs

1. **Velocity Champion (Superpowers):** Superpowers recorded a lower mean wall-clock latency (**363.9s vs. 530.6s**), demonstrating high efficiency on algorithmic tasks through modular SKILL definitions.
2. **Depth Champion (Supreme Agent):** Supreme Agent achieved the highest overall accuracy (**23.1%**, 9 victories), spending more time in verification loops (mean 530.6s) while maintaining lower mean token overhead (**317k vs. 344k tokens**).
