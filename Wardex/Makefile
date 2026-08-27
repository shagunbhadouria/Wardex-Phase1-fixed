.PHONY: help dev monitoring build down test lint format seed clean

help:
	@echo "SentinelAI Developer Commands:"
	@echo "  make dev          Start 4 core services (api, worker, postgres, redis)"
	@echo "  make monitoring   Start Prometheus and Grafana stack"
	@echo "  make build        Build Docker images"
	@echo "  make down         Stop all Docker Compose services"
	@echo "  make test         Run pytest test suite"
	@echo "  make lint         Run flake8, isort, and mypy checks"
	@echo "  make format       Auto-format code with black and isort"
	@echo "  make seed         Seed database with demo dataset"
	@echo "  make clean        Remove cache, build, and bytecode artifacts"
	@echo ""
	@echo "  (make train-models returns in Phase 6 — ML models don't exist yet)"

dev:
	docker compose up

monitoring:
	docker compose -f docker-compose.monitoring.yml up -d

build:
	docker compose build

down:
	docker compose down
	docker compose -f docker-compose.monitoring.yml down

test:
	docker compose exec sentinelai-api pytest app   

lint:
	docker compose exec sentinelai-api flake8 app
	docker compose exec sentinelai-api isort --check-only app
	docker compose exec sentinelai-api mypy app

format:
	black app
	isort app

seed:
	python -m app.shared.seed

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache
