FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_HOME=/app
WORKDIR ${APP_HOME}
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python benchmark_thermal_solver.py && python plot_benchmarks.py
CMD ["python", "thermal_solver.py"]
