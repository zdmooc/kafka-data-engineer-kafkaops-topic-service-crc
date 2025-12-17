SHELL := /bin/bash

.PHONY: help up down logs api shell lint test fmt

help:
	@echo "Targets:"
	@echo "  up     - Start local stack (Kafka + UI + Topic-as-a-Service)"
	@echo "  down   - Stop local stack"
	@echo "  logs   - Tail logs"
	@echo "  api    - Run Topic-as-a-Service locally (venv required)"
	@echo "  shell  - Open a shell inside the topic service container"
	@echo "  lint   - Lint (ruff)"
	@echo "  fmt    - Format (ruff)"
	@echo "  test   - Run tests (pytest)"

up:
	docker compose -f infra/docker-compose/compose.yaml up -d --build

down:
	docker compose -f infra/docker-compose/compose.yaml down -v

logs:
	docker compose -f infra/docker-compose/compose.yaml logs -f --tail=200

shell:
	docker compose -f infra/docker-compose/compose.yaml exec topic-service /bin/sh

api:
	cd services/topic-as-a-service && \
		python -m venv .venv && . .venv/bin/activate && \
		pip install -U pip && pip install -e ".[dev]" && \
		uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload

lint:
	cd services/topic-as-a-service && \
		python -m venv .venv && . .venv/bin/activate && \
		pip install -U pip && pip install -e ".[dev]" && \
		ruff check .

fmt:
	cd services/topic-as-a-service && \
		python -m venv .venv && . .venv/bin/activate && \
		pip install -U pip && pip install -e ".[dev]" && \
		ruff format .

test:
	cd services/topic-as-a-service && \
		python -m venv .venv && . .venv/bin/activate && \
		pip install -U pip && pip install -e ".[dev]" && \
		pytest -q
