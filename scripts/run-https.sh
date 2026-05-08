#!/bin/bash
# Run Pension Calculator API with HTTPS (lokální vývoj)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

CERT_FILE="${SSL_CERT_PATH:-./certs/cert.pem}"
KEY_FILE="${SSL_KEY_PATH:-./certs/key.pem}"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "CHYBA: SSL certifikáty nenalezeny."
    echo "Vygeneruj je pomocí:"
    echo "  make certs"
    exit 1
fi

echo "Starting Pension Calculator API with HTTPS..."
echo "API: https://localhost:8443"
echo "Docs: https://localhost:8443/docs"
echo ""

./venv/bin/uvicorn api.main:app \
    --host 0.0.0.0 \
    --port 8443 \
    --ssl-certfile "$CERT_FILE" \
    --ssl-keyfile "$KEY_FILE" \
    --reload
