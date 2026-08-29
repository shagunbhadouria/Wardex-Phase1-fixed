# Multi-stage Dockerfile for SentinelAI

# Stage 1: Builder — production dependencies only
# TECH DEBT FIX (Phase 2 close-out): previously this stage installed
# requirements-dev.txt too, and the `production` target copied that
# venv wholesale — meaning pytest, mypy, flake8, and pip-audit shipped
# inside the deployed image. Split into two builder stages so the
# `production` target only ever inherits from `builder-prod`.
FROM python:3.11-slim as builder-prod

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Builder — adds dev/test dependencies on top of prod deps.
# Used only by the `test` target (e.g. CI, local `docker build --target test`)
# — never by `production`.
FROM builder-prod as builder-dev

COPY requirements-dev.txt ./

RUN pip install --no-cache-dir --user -r requirements-dev.txt

# Stage 3: Test target — full dev/test toolchain, source code, for CI use
FROM python:3.11-slim as test

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder-dev /root/.local /root/.local
COPY . .
RUN mkdir -p /app/models

CMD ["pytest", "app/", "--cov=app", "--cov-report=term-missing"]

# Stage 4: Production — prod dependencies only, no test tooling
FROM python:3.11-slim as production

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from the prod-only builder stage
COPY --from=builder-prod /root/.local /root/.local

# Copy application source code
COPY . .

# Ensure models directory exists
RUN mkdir -p /app/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
