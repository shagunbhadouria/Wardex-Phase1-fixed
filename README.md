# SentinelAI

> **Autonomous Operational Intelligence & Observability Platform**
> 
> *Detect infrastructure anomalies, predict deployment risks before shipping, and run deterministically validated LLM root cause analysis with 3-gate self-healing.*

---

## 🌟 Key Features

- **Real-Time Metric Anomaly Detection**: Unsupervised point anomaly detection using **Isolation Forest** with adaptive baselines refitted on real metrics.
- **Pre-Deployment Risk Scoring**: Real-time 0–100 risk scoring with **XGBoost** on 6 high-signal deployment features via GitHub webhooks (< 800ms).
- **Deterministic Correlation Guard**: Safety engine that validates every LLM causal claim against actual metric and log evidence before surfacing it to humans.
- **3-Node LangGraph Incident Pipeline**: Focused state graph (Coordinator $\rightarrow$ Analysis Agent $\rightarrow$ Correlation Guard) delivering validated RCA in < 60s.
- **3-Gate Self-Healing Safety System**: Autonomous actions bounded by Confidence ($>0.82$), Risk Class (`LOW`/`MED`, never `HIGH`), and Historical Success Count ($\ge 3$).
- **Integrated Observability**: Prometheus metrics + Grafana dashboard for service health and LLM call latency tracking.

---

## 🏗️ Architecture

SentinelAI is built as a **Modular Monolith** with an asynchronous background worker layer:
- **API Server**: FastAPI (async HTTP & WebSocket endpoints, < 50ms ack)
- **Task Worker**: Celery 5 consuming from Redis
- **Primary Datastore**: PostgreSQL 15
- **Broker & Cache**: Redis 7
- **Observability Stack**: Prometheus (6 custom metrics) + Grafana

---

## 🚀 Quickstart (Under 10 Minutes)

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Docker + Docker Compose)
- Git
- Python 3.11+ (for local development)
- [Groq API Key](https://console.groq.com) (Free tier)

### 2. Clone & Configure Environment
```bash
git clone https://github.com/your-org/sentinelai.git
cd sentinelai

cp .env.example .env
# Edit .env to supply your GROQ_API_KEY and other optional secrets
```

### 3. Start the Core Services
```bash
make dev
# Starts: FastAPI Backend, Celery Worker, PostgreSQL 15, Redis 7
```
Core services will be available:
- **FastAPI Backend**: `http://localhost:8000`
- **Interactive OpenAPI Docs**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

### 4. Optional: Start Monitoring Stack
```bash
make monitoring
# Starts: Prometheus (localhost:9090) and Grafana (localhost:3001)
```

### 5. Health Check
Verify system status:
```bash
curl http://localhost:8000/health
# Returns: {"success":true,"data":{"status":"starting",...},"error":null,...}
```

---

## 🧪 Testing & Linting

```bash
# Run unit & integration tests with coverage
make test

# Run code style & type checks (flake8, isort, mypy)
make lint

# Auto-format codebase
make format
```

---

## 📁 Repository Structure

> **Build status:** Phase 1 (Repository Foundation) complete. Only the
> modules below exist. `anomaly_detection/`, `deployment_risk/`,
> `incident_analysis/`, `healing/`, `ml/`, `observability/`,
> `ingestion/`, and `websocket/` are **not yet built** — per the
> Blueprint's phase gate (R-69, R-77), each lands in its own phase
> (Phases 5–9), not ahead of it. See `Wardex-Blueprint-v2.md` Section
> 4.2 for the full phase order.

```
sentinelai/
├── app/
│   ├── main.py                     # FastAPI application factory + /health stub
│   ├── config.py                   # Pydantic settings & env validation
│   ├── database.py                 # SQLAlchemy 2.0 engine & session (no models yet — Phase 3)
│   ├── celery_app.py               # Celery app instance (no tasks yet — Phase 5)
│   ├── shared/                     # Constants, errors, logging, middleware, types, seed
│   ├── auth/                       # Placeholder package — Google OAuth & JWT land in Phase 4
│   └── test_main.py                # Health check tests (co-located per R-17)
├── migrations/                     # Placeholder package — Alembic migrations land in Phase 3
├── models/                         # Placeholder dir for trained model artifacts (Phase 6)
├── prometheus/                     # Prometheus scrape config & alert rules (used from Phase 9)
├── grafana/                        # Grafana datasources & dashboards (used from Phase 9)
├── docker-compose.yml              # 4 Core services (api, worker, db, redis)
├── docker-compose.monitoring.yml   # Prometheus & Grafana stack (opt-in, see make monitoring)
├── Dockerfile                      # Multi-stage container build
├── Makefile                        # Developer workflows
└── pyproject.toml                  # Project metadata & tool config
```

---

## 📜 Governance & Rules
This project follows [**Industrial Vibe Coding Rules v4**](industrial-vibe-coding-rules-v4.md) and the [**SentinelAI Master Blueprint v2**](Wardex-Blueprint-v2.md).
