# KALKULAČKA PENZÍ PRO 🇨🇿

> Expertní ekosystém pro důchodovou analýzu a optimalizaci (Next-Gen Pension Portal)

**Verze:** 0.1.0-alpha  
**Status:** 🚀 MVP + Engine  
**Licence:** MIT (soukromý repo)

---

## 📋 Přehled projektu

Komplexní platforma pro výpočet a optimalizaci starobních důchodů v ČR podle zákona č. 155/1995 Sb. Systém identifikuje skryté finanční rezervy, které standardní státní nástroje (IDA, ePortál ČSSZ) ignorují.

### Klíčové funkce
- ✅ **OVZ Kalkulator** - Osobní vyměřovací základ (§15 ZDP)
- ✅ **Redukční hranice** - Automatická aplikace redukčních mezí
- ✅ **Paradox Resolver** - Optimalizace náhradních dob
- ✅ **Starobní důchod** - Výpočet + předčasný důchod
- 📋 **E2E testy** - Validace proti MPSV standardům
- 🎨 **Multi-tier UI** - Public | Advisor | Client

---

## 🏗️ Architektura

```
PensionCalculator/
├── api/                           # FastAPI backend
│   └── main.py                   # Endpoints + CORS
├── src/
│   └── backend/
│       ├── api/                  # API layer (budoucí)
│       └── engine/               # Výpočetní jádro ⭐
│           ├── ovz_calculator.py
│           ├── reduction_engine.py
│           ├── paradox_resolver.py
│           └── pension_calculator.py
├── config/
│   └── legislative_2026.yaml     # Parametry zákona
├── frontend/
│   ├── index.html                # MVP SPA (přechod na Vue 3)
│   └── [components/]             # (budoucí)
├── tests/
│   └── unit/                     # 13 testů (pylint 8.78/10)
├── scripts/
│   └── run.sh                    # Dev server
├── requirements.txt              # Závislosti Python
└── README.md                     # Dokumentace
```

---

## 🚀 Spuštění

### Prerequisity
- Python 3.9+
- pip / venv
- Node.js 18+ (pro frontend - budoucí)

### Lokální dev environment

```bash
# 1. Klonovat & vstoupit
cd PensionCalculator

# 2. Virtuální prostředí
python3 -m venv venv
source venv/bin/activate

# 3. Instalace závislostí
pip install -r requirements.txt

# 4. Spuštění
./scripts/run.sh
```

**API bude na:** http://localhost:8000  
**Swagger docs:** http://localhost:8000/docs  
**Frontend (MVP):** Otevři `frontend/index.html` v prohlížeči

---

## 📡 API Endpoints

| Endpoint | Metoda | Popis |
|----------|--------|-------|
| `/calculate-pension` | POST | Výpočet starobního důchodu |
| `/calculate-early-retirement` | POST | Předčasný důchod (redukce) |
| `/calculate-ovz` | POST | Osobní vyměřovací základ |
| `/resolve-paradox` | POST | Optimalizace náhradních dob |

Příklad:
```bash
curl -X POST http://localhost:8000/calculate-pension \
  -H "Content-Type: application/json" \
  -d '{
    "annual_incomes": [25000, 27000, 30000],
    "coefficients": [0.95, 0.97, 1.0],
    "insurance_years": 35
  }'
```

---

## ✅ Testování

```bash
# Všechny testy
pytest tests/unit/ -v

# Pokrytí kódu
pytest --cov=src/backend tests/unit/

# Pylint kontrola
pylint src/backend/engine/ --disable=all --enable=W,E
```

**Current Status:** 13/13 testů prochází ✅

---

## 📅 Roadmap

### Fáze 1: Git & CI/CD (NYNÍ)
- [x] Git inicializace
- [ ] GitHub repo setup
- [ ] GitHub Actions workflow (test → build → deploy)
- [ ] CHANGELOG.md

### Fáze 2: Frontend Migration (2-3 týdny)
- [ ] Vue 3 scaffolding
- [ ] UI Design System (barvy, komponenty)
- [ ] Form validation + API integration
- [ ] Responsive layout (mobile-first)
- [ ] Deployment na CF Pages

### Fáze 3: Database & Auth (3-4 týdny)
- [ ] D1 schema design
- [ ] OAuth integration (Google, Microsoft, iCloud, Seznam)
- [ ] JWT auth layer
- [ ] User calculation history

### Fáze 4: E2E Testing & Deployment (2 týdny)
- [ ] Playwright testy
- [ ] Railway deployment
- [ ] Production monitoring

### Fáze 5: Advanced Features (iterativně)
- [ ] NVIDIA NIM integration
- [ ] Public API docs
- [ ] Export reports (PDF, CSV)
- [ ] Real-time collaboration

---

## 🔐 Environment Variables

Kopíruj `.env.example` na `.env` a vyplň:

```bash
cp .env.example .env
```

**Důležité:** Nikdy nejspamuj `.env` do gitu!

---

## 📚 Legislativní Reference

- **Zákon č. 155/1995 Sb.** - Zákon o důchodovém pojištění
- **MPSV Vyhlášky** - Redukční hranice, VVZ, koeficienty (aktualizují se ročně)
- **ePortál ČSSZ** - Importuj IOLDP data
- **IDA aplikace** - Ověřování výpočtů

---

## 🛠️ Technologický Stack

| Vrstva | Technologie | Verze |
|--------|-------------|-------|
| **Backend** | FastAPI | 0.100.0+ |
| **Engine** | Python | 3.9+ |
| **Testy** | pytest | 7.0.0+ |
| **Frontend** | Vue 3 / React | (migrate) |
| **Cloud** | Cloudflare Pages + Workers | - |
| **Database** | D1 (SQLite) + Railway.com | - |
| **Auth** | OAuth 2.0 + JWT | - |

---

## 🤝 Contributing

1. Branch: `git checkout -b feature/xxx`
2. Commit: `git commit -m "feat: description"`
3. Push: `git push origin feature/xxx`
4. Pull Request na `main`

**Code Quality:**
- Pylint score: min. 8.0/10
- Test coverage: min. 80%
- Type hints: povinné pro nový kód

---

## 📞 Support & Contact

**Vlastník projektu:** Matej Kocanda  
**GitHub:** https://github.com/  
**Email:** matej.kocanda@example.com

---

## 📄 Licence

MIT License © 2026 KALKULAČKA PENZÍ PRO

---

**Last Updated:** 7. května 2026
