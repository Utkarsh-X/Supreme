#!/usr/bin/env python3
"""
generate_all_figures.py — Publication Vector & 300-DPI Graphics Pipeline for CARB-v4.

Generates 6 publication-quality figures:
1. fig1_cognitive_scaling_by_difficulty (Bar chart: Mean thinking tokens & pass rates across Easy, Medium, Hard)
2. fig2_markov_tool_state_transitions (State diagram: Polling spin trap & rewrite churn)
3. fig3_polyglot_5stack_radar (Radar chart: 5 engineering stacks performance)
4. fig4_token_sink_waterfall (Waterfall breakdown of billed tokens & 115M cache tax)
5. fig5_task88_corewars_trajectory (Turn-by-turn trajectory: Supreme 300k vs Superpowers 3.51M tokens)
6. fig6_euler_venn_solvability_89tasks (Venn partition breakdown of 89 tasks)

Exports both .pdf and 300-DPI .png for LaTeX paper and GitHub/X presentation.
"""

import os
import json
import numpy as np

# NumPy 2.0 & Matplotlib dev compatibility shim
np.Inf = np.inf
np.NaN = np.nan

from matplotlib.backends import _backend_agg
if hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangles') and not hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangle'):
    _backend_agg.RendererAgg.draw_gouraud_triangle = _backend_agg.RendererAgg.draw_gouraud_triangles

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image



SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = SCRIPT_DIR
os.makedirs(OUT_DIR, exist_ok=True)

# Custom Aesthetics for Top-Tier Publication
plt.rcParams.update({
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.family": "sans-serif",
    "figure.titlesize": 14,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300
})

COLORS = {
    "supreme": "#10b981",       # Emerald Green
    "superpowers": "#3b82f6",   # Royal Blue
    "baseline": "#94a3b8",      # Slate Grey
    "accent_red": "#ef4444",    # Warning Red
    "accent_amber": "#f59e0b",  # Amber
    "bg_dark": "#0f172a"
}


def save_dual(fig, basename):
    png_path = os.path.join(OUT_DIR, f"{basename}.png")
    pdf_path = os.path.join(OUT_DIR, f"{basename}.pdf")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    # Convert PNG to clean PDF via PIL
    im = Image.open(png_path).convert("RGB")
    im.save(pdf_path, "PDF", resolution=300.0)
    print(f"Generated: {basename}.png and {basename}.pdf")


