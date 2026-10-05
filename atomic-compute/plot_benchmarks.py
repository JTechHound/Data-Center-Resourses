"""v1.0.1 benchmark trend plotter - reconstructed 2026-10-05.

[REPAIRED] PDF extraction damage only. Source change vs v1.0: timestamp slice
corrected to [11:19], isolating HH:MM:SS from the timezone-aware ISO format
(verified 2026-10-05 - the audit-repair doc's [-14:-6] yielded microsecond
fragments on the new format). Headless (Agg).
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
        print("Telemetry logs missing.")
        return
    with open(log_file, "r") as f:
        data = json.load(f)
    # Correct timestamp slicing index: isolates clean HH:MM:SS
    timestamps = [entry["timestamp"][11:19] for entry in data][-15:]
    conv_times = [entry["metrics"]["convection_ms"] for entry in data][-15:]
    fric_times = [entry["metrics"]["friction_ms"] for entry in data][-15:]
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, conv_times, label="Convection Tracking (ms)",
             marker='o', color='#007acc')
    plt.plot(timestamps, fric_times, label="Friction Solver (ms)",
             marker='s', color='#e06666')
    plt.axhline(y=0.015, color='#007acc', linestyle='--', alpha=0.4,
                label="Convection Budget Floor")
    plt.axhline(y=0.050, color='#e06666', linestyle='--', alpha=0.4,
                label="Friction Budget Floor")
    plt.title("Atomic Compute Latency Scaling Metrics", fontsize=11,
              fontweight='bold')
    plt.xlabel("Execution Runtime Window (HH:MM:SS UTC)", fontsize=9)
    plt.ylabel("Processing Overhead (ms)", fontsize=9)
    plt.legend(loc="upper right", fontsize=8)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_img, dpi=150)
    print("Graph generated cleanly with correct timestamp index formatting.")


if __name__ == "__main__":
    generate_trend_charts()
