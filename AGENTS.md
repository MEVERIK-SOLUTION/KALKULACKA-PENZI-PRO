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
