# KALKULAČKA PENZÍ PRO - API & Služby Roadmap

> Kompletes seznam technologií, tokenů a služeb potřebných pro plný projekt

---

## 📦 Objednaně & Řídící Infrastruktura

### ✅ Již máme
- [x] **GitHub** - Source control + Actions (pro CI/CD)
- [x] **Python 3.11** - Backend runtime
- [x] **FastAPI** - API framework
- [x] **pytest** - Testing framework

### 📋 Potřebuješ objednat / Získat tokeny

---

## 🌐 Frontend & Hosting

### 1. **Cloudflare Pages** (Frontend Hosting)
- **Účel:** Deploy Vue 3/React frontend
- **Konfiguraci:** Wrangler CLI
- **Potřebuje se:** Cloudflare účet + API token
- **Cena:** Free tier (50k requests/den), Pro ($20/měsíc)
- **Co dostat:** 
  - Cloudflare Account ID
  - Cloudflare API Token (Master)
  - Cloudflare Zone ID

### 2. **Cloudflare Workers** (Edge Computing/API Gateway)
- **Účel:** Serverless edge functions, request routing, caching
- **Příklady:** Rate limiting, content security, session management
- **Potřebuje se:** Cloudflare API token
- **Cena:** Free tier (100k requests/den), Paid ($5/měsíc)

### 3. **Cloudflare D1** (Database)
- **Účel:** SQLite edge-native database (vhodné pro GDPR - data v EU)
- **Potřebuje se:** Wrangler setup, API token
- **Cena:** Free tier (3 DB, 5GB storage), Paid scale
- **Co dostat:**
  - D1 Database ID
  - Database token

### 4. **Cloudflare R2** (Object Storage)
- **Účel:** Ukládání IOLDP PDFs, backupů, reports
- **Potřebuje se:** R2 bucket + credentials
- **Cena:** Free tier (10GB/měsíc), Paid $0.015/GB
- **Co dostat:**
  - R2 Bucket name
  - R2 API token + secret

### 5. **Cloudflare Analytics Engine**
- **Účel:** Real-time analytics na calc usage, errors
- **Potřebuje se:** Wrangler config
- **Cena:** Included with Workers

---

## 🔐 Authentication & Authorization

### 6. **Google OAuth 2.0**
- **Účel:** "Sign in with Google" button
- **Konfig:** Google Cloud Console
- **Cena:** Free
- **Co dostat:**
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - Redirect URI: `https://pension-calculator-pro.app/callback/google`

### 7. **Microsoft Entra ID** (Azure AD)
- **Účel:** "Sign in with Microsoft" + iCloud (via Apple)
- **Konfig:** Azure Portal → App registrations
- **Cena:** Free (with Azure subscription)
- **Co dostat:**
  - `MICROSOFT_TENANT_ID`
  - `MICROSOFT_CLIENT_ID`
  - `MICROSOFT_CLIENT_SECRET`
  - Redirect URI: `https://pension-calculator-pro.app/callback/microsoft`

### 8. **Apple Sign-In** (via Entra ID nebo Firebase)
- **Účel:** "Sign in with iCloud"
- **Konfig:** Apple Developer account + Services ID
- **Cena:** Free (s Apple Developer membership $99/rok)
- **Co dostat:**
  - `APPLE_TEAM_ID`
  - `APPLE_SERVICE_ID`
  - `APPLE_KEY_ID`
  - Certificate (P8 file)

### 9. **Seznam.cz OAuth** (Česká alternativa)
- **Účel:** "Přihlaš se se Seznamem"
- **Konfig:** Seznam Partner Portal
- **Cena:** Free
- **Co dostat:**
  - `SEZNAM_CLIENT_ID`
  - `SEZNAM_CLIENT_SECRET`
  - Redirect URI: `https://pension-calculator-pro.app/callback/seznam`

---

## 🚀 Backend Deployment

### 10. **Railway.com** (Backend Hosting)
- **Účel:** Deploy FastAPI backend, alternativa k Heroku
- **Konfig:** Git push → auto deploy
- **Cena:** Free tier (5GB RAM/měsíc), Paid $5+/měsíc
- **Co dostat:**
  - Railway API Token
  - Project ID

**Alternativy:**
- **Render.com** - Free tier s polospánkem
- **PythonAnywhere** - Python-specific hosting
- **Azure App Service** - Pokud chceš Azure stack

---

## 🤖 AI & ML Services

### 11. **NVIDIA NIM** (Optional - Pro AI features)
- **Účel:** LLM inference na edge (Pension analysis interpretace)
- **Konfig:** Docker containers nebo API
- **Cena:** Free (community) / Paid (enterprise)
- **Co dostat:**
  - NVIDIA API Key
  - Model selection (Llama 2 70B, Mistral, atd.)
  - **Příklady modelů:**
    - `meta/llama2-70b-chat` - Legální interpretace
    - `mistralai/mistral-7b-instruct-v2` - Lehčí variant

**Alternativy:**
- **OpenAI API** - GPT-4 (drahý ale nejlepší)
- **Anthropic Claude** - API (dobrý pro compliance)
- **HuggingFace Inference API** - Open models

---

## 📊 Public Data & APIs (Česko)

### 12. **ČÚZK - Katastrální data API**
- **Účel:** Informace o nemovitostech (v tahu)
- **Konfig:** Public API (bez autentizace)
- **Cena:** Free
- **Endpoint:** https://geoportal.cuzk.cz/
- **Docs:** Dokumentace na webu

