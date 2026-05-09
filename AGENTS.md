# AGENTS.md — Projektový deník

## Session 2026-05-09

### Hotovo
- Opraveny chybějící importy `calculatorService` v `CalculationVisualization.vue`, `ParadoxResolver.vue`, `EarlyRetirement.vue`, `OVZCalculator.vue`
- Opraveno `registerables()` → `Chart.register(...registerables)` v `CalculationVisualization.vue` (runtime chyba — volalo se to jako funkce, ale je to pole)
- Doplněn chybějící typ `EarlyRetirementResponse` do `pension.ts`
- Přejmenováno `useDataForCalculation` → `applyToCalculator` v `IOLDPUploader.vue`
- Odstraněny nepoužité importy a proměnné napříč projektem
- Přidán `vite-env.d.ts` pro podporu `import.meta.env`
- Opraven výpočet výše důchodu v `PensionChart.vue` — přidán `insuranceYears` do vzorce

### Architektura / důležité souvislosti
- FE: Vue 3 + Vite + Chart.js (raw canvas, nikoli vue-chartjs komponenty)
- BE: FastAPI na Railway (`/calculate-pension`, `/calculate-ovz`, `/resolve-paradox`, `/calculate-early-retirement`)
- Deploy: Cloudflare Pages (FE) + Railway (BE)
- API base URL: `import.meta.env.VITE_API_BASE_URL` (fallback `localhost:8002`)
- Store: Pinia `useCalculatorStore` s `lastResult`, `error` atd.
- Důchodový vzorec: `pension = base_pension + (vz * percent_rate / 100 * insurance_years)`

### Možné další kroky
- Ověřit funkčnost všech záložek na nasazené verzi
- Dát zpětnou vazbu uživateli k otestování
- Případné doladění UI/UX

## Session 2026-05-09 (odpoledne) — Fáze 1: Stabilizace

### Hotovo
- Odstraněn duplikátní `/health` endpoint v `api/main.py`
- API key přesunut z hardcoded `'dev-key-123'` na `VITE_API_KEY` env proměnnou
- Sjednocena redukční logika — `calculate_reduced_base()` deleguje na `reduction_engine.calculate_vz()`
- Přidána numerická pravidla pro důchodový věk žen (`child_reduction_months`)
- Implementována 3-stupňová progresivní redukce předčasného důchodu (0.9%/1.2%/1.5% za 90 dní)
- Rozšířen TypeScript typ `EarlyRetirementResponse` o `days_early` a `reduction_breakdown`
- Přidán `VITE_API_KEY` do `.env.example`
- Commit `355c678` pushnut na GitHub

### Architektura / důležité souvislosti
- Předčasný důchod: API nově vrací `reduction_breakdown` — pole s detailem redukce po stupních
- Legislativní YAML: důchodový věk v měsících (720=60let, 780=65let), ženy: `child_reduction_months`
- API key: `VITE_API_KEY` nutno nastavit v Cloudflare Pages env pro production
- Redukce: jediný zdroj pravdy je `reduction_engine.py`, volá se i z `ovz_calculator.py`
