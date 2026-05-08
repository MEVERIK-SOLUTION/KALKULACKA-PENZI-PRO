#!/bin/bash
# Run the Pension Calculator application

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Starting Pension Calculator API..."
echo "API will be available at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo "Frontend at file://$PROJECT_DIR/frontend/index.html"
echo ""

# Run with entry point (loads .env)
./venv/bin/python run.py