### 13. **ČSSZ API** (Czech Social Security Administration)
- **Účel:** Veřejné info o důchodovém systému, vyhlášky
- **Konfig:** XML/JSON endpoints
- **Cena:** Free (veřejný portál)
- **Endpoint:** https://www.cssz.cz/
- **Poznámka:** Není firemní API - webové scraping + dokumenty

### 14. **Národní katalog otevřených dat**
- **Účel:** Czech government open data
- **Konfig:** Public API
- **Cena:** Free
- **Endpoint:** https://data.gov.cz/
- **Docs:** REST API docs na webu

### 15. **Hlídač státu API**
- **Účel:** Transparency - veřejné contracts, lobbying, výběrová řízení
- **Konfig:** REST API s registrací
- **Cena:** Free
- **Endpoint:** https://www.hlidacstatu.cz/api
- **Co dostat:** API Key (zdarma na webu)

### 16. **OpenStreetMap / Mapbox** (Mapy)
- **Účel:** Zobrazení lokálních sociálních služeb, poboček ČSSZ
- **Konfig:** Mapbox GL nebo Leaflet
- **Cena:** Free (Leaflet/OSM), Paid (Mapbox $5+/měsíc)
- **Co dostat:**
  - Mapbox Token (pokud Mapbox)
  - API key

---

## 📧 Communications & Notifications

### 17. **SendGrid / Mailgun** (Email)
- **Účel:** Notifikace, report emaily
- **Cena:** Free (100 emails/den), Paid scale
- **Co dostat:**
  - SendGrid API Key
  - Verified sender

### 18. **Twilio** (SMS - Optional)
- **Účel:** SMS notifikace (2FA, alerts)
- **Cena:** Paid ($0.01-0.50/SMS)
- **Co dostat:**
  - Twilio Account SID
  - Auth Token

---

## 🔒 Security & Monitoring

### 19. **GitHub Secrets Management**
- Cloudflare API Token → `CLOUDFLARE_API_TOKEN`
- Cloudflare Account ID → `CLOUDFLARE_ACCOUNT_ID`
- Railway Token → `RAILWAY_TOKEN`
- Database password → `DATABASE_PASSWORD`

### 20. **Sentry** (Error Tracking - Optional)
- **Účel:** Monitor errors v production
- **Cena:** Free tier (7 days), Paid $29+/měsíc
- **Co dostat:**
  - Sentry DSN key

---

## 📋 Kompletní Checklist - Co ti mám připravit

Prosím ti řekni nebo potvrď:

```
☐ Cloudflare Account Setup
  ☐ Master API Token
  ☐ Account ID
  ☐ Zone ID

☐ Railway.com
  ☐ API Token
  ☐ Project vytvoření

☐ OAuth Providers
  ☐ Google (Client ID + Secret)
  ☐ Microsoft (Client ID + Secret)
  ☐ Apple (Team ID + Service ID)
  ☐ Seznam (Client ID + Secret)

☐ Optional AI
  ☐ NVIDIA NIM API Key (pokud chceš AI)
  ☐ Nebo jiný LLM (OpenAI, Anthropic)

☐ Public APIs
  ☐ Mapbox Token (pokud Mapbox místo OSM)
  ☐ Hlídač státu API Key
  ☐ SendGrid API Key (for emails)
```

---

## 🚀 Pořadí Implementace

### Phase 1: Foundation (Týden 1-2) ✅
- ✅ GitHub + CI/CD (done)
- ✅ Docker setup (done)
- [ ] Cloudflare Pages setup
- [ ] Railway.com deploy

### Phase 2: Frontend (Týden 2-4)
- [ ] Vue 3 scaffolding
- [ ] Authentication setup (Google + Microsoft)
- [ ] UI components library
- [ ] Cloudflare Pages deploy

### Phase 3: Database & Backend (Týden 4-6)
- [ ] D1 schema design
- [ ] User management (JWT)
- [ ] Calculation history storage
- [ ] Railway.com API deploy

### Phase 4: Advanced (Týden 6+)
- [ ] NVIDIA NIM integration
- [ ] Public data API integration
- [ ] Analytics + monitoring
- [ ] E2E tests

---

## 💰 Odhadovaný Měsíční Náklady (Production)

| Služba | Tier | Měsíč |
|--------|------|-------|
| Cloudflare Pages | Pro | $20 |
| Railway.com | Standard | $5-20 |
| Mapbox | Basic | $5 |
| SendGrid | Basic | $10-20 |
| **CELKEM** | | **$40-65** |

**Notes:**
- Free tiers stačí na MVP (100k users/měsíc)
- Škálujeme podle actual usage
- AI services (NVIDIA NIM, OpenAI) se účtují separátně

---

## 📞 Akční Body PRO TEBE

1. **Vygeneruj Cloudflare Master Token** (viz SECRETS.md)
2. **Zaregistruj se na Railway.com** a vygeneruj API token
3. **OAuth Providers** - vygeneruj credentials z Google Console, Azure, Apple
4. **Volitelně** - pokud chceš AI, vygeneruj NVIDIA NIM account

Vše mi vlož do bezpečného prostředku (KeePass, bitwarden, nebo mi poslání přímo).

---

**Status:** Připraven na implementaci  
**Čekám na:** Tvé tokeny a confirmaci verzí služeb
