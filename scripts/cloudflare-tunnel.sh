#!/bin/bash
# Spustit Cloudflare Tunnel pro Pension Calculator API
# Vyžaduje: cloudflared login + cloudflared tunnel create

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

TUNNEL_NAME="${CF_TUNNEL_NAME:-pension-api}"
TUNNEL_DOMAIN="${CF_TUNNEL_DOMAIN:-}"

if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared není nainstalovaný."
    echo "   Nainstaluj: brew install cloudflared"
    exit 1
fi

# Kontrola zda existuje tunel
if ! cloudflared tunnel list 2>/dev/null | grep -q "$TUNNEL_NAME"; then
    echo ""
    echo "⚠️  Cloudflare Tunnel '$TUNNEL_NAME' neexistuje."
    echo ""
    echo "1. Spusť: cloudflared tunnel login"
    echo "2. Spusť: cloudflared tunnel create $TUNNEL_NAME"
    echo "3. Nastav DNS: cloudflared tunnel route dns $TUNNEL_NAME <domena>"
    echo "4. Pak spusť tento skript znovu"
    echo ""
    exit 1
fi

TUNNEL_ID=$(cloudflared tunnel list | grep "$TUNNEL_NAME" | awk '{print $1}')

echo "🌤 Spouštím Cloudflare Tunnel '$TUNNEL_NAME' (ID: $TUNNEL_ID)..."
echo "   Lokální API: http://localhost:8000"
echo ""

cloudflared tunnel run "$TUNNEL_NAME"
