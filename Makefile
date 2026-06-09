# Makefile
#
# Purpose:
# Entry point for monorepo development, testing, and container deployment.
#
# Dependencies:
# make, docker, docker-compose, npm, python3
#
# Usage:
# Run: make <target> (e.g. make docker-up)
#
# Notes:
# Validated for macOS, Linux, and Windows WSL.
#
# Future Improvements:
# - Add auto-versioning pre-release hook calls

.PHONY: help install build test lint docker-up docker-down

help:
	@echo "Pinterest MCP Development Automation Target List:"
	@echo "  install      - Install Node.js workspaces and Python environment dependencies"
	@echo "  build        - Compile TypeScript workspace packages"
	@echo "  test         - Run linting and pytests"
	@echo "  lint         - Check code styles with ruff/flake8 and eslint"
	@echo "  docker-up    - Build and launch Postgres, Redis, Qdrant and Core-API containers"
	@echo "  docker-down  - Shut down running dev containers and delete local data volumes"

install:
	npm install
	poetry install

build:
	npm run build

test:
	poetry run pytest

lint:
	npm run lint
	poetry run ruff check .

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down -v

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Integrate automated database seed target loaders
# 2. Add local SSL dev cert generation targets
#
# ============================================
