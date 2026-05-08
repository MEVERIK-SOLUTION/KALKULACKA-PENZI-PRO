.PHONY: help setup install run test lint mypy tox security audit clean

help:
	@echo "Pension Calculator - Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup & Install:"
	@echo "  make setup          - Create virtual environment"
	@echo "  make install        - Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run            - Start API server (uvicorn)"
	@echo "  make run-https      - Start API with HTTPS (port 8443)"
	@echo "  make test           - Run all tests with pytest"
	@echo "  make test-api       - Run cz_pension_api tests"
	@echo "  make test-auth      - Run only security/auth tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make lint           - Run ruff linter"
	@echo "  make lint-fix       - Run ruff with auto-fix"
	@echo "  make mypy           - Run mypy type checker"
	@echo "  make tox            - Run tox (all Python versions)"
	@echo ""
	@echo "Security:"
	@echo "  make audit          - Run pip-audit (dependency CVEs)"
	@echo "  make safety         - Run safety scan"
	@echo "  make certs          - Generate HTTPS certs via mkcert"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Remove cache & build files"
	@echo "  make venv-clean     - Remove virtual environment"

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

install: setup
	@echo "Installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

run:
	@echo "Starting API server..."
	. venv/bin/activate && python run.py

run-https:
	@echo "Starting API server with HTTPS..."
	. venv/bin/activate && python run.py --port 8443 --ssl

test:
	@echo "Running all tests..."
	. venv/bin/activate && python -m pytest tests/ -v --tb=short

test-api:
	@echo "Running cz_pension_api tests..."
	. venv/bin/activate && python -m pytest "../Vývoj a rešerše s OpenCode/cz_pension_api/tests" -v --tb=short

test-auth:
	@echo "Running security/auth tests..."
	. venv/bin/activate && python -m pytest tests/auth/ -v --tb=short -m security

test-cov:
	@echo "Running tests with coverage..."
	. venv/bin/activate && python -m pytest tests/ --cov=src/backend --cov=api --cov-report=html --cov-report=term

lint:
	@echo "Running ruff linter..."
	. venv/bin/activate && ruff check src/ tests/ api/

lint-fix:
	@echo "Running ruff with auto-fix..."
	. venv/bin/activate && ruff check --fix src/ tests/ api/

mypy:
	@echo "Running mypy type checker..."
	. venv/bin/activate && mypy src/ api/ --ignore-missing-imports || true

tox:
	@echo "Running tox..."
	. venv/bin/activate && tox || true

audit:
	@echo "Running pip-audit (dependency CVE scan)..."
	. venv/bin/activate && pip-audit --desc

safety:
	@echo "Running safety scan..."
	. venv/bin/activate && safety scan

certs:
	@echo "Generating HTTPS certificates via mkcert..."
	@mkdir -p certs
	@mkcert -install 2>/dev/null || true
	mkcert -key-file ./certs/key.pem -cert-file ./certs/cert.pem localhost 127.0.0.1 ::1

docker-build:
	@echo "Building Docker image..."
	docker build -t pension-calculator-api:latest .

docker-up: docker-build
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f api

docker-prod-up:
	@echo "Starting production containers..."
	docker-compose -f docker-compose.prod.yml up -d

docker-prod-down:
	@echo "Stopping production containers..."
	docker-compose -f docker-compose.prod.yml down

docker-prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f api

# --- Monitoring ---

mon-up:
	@echo "Starting monitoring stack..."
	docker-compose -f docker-compose-monitoring.yml up -d

mon-down:
	@echo "Stopping monitoring stack..."
	docker-compose -f docker-compose-monitoring.yml down

mon-logs:
	docker-compose -f docker-compose-monitoring.yml logs -f

mon-test:
	@echo "Testing monitoring endpoints..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana:    http://localhost:3001 (admin/admin)"
	@echo "Loki:       http://localhost:3100/ready"
	@echo "API:        http://localhost:8000/metrics"

# --- Deployment ---

ngrok-tunnel:
	@echo "Starting ngrok tunnel..."
	./scripts/ngrok.sh

cloudflare-tunnel:
	@echo "Starting Cloudflare Tunnel..."
	./scripts/cloudflare-tunnel.sh

deploy-azure:
	@echo "Deploying to Azure..."
	./scripts/deploy-azure.sh

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
