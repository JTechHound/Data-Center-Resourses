# v1.0.1 - reconstructed 2026-10-05 from the audit-repair doc.
# Changes vs v1.0: benchmark pulled out of the build layer (slow build hosts
# no longer fail the docker build on timing budgets); runs as non-root user.
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app
WORKDIR ${APP_HOME}
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m simulation_user && chown -R simulation_user:simulation_user ${APP_HOME}
USER simulation_user
# Benchmarking removed from build layer - timing budgets belong in CI.
CMD ["python", "thermal_solver.py"]