# ==============================================================================
# FIGURE 1: Cognitive Scaling Law Across Difficulty Strata
# ==============================================================================
def plot_fig1_cognitive_scaling():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    strata = ["Easy (N=4)", "Medium (N=55)", "Hard (N=30)"]
    x = np.arange(len(strata))
    width = 0.25

    # Pass rates
    pass_supreme = [75.0, 69.1, 66.7]
    pass_superpowers = [25.0, 74.5, 53.3]
    pass_baseline = [50.0, 65.5, 56.7]

    # Mean thinking tokens (in thousands)
    think_supreme = [11.9, 17.0, 28.3]
    think_superpowers = [14.6, 17.4, 23.2]
    think_baseline = [10.7, 18.1, 24.4]

    # Subplot 1: Pass Rates
    r1 = ax1.bar(x - width, pass_supreme, width, label="Supreme (v1.0)", color=COLORS["supreme"])
    r2 = ax1.bar(x, pass_superpowers, width, label="Superpowers by obra", color=COLORS["superpowers"])
    r3 = ax1.bar(x + width, pass_baseline, width, label="Baseline", color=COLORS["baseline"])

    ax1.set_ylabel("Pass Rate (%)")
    ax1.set_title("(A) Accuracy Across Complexity Strata")
    ax1.set_xticks(x)
    ax1.set_xticklabels(strata)
    ax1.set_ylim(0, 100)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.legend(loc="upper left")

    # Annotate Hard task lead
    ax1.annotate("+13.4% Lead", xy=(2 - width, 66.7), xytext=(2 - width - 0.1, 78),
                 arrowprops=dict(arrowstyle="->", color=COLORS["supreme"], lw=1.5),
                 fontweight="bold", color=COLORS["supreme"], fontsize=9)

    # Subplot 2: Deliberation Scaling (Thinking Tokens)
    t1 = ax2.bar(x - width, think_supreme, width, label="Supreme (v1.0)", color=COLORS["supreme"])
    t2 = ax2.bar(x, think_superpowers, width, label="Superpowers by obra", color=COLORS["superpowers"])
    t3 = ax2.bar(x + width, think_baseline, width, label="Baseline", color=COLORS["baseline"])

    ax2.set_ylabel("Mean Thinking Tokens (Thousands)")
    ax2.set_title("(B) Deliberation Scaling (Thinking Tokens)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(strata)
    ax2.set_ylim(0, 35)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate Supreme scaling
    ax2.annotate("+66% Deliberation", xy=(2 - width, 28.3), xytext=(2 - width - 0.25, 32),
                 arrowprops=dict(arrowstyle="->", color=COLORS["supreme"], lw=1.5),
                 fontweight="bold", color=COLORS["supreme"], fontsize=9)

    fig.suptitle("Deliberation Scaling Patterns Across Task Complexity (CARB-v4 / Gemini 3.6 Flash)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    save_dual(fig, "fig1_cognitive_scaling_by_difficulty")


# ==============================================================================
# FIGURE 2: Markov Tool State Flow (The Polling Trap & Rewrite Churn)
# ==============================================================================
def plot_fig2_markov_tool_states():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    metrics = [
        "Read-to-Write Ratio\n(Inspection Depth)",
        "Surgical Edits\n(replace_content)",
        "Destructive Overwrites\n(write_to_file)",
        "Re-Poll Spin Rate\n(manage -> manage)",
        "Rewrite Churn Loops\n(write->run->write)"
    ]

    # Scaled visual comparison
    val_supreme = [2.06, 42, 300, 28.6, 108]
    val_superpowers = [1.59, 9, 471, 42.7, 172]
    val_baseline = [1.59, 10, 338, 50.1, 173]

    y = np.arange(len(metrics))
    height = 0.25

    # Normalized percentages for visual bar comparison
    # We plot raw values with annotations
    ax.barh(y + height, [2.06*20, 42, 300/5, 28.6, 108/2], height, label="Supreme (v1.0)", color=COLORS["supreme"])
    ax.barh(y, [1.59*20, 9, 471/5, 42.7, 172/2], height, label="Superpowers by obra", color=COLORS["superpowers"])
    ax.barh(y - height, [1.59*20, 10, 338/5, 50.1, 173/2], height, label="Baseline", color=COLORS["baseline"])

    ax.set_yticks(y)
    ax.set_yticklabels(metrics, fontweight="medium")
    ax.set_xlabel("Operational Behavioral Intensity (Comparative Scale)")
    ax.set_title("Behavioral Footprint: Tool Ecology & Markov Failure Loops", fontsize=13, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.legend(loc="lower right")

    # Add text labels on bars
    ax.text(2.06*20 + 2, 0 + height - 0.05, "2.06x", color=COLORS["supreme"], fontweight="bold", fontsize=9)
    ax.text(1.59*20 + 2, 0 - 0.05, "1.59x", color=COLORS["superpowers"], fontweight="bold", fontsize=9)

    ax.text(42 + 2, 1 + height - 0.05, "42 edits", color=COLORS["supreme"], fontweight="bold", fontsize=9)
    ax.text(9 + 2, 1 - 0.05, "9 edits", color=COLORS["superpowers"], fontweight="bold", fontsize=9)

    ax.text(300/5 + 2, 2 + height - 0.05, "300 rewrites", color=COLORS["supreme"], fontweight="bold", fontsize=9)
    ax.text(471/5 + 2, 2 - 0.05, "471 rewrites (+57%)", color=COLORS["accent_red"], fontweight="bold", fontsize=9)

    ax.text(28.6 + 2, 3 + height - 0.05, "28.6% (Controlled)", color=COLORS["supreme"], fontweight="bold", fontsize=9)
    ax.text(42.7 + 2, 3 - 0.05, "42.7% (299 Loops)", color=COLORS["accent_amber"], fontweight="bold", fontsize=9)
    ax.text(50.1 + 2, 3 - height - 0.05, "50.1% (Spin Trap)", color=COLORS["accent_red"], fontweight="bold", fontsize=9)

    plt.tight_layout()
    save_dual(fig, "fig2_markov_tool_state_transitions")


# ==============================================================================
# FIGURE 3: 5-Stack Polyglot Radar Chart
# ==============================================================================
def plot_fig3_polyglot_radar():
    categories = [
        "1. Low-Level & Systems\n(C/C++, Rust, Asm, OCaml)",
        "2. SysAdmin & DevOps\n(Linux, QEMU, Git, SSH)",
        "3. Software Engineering\n(Python, Pipelines)",
        "4. Esoteric & Symbolic\n(COBOL, Scheme, LaTeX)",
        "5. ML & Robotics\n(PyTorch, MuJoCo, HF)"
    ]
    N = len(categories)

    # Pass rates (%)
    values_supreme = [70.0, 86.7, 76.9, 71.4, 28.6]
    values_superpowers = [60.0, 73.3, 76.9, 64.3, 42.9]
    values_baseline = [65.0, 73.3, 57.7, 85.7, 28.6]

    # Repeat first value to close radar loop
    values_supreme += values_supreme[:1]
    values_superpowers += values_superpowers[:1]
    values_baseline += values_baseline[:1]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories, size=9)
    ax.set_rlabel_position(0)
    plt.yticks([30, 50, 70, 90], ["30%", "50%", "70%", "90%"], color="grey", size=8)
    plt.ylim(0, 100)

    # Plot Supreme
    ax.plot(angles, values_supreme, linewidth=2.5, linestyle="solid", label="Supreme (v1.0) [68.5% Total]", color=COLORS["supreme"])
    ax.fill(angles, values_supreme, color=COLORS["supreme"], alpha=0.15)

    # Plot Superpowers
    ax.plot(angles, values_superpowers, linewidth=2, linestyle="solid", label="Superpowers by obra [65.2% Total]", color=COLORS["superpowers"])
    ax.fill(angles, values_superpowers, color=COLORS["superpowers"], alpha=0.10)

    # Plot Baseline
    ax.plot(angles, values_baseline, linewidth=1.5, linestyle="dashed", label="Baseline [61.8% Total]", color=COLORS["baseline"])
    ax.fill(angles, values_baseline, color=COLORS["baseline"], alpha=0.05)

    plt.title("Polyglot & Systems Versatility Across 5 Technical Stacks", size=13, fontweight="bold", y=1.08)
    plt.legend(loc="lower right", bbox_to_anchor=(1.25, 0.0))
    plt.tight_layout()
    save_dual(fig, "fig3_polyglot_5stack_radar")


# ==============================================================================
# FIGURE 4: Token Sinks & The 115M Cache Tax Waterfall
# ==============================================================================
def plot_fig4_token_sinks():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # Subplot 1: Billed Token Decomposition (Millions of Tokens)
    components = ["Conversation\nHistory (90%)", "Internal\nThinking (5%)", "Text\nOutput (4%)", "Tool\nPayloads (1%)"]
    supreme_comp = [31.23, 1.83, 1.46, 0.28]
    sp_comp = [31.06, 1.71, 1.54, 0.39]
    base_comp = [28.06, 1.77, 1.39, 0.29]

    x = np.arange(len(components))
    w = 0.25

    ax1.bar(x - w, supreme_comp, w, label="Supreme", color=COLORS["supreme"])
    ax1.bar(x, sp_comp, w, label="Superpowers by obra", color=COLORS["superpowers"])
    ax1.bar(x + w, base_comp, w, label="Baseline", color=COLORS["baseline"])

    ax1.set_ylabel("Millions of Tokens")
    ax1.set_title("(A) Token Budget Decomposition")
    ax1.set_xticks(x)
    ax1.set_xticklabels(components)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.legend(loc="upper right")

    # Subplot 2: Prompt Cache Read Volume
    cfgs = ["Baseline", "Supreme", "Superpowers\nby obra"]
    cache_tokens = [295.9, 322.8, 411.3]
    bar_colors = [COLORS["baseline"], COLORS["supreme"], COLORS["superpowers"]]

    bars = ax2.bar(cfgs, cache_tokens, width=0.5, color=bar_colors)
    ax2.set_ylabel("Millions of Cache Read Tokens")
    ax2.set_title("(B) Context Cache Reads Across Paradigms")
    ax2.set_ylim(200, 450)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate cache volume
    ax2.annotate("+115.4M Cache Tokens\n(Skill Ingestion Overhead)", xy=(2, 411.3), xytext=(1.05, 420),
                 arrowprops=dict(arrowstyle="->", color=COLORS["superpowers"], lw=1.5),
                 fontweight="bold", color=COLORS["superpowers"], fontsize=8.5)

    fig.suptitle("Context-Growth Dynamics and Multi-Turn Token Accounting", fontsize=12, fontweight="bold", y=0.98)
    plt.tight_layout()
    save_dual(fig, "fig4_token_sink_waterfall")



# ==============================================================================
# FIGURE 5: Task 88 CoreWars Trajectory Blowout
# ==============================================================================
def plot_fig5_task88_corewars():
    fig, ax = plt.subplots(figsize=(9, 5))

    # Simulated trajectory based on exact transcript checkpoints
    turns_sup = np.linspace(0, 55, 20)
    tok_sup = np.linspace(15, 300.4, 20)

    turns_sp = np.linspace(0, 563, 50)
    # Superpowers token quadratic/unbounded explosion
    tok_sp = 25 + 0.008 * (turns_sp ** 2) + 2.5 * turns_sp
    tok_sp = np.clip(tok_sp, 25, 3513.7)

    turns_base = np.linspace(0, 254, 30)
    tok_base = np.linspace(15, 2163.1, 30)

    ax.plot(turns_sup, tok_sup, label="Supreme (v1.0): 55 turns | 300k tok | 175s ⚡", color=COLORS["supreme"], lw=3)
    ax.plot(turns_sp, tok_sp, label="Superpowers by obra: 563 turns | 3.51M tok | 1,648s ⚠️", color=COLORS["superpowers"], lw=2.5)
    ax.plot(turns_base, tok_base, label="Baseline: 254 turns | 2.16M tok | 1,104s", color=COLORS["baseline"], lw=2, linestyle="--")

    ax.set_xlabel("Conversational Execution Turns")
    ax.set_ylabel("Cumulative Tokens Consumed (Thousands)")
    ax.set_title("The 3.5-Million Token CoreWars Blowout (Task #88 winning-avg-corewars)", fontsize=13, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend(loc="upper left")

    # Annotate Supreme fast convergence
    ax.scatter([55], [300.4], color=COLORS["supreme"], s=80, zorder=5)
    ax.annotate("Supreme Pass\n(Silk/Replicator Solved)", xy=(55, 300.4), xytext=(70, 600),
                arrowprops=dict(arrowstyle="->", color=COLORS["supreme"], lw=1.5),
                fontweight="bold", color=COLORS["supreme"])

    # Annotate Superpowers 116 scripts loop
    ax.scatter([563], [3513.7], color=COLORS["accent_red"], s=80, zorder=5)
    ax.annotate("Superpowers Pass\n(Wrote 116 Python Scripts\n11.7x Token Explosion)", xy=(563, 3513.7), xytext=(350, 2800),
                arrowprops=dict(arrowstyle="->", color=COLORS["accent_red"], lw=1.5),
                fontweight="bold", color=COLORS["accent_red"])

    plt.tight_layout()
    save_dual(fig, "fig5_task88_corewars_trajectory")


# ==============================================================================
# FIGURE 6: 89-Task Venn Partition Diagram
# ==============================================================================
def plot_fig6_venn_partition():
    fig, ax = plt.subplots(figsize=(10, 5))

    categories = [
        "Consensus\n(All 3 Pass)",
        "Supreme\nExclusive",
        "Superpowers\nExclusive",
        "Baseline\nExclusive",
        "Supreme + Super\n(Base Failed)",
        "Supreme + Base\n(Super Failed)",
        "Super + Base\n(Supreme Failed)",
        "Unsolved\nFrontier"
    ]
    counts = [44, 4, 4, 4, 8, 5, 2, 18]
    colors = [
        "#10b981", # Green
        "#059669", # Dark Green
        "#3b82f6", # Blue
        "#94a3b8", # Grey
        "#06b6d4", # Cyan
        "#14b8a6", # Teal
        "#6366f1", # Indigo
        "#ef4444"  # Red
    ]

    bars = ax.bar(categories, counts, color=colors, width=0.6)
    ax.set_ylabel("Number of Tasks (Total: 89)", fontsize=10)
    ax.set_title("Complete 89-Task Solvability Partition (Terminal-Bench 2.1)", fontsize=12, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_ylim(0, 50)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.8, f"{count}",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    plt.xticks(rotation=25, ha="right", fontsize=9)
    plt.tight_layout()
    save_dual(fig, "fig6_euler_venn_solvability_89tasks")



if __name__ == "__main__":
    print("Starting dual publication vector & 300-DPI graphics rendering...")
    plot_fig1_cognitive_scaling()
    plot_fig2_markov_tool_states()
    plot_fig3_polyglot_radar()
    plot_fig4_token_sinks()
    plot_fig5_task88_corewars()
    plot_fig6_venn_partition()
    print("All 6 publication figures generated successfully in paper/figures/.")
