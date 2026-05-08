#!/bin/bash
# Deploy Pension Calculator API to Azure Container Apps
# Vyžaduje: az login, Azure subscription

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# --- Konfigurace ---
RESOURCE_GROUP="${AZURE_RG:-pension-api-rg}"
LOCATION="${AZURE_LOCATION:-westeurope}"
ENVIRONMENT_NAME="${AZURE_ENV:-pension-api-env}"
APP_NAME="${AZURE_APP:-pension-api}"
REGISTRY_NAME="${AZURE_REGISTRY:-pensionapiregistry}"
IMAGE_NAME="${REGISTRY_NAME}.azurecr.io/${APP_NAME}:latest"

echo "🚀 Deploy Pension Calculator API do Azure Container Apps"
echo "========================================================"
echo ""

# 1. Kontrola Azure CLI
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI není nainstalovaný."
    echo "   Nainstaluj: brew install azure-cli"
    exit 1
fi

# 2. Kontrola přihlášení
ACCOUNT=$(az account show --query name -o tsv 2>/dev/null || true)
if [ -z "$ACCOUNT" ]; then
    echo "🔑 Přihlašuji se do Azure..."
    az login
else
    echo "✅ Přihlášen jako: $ACCOUNT"
fi

# 3. Vytvoření Resource Group
echo ""
echo "📦 Vytvářím Resource Group: $RESOURCE_GROUP"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

# 4. Vytvoření Azure Container Registry
echo "📦 Vytvářím Container Registry: $REGISTRY_NAME"
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$REGISTRY_NAME" \
    --sku Basic \
    --admin-enabled true \
    --output none 2>/dev/null || echo "   (již existuje)"

# 5. Build + Push Docker image
echo ""
echo "🐳 Buildím Docker image..."
docker build -t "$APP_NAME:latest" .

echo "🐳 Taguju a pushuji do ACR..."
docker tag "$APP_NAME:latest" "$IMAGE_NAME"
az acr login --name "$REGISTRY_NAME"
docker push "$IMAGE_NAME"

# 6. Nasazení Bicep
echo ""
echo "🧩 Nasazuji Bicep šablonu..."
API_KEYS="${API_KEYS:-}"
DATABASE_URL="${DATABASE_URL:-}"

if [ -z "$API_KEYS" ]; then
    echo "⚠️  API_KEYS není nastaveno. Generuji náhodný klíč..."
    API_KEYS="ak-$(openssl rand -hex 16)"
    echo "   Vygenerovaný klíč: $API_KEYS"
fi

az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file "$PROJECT_DIR/infra/main.bicep" \
    --parameters \
        containerImage="$IMAGE_NAME" \
        apiKeys="$API_KEYS" \
        databaseUrl="$DATABASE_URL" \
        corsOrigins='["https://kalkulacka-penzi-pro.pages.dev","https://bd607bd0.kalkulacka-penzi-pro.pages.dev"]' \
    --output table

# 7. Získání veřejné URL
echo ""
echo "🌐 Získávám veřejný endpoint..."
FQDN=$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_NAME" \
    --query properties.configuration.ingress.fqdn \
    -o tsv)

echo ""
echo "✅ Hotovo!"
echo "   API URL: https://$FQDN"
echo "   Docs:    https://$FQDN/docs"
echo "   Health:  https://$FQDN/health"
echo ""
echo "💡 Pro ověření:"
echo "   curl -H 'X-API-Key: $API_KEYS' https://$FQDN/health"
