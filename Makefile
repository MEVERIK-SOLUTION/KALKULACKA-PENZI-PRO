.PHONY: help setup install run test lint clean docker-build docker-up docker-down

help:
	@echo "KALKULAČKA PENZÍ PRO - Dev Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup & Install:"
	@echo "  make setup          - Initialize virtual environment"
	@echo "  make install        - Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run            - Start API server"
	@echo "  make test           - Run unit tests"
	@echo "  make lint           - Run pylint checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Remove cache & build files"
	@echo "  make venv-clean     - Remove virtual environment"
	@echo ""

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

install: setup
	@echo "Installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

run:
	@echo "Starting API server..."
	. venv/bin/activate && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

test:
	@echo "Running unit tests..."
	. venv/bin/activate && pytest tests/unit/ -v --tb=short

test-coverage:
	@echo "Running tests with coverage..."
	. venv/bin/activate && pytest tests/unit/ --cov=src/backend --cov-report=html --cov-report=term

lint:
	@echo "Running pylint..."
	. venv/bin/activate && pylint src/backend/engine/ --disable=all --enable=W,E || true

lint-strict:
	@echo "Running strict pylint (score > 8.0)..."
	. venv/bin/activate && pylint src/backend/engine/ --fail-under=8.0

docker-build:
	@echo "Building Docker image..."
	docker build -t pension-calculator-api:0.1.0 .

docker-up: docker-build
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f api

clean:
	@echo "Cleaning cache & build files..."
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name '*.pyc' -delete || true
	rm -rf .pytest_cache/ .mypy_cache/ htmlcov/ dist/ build/ || true
	rm -rf .coverage || true

venv-clean:
	@echo "Removing virtual environment..."
	rm -rf venv/

fresh-install: venv-clean install
	@echo "Fresh installation complete!"

.PHONY: help setup install run test lint clean docker-build docker-up docker-down
