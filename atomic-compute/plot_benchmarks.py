"""Benchmark trend plotter - reconstructed 2026-10-05 from the consolidated
structure doc. [REPAIRED] page-break word joins only. Headless (Agg).

NOTE: the x-axis labels use timestamp[-9:-1], which grabs fractional-second
digits of the ISO stamp rather than a readable clock time - cosmetic, kept
verbatim from source.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_trend_charts():
    log_file = "benchmark_history.json"
    output_img = "benchmark_trends.png"
    if not os.path.exists(log_file):
        print("No historical telemetry found to plot.")
        return
    with open(log_file, "r") as f:
        data = json.load(f)
    timestamps = [entry["timestamp"][-9:-1] for entry in data][-15:]
    conv_times = [entry["metrics"]["convection_ms"] for entry in data][-15:]
    fric_times = [entry["metrics"]["friction_ms"] for entry in data][-15:]
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, conv_times, label="Convection Math (ms)",
             marker='o', color='#007acc', linewidth=2)
    plt.plot(timestamps, fric_times, label="Friction Solver (ms)",
             marker='s', color='#e06666', linewidth=2)
    plt.axhline(y=0.015, color='#007acc', linestyle='--',
                alpha=0.5, label="Convection Budget")
    plt.axhline(y=0.050, color='#e06666', linestyle='--',
                alpha=0.5, label="Friction Budget")
    plt.title("Atomic Compute Algorithmic Execution Latency Profile Over Time",
              fontsize=12, fontweight='bold')
    plt.xlabel("Execution Runtime Window (UTC Timestamp)", fontsize=10)
    plt.ylabel("Operational Latency Time (ms)", fontsize=10)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_img, dpi=150)
    print(f"Graph asset compiled successfully as '{output_img}'")


if __name__ == "__main__":
    generate_trend_charts()
