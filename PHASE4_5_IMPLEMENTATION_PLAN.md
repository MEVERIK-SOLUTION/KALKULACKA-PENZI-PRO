# Phase 4 & 5: Hloubkový implementační plán

## Přehled
Rozdělení na 4 úseky (sprinty) s jasnou pipeline pro testování, deployment a pokročilé funkce.

---

## ÚSEK 1: E2E Testing & CI/CD Setup (Phase 4)
**Cíl**: Plně automatizované testy a CI/CD pipeline

### 1.1 Playwright E2E Testy
**Soubory**: `e2e/` nový adresář
**Ověření**: Spuštění testů lokálně i v CI

#### Krok 1.1.1: Setup Playwright
```bash
cd /tmp/pension-calculator-frontend
npm init playwright@latest
# Vybrat: TypeScript, GitHub Actions, všechny prohlížeče
```

#### Krok 1.1.2: Testovací scénáře (vytvořit soubory)
- `e2e/pension-calculator.spec.ts` - hlavní kalkulačka
- `e2e/early-retirement.spec.ts` - předčasný důchod
- `e2e/ovz-calculator.spec.ts` - OVZ výpočet
- `e2e/dark-mode.spec.ts` - přepínání tmavého režimu
- `e2e/visualization.spec.ts` - grafy a vizualizace

#### Krok 1.1.3: Mock API helper
- `e2e/helpers/api-mock.ts` - mockování Railway API odpovědí

### 1.2 GitHub Actions CI/CD
**Soubor**: `.github/workflows/deploy.yml` (nový)

#### Krok 1.2.1: Workflow konfigurace
```yaml
name: Deploy to Cloudflare Pages
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:e2e
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci && npm run build
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy frontend/dist --project-name=kalkulacka-penzi-pro
```

#### Krok 1.2.2: Secrets v GitHub
- `CLOUDFLARE_API_TOKEN` - z Cloudflare Dashboard
- `CLOUDFLARE_ACCOUNT_ID` - z Cloudflare Dashboard

### 1.3 API Integration Testy
**Soubory**: `tests/` v rootu (nový adresář)

#### Krok 1.3.1: Python testy pro backend
- `tests/test_ovz_calculator.py`
- `tests/test_reduction_engine.py`
- `tests/test_paradox_resolver.py`
- `tests/test_pension_calculator.py`

#### Krok 1.3.2: Pytest setup
- `tests/conftest.py` - fixtures
- `requirements-test.txt` - pytest, httpx

**Ověření**: `cd /Users/matejkocanda/.../PensionCalculator && python -m pytest tests/`

---

## ÚSEK 2: Engine Validation & Data Integrity (Phase 5 - část 1)
**Cíl**: Zajištění správnosti výpočtů a validace vstupů

### 2.1 Validace vstupních dat (frontend)
**Soubory**: `frontend/src/utils/validators.ts` (nový)

#### Krok 2.1.1: Validator funkce
```typescript
export function validateIncome(income: number): ValidationResult
export function validateInsuranceYears(years: number): ValidationResult
export function validateExcludedDays(days: number, totalDays: number): ValidationResult
export function validateCoefficient(coeff: number): ValidationResult
```

#### Krok 2.1.2: Integrace do komponent
- Přidat `validators.ts` import do všech formulářů
- Zobrazovat chyby pod inputy (už v `Input.vue` je `error` prop)

### 2.2 Engine Validation (backend)
**Soubory**: `src/backend/engine/validator.py` (nový)

#### Krok 2.2.1: Python validátory
```python
def validate_ovz_inputs(annual_incomes: List[float], coefficients: List[float], ...)
def validate_pension_inputs(insurance_years: int, ...)
def validate_reduction_limits(ovz: float, limits: List[dict])
```

#### Krok 2.2.2: Integration do API
- Upravit `api/main.py` - volat validaci před výpočtem
- Vrátit `400 Bad Request` s detaily chyby

### 2.3 Edge Cases & Stress Testy
**Soubory**: `tests/test_edge_cases.py` (nový)

#### Krok 2.3.1: Testovací scénáře
- Velmi nízký příjem (0 Kč)
- Velmi vysoký příjem (10M+ Kč)
- Mezní hodnoty pojištění (0 let, 50 let)
- Záporné hodnoty (by měly být odmítnuty)
- Přetečení (extrémní hodnoty)
- Neplatné koeficienty (0, záporné, příliš vysoké)

**Ověření**: `python -m pytest tests/test_edge_cases.py -v`

---

## ÚSEK 3: Advanced Features (Phase 5 - část 2)
**Cíl**: Rozšíření funkčnosti a použitelnosti

### 3.1 Export & Reporting
**Soubory**: `frontend/src/components/calculator/ExportReport.vue` (nový)

#### Krok 3.1.1: PDF export
- Nainstalovat `jspdf` a `jspdf-autotable`
- Vytvořit `services/exportService.ts`
- Generovat PDF s výsledky (OVZ, redukce, důchod)

#### Krok 3.1.2: CSV/Excel export
- Nainstalovat `json2csv` nebo `xlsx`
- Exportovat historická data (IOLDP, ekonomické ukazatele)

