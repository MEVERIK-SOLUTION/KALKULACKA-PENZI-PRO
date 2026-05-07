# KALKULAČKA PENZÍ PRO - Secrets Management Guide

> Bezpečné ukládání API tokenů a citlivých dat pro GitHub, Cloudflare, Railway a další služby

---

## 🔐 Cloudflare Wrangler Setup

### Krok 1: Získat Cloudflare API Token

1. Přejdi na https://dash.cloudflare.com/profile/api-tokens
2. Klikni "Create Token"
3. Vyberi "Custom token" (nebo Edit Cloudflare Workers - pre-made)
4. Přidej oprávnění:
   - **Permissions:**
     - `account.access:read`
     - `workers.scripts:read`
     - `workers.scripts:write`
     - `workers.routes:read`
     - `workers.routes:write`
     - `pages:read`
     - `pages:write`
     - `d1:read`
     - `d1:write`
   - **Resources:** All accounts, All zones

5. Vygeneruj token a **ulož si ho** (v mailu ti pošlu)

### Krok 2: Secure Storage pro Wrangler

Máš 2 možnosti:

#### Option A: Environment Variables (LOCAL DEV)
```bash
# V lokálním terminálu (NIKDY na GitHub!)
export CLOUDFLARE_API_TOKEN="tvoj-token-here"
export CLOUDFLARE_ACCOUNT_ID="tvoj-account-id"
export CLOUDFLARE_EMAIL="tvuj-email@example.com"
```

#### Option B: Wrangler Secrets (PRODUCTION)
```bash
# Ulož token v Wranglerovi (encrypted)
wrangler secret put CLOUDFLARE_API_TOKEN
# Paste token, Enter, Ctrl+D

wrangler secret put D1_DATABASE_TOKEN
wrangler secret put R2_BUCKET_TOKEN
```

### Krok 3: GitHub Secrets (CI/CD Deployment)

1. V GitHub repo: **Settings → Secrets and variables → Actions**
2. Přidej nové secrets:
   - `CLOUDFLARE_API_TOKEN` - tvůj token
   - `CLOUDFLARE_ACCOUNT_ID` - ID z profilu
   - `CLOUDFLARE_EMAIL` - email účtu
   - `CF_PROJECT_NAME` - "pension-calculator-pro"

3. GitHub Actions workflows k tomu pak přistoupí jako:
   ```yaml
   env:
     CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
   ```

---

## 🚂 Railway.com Setup

### Krok 1: Vytvořit Railway Account
1. https://railway.app/ → Sign up
2. Vytvoř project "pension-calculator-pro"
3. Vytvoř environment (dev, prod)

### Krok 2: Railway API Token
1. Na https://railway.app/account/tokens
2. "Create new token" → zkopíruj
3. Ulož v GitHub Secrets jako `RAILWAY_TOKEN`

### GitHub Secret:
```
RAILWAY_TOKEN=your-railway-api-token
```

---

## 🔑 GitHub Secrets Konfigurace

### Kompletní seznam co vložit:

| Secret Name | Typ | Kde získat |
|-------------|-----|-----------|
| `CLOUDFLARE_API_TOKEN` | Master Token | Cloudflare Dashboard |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID | Cloudflare Dashboard (pravý sloupec) |
| `CLOUDFLARE_EMAIL` | Email | Tvůj CF email |
| `RAILWAY_TOKEN` | API Token | Railway.app Account |
| `GOOGLE_CLIENT_ID` | OAuth 2.0 | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth 2.0 | Google Cloud Console |
| `MICROSOFT_CLIENT_ID` | OAuth 2.0 | Azure Entra ID |
| `MICROSOFT_CLIENT_SECRET` | OAuth 2.0 | Azure Entra ID |
| `APPLE_BUNDLE_ID` | Service ID | Apple Developer |
| `SEZNAM_CLIENT_ID` | OAuth 2.0 | Seznam API portal |
| `SEZNAM_CLIENT_SECRET` | OAuth 2.0 | Seznam API portal |

---

## 📝 Přístupový Prostor pro Tokeny

Vytvořím ti **Cloudflare Workers KV Namespace** nebo **D1 table** pro bezpečné předávání tokenů.

### Option: GitHub Secret + Environment Variable

Jakmile mi dáš token, vložím do GitHub Secrets takto:

```bash
# Lokálně:
gh secret set CLOUDFLARE_API_TOKEN --body "tvoj-token-2024..."
```

### Option: Wrangler .dev.vars File (LOCAL ONLY)

```toml
# wrangler.toml
[env.development.vars]
DATABASE_URL = "..."
NVIDIA_API_KEY = "..."

# .dev.vars (NIKDY na GitHub!)
CLOUDFLARE_API_TOKEN=token-here
D1_DATABASE_ID=d1-id-here
R2_BUCKET_NAME=bucket-name
```

---

## 🛡️ Security Best Practices

1. **NIKDY** nedávej `.env` do gitu
2. **VŽDY** použi `.env.example` s placeholdery
3. Tokeny s časovým limitem (30 dní) - zkontroluj expiraci
4. Minimální oprávnění (least privilege)
5. Rotuj tokeny každé 3-6 měsíců
6. Loguj přístup v Cloudflare Analytics

---

## ⚙️ Automation Flow

```
Ty vytvoříš API token
    ↓
Vložíš do GitHub Secrets
    ↓
GitHub Actions načte secret
    ↓
Wrangler se autentizuje
    ↓
Deploy na Cloudflare Pages/Workers
```

---

## 📞 Postup Setup

1. **Ty**: Vygeneruješ Cloudflare API token
2. **Ty**: Vložíš do bezpečného prostředku (poslat mi)
3. **Já**: Vložím do GitHub Secrets
4. **Já**: Vytvořím Wrangler config
5. **Automaticky**: GitHub Actions pushe změny na Cloudflare

---

**Čekám na tvý tokeny! Oznám mi, až je budeš mít.**
