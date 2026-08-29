**SENTINELAI**

Engineering Master Blueprint — v2 (Trimmed)

*Autonomous Operational Intelligence Platform*

| **Document**  | **Value**                                                    |
|---------------|---------------------------------------------------------------|
| Document Type | Engineering Master Blueprint — DOC-02 of 04 — **v2**           |
| Project       | SentinelAI v1.0 (trimmed scope)                                |
| Domain        | Infrastructure Observability / MLOps                            |
| Tech Domain   | Python + FastAPI + PostgreSQL + Redis + ML + LLM                |
| Status        | Blueprint Freeze — Fill before Phase 1 begins                   |
| Pairs With    | Vibe Coding Rules (DOC-01) · Engineering Journal (DOC-03)        |
| Supersedes    | Wardex-Blueprint-v1.md — see Section 0 for cut rationale         |

> *This document defines WHAT you are building and HOW before a single
> line of code is written. Every decision here is a locked contract.*

---

## SECTION 0 — What Changed from v1 and Why

**[Certain]** v1 violated its own Rule R-06 ("no overengineering... an
MVP doesn't need a message queue"). It specified 7 Docker services, 3 ML
models, a 5-node LangGraph agent system, RAG, and a fabricated RL
lookup table dressed as reinforcement learning — for a project
explicitly scoped as a solo fresher's portfolio build on a 10-week
timeline. That is not a stack. That is a resume keyword list with a
database attached.

**Cut entirely — near-zero marginal signal, real time cost:**

| Cut | Reason |
|---|---|
| **RL signal table + outcome-check Celery task** | It's a lookup table, not RL. The v1 doc admits this in its own WHY note (old 8.5) — "even a simple lookup table... demonstrates RL principles" is a claim that collapses under one follow-up question ("what's your policy update rule?"). Framing a static counter as RL is a credibility risk, not a strength. |
| **Prophet forecasting** | Third ML model doing time-series prediction when two models (Isolation Forest, XGBoost) already prove two distinct competencies — unsupervised anomaly detection and supervised classification. A third model adds surface area, not new signal. |
| **MLflow** | Redundant with Grafana for "I track things I built." Was also a 7th Docker service the v1 doc never correctly counted anywhere it listed "all N services." |
| **sentence-transformers + DBSCAN log clustering** | Real technique, but it's plumbing for RAG, not a standalone interview story. Folded into simpler direct-retrieval logic below. |
| **3 of 5 LangGraph nodes** (Infrastructure/Application/Deployment specialists as separate parallel agents) | "3 parallel agents" tests badly under questioning. Collapsed to coordinator → single analysis node → Correlation Guard. Keeps the actual differentiator (deterministic safety validation of LLM output) without the state-machine debugging risk v1's own Phase 7 notes flagged as the top blocker. |
| **React Flow live agent graph** | Visually impressive, but it's a frontend-skill demo, not a backend/ML/systems-skill demo — which is what a FAANG backend or ML interview actually scores. Replaced with a simple status timeline component (still real-time via WebSocket, far less build risk). |
| **12-feature XGBoost → 6 features** | 12 hand-picked features on synthetic data doesn't demonstrate more ML competence than 6 does. More features = more synthetic-data-generation surface area for zero extra signal. |

**Kept — this is where the actual signal lives:**

1. Isolation Forest anomaly detection (unsupervised)
2. XGBoost deployment risk, 6 features (supervised — deliberate contrast with #1)
3. PostgreSQL + pgvector (one database, ACID + vector search, real architectural tradeoff)
4. Celery + Redis (plain task queue — no Redis Streams complexity layered on top)
5. LangGraph: coordinator → analysis node → Correlation Guard (deterministic validation of LLM output — the actual differentiator)
6. Three-gate self-healing (kept, simplified — Gate 3 reads a static success counter, no RL table required)
7. Prometheus + Grafana (single monitoring story, not split with MLflow)
8. Postmortem generation (cheap, one LLM call, demo-visible)

**Result:** 4 Docker services instead of 7. 2 ML models instead of 3.
1 LLM pipeline with 3 nodes instead of 5. No claim you can't defend
under cross-examination. Every remaining piece has a distinct,
defensible "why this and not the alternative" — which is what reads as
senior-level judgment in an interview, not the technology count.

---

## PART 01 — Product Blueprint

### 1.1 — Project Overview

**Project Name:** SentinelAI

**One-Line Tagline:** An observability platform that detects
infrastructure anomalies using unsupervised ML, predicts deployment
risk before code ships using supervised ML, and — when something
breaks — runs an LLM analysis pipeline whose output is never trusted
directly, only after deterministic validation against real evidence.

> **WHY:** This tagline is honest about scope. It does not claim
> autonomy, prediction-into-the-future, or self-improving intelligence
> — it claims three specific, defensible things you can go deep on.

**Problem Statement**

Engineering teams running microservices spend significant on-call time
manually investigating failures that were already predictable from
metric patterns. Deployments go out without automated risk assessment
— a high-risk Friday night push gets the same treatment as a small
Tuesday hotfix. When something does break, reconstructing root cause
from scattered logs takes time better spent building.

**Target Users**

Primary: SREs and DevOps engineers who carry the pager. Secondary:
Backend engineers who want to know if their deployment is risky before
it ships.

> **WHY narrower than v1:** v1 added a third persona (engineering
> manager) and reporting features to serve them. Cut — two personas
> is enough to justify every feature; a third persona used to justify
> nothing that wasn't already built for the first two.

**Core Goal**

Detect infrastructure anomalies before they become outages. Predict
deployment risk before code ships. When an incident occurs, produce a
validated root-cause analysis faster than manual log archaeology — with
every LLM claim checked against real evidence before it's shown to a
human.

### 1.2 — Vision, Scope & Non-Goals

**In Scope — v1 Must Have**

- Metric collection endpoint — CPU, memory, error rate, API latency per service
- GitHub Actions webhook receiver for deployment event tracking
- Isolation Forest anomaly detection on service metrics
- XGBoost deployment risk scorer — 0-100 score, 6 features, with feature explanation
- LangGraph 3-node incident pipeline: Coordinator → Analysis Agent → Correlation Guard
- Correlation Guard — deterministic validation, every causal claim checked against log/metric evidence before acceptance
- Three-gate self-healing — confidence threshold, action risk classification, static historical success count
- Prometheus metrics — 6 custom application metrics
- One Grafana dashboard — Infrastructure Health + AI pipeline latency combined
- LLM observability — every Groq call logged with latency, tokens, cost
- Plain-text postmortem generation after resolved incidents
- Two chaos engineering scenarios for demo validation
- GitHub Actions 3-stage CI/CD pipeline (test → build/push → deploy)
- React + Recharts dashboard — real-time metric charts, anomaly markers, deployment risk history, incident list, incident status timeline (real-time via WebSocket, not a node graph)

**Out of Scope — v1 Explicitly Not Included**

- RL / reinforcement learning of any kind — Gate 3 uses a static counter, not a learned policy. Never call this RL in the pitch.
- Prophet / time-series forecasting — v2 candidate only if a real need appears post-v1
- MLflow / formal experiment tracking — training runs logged to a flat JSON file with params + metrics; sufficient for 2 models trained a handful of times each
- sentence-transformers embeddings + DBSCAN clustering — episodic memory retrieval uses direct SQL filtering on incident fingerprint (service, error type, time bucket), not vector similarity, until corpus size justifies it
- Multi-agent parallel specialist fan-out — one analysis node handles infrastructure, application, and deployment signals in a single structured prompt
- React Flow / animated agent graph — a plain status list with live-updating badges
- PyTorch, Kubernetes, Terraform, multi-tenancy — same reasoning as v1, still correct
- pgvector HNSW / vector search — table has too few rows in a portfolio demo (dozens of incidents, not thousands) to justify an ANN index; exact cosine over a filtered candidate set is fine at this scale, and admitting that is more credible than pretending you need HNSW for 30 rows

> **WHY the RAG cut specifically:** pgvector + HNSW was justified in v1
> by "up to 100k+ incidents." A portfolio demo will have 5-20 incidents.
> An interviewer who asks "how many incidents are in your corpus" and
> hears "twelve" while you're running an HNSW ANN index is a worse
> outcome than a filtered SQL query with an honest explanation of when
> you'd introduce vector search.

**Long-Term Vision — v2 and Beyond**

v2 candidates, only after v1 is fully built, tested, and demoed
successfully: Prophet forecasting, real embedding-based RAG once corpus
size justifies it, XGBoost online learning after real deployment
outcomes accumulate, a second parallel analysis node if the single-node
pipeline proves too coarse in practice. Nothing here blocks v1 and
nothing here is claimed as already built.

### 1.3 — Competitor Analysis & Market Gap

| **Existing Solution** | **What It Does Well** | **Key Weakness / Limitation** | **SentinelAI Advantage** |
|---|---|---|---|
| Datadog | Comprehensive monitoring, great dashboards, wide integrations | Expensive, rule-based alerts only, no autonomous remediation, no deployment risk prediction | ML-based anomaly detection adapts to each service's patterns without manual threshold tuning. Deployment risk prediction before code ships. |
| PagerDuty | Excellent on-call routing and escalation, incident management workflows | Purely reactive — alerts after failure, no prediction or prevention, no AI-powered root cause analysis | LLM-assisted root cause analysis whose output is deterministically validated against evidence before being shown to a human — not reactive-only, and not blindly trusted. |
| New Relic | Full-stack observability, APM, distributed tracing | Complex setup, expensive, AI features are surface-level | Isolation Forest provides unsupervised anomaly detection out of the box with zero manual threshold configuration. |
| Prometheus + Grafana | Free, flexible, industry standard for metrics collection and visualization | No anomaly detection, no AI, no incident analysis, threshold-only alerts | SentinelAI adds an ML + validated-LLM intelligence layer on top of the same Prometheus metrics pattern — extending the standard tooling rather than replacing it. |
| AWS CloudWatch | Tight AWS integration, serverless-friendly, managed service | AWS-only lock-in, anomaly detection is basic statistical threshold | Cloud-agnostic, and the LLM layer's causal claims are checked against real evidence rather than asserted. |

**The Gap SentinelAI Fills**

Every existing tool is reactive — it tells you something broke after it
broke. The gap is a system that predicts deployment risk before the
deploy goes out, detects anomaly patterns statistically before they
become outages, and — when the LLM is used to reason about an incident
— never surfaces a causal claim to a human without first checking it
deterministically against real log and metric evidence. That last
property, not the number of models or agents involved, is the actual
differentiator, and it is fully implemented rather than partially
implemented across too many components to finish.

### 1.4 — User Personas

**Persona 1 — Arjun, SRE at a 200-person startup**

| Attribute | Detail |
|---|---|
| Pain Points | Paged for failures predictable from metric trends; reconstructs root cause from logs manually |
| What They Need | Anomaly detection that learns per-service normal patterns; validated root-cause analysis when an alert fires; deployment risk scores pre-ship |
| How They Use SentinelAI | Connects services, sets up GitHub webhook, dashboard is first screen on alert |

**Persona 2 — Divya, Backend Engineer**

| Attribute | Detail |
|---|---|
| Pain Points | Never knows if a deploy is risky until it causes an incident; writes postmortems manually |
| What They Need | Risk score before every deploy; automatic postmortem after incidents |
| How They Use SentinelAI | Checks risk score in GitHub Actions before approving; reads generated postmortems |

### 1.5 — Goals, Objectives & Success Metrics

**Functional Goals**

- Detect point anomalies in service metrics within 30 seconds
- Score every deployment 0-100 for risk within 800ms of webhook receipt
- Run incident analysis pipeline and return a validated diagnosis within 60 seconds (relaxed from v1's 90s target — 3 nodes, not 5, should be faster; if it isn't, that's a real finding worth logging)
- Execute automated remediation (container restart) only when all three gates pass
- Generate plain-text postmortem after every resolved incident

**Non-Functional Goals**

- No sensitive data in logs or API responses
- Setup from scratch under 5 minutes using `docker-compose up`

| **Metric / KPI** | **Target** | **Failure If** |
|---|---|---|
| Anomaly detection latency | < 30s from metric arrival to WebSocket alert | > 60s consistently |
| Deployment risk score latency | < 800ms webhook to score displayed | > 2s on any deployment |
| Incident analysis latency | < 60s from anomaly confirmation to validated diagnosis | > 2 min consistently |
| Isolation Forest false positive rate | < 8% on real metric data | > 15% on normal traffic |
| XGBoost accuracy | > 78% on held-out synthetic test set | < 65% on test set |
| Correlation Guard rejection rate | Logged and reported honestly — no target, this is a measurement not a KPI | N/A — the point is to show the number, whatever it is |
| API p95 latency | < 200ms for all non-LLM endpoints | Any endpoint p95 > 500ms under load |

> **WHY the Correlation Guard row has no target:** v1 set a target
> ("<10% hallucination rate") for a number that is directly a function
> of prompt quality you haven't written yet. Setting a target before
> you have a baseline is decoration. Measure it honestly in the demo
> and explain what the number means — that's a stronger interview
> answer than a suspiciously round target hit exactly.

---

## PART 02 — Technical Blueprint

### 2.1 — Architecture Design

**Architecture Type:** Modular Monolith. Single FastAPI process,
feature-based modules (`ingestion`, `anomaly_detection`,
`deployment_risk`, `incident_analysis`, `healing`, `observability`),
Celery + Redis for async work off the request path.

**Why Modular Monolith — Not Microservices:** Microservices would mean
separate deployable services for ingestion, ML inference, and the API
— adding service discovery, inter-service auth, and distributed tracing,
each a real chunk of work. As a solo developer building a portfolio
project, that overhead is not justified. Microservices make sense when
you need to scale a specific component independently or need different
tech stacks per component — neither applies here. Module boundaries
inside the monolith are drawn so services could be extracted later
without a business-logic rewrite, if that ever became necessary.

> **→** *Interview answer: "I chose a modular monolith because the
> deployment bottleneck for a solo portfolio project is operational
> complexity, not scaling individual components. Clean module
> boundaries mean I could extract services later without refactoring
> business logic — but I didn't build that I'd need to, because I
> don't."*

**Why plain Celery task queue — not Redis Streams:** v1 used Redis
Streams with consumer groups for the ingestion path, justified by "the
ingestion layer IS event-driven because it genuinely needs async
processing of high-volume webhooks." At portfolio-demo volume (dozens
of requests per minute during a live demo, not thousands per second),
a standard Celery task queue provides the same "API responds fast,
heavy work happens off-thread" property with less code, less to debug,
and one less thing to explain wrong in an interview. Redis Streams
consumer-group semantics are a legitimate answer to "how do you handle
10,000 events/sec with exactly-once processing" — a question this
project's actual scale does not raise. Claiming Streams for volume you
don't have is the same mistake as claiming HNSW for a 12-row table.

**High-Level System Flow**

External event (GitHub webhook, metric POST) → FastAPI route validates
and acknowledges (<50ms) → event enqueued to Celery via Redis → Celery
worker runs the relevant pipeline: for metrics, Isolation Forest scores
the snapshot; for deployments, XGBoost scores the webhook payload → if
anomaly confirmed, LangGraph coordinator triggered → Analysis Agent
produces draft diagnosis → Correlation Guard validates every causal
claim against stored log/metric evidence, strips unsupported claims →
self-healing gates evaluated → action taken or escalated → result
broadcast via WebSocket → incident stored in PostgreSQL → postmortem
generated → everything logged to `llm_call_log`.

### 2.2 — Tech Stack — Every Technology with Reason

| **Layer** | **Technology** | **Why Chosen** | **Alternatives Rejected & Why** |
|---|---|---|---|
| Runtime | Python 3.11 | Required for scikit-learn, XGBoost. First-class ML library support. | Node.js — thinner ML ecosystem |
| API Framework | FastAPI | Native async, automatic OpenAPI docs, Pydantic validation, built-in WebSocket support | Flask — no native async/validation. Django — heavyweight for an API-first service |
| Task Queue | Celery 5 (plain task queue, not Streams) | Retry with backoff, dead letter handling, industry-recognized. Matches actual event volume of a portfolio demo. | Redis Streams consumer groups — solves a 10k-events/sec problem this project doesn't have. FastAPI BackgroundTasks — no retry, dies with process. |
| Broker/Cache | Redis 7 | Celery broker + WebSocket pub/sub + query cache in one service | RabbitMQ/Kafka — complexity with no benefit at this scale |
| Primary Database | PostgreSQL 15 | ACID for incidents/deployments/metrics, pgvector available in the same instance if v2 needs it, JSON support for fingerprints | MongoDB — wrong model for relational incident/metric data. SQLite — no concurrent writes. |
| Anomaly Detection | Isolation Forest (scikit-learn) | Unsupervised — no labeled anomaly data required. Interpretable score. | Z-score — static, doesn't adapt per-service |
| Deployment Risk | XGBoost Classifier, 6 features | Native missing-feature handling, built-in feature importance, fast inference | Random Forest — less interpretable importance. Neural net — overkill for 6-feature tabular data. |
| Agent Orchestration | LangGraph — 3 nodes (Coordinator, Analysis, done) | Stateful graph with conditional routing, without the 5-node fan-out complexity that doesn't add signal | LangChain fixed sequential chain — fine actually, LangGraph chosen because state-machine framing is the more common FAANG-adjacent pattern and 3 nodes is small enough to fully understand |
| LLM Provider | Groq API (LLaMA 3.1 70B) | Fast inference, free tier sufficient for portfolio demo volume | OpenAI — costs money, variable latency |
| Local LLM Fallback | Ollama (llama3) | Offline fallback when Groq rate-limited | Single point of failure on Groq alone |
| Observability | Prometheus + Grafana (single dashboard) | Industry-standard, every SRE interviewer has used both. One dashboard, not split across two tools. | Adding MLflow on top — redundant "I track things" story |
| Frontend | React + TypeScript + Tailwind + Recharts | Recharts handles real-time metric charts; no need for React Flow's node-graph complexity for a 3-node pipeline | React Flow — justified for 5 animated nodes, not justified for 3; a status list with live badges shows the same information |
| CI/CD | GitHub Actions, 3-stage (test → build/push → deploy) | Free, familiar, sufficient for this deploy target | 4th stage (v1's "integration tests" as a separate stage) folded into stage 1 — real DB/Redis spun up in the same job, one less pipeline stage to maintain |
| Deployment | Render (backend) + Vercel (frontend) | Free tiers, zero-config from GitHub | — |
| Containers | Docker + Docker Compose — **4 services**: postgres, redis, api, worker | One command starts everything. No Prometheus/Grafana in the always-on compose file — run via a separate `docker-compose.monitoring.yml` invoked only when demoing the dashboard, since they add startup time without being needed for core development. | v1's 6-7 service compose — Prometheus/Grafana split out because you don't need them running while writing business logic, only when demoing observability specifically |

### 2.3 — Database Design

**Database Type:** PostgreSQL 15. pgvector extension installed but
**not indexed with HNSW in v1** — reserved for v2 if corpus size ever
justifies it. Table names plural.

**Table: services**

Tracks every connected service. All other tables reference this.

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | UUID | PK DEFAULT gen_random_uuid() | Unique service identifier |
| name | VARCHAR(100) | NOT NULL UNIQUE | e.g. "payment-service" |
| environment | VARCHAR(20) | NOT NULL DEFAULT 'production' | production, staging, development |
| baseline_cpu | FLOAT | DEFAULT 0 | Rolling average CPU |
| baseline_memory | FLOAT | DEFAULT 0 | Rolling average memory |
| baseline_error_rate | FLOAT | DEFAULT 0 | Rolling average error rate |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | |

Indexes: UNIQUE on `name`. Few rows, mostly read-only after setup — no other indexes needed.

**Table: metric_snapshots**

Time-series metric data. Queried by anomaly detection.

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | BIGSERIAL | PK | Sequential — faster inserts than UUID at this write volume |
| service_id | UUID | NOT NULL REFERENCES services(id) | |
| cpu_percent | FLOAT | NOT NULL | 0-100 |
| memory_percent | FLOAT | NOT NULL | 0-100 |
| error_rate | FLOAT | NOT NULL | Errors per second |
| api_latency_ms | FLOAT | NOT NULL | |
| request_count | INTEGER | NOT NULL DEFAULT 0 | |
| anomaly_score | FLOAT | DEFAULT NULL | Isolation Forest score, filled post-detection |
| is_anomalous | BOOLEAN | DEFAULT FALSE | True if anomaly_score exceeds threshold |
| recorded_at | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | |

Indexes: `(service_id, recorded_at DESC)` — primary query pattern for anomaly detection. `(is_anomalous, recorded_at)` — recent anomalies for dashboard.

**Table: deployments** — **trimmed to 6 XGBoost features** instead of
12:

| Column | Type | Description |
|---|---|---|
| id | UUID | PK |
| service_id | UUID | FK |
| commit_sha | VARCHAR(40) | |
| author_github | VARCHAR(100) | |
| lines_changed | INTEGER | Feature 1 |
| files_changed | INTEGER | Feature 2 |
| pr_review_count | INTEGER | Feature 3 |
| deploy_hour | INTEGER | Feature 4 — 0-23 |
| day_of_week | INTEGER | Feature 5 — 0=Monday |
| author_incident_rate | FLOAT | Feature 6 — computed from author's deploy history |
| risk_score | FLOAT | XGBoost output, 0-100 |
| risk_explanation | JSONB | Top 3 contributing features |
| outcome | VARCHAR(20) | success, incident, rollback |
| incident_id | UUID | FK, nullable |
| deployed_at | TIMESTAMPTZ | |

> **WHY these 6 and not v1's 12:** test_coverage_delta, ci_flakiness_score,
> days_since_last_deploy, similar_change_incidents, and
> deploy_frequency_7d were cut. Each is individually plausible, but
> none of them changes the interview conversation — "I extracted N
> features" carries the same weight at 6 as at 12 if you can explain
> every one deeply, and 6 is a set you can actually defend line-by-line
> without notes (R-50 from your own rules doc).

**Table: incidents** — trimmed. Removed `embedding vector(384)` column
(no vector RAG in v1 — see 1.2). Kept: id, service_id, status,
severity, anomaly_type, fingerprint (JSONB), root_cause,
confidence_score, remediation_action, remediation_success, postmortem,
detected_at, resolved_at. Removed `blast_radius` and `runbook` — real
features, cut because they're additive polish that don't change the
core pitch and cost real build time; add back in v2 if time permits
after core is solid.

**Table: remediations**

Every automated remediation action, successful or not. Gate 3 reads
this table directly via COUNT — see 2.3 note below.

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | UUID | PK DEFAULT gen_random_uuid() | |
| incident_id | UUID | NOT NULL REFERENCES incidents(id) | |
| action_type | VARCHAR(50) | NOT NULL | container_restart, resource_scale_up, alert_escalation |
| gate1_passed | BOOLEAN | NOT NULL | Confidence threshold gate |
| gate2_passed | BOOLEAN | NOT NULL | Action risk classification gate |
| gate3_passed | BOOLEAN | NOT NULL | Historical success count gate |
| executed | BOOLEAN | NOT NULL DEFAULT FALSE | Whether all gates passed and action ran |
| success | BOOLEAN | DEFAULT NULL | Whether service recovered within 15 minutes |
| recovery_time_seconds | INTEGER | DEFAULT NULL | |
| executed_at | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | |

Indexes: `(incident_id)`. `(action_type, success)` — this is what Gate 3
queries: `SELECT COUNT(*) FROM remediations WHERE action_type = ? AND
success = true` joined against incidents on matching service/anomaly
type. No separate signal table — same gate, one less table to maintain,
no implied "learned success rate" that isn't actually learned.

**Removed entirely:** `remediation_rl_signal` table. Gate 3's "historical
success count" check now reads directly from a `COUNT(*) WHERE
action_type = ? AND success = true` query against `remediations`,
filtered by incident type via a join. Same functional gate, no separate
table, no "success_rate" column implying a learned rate that isn't
learned.

**Table: llm_call_log**

Every single Groq call, logged. Implements Rule R-96 directly.

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | UUID | PK DEFAULT gen_random_uuid() | |
| stage | VARCHAR(50) | DEFAULT NULL | "coordinator" or "analysis" — which pipeline stage made this call |
| incident_id | UUID | REFERENCES incidents(id) | |
| model | VARCHAR(50) | NOT NULL | llama-3.1-70b-versatile |
| prompt_tokens | INTEGER | NOT NULL | |
| completion_tokens | INTEGER | NOT NULL | |
| latency_ms | INTEGER | NOT NULL | |
| success | BOOLEAN | NOT NULL | |
| error_message | TEXT | DEFAULT NULL | |
| called_at | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | |

Indexes: `(incident_id)`. `(stage, called_at DESC)` — per-stage latency in the dashboard.

**Six tables total:** services, metric_snapshots, deployments,
incidents, remediations, llm_call_log. (v1 had eight — cut
`remediation_rl_signal` entirely and removed the `embedding` vector
column from `incidents`.)

### 2.4 — API Design & Contracts

**Base URL:** `/api/v1/` — unchanged. **WebSocket:** `ws://localhost:8000/ws/dashboard`

**WebSocket Events — trimmed from v1's 7 to 5** (removed `agent_tool_call`
— was for React Flow edge labels, not needed for a status-list UI;
removed the forecast fields from `metric_update`):

| Event | Payload | When Emitted |
|---|---|---|
| `anomaly_detected` | `{ service_id, service_name, anomaly_score, metric_snapshot, timestamp }` | Isolation Forest confirms anomaly |
| `analysis_status` | `{ incident_id, stage: "coordinator"\|"analyzing"\|"validating"\|"complete"\|"failed", summary? }` | Pipeline stage transitions — drives the status-list UI |
| `incident_diagnosed` | `{ incident_id, root_cause, confidence, recommended_action, rejected_claims }` | Correlation Guard finishes validation |
| `healing_action` | `{ incident_id, action_type, gate1, gate2, gate3, executed }` | Three-gate evaluation completes |
| `deployment_scored` | `{ deployment_id, service_name, risk_score, top_features }` | XGBoost scores a webhook |

**Standard Response Envelope — Every Response Uses This Shape**

| Field | Type | Always Present | Description |
|---|---|---|---|
| success | boolean | Yes | true for 2xx, false for errors |
| data | object \| null | Yes | Payload on success, null on error |
| error | object \| null | Yes | null on success; `{ code, message, fields }` on error |
| meta | object | Yes | `{ version: "v1", request_id, timestamp }` |

**Breaking Change Protocol:** deprecation header `X-Deprecated: true` →
CHANGELOG entry → old endpoint kept working 30 days → new version under
`/api/v2/`. Never remove an endpoint without a sunset period.

**API Endpoints — 13 total**

| Method | Path | Auth | Request | Success Response | Error Codes | Rate Limit |
|---|---|---|---|---|---|---|
| POST | /auth/google | None | `{ code }` | 200: `{ token, refresh_token, user }` | INVALID_OAUTH_CODE | 20/min |
| POST | /auth/refresh | None | `{ refresh_token }` | 200: `{ token, refresh_token }` | TOKEN_EXPIRED | 30/min |
| GET | /services | JWT | — | 200: `{ services[] }` | UNAUTHORIZED | 100/min |
| POST | /services | JWT | `{ name, environment }` | 201: `{ service }` | VALIDATION_ERROR | 20/min |
| GET | /services/:id/metrics | JWT | `?from&to&limit` | 200: `{ metrics[] }` | NOT_FOUND | 100/min |
| POST | /services/:id/metrics | API Key | `{ cpu, memory, error_rate, latency_ms, request_count }` | 201: `{ snapshot_id, anomaly_detected }` | VALIDATION_ERROR | 1000/min |
| POST | /deployments/webhook | GitHub HMAC | GitHub payload | 202: `{ deployment_id, risk_score, risk_explanation }` | INVALID_SIGNATURE | 100/min |
| GET | /deployments | JWT | `?service_id&limit` | 200: `{ deployments[] }` | UNAUTHORIZED | 100/min |
| GET | /incidents | JWT | `?status&severity&limit` | 200: `{ incidents[], total }` | UNAUTHORIZED | 100/min |
| GET | /incidents/:id | JWT | — | 200: `{ incident, remediations, llm_calls, similar_past[] }` | NOT_FOUND | 200/min |
| POST | /incidents/:id/resolve | JWT | `{ notes? }` | 200: `{ incident, postmortem }` | ALREADY_RESOLVED | 20/min |
| POST | /chaos/inject | JWT + Admin | `{ scenario, service_id, duration_seconds }` | 200: `{ scenario_id, started_at }` | INVALID_SCENARIO | 5/min |
| GET | /health | None | — | 200: `{ status, services: { db, redis, celery, groq } }` | None | 200/min |

> **WHY 13 not 16:** `/observability/llm-calls` folded into the
> `/incidents/:id` response (LLM call log for that incident is shown
> alongside the incident, not queried separately — nobody browses raw
> LLM logs without an incident to anchor them). `/forecasts/:service_id`
> removed with Prophet. `/auth/logout` folded into `/auth/refresh`
> accepting a revoke flag rather than a dedicated endpoint.

### 2.5 — Security Architecture

**Authentication Strategy**

Google OAuth 2.0 via Authlib. User clicks Sign in with Google → Google
returns an authorization code → `POST /auth/google` exchanges it for
user info → create/update user in PostgreSQL → issue JWT access token
(15 min expiry) + refresh token (7 day expiry, stored in Redis with
blacklist support).

API Key authentication for `/services/:id/metrics` — service agents
posting metrics use a per-service API key from environment variables,
not JWTs. Keys hashed with SHA-256 before storage.

**Authorization / RBAC**

| Role | Permissions | Who Has It |
|---|---|---|
| admin | All endpoints including `/chaos/inject` | First registered user, manually promoted |
| engineer | Read all data, resolve incidents | All other authenticated users |
| service_agent | POST `/services/:id/metrics` only | Machine-to-machine, API key not JWT |

**OWASP Top 10 Coverage**

| Threat | Mitigation |
|---|---|
| A01 Broken Access Control | RBAC middleware on every protected endpoint; unauthorized returns 403 not 404 |
| A02 Cryptographic Failures | JWT signed RS256; refresh tokens hashed; API keys SHA-256; HTTPS via Render |
| A03 Injection | SQLAlchemy parameterized queries throughout — no string concatenation in SQL |
| A04 Insecure Design | Three-gate self-healing prevents autonomous execution without explicit checks; Correlation Guard prevents LLM output from directly triggering actions |
| A05 Security Misconfiguration | CORS restricted to frontend origin; security headers via middleware |
| A06 Vulnerable Components | pip-audit in CI; Dependabot enabled; pinned versions |
| A07 Authentication Failures | Rate limiting on auth endpoints; expired tokens return 401 not 500; Redis blacklist on logout |
| A08 Software Integrity Failures | Docker image from pinned base; no external scripts at runtime |
| A09 Logging Failures | structlog on every request; sensitive fields excluded from logs |
| A10 SSRF | No user-controlled URL fetching; outbound calls only to allowlisted domains |

**Secrets Management**

All secrets in environment variables — `.env` locally, GitHub Secrets
for CI, Render env vars for production. Never committed;
`.gitignore` includes `.env*`. `.env.example` kept current with every
new variable. App validates all required secrets on startup via
Pydantic Settings and refuses to start with missing values.

### 2.6 — Scalability & Failure Recovery

Unchanged principles from v1, adjusted for plain Celery instead of
Streams: Celery worker crash mid-task → task requeued via standard
Celery ack semantics, not Streams visibility timeout. Everything else
(Postgres connection loss, Redis loss, Groq rate limit, Groq outage) —
same failure modes, same recovery strategies as v1's Section 2.6.

---

## PART 03 — Engineering Blueprint

### 3.1 — Folder Structure

Same feature-based structure as v1 (R-15), with these modules removed:
`forecasting/`, `rag/` (folded into `incident_analysis/` as a simple
query function, not a separate module), `ml/mlflow_tracker.py` (replaced
by a plain `ml/run_logger.py` writing JSON). `sentinelai/frontend/src/
components/AgentGraph/` replaced with `StatusTimeline/`.

**Docker Compose — 4 services always-on:** postgres, redis,
sentinelai-api, sentinelai-worker. Prometheus + Grafana moved to
`docker-compose.monitoring.yml`, started only for demo/observability
work — `make dev` starts the 4 core services in under 2 minutes, not
5+.

### 3.2 — Coding Standards & Conventions

**Naming:** Files snake_case (`anomaly_detection/model.py`). Classes
PascalCase (`IsolationForestDetector`, `ThreeGateChecker`). Functions/
variables snake_case (`run_detection()`, `risk_score`). Constants
UPPER_SNAKE_CASE (`ANOMALY_THRESHOLD`, `MAX_RETRY_ATTEMPTS`). Pydantic
models PascalCase with suffix (`MetricSnapshotCreate`,
`DeploymentRiskResponse`). Celery tasks verb_noun snake_case
(`run_incident_analysis`). Tables plural snake_case (`incidents`,
`metric_snapshots`). Error codes UPPER_SNAKE_CASE.

**Patterns allowed:** Repository pattern — all DB access through
repository classes, service layer never writes SQL directly. Dependency
injection via FastAPI `Depends`. Factory pattern for model loading —
singleton, loaded once on startup. Context manager for LLM calls —
every Groq call wrapped for automatic logging. Celery retry with
exponential backoff, `max_retries=3`.

**Patterns forbidden:** God objects — no class with more than 3
responsibilities. Global mutable state, except singleton model
instances loaded once. Raw SQL string concatenation. Nested
conditionals beyond 3 levels — extract to named functions. Bare
`except Exception:` without a comment and specific handling.

**Module Dependency Rules — flow strictly downward:**

1. Routes — validate input, call service, return response. No business logic.
2. Services — business logic. Calls repositories and ML models. No SQL, no HTTP clients directly.
3. Repositories — DB queries only. No business logic.
4. ML models — inference only, loaded once. No database access.
5. Shared utilities — pure functions and constants. No upward dependencies.

If you find yourself importing a service from a repository, or a route
from a service — stop. That's a dependency inversion. Extract a shared
utility instead.

**Integration Sequence:** Database layer → Service layer → Route layer
→ ML models → Celery tasks → LLM/Agent pipeline → Frontend. Each layer
tested before the next is built.

### 3.3 — Git Workflow & Standards

**Branching:** `main` — production-ready only, never commit directly.
`dev` — integration branch, CI runs on every push. `feature/description`,
`fix/description`, `chore/description` — branch from `dev`.

**Commit format:** `type(scope): description` — e.g.
`feat(anomaly_detection): add adaptive threshold retraining task`.
Types: feat, fix, chore, test, docs, refactor, perf. Scope: module name.
Description present tense, under 72 characters.

**PR Checklist — all must pass before merge:**

- All CI checks pass (lint, type check, unit + integration tests)
- No `print()` statements — structlog only
- No TODO stubs without a Tech Debt Register entry
- New env vars added to `.env.example`
- New feature has unit tests AND at least one integration test
- No changes outside the scope of this PR
- No sensitive data in logs, responses, or comments
- API changes match the locked contract in 2.4
- You can explain every line of this PR without notes

---

## PART 04 — Execution Blueprint

### 4.1 — Development Philosophy

Unchanged principle: infrastructure first, intelligence second, one
module at a time. What changes is what "intelligence second" now
contains — less of it.

### 4.2 — Phase-by-Phase Build Order (Trimmed)

| Phase | Focus | Key Change from v1 |
|---|---|---|
| 0 | Planning Freeze | Same |
| 1 | Repository Foundation | Docker Compose is 4 services, not 6-7 |
| 2 | Backend Skeleton | 13 route stubs, not 16 |
| 3 | Database Layer | 6 tables, not 8 — no `remediation_rl_signal`, no embedding column |
| 4 | Auth & Security | Same |
| 5 | Ingestion Pipeline | Plain Celery task queue — no Streams consumer group debugging |
| 6 | ML Models | Isolation Forest + XGBoost only. No Prophet, no MLflow — flat JSON run log instead |
| 7 | Incident Analysis | LangGraph 3-node pipeline (Coordinator → Analysis → Correlation Guard), not 5-node fan-out. No embedding-based retrieval — direct SQL fingerprint filter. |
| 8 | Self-Healing | Three-gate system, Gate 3 reads a COUNT query — no RL table, no outcome-recompute task |
| 9 | Observability | Prometheus (6 metrics, not 8) + one Grafana dashboard |
| 10 | Security Hardening | Same as v1 Phase 11 |
| 11 | Performance + Chaos | 2 chaos scenarios, not 3 — drop the deployment-risk chaos scenario, keep high-error-rate and memory-leak |
| 12 | Docs + Demo Prep | Same principle, smaller demo script (see 6.1 below) |

**12 phases instead of 14.** This is not just fewer features — it's
fewer places for a solo build to run out of time before reaching demo
polish, which is where the previous plan's own risk notes (Week 7,
"LangGraph state mutation bugs" + "React Flow WebSocket sync") were
concentrated.

### 4.3 — Weekly Milestone Plan (Trimmed to 7 Weeks)

| Week | Phase | Deliverable | Done When |
|---|---|---|---|
| 1 | 0 | Blueprint frozen, docker-compose.yml (4 services) written | Someone else could build this from the doc alone |
| 2 | 1-2 | Repo, CI skeleton, FastAPI skeleton, 13 route stubs | CI green, every endpoint returns standard envelope |
| 3 | 3-4 | 6 tables migrated, OAuth + JWT + rate limiting | Integration test: metric posted arrives in DB in <5s |
| 4 | 5-6 | Ingestion pipeline, Isolation Forest, XGBoost | Isolation Forest catches injected spike in test; XGBoost >78% accuracy |
| 5 | 7 | LangGraph 3-node pipeline, Correlation Guard | Full analysis completes <60s on chaos test; Guard rejects at least 1 uncorroborated claim in 10 test runs |
| 6 | 8-9 | Three-gate self-healing, Prometheus + Grafana | Container restart executes only when all 3 gates pass; dashboard shows real data |
| 7 | 10-12 | Security hardening, 2 chaos scenarios, demo prep | Both chaos scenarios pass end-to-end; README runnable by a stranger in <10 min |

> **[Likely]** 7 weeks is still not slack-free for a solo builder
> learning LangGraph and XGBoost from scratch, but it's a plan that
> can plausibly finish with room for the failure-story polish that
> actually drives interview scores (R-91) — which the original 10-week,
> 14-phase, 7-service plan structurally could not guarantee, because
> its own highest-risk work was scheduled in the second-to-last week.

---

## PART 06 — Demo & Presentation Blueprint (Trimmed)

### 6.1 — Demo Storyline

Problem (20s) → Architecture overview (40s) → Live anomaly detection
(90s) → Live incident analysis with Correlation Guard shown rejecting
a claim (90s) → Self-healing gates shown passing/failing (45s) →
Deployment risk demo (45s) → Honest failure story from building it
(60s) → What you'd add in v2 and why you didn't build it now (30s).

**~7 minutes total**, not v1's ~9. Shorter, denser, no segment
dependent on a system (React Flow, RL dashboard) that doesn't exist
anymore.

> **The most important addition:** end on the v2 section, stated
> honestly — "I did not build RAG-based retrieval because my corpus
> size doesn't justify vector search yet, and I did not build RL
> because a lookup table isn't RL and I'd rather say that than call it
> something it's not." That line does more for a FAANG interview score
> than any of the cut features would have.

### 6.3 — Interview Prep — Updated Expected Questions

| Expected Question | Prepared Answer Direction |
|---|---|
| Why LangGraph with only 3 nodes — why not more agents? | A single well-prompted analysis node handles infrastructure/application/deployment context in one structured call. Fan-out to separate specialist agents adds latency and state-sync complexity without adding accuracy at this scale — I'd add it back if I had evidence one node was missing signal a specialist would catch. |
| Is your RL signal actually reinforcement learning? | No — it's a static success counter used as Gate 3's historical-evidence check. I chose not to call it RL because it isn't; a lookup table with a count threshold is not a learned policy. |
| Why no vector search / RAG for episodic memory? | Corpus size in a demo is a few dozen incidents at most. HNSW and cosine similarity exist to solve retrieval at scale I don't have. A filtered SQL query on incident fingerprint does the same job honestly at this size. |
| What would you add first in v2? | Whichever of forecasting, real embedding retrieval, or a second analysis node the demo data actually showed a gap for — not all three preemptively. |

---

## PART 07 — Appendices

### 7.2 — Decision Log (New Entries)

| Date | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| v2 revision | Overall scope | 4 services, 2 ML models, 3-node LLM pipeline | v1's 7 services, 3 ML models, 5-node pipeline + RAG + RL | Solo 7-week build; every cut item scored high on "sounds impressive," low on "survives a follow-up question" |
| v2 revision | Gate 3 implementation | Static COUNT query on `remediations` | Dedicated RL signal table with success_rate recompute | Same functional gate, no misleading "RL" framing, no extra table/task to maintain |
| v2 revision | Episodic retrieval | Direct SQL filter on fingerprint | pgvector HNSW cosine similarity | Corpus size (dozens of rows) doesn't justify ANN infrastructure — filtered SQL is the honest tool at this scale |
| v2 revision | Ingestion async layer | Plain Celery task queue | Redis Streams + consumer groups | Streams solves a throughput problem (thousands of events/sec) this project's actual demo volume doesn't have |
| Phase 1 audit | Route module naming vs Blueprint 2.1 architecture modules | `deployments/` → `deployment_risk/`, `incidents/` → `incident_analysis/`; `auth/`, `chaos/`, `services/` kept as resource-based names | Renaming all five route folders to match 2.1's six module names (`ingestion`, `anomaly_detection`, `deployment_risk`, `incident_analysis`, `healing`, `observability`), or leaving all five unchanged and letting Phase 5-9 invent parallel logic-module folders | 2.1 lists six architecture modules; three of the five existing route folders (`auth`, `chaos`, `services`) have no 1:1 match in that list — `auth` is cross-cutting infra, `chaos` is a Phase 11 testing tool, and `services` covers both service CRUD (not a 2.1 module) and metric ingestion (which IS `ingestion`, but can't be split out without breaking the locked `/services/:id/metrics` URL contract in 2.4). Only `deployments`→`deployment_risk` and `incidents`→`incident_analysis` are genuine 1:1 matches, so only those two were renamed. Forcing a rename on the other three would invent module names the blueprint never specified. The risk of doing nothing: Phase 5-9 building `ingestion`/`anomaly_detection`/`healing`/`observability` as new folders alongside `services`/`deployments`/`incidents` would create two parallel folder trees (routes vs logic) — the exact type-based split R-15 forbids, just inverted. |

### 7.3 — Tech Debt Log (Carried Forward, Trimmed)

| ID | Description | Fix Plan | Priority |
|---|---|---|---|
| DEBT-001 | No forecasting model | Add Prophet in v2 only if a real use case for 30-min-ahead prediction appears in practice | Low |
| DEBT-002 | Episodic retrieval is SQL-filtered, not embedding-based | Migrate to pgvector once corpus exceeds ~500 incidents and filtered SQL stops being precise enough | Low |
| DEBT-003 | Gate 3 uses a static counter, not a learned success rate | Revisit only if real remediation volume (hundreds of executions) makes a learned weighting meaningfully different from a raw count | Low |
| DEBT-004 | Single LangGraph analysis node handles all context types | Split into specialist nodes only if demo/testing shows the single node missing signal a specialist would catch | Low |

---

**End of v2. This is the version to paste into AI sessions per Rule
R-01 going forward — not v1.**