#### Krok 3.1.3: UI komponenta
- Přidat tlačítka "Export PDF", "Export CSV" do výsledků
- Stylizovat pro dark mode

### 3.2 Comparison Tool (Porovnání scénářů)
**Soubory**: `frontend/src/components/calculator/ComparisonTool.vue` (nový)

#### Krok 3.2.1: Store pro porovnání
- Rozšířit `stores/calculator.ts` o `comparisonScenarios: []`
- Metody: `addScenario()`, `removeScenario()`, `compare()`

#### Krok 3.2.2: UI pro porovnání
- Side-by-side zobrazení dvou a více scénářů
- Grafy pro porovnání (zvlášť v Chart.js)
- Tabulka s rozdíly

### 3.3 What-If Analysis (Simulace dopadů)
**Soubory**: `frontend/src/components/calculator/WhatIfAnalysis.vue` (nový)

#### Krok 3.3.1: Simulace parametrů
- Posuvníky pro změnu příjmu, let pojištění
- Živá aktualizace výpočtu (debounced)
- Zobrazení rozdílů oproti původnímu stavu

#### Krok 3.3.2: Vizualizace dopadů
- Line chart: Vývoj důchodu v čase
- Bar chart: Dopad na OVZ při různých příjmech
- Sdílení výsledků (copy link s parametry v URL)

---

## ÚSEK 4: Performance & Monitoring (Phase 5 - část 3)
**Cíl**: Optimalizace a monitoring produkční aplikace

### 4.1 Frontend Performance
**Soubory**: `frontend/vite.config.ts` (úprava), `frontend/src/composables/useDebounce.ts` (nový)

#### Krok 4.1.1: Code splitting & Lazy loading
- Rozdělit komponenty na chunks (dynamicke importy)
- Lazy load grafů (Chart.js až po kliknutí na tab)

#### Krok 4.1.2: Caching strategie
- Přidat `services/cacheService.ts` pro caching API odpovědí
- LocalStorage pro ukládání posledních výpočtů

#### Krok 4.1.3: Debounce pro výpočty
- Vytvořit `useDebounce()` composable
- Aplikovat na OVZ a Visualization (čekat 500ms po poslední změně)

**Ověření**: Lighthouse audit (target: 90+)

### 4.2 API Performance & Monitoring
**Soubory**: `api/main.py` (úprava), `api/monitoring.py` (nový)

#### Krok 4.2.1: Logging & Metrics
- Přidat strukturované logování (Python `logging`)
- Metriky: doba výpočtu, počet requestů, chybovost
- Endpoint `/api/metrics` pro monitoring

#### Krok 4.2.2: Rate limiting
- Přidat `slowapi` pro rate limiting
- Limit: 100 req/min na IP

#### Krok 4.2.3: Railway monitoring
- Zapnout Railway metrics
- Nastavit alerting (přes Railway nebo externí)

### 4.3 Error Tracking & User Feedback
**Soubory**: `frontend/src/services/errorTracking.ts` (nový), `frontend/src/components/common/ErrorBoundary.vue` (nový)

#### Krok 4.3.1: Error Boundary
- Vue 3 error boundary komponenta
- Fallback UI při chybě
- Logování chyb do konzole + (nepovinně) externí služby

#### Krok 4.3.2: User feedback
- Přidat tlačítko "Nahlásit chybu" v patičce
- Jednoduchý formulář (odeslat email nebo GitHub issue)
- Dark mode styling

---

## Pracovní pipeline (doporučené pořadí)

```
1. ÚSEK 1: E2E Testing & CI/CD
   ↓
2. ÚSEK 2: Engine Validation & Data Integrity
   ↓
3. ÚSEK 3: Advanced Features (Export → Comparison → What-If)
   ↓
4. ÚSEK 4: Performance & Monitoring
   ↓
5. Finální audit a spuštění na produkci
```

## Závislosti pro jednotlivé úseky

### ÚSEK 1:
- `npm install -D @playwright/test`
- GitHub repository secrets

### ÚSEK 2:
- `pip install pytest httpx`
- Rozšíření backend engine o validaci

### ÚSEK 3:
- `npm install jspdf jspdf-autotable json2csv`
- Rozšíření Pinia store

### ÚSEK 4:
- `pip install slowapi`
- `npm install lodash.debounce`
- Lighthouse (globálně nebo v CI)

## Finální dodání
- [ ] Všechny E2E testy procházejí
- [ ] CI/CD pipeline funkční (auto-deploy na main)
- [ ] Backend validace odmítá neplatné vstupy
- [ ] PDF/CSV export funkční
- [ ] Performance audit 90+ (Lighthouse)
- [ ] Error tracking nastaven
- [ ] Dokumentace aktualizována (README.md)

## Poznámky
- Každý úsek bude mít vlastní commit a deploy na Cloudflare
- Testy píšeme před implementací (TDD přístup pro kritickou logiku)
- Dark mode musí být zachován ve všech nových komponentách
- API musí vracet smysluplné chybové kódy (400, 422 pro validaci)
