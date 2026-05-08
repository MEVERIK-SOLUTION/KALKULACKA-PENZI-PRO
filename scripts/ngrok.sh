#!/bin/bash
# Spustit ngrok tunel pro Pension Calculator API
# Vyžaduje: ngrok authtoken (https://dashboard.ngrok.com)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Načíst .env pro API_KEYS
export $(grep -v '^#' .env | xargs)

# Kontrola authtoken
if ! ngrok config check 2>/dev/null; then
    echo ""
    echo "⚠️  ngrok authtoken není nastaven."
    echo ""
    echo "1. Zaregistruj se na https://dashboard.ngrok.com/signup"
    echo "2. Zkopíruj authtoken z https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. Spusť: ngrok config add-authtoken <TOKEN>"
    echo "4. Pak spusť tento skript znovu"
    echo ""
    exit 1
fi

echo "🚇 Spouštím ngrok tunel pro Pension API..."
echo "   Lokální API: http://localhost:8000"
echo "   Veřejný URL: (zobrazí se v ngrok dashboardu)"
echo ""
echo "💡 Pro webové rozhraní ngrok: http://localhost:4040"
echo ""

ngrok http 8000 \
    --domain="${NGROK_DOMAIN:-}" \
    --region="${NGROK_REGION:-eu}" \
    --log=stdout
