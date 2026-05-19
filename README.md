# KALKULAČKA PENZÍ PRO

**Expertní výpočetní engine pro analýzu a optimalizaci českých státních důchodů.**

Tento repozitář obsahuje výpočetní jádro první aplikace plánovaného ekosystému finančních nástrojů. Cílem je přejít od jednorázového státního výpočtu k plnohodnotné, persistentní správě důchodového aktiva.

---

## Co to řeší

Státní nástroje (ePortál ČSSZ, aplikace IDA) jsou **stateless** — data se neukládají, výsledky se neoptimalizují, skryté rezervy zůstávají neobjeveny. Průměrný občan přichází o ~10 % výše důchodu kvůli neúplné evidenci (studium před 1996, vojna, péče o dítě, chybějící OSVČ doplatky).

Tento engine implementuje legislativu zákona č. 155/1995 Sb. v aktuální verzi pro rok 2026, včetně:

- **Decision Paradox** — doložení náhradní doby může *snížit* důchod kvůli diluci osobního vyměřovacího základu (OVZ). Engine to detekuje a doporučuje správný postup.
- **Optimalizace OSVČ** — simulace dopadu dobrovolných doplatků na pojistném v posledních letech před důchodem.
- **Předčasný důchod** — 3-stupňová progresivní redukce (0,9 % / 1,2 % / 1,5 % za každých 90 dní).
- **Důchodový věk žen** — závislý na počtu vychovaných dětí.

---

## Architektura výpočetního jádra

Legislativní konstanty jsou striktně odděleny od logiky — změna parametrů (VVZ, redukční hranice) se provádí výhradně přes `config/legislative_2026.yaml` bez zásahu do zdrojového kódu.

```
src/backend/engine/
├── ovz_calculator.py          # Osobní vyměřovací základ
├── reduction_engine.py        # Redukční meze (jediný zdroj pravdy)
├── paradox_resolver.py        # Detekce Decision Paradox
├── pension_calculator.py      # Výpočet starobního a předčasného důchodu
└── retirement_age_calculator.py  # Důchodový věk (muži i ženy dle dětí)
```

**Klíčové parametry 2026:**
| Parametr | Hodnota |
|---|---|
| Accrual Rate | 1,495 % / rok (klesá o 0,005 % ročně) |
| Redukční hranice | 21 331 Kč (99 % zápočet) |
| Základní výměra | 4 900 Kč |
| Minimální důchod | 9 800 Kč |

---

## Stack (dev/pilot setup)

| Vrstva | Technologie |
|---|---|
| Frontend | Cloudflare Pages — Vue 3, TypeScript, Vite, Tailwind CSS, Pinia |
| API / Engine | Google Cloud Run — Python 3.11, FastAPI, Pydantic |
| Databáze | Neon.tech — serverless PostgreSQL, SQLAlchemy + Alembic |
| Blob storage | Cloudflare R2 — IOLDP dokumenty, PDF reporty |
| Cache | Upstash Redis |
| Auth | Firebase Auth + Custom Claims (RBAC) |
| Secrets | Google Secret Manager |
| Monitoring | Prometheus + Grafana + Sentry |
| CI/CD | GitHub Actions |

Setup je dimenzovaný na pilotní provoz (≤1 000 req/měsíc, ≤100 DAU, ≤10 GB/den) s prakticky nulovými provozními náklady — všechny vrstvy v rámci free tier.

---

## Nasazení

| Komponenta | URL |
|---|---|
| Frontend | `https://kalkulacka-penzi-pro.pages.dev` |
| API | `https://pension-api-production-e782.up.railway.app` |
| API Docs (Swagger) | `https://pension-api-production-e782.up.railway.app/docs` |

---

## Spuštění lokálně

```bash
# Backend (Docker)
docker compose up

# Frontend
cd frontend && npm install && npm run dev
```

Proměnné prostředí viz `.env.example`.

---

## API Endpoints

| Endpoint | Popis |
|---|---|
| `POST /calculate-pension` | Výpočet starobního důchodu |
| `POST /calculate-ovz` | Výpočet osobního vyměřovacího základu |
| `POST /resolve-paradox` | Detekce a řešení Decision Paradox |
| `POST /calculate-early-retirement` | Výpočet předčasného důchodu |
| `POST /calculate-retirement-age` | Výpočet důchodového věku |
| `GET /health` | Health check (s Redis stavem) |

---

## Kontext v ekosystému

Tento engine je **první vrstvou** plánovaného tříúrovňového portálu:

1. **Veřejná zóna** — edukace, orientační kalkulačka (Shadow Calculator)
2. **Advisor Branch** — CRM pro finančního poradce, IOLDP OCR, hromadná správa klientů
3. **Client Space** — persistentní klientský portál se správou důchodového aktiva

Portál sám o sobě bude jedním z nástrojů v rámci širšího ekosystému finančního poradenství.

---

## Stav projektu

Viz [TODO_ROADMAP.md](TODO_ROADMAP.md) a [WORK_DIARY.md](WORK_DIARY.md).

**Dokončeno:** Výpočetní jádro (100 %), API (MVP), Frontend Vue 3 (základní), DB integrace, CI/CD  
**Probíhá:** Historie výpočtů (CRUD), Retirement Age kalkulačka (frontend komponenta)  
**Plánováno:** AI agent (ChromaDB + RAG), Voice interface, Export PDF/CSV, Comparison Tool
