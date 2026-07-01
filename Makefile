# Makefile for development and deployment

.PHONY: help install dev test docker-build docker-up docker-down migrate lint format

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev          - Start development environment"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker stack"
	@echo "  make docker-down  - Stop Docker stack"
	@echo "  make migrate      - Run database migrations"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"

install:
	@echo "Installing dependencies..."
	for dir in services/*/; do cd "$$dir" && pip install -r requirements.txt && cd ../..; done

dev:
	@echo "Starting development environment..."
	docker-compose -f infra/docker-compose.yml up -d
	@echo "Waiting for services to be ready..."
	sleep 10
	make migrate
	@echo "Development environment ready!"

test:
	@echo "Running tests..."
	pytest tests/ -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v

docker-build:
	@echo "Building Docker images..."
	docker build -t investment-platform/api-gateway:latest services/api-gateway/
	docker build -t investment-platform/ingestion-agent:latest services/ingestion-agent/
	docker build -t investment-platform/document-intel-agent:latest services/document-intel-agent/
	docker build -t investment-platform/research-rag-agent:latest services/research-rag-agent/
	docker build -t investment-platform/investment-scorer:latest services/investment-scorer/
	docker build -t investment-platform/portfolio-analytics:latest services/portfolio-analytics-agent/
	docker build -t investment-platform/risk-monitor-agent:latest services/risk-monitor-agent/
	docker build -t investment-platform/briefing-generator:latest services/briefing-generator/
	docker build -t investment-platform/compliance-governance:latest services/compliance-governance/

docker-up:
	docker-compose -f infra/docker-compose.yml up -d
	@echo "Stack started. Waiting for services..."
	sleep 15
	make migrate

docker-down:
	docker-compose -f infra/docker-compose.yml down

migrate:
	@echo "Running database migrations..."
	python scripts/migrations/run_migrations.py

lint:
	@echo "Running linters..."
	flake8 services/ --max-line-length=120
	pylint services/ --disable=all --enable=E

format:
	@echo "Formatting code..."
	black services/ --line-length=120
	isort services/

clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.coverage' -delete
