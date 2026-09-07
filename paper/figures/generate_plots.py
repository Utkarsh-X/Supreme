#!/usr/bin/env python3
"""
Publication-Quality Figure Generator for CARB-v4 Academic Paper
Outputs 300-DPI PNG and publication-grade PDF plots using Okabe-Ito colorblind palette.
"""

import os
import json
import numpy as np
from PIL import Image

# NumPy 2.0 & Matplotlib C-API compatibility layer
np.Inf = np.inf
np.NaN = np.nan
from matplotlib.backends import _backend_agg
if hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangles') and not hasattr(_backend_agg.RendererAgg, 'draw_gouraud_triangle'):
    _backend_agg.RendererAgg.draw_gouraud_triangle = _backend_agg.RendererAgg.draw_gouraud_triangles

import matplotlib.pyplot as plt

# Styling configuration
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

# Okabe-Ito Palette
COLOR_SUPREME = "#0072B2"      # Blue
COLOR_SUPERPOWERS = "#E69F00"  # Orange
COLOR_BASELINE = "#999999"     # Grey

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_JSON = os.path.join(OUT_DIR, "../../carb_benchmark/results_v4/v4_parallel_progress.json")

def save_dual_formats(fig, base_name):
    """Saves both 300-DPI PNG and publication-grade PDF."""
    png_path = os.path.join(OUT_DIR, f"{base_name}.png")
    pdf_path = os.path.join(OUT_DIR, f"{base_name}.pdf")
    plt.savefig(png_path, dpi=300)
    plt.close()
    
    img = Image.open(png_path).convert("RGB")
    img.save(pdf_path, "PDF", resolution=300.0)
    print(f"Generated: {png_path} & {pdf_path}")

def generate_accuracy_latency_chart():
    """Generates Figure 1: Win Rate & Wall-Clock Execution Latency across Paradigms."""
    labels = ["Supreme (v1.0)", "Superpowers by obra", "Baseline"]
    pass_rates = [68.5, 65.2, 61.8]
    total_hours = [15.15, 18.30, 16.92]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    
    # 1. Pass Rates
    bars1 = ax1.bar(labels, pass_rates, color=[COLOR_SUPREME, COLOR_SUPERPOWERS, COLOR_BASELINE], width=0.55, edgecolor="black", linewidth=0.8)
    ax1.set_ylabel("Pass Rate (%)")
    ax1.set_ylim(50, 75)
    ax1.set_title("A: Benchmark Accuracy (89 Tasks)")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}%", ha="center", va="bottom", fontweight="bold")
        
    # 2. Total Execution Time
    bars2 = ax2.bar(labels, total_hours, color=[COLOR_SUPREME, COLOR_SUPERPOWERS, COLOR_BASELINE], width=0.55, edgecolor="black", linewidth=0.8)
    ax2.set_ylabel("Total Benchmark Latency (Hours)")
    ax2.set_ylim(10, 21)
    ax2.set_title("B: Total Wall-Clock Latency (Lower is Better)")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval:.2f}h", ha="center", va="bottom", fontweight="bold")
        
    plt.tight_layout()
    save_dual_formats(fig, "accuracy_latency_comparison")

def generate_tool_thrashing_case_study():
    """Generates Figure 2: Tool Thrashing on Task #88 (winning-avg-corewars)."""
    labels = ["Supreme (v1.0)", "Superpowers by obra", "Baseline"]
    tool_calls = [53, 535, 249]
    tokens = [300413, 3513757, 2163114]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    
    # Tool Invocations
    bars1 = ax1.bar(labels, tool_calls, color=[COLOR_SUPREME, COLOR_SUPERPOWERS, COLOR_BASELINE], width=0.55, edgecolor="black", linewidth=0.8)
    ax1.set_ylabel("Tool Calls (Count)")
    ax1.set_title("A: Tool Invocations on Task #88 (Redcode)")
    ax1.set_yscale("log")
    ax1.set_ylim(20, 1000)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"{int(yval)}", ha="center", va="bottom", fontweight="bold")
        
    # Total Tokens
    tokens_k = [t / 1000 for t in tokens]
    bars2 = ax2.bar(labels, tokens_k, color=[COLOR_SUPREME, COLOR_SUPERPOWERS, COLOR_BASELINE], width=0.55, edgecolor="black", linewidth=0.8)
    ax2.set_ylabel("Tokens Consumed (Thousands)")
    ax2.set_title("B: Token Footprint on Task #88")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{int(yval)}k", ha="center", va="bottom", fontweight="bold")
        
    plt.tight_layout()
    save_dual_formats(fig, "task88_tool_thrashing")

def generate_pareto_cost_curve():
    """Generates Figure 3: Cost per Solved Task vs Win Rate."""
    data = {
        "Supreme (v1.0)": {"rate": 68.5, "cost": 565.9, "color": COLOR_SUPREME, "marker": "o"},
        "Superpowers by obra": {"rate": 65.2, "cost": 591.4, "color": COLOR_SUPERPOWERS, "marker": "s"},
        "Baseline": {"rate": 61.8, "cost": 567.6, "color": COLOR_BASELINE, "marker": "^"}
    }
    
    fig = plt.figure(figsize=(6.5, 4.5))
    for name, d in data.items():
        plt.scatter(d["cost"], d["rate"], color=d["color"], s=160, marker=d["marker"], edgecolors="black", linewidth=1.2, label=name, zorder=5)
        plt.annotate(f"{name}\n({d['rate']:.1f}%, {d['cost']:.1f}k)", (d["cost"], d["rate"]), textcoords="offset points", xytext=(10, -5), fontweight="bold")
        
    plt.xlabel("Tokens per Solved Task (Thousands — Lower is More Efficient)")
    plt.ylabel("Overall Pass Rate (%)")
    plt.title("Pareto Frontier: Accuracy vs. Operational Cost")
    plt.xlim(540, 620)
    plt.ylim(60, 72)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="lower left")
    
    plt.tight_layout()
    save_dual_formats(fig, "pareto_cost_vs_accuracy")

if __name__ == "__main__":
    generate_accuracy_latency_chart()
    generate_tool_thrashing_case_study()
    generate_pareto_cost_curve()
    print("All publication figures successfully created!")
