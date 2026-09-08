#!/usr/bin/env python3
"""
generate_macro_summary.py — Publication-Grade 4-Panel Macro Benchmark Overview
Generates the authoritative executive summary figure for CARB-v4 on Terminal-Bench 2.1:
  Panel A: Macro Benchmark Accuracy (All 89 Tasks with Wilson 95% CIs)
  Panel B: Total Wall-Clock Execution Latency (Hours, Lower is Better)
  Panel C: Modeled API Cost per Solved Task ($/solve, Lower is Better)
  Panel D: Hard Task Completion Frontier (N=30 Most Difficult Tasks)
Outputs 300-DPI PNG and vector PDF for README, paper, and release media.
"""

import os
import numpy as np

# Compatibility layer
np.Inf = np.inf
np.NaN = np.nan
from matplotlib.backends import _backend_agg
if hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangles') and not hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangle'):
    _backend_agg.RendererAgg.draw_gouraud_triangle = _backend_agg.RendererAgg.draw_gouraud_triangles

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

plt.rcParams.update({
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.family": "sans-serif",
    "figure.titlesize": 15,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 300
})

COLORS = {
    "supreme": "#10b981",       # Emerald Green (Primary system)
    "superpowers": "#3b82f6",   # Royal Blue (obra/superpowers)
    "baseline": "#94a3b8",      # Slate Grey (Unprompted control)
    "dark_text": "#0f172a",
    "grid": "#e2e8f0"
}

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(OUT_DIR, "../../assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

fig, axes = plt.subplots(1, 4, figsize=(18, 4.6), gridspec_kw={'wspace': 0.28})

configs = ["Supreme", "Superpowers", "Baseline"]
bar_colors = [COLORS["supreme"], COLORS["superpowers"], COLORS["baseline"]]

# ----------------------------------------------------------------------
# Panel A: Macro Benchmark Accuracy (N=89)
# ----------------------------------------------------------------------
ax = axes[0]
acc = [68.5, 65.2, 61.8]
ci_low = [68.5 - 58.3, 65.2 - 54.8, 61.8 - 51.4]
ci_high = [77.2 - 68.5, 74.3 - 65.2, 71.2 - 61.8]
yerr = [ci_low, ci_high]

bars = ax.bar(configs, acc, color=bar_colors, width=0.55, edgecolor="#1e293b", linewidth=1.1,
              yerr=yerr, capsize=4, error_kw={'elinewidth': 1.2, 'ecolor': '#334155'})
ax.set_ylabel("Pass Rate (%)", fontweight="bold", color=COLORS["dark_text"])
ax.set_title("(A) Macro Accuracy (N=89 Tasks)", fontweight="bold", pad=12)
ax.set_ylim(40, 85)
ax.grid(axis="y", linestyle="--", alpha=0.6, color=COLORS["grid"])

labels_a = ["61 / 89\n(68.5%)", "58 / 89\n(65.2%)", "55 / 89\n(61.8%)"]
for bar, txt in zip(bars, labels_a):
    ax.text(bar.get_x() + bar.get_width()/2, 43, txt, ha="center", va="bottom",
            fontweight="bold", fontsize=9.5, color="white",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#1e293b", alpha=0.85, edgecolor="none"))

ax.axhline(68.5, color=COLORS["supreme"], linestyle=":", alpha=0.5, linewidth=1.2)

# ----------------------------------------------------------------------
# Panel B: Total Wall-Clock Latency (Lower is Better)
# ----------------------------------------------------------------------
ax = axes[1]
time_h = [15.15, 18.30, 16.92]
bars = ax.bar(configs, time_h, color=bar_colors, width=0.55, edgecolor="#1e293b", linewidth=1.1)
ax.set_ylabel("Total Compute Time (Hours)", fontweight="bold", color=COLORS["dark_text"])
ax.set_title("(B) Wall-Clock Latency (Lower is Better)", fontweight="bold", pad=12)
ax.set_ylim(0, 22)
ax.grid(axis="y", linestyle="--", alpha=0.6, color=COLORS["grid"])

for bar, val in zip(bars, time_h):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.2f}h", ha="center", va="bottom",
            fontweight="bold", fontsize=10, color=COLORS["dark_text"])

