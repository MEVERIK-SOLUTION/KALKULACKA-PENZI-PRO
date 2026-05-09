# 📓 PRACOVNÍ DENÍK — KALKULAČKA PENZÍ PRO

---

## Fáze 1: Stabilizace ✅ DOKONČENO
**Datum:** 9. května 2026, 17:08  
**Commit:** `355c678` — `fix: Phase 1 stabilization`  
**Push:** ✅ GitHub `main` branch  

### Provedené změny

| # | Úkol | Soubor | Stav |
|---|------|--------|------|
| 1.1 | Odstranit duplikátní `/health` endpoint | `api/main.py` | ✅ |
| 1.2 | Přesunout API key z hardcoded na env | `frontend/src/services/calculator.ts`, `.env.example` | ✅ |
| 1.3 | Sjednotit redukční logiku | `src/backend/engine/ovz_calculator.py` | ✅ |
| 1.4 | Numerické pravidla důchodový věk žen | `config/legislative_2026.yaml` | ✅ |
| 1.5 | 3-stupňová redukce předčasného důchodu | `src/backend/engine/pension_calculator.py`, `frontend/src/types/pension.ts` | ✅ |

### Detaily změn

#### 1.1 Duplikátní /health endpoint
- **Problém:** Dva `@app.get("/health")` v `api/main.py`.
- **Řešení:** Smazán stub, zachován verze s Redis cache check.

#### 1.2 Hardcoded API key
- **Problém:** `'dev-key-123'` natvrdo ve frontend service.
- **Řešení:** Přesunuto na `VITE_API_KEY` env proměnnou.
- **Dopad:** ⚠️ Nutno nastavit v Cloudflare Pages env variables pro production.

#### 1.3 Duplicitní redukční logika
- **Problém:** `ovz_calculator.py` měl vlastní implementaci redukce odlišnou od `reduction_engine.py`.
- **Řešení:** `calculate_reduced_base()` deleguje na `reduction_engine.calculate_vz()`.

#### 1.4 Důchodový věk žen
- **Problém:** Textové popisy místo čísel.
- **Řešení:** `child_reduction_months: {0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20}`.

#### 1.5 Progresivní redukce předčasného důchodu
- **Řešení:** 3-stupňová: 0.9% / 1.2% / 1.5% za 90 dní.
- **Ověřeno:** 12m→3.6%, 24m→8.4%, 36m→14.4% ✅

### Nové výzvy (k řešení po dokončení všech fází)
1. Frontend `EarlyRetirement.vue` by měla zobrazovat `reduction_breakdown`
2. Koeficient `1.0581` hardcoded na mnoha místech frontendu
3. `pytest` chybí na systému (Python 3.14)
