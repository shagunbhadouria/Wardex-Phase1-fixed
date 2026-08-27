# Multi-stage Dockerfile for SentinelAI

# Stage 1: Builder / Dev Stage
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir --user -r requirements.txt -r requirements-dev.txt

# Stage 2: Final Production Stage
FROM python:3.11-slim AS production

WORKDIR /app

RUN useradd -m -u 1000 sentinelai

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/sentinelai/.local/bin:$PATH \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder --chown=1000:1000 /root/.local /home/sentinelai/.local

# Copy application source code
COPY --chown=1000:1000 . .

# Ensure models directory exists
RUN mkdir -p /app/models && chown -R sentinelai:sentinelai /app/models

USER sentinelai

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]