ax.annotate("-3.15h (-17.2%)\nvs. Superpowers", 
            xy=(0, 15.15), xytext=(0.4, 10.5),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5),
            ha="center", fontsize=9, fontweight="bold", color="#059669",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ecfdf5", edgecolor="#a7f3d0"))

# ----------------------------------------------------------------------
# Panel C: Modeled API Cost per Solved Task (Lower is Better)
# ----------------------------------------------------------------------
ax = axes[2]
cost_solve = [0.489, 0.506, 0.497]
bars = ax.bar(configs, cost_solve, color=bar_colors, width=0.55, edgecolor="#1e293b", linewidth=1.1)
ax.set_ylabel("API Cost / Solved Task ($ USD)", fontweight="bold", color=COLORS["dark_text"])
ax.set_title("(C) Unit Economics (Lower is Better)", fontweight="bold", pad=12)
ax.set_ylim(0.35, 0.56)
ax.grid(axis="y", linestyle="--", alpha=0.6, color=COLORS["grid"])

for bar, val in zip(bars, cost_solve):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.005, f"${val:.3f}", ha="center", va="bottom",
            fontweight="bold", fontsize=10, color=COLORS["dark_text"])

ax.annotate("-3.4% Cost/Solve\nvs. Superpowers", 
            xy=(0, 0.489), xytext=(0.4, 0.415),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5),
            ha="center", fontsize=9, fontweight="bold", color="#059669",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ecfdf5", edgecolor="#a7f3d0"))

# ----------------------------------------------------------------------
# Panel D: Hard Tasks Frontier (N=30)
# ----------------------------------------------------------------------
ax = axes[3]
hard_pass = [66.7, 53.3, 56.7]
bars = ax.bar(configs, hard_pass, color=bar_colors, width=0.55, edgecolor="#1e293b", linewidth=1.1)
ax.set_ylabel("Hard Pass Rate (%)", fontweight="bold", color=COLORS["dark_text"])
ax.set_title("(D) Hard Task Frontier (N=30)", fontweight="bold", pad=12)
ax.set_ylim(35, 80)
ax.grid(axis="y", linestyle="--", alpha=0.6, color=COLORS["grid"])

labels_d = ["20 / 30\n(66.7%)", "16 / 30\n(53.3%)", "17 / 30\n(56.7%)"]
for bar, txt in zip(bars, labels_d):
    ax.text(bar.get_x() + bar.get_width()/2, 38, txt, ha="center", va="bottom",
            fontweight="bold", fontsize=9.5, color="white",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#1e293b", alpha=0.85, edgecolor="none"))

ax.annotate("+13.4 pts Lead\nvs. Superpowers", 
            xy=(0, 66.7), xytext=(0.45, 52.0),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5),
            ha="center", fontsize=9, fontweight="bold", color="#059669",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ecfdf5", edgecolor="#a7f3d0"))

# Overall Figure Super Title & Note
fig.suptitle("CARB-v4 Master Benchmark Overview: Terminal-Bench 2.1 (89 Tasks • Gemini 3.6 Flash High)",
             fontsize=14, fontweight="bold", y=1.03, color=COLORS["dark_text"])

fig.text(0.5, -0.04, 
         "Note: Evaluated across 267 isolated container sessions. Aggregate pass differences are not statistically significant (McNemar p > 0.05). Costs modeled at OpenRouter evaluation rates ($0.5598 in / $3.745 out per M tokens).",
         ha="center", fontsize=8.5, color="#64748b", style="italic")

# Save outputs
png_out = os.path.join(OUT_DIR, "macro_benchmark_summary.png")
pdf_out = os.path.join(OUT_DIR, "macro_benchmark_summary.pdf")
asset_png = os.path.join(ASSETS_DIR, "macro_benchmark_summary.png")

plt.savefig(png_out, dpi=300, bbox_inches="tight")
plt.close(fig)

im = Image.open(png_out).convert("RGB")
im.save(pdf_out, "PDF", resolution=300.0)
im.save(asset_png, "PNG")

print(f"Successfully generated:\n - {png_out}\n - {pdf_out}\n - {asset_png}")
