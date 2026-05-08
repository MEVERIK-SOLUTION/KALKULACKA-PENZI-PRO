#!/bin/bash
# Build Docker image s podporou pro symlink cz_pension_api
# cz_pension_api v PensionCalculator/ je symlink na Vývoj a rešerše s OpenCode/cz_pension_api
# Docker neumí follow symlinky mimo build context, proto kopírujeme do /tmp.

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

BUILD_DIR="/tmp/pension-docker-build"
TAG="${1:-pension-calculator-api:latest}"

echo "🐳 Buildím Docker image: $TAG"
echo ""

# Vytvořit čistý build context bez symlinků
echo "📦 Připravuji build context v $BUILD_DIR ..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Kopírovat všechny soubory kromě symlinků
for item in "$PROJECT_DIR"/* "$PROJECT_DIR"/.[!.]*; do
    basename_item=$(basename "$item")
    # Přeskočit venv, .git, cache adresáře
    case "$basename_item" in
        venv|.git|__pycache__|*.pyc|.pytest_cache|.mypy_cache|.ruff_cache|node_modules|.DS_Store)
            continue ;;
    esac
    if [ -L "$item" ]; then
        # Symlink - zkopírovat skutečný obsah
        target=$(readlink "$item")
        if [[ "$target" = /* ]]; then
            cp -RL "$item" "$BUILD_DIR/$basename_item" 2>/dev/null || true
        else
            # Relativní symlink - vyřešit vůči PROJECT_DIR
            resolved="$PROJECT_DIR/$target"
            if [ -e "$resolved" ]; then
                cp -RL "$resolved" "$BUILD_DIR/$basename_item" 2>/dev/null || true
            fi
        fi
    elif [ -e "$item" ]; then
        cp -R "$item" "$BUILD_DIR/$basename_item" 2>/dev/null || true
    fi
done

echo "✅ Build context připraven."
echo ""

# Postavit Docker image
docker build -t "$TAG" -f "$BUILD_DIR/Dockerfile" "$BUILD_DIR"

echo ""
echo "✅ Image $TAG postaven."
echo ""
echo "💡 Spuštění:"
echo "   docker run -p 8000:8000 $TAG"
echo "   docker compose -f docker-compose.prod.yml up -d"
