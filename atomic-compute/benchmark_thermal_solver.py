"""v1.0.1 micro-benchmark harness - reconstructed 2026-10-05 from the
audit-repair doc.

[REPAIRED] PDF extraction damage only. Source change vs v1.0: timestamp
uses timezone-aware datetime.now(timezone.utc) instead of deprecated
datetime.utcnow().
"""
import time
import sys
import json
import os
from datetime import datetime, timezone
from thermal_solver import DataCenterThermalSolver


def run_performance_benchmarks():
    solver = DataCenterThermalSolver()
    iterations = 50000
    # Benchmark 1: Convection Math
    start_time = time.perf_counter()
    for i in range(iterations):
        velocity = 0.5 + (i % 10) * 0.1
        d_h = 0.002 + (i % 5) * 0.0005
        _ = solver.calculate_forced_convection_nusselt(velocity, d_h)
    end_time = time.perf_counter()
    convection_total_time = end_time - start_time
    convection_avg_time_ms = (convection_total_time / iterations) * 1000
    # Benchmark 2: Friction Math
    start_time = time.perf_counter()
    for i in range(iterations):
        velocity = 1.0 + (i % 5) * 0.2
        d_h = 0.01 + (i % 3) * 0.01
        _ = solver.calculate_wall_shear_stress(velocity, d_h)
    end_time = time.perf_counter()
    friction_total_time = end_time - start_time
    friction_avg_time_ms = (friction_total_time / iterations) * 1000

    CONVECTION_BUDGET_MS = 0.015
    FRICTION_BUDGET_MS = 0.050
    convection_pass = convection_avg_time_ms <= CONVECTION_BUDGET_MS
    friction_pass = friction_avg_time_ms <= FRICTION_BUDGET_MS

    log_file = "benchmark_history.json"
    new_entry = {
        # Timezone-aware UTC - suppresses the 3.12 utcnow() deprecation
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "convection_ms": round(convection_avg_time_ms, 6),
            "friction_ms": round(friction_avg_time_ms, 6),
        },
        "passed": bool(convection_pass and friction_pass),
    }
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                history_data = json.load(f)
        except:  # noqa: E722 - verbatim from source
            history_data = []
    else:
        history_data = []
    history_data.append(new_entry)
    with open(log_file, "w") as f:
        json.dump(history_data, f, indent=4)

    if not (convection_pass and friction_pass):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    run_performance_benchmarks()
