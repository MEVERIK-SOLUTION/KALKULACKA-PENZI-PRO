# Fáze 2-4: Implementační plán - KALKULAČKA PENZÍ PRO

*Datum: 7. května 2026*

---

## 🎯 CÍLE FÁZE 2 (Kalkulátor Integrace)

### 2.1 Rozšíření Vue 3 komponent (5 dní)

| Komponenta | Popis | Zdroj (z tvých podkladů) | Status |
|-----------|-------|-----------------------------|--------|
| `EarlyRetirement.vue` | Předčasný důchod + krácení | § 31 ZDP + MPSV Excel (kapitola 7) | 🔲 TODO |
| `ParadoxResolver.vue` | Vizualizace rozhodovacího paradoxu | § 12-13 ZDP + MPSV Excel (kapitola 9) | 🔲 TODO |
| `OVZCalculator.vue` | Krok-po-kroku OVZ s grafem | § 15 ZDP + MPSV Excel (kapitola 2) | 🔲 TODO |
| `PensionResult.vue` | Detailní rozpis výpočtu | MPSV Excel (kapitola 4-6) | 🔲 TODO |
| `IOLDPUploader.vue` | Nahrání IOLDP XML/PDF | Dokumentace 5.1 (ČSSZ ePortál) | 🔲 TODO |

### 2.2 Integrace výpočetního enginu (3 dny)

**A) Přes API (Railway)** - již máme ✅
- `/calculate-pension` → hlavní výpočet
- `/calculate-ovz` → OVZ výpočet
- `/resolve-paradox` → paradox resolver
- `/calculate-early-retirement` → krácení

**B) Přes WebAssembly (budoucí)**
- Kompilace Python enginu do WASM
- Bleskově rychlé lokální výpočty
- Offline režim

### 2.3 Vizualizace výpočtu (2 dny)

| Graf | Knihovna | Popis |
|------|----------|-------|
| OVZ průběh | Chart.js / Vue-Chartjs | Roční příjmy → OVZ křivka |
| Redukční meze | D3.js / Vue-D3 | Sloupce s barvami (zelená/červená) |
| Důchod vs. příjem | Recharts | Poměr důchod/příjem v čase |
| Paradox resolver | Custom SVG | Sankey diagram s vybranou variantou |

---

## 🎨 FÁZE 3: UI/UX Polish (3 dny)

### 3.1 Dark Mode + Responzivita
- Toggle dark/light mode (v `App.vue`)
- Breakpointy: sm (640px), md (768px), lg (1024px), xl (1280px)
- Mobile-first navigace (hamburger menu)

### 3.2 Animace a přechody
- Vue Transition komponenty
- Loading skeletons (během API volání)
- Toast notifikace (vue-toastification)

### 3.3 Accessibility (WCAG AA)
- ARIA labely na formulářích
- Keyboard navigation (Tab, Enter, Escape)
- Screen reader podpora

---

## 🧪 FÁZE 4: Testing & Deployment (2 dny)

### 4.1 Unit Testy (Vitest)
```
tests/
├── unit/
│   ├── components/
│   │   ├── EarlyRetirement.spec.ts
│   │   ├── ParadoxResolver.spec.ts
│   │   └── OVZCalculator.spec.ts
│   └── stores/
│       └── calculator.spec.ts
```

### 4.2 E2E Testy (Playwright)
- Scénář 1: Kompletní výpočet důchodu (35 let, 38k měsíčně)
- Scénář 2: Předčasný důchod (krácení)
- Scénář 3: Paradox resolver (studium vs. bez studia)
- Scénář 4: IOLDP nahrání a parsování

### 4.3 CI/CD (GitHub Actions)
- `test-build.yml` ← spouštět Vitest + Playwright
- `deploy-pages.yml` ← nasazení na Cloudflare Pages
- `deploy-railway.yml` ← nasazení API na Railway

---

## 🔧 INTEGRACE VEŘEJNÝCH API

### API 1: ČSÚ – DataStat ✅ (opraveno – ověřeno v rešerši #1)

Správné endpointy (CRUHVD1T2 byla turistika, ne inflace!):

```typescript
// services/dataService.ts
const API_BASE = 'http://localhost:8000';

export async function getInflationRate() {
  const response = await fetch(`${API_BASE}/data/inflation`);
  return response.json(); // { rate: 2.6, unit: '%', source: 'ČSÚ DataStat' }
}

export async function getAvgWage() {
  const response = await fetch(`${API_BASE}/data/avg-wage`);
  return response.json(); // { amount: 49262, unit: 'Kč/měsíc', source: 'ČSÚ DataStat' }
}

export async function getWageGrowth(years: number = 10) {
  const response = await fetch(`${API_BASE}/data/wage-growth?years_back=${years}`);
  return response.json(); // { rate: 5.2, period_years: 10, unit: '% p.a.' }
}
```

Nebo přímo z DataStat:

```typescript
// services/datastatApi.ts
const DATASTAT = 'https://data.csu.gov.cz/api/dotaz/v1/data/vybery';

export async function getInflation() {
  const response = await fetch(`${DATASTAT}/WCEN01MT01?format=CSV`);
  return response.text(); // CSV s měsíční inflací
}

export async function getWages() {
  const response = await fetch(`${DATASTAT}/MZDQ1T1?format=CSV`);
  return response.text(); // CSV s mzdami (data od 2000)
}
```

---

## 📂 IOLDP UPLOAD (Dokumentace 5.1)

### Formát IOLDP
- **XML**: Strukturovaná data (příjmy, doby pojištění)
- **PDF**: Skentovaný Osobní list důchodového pojištění

### Parser (Vue 3 komponenta)
```vue
<template>
  <div class="iol-dp-uploader">
    <input type="file" accept=".xml,.pdf" @change="handleFileUpload" />
    <div v-if="parsedData" class="parsed-preview">
      <h4>Parsovaná data:</h4>
      <pre>{{ JSON.stringify(parsedData, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const parsedData = ref(null);

function handleFileUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const text = e.target?.result as string;
    if (file.name.endsWith('.xml')) {
      parsedData.value = parseXML(text);
    } else if (file.name.endsWith('.pdf')) {
      parsedData.value = parsePDF(text);
    }
  };
  reader.readAsText(file);
}

function parseXML(xmlText: string) {
  // XML parser implementace
  // Extrahuje: roční příjmy, koeficienty, doby pojištění
  return { annual_incomes: [], coefficients: [], years: 0 };
}
</script>
```

---

## 📊 DETAILNÍ ROZPIS KROKŮ (Fáze 2)

### Den 1-2: EarlyRetirement komponenta
- [ ] Vytvořit `EarlyRetirement.vue` v `src/components/calculator/`
- [ ] Přidat formulář (důchod, měsíce předčasnosti)
- [ ] Zobrazit krácení (§ 31 ZDP - 1.5% za 90 dní)
- [ ] Vizualizace (progress bar s krácením)

### Den 3-4: ParadoxResolver s vizualizací
- [ ] Vytvořit `ParadoxResolver.vue`
- [ ] Sankey diagram (D3.js) - varianta A vs. B
- [ ] Tabulka s porovnáním (OVZ s/bez náhradní doby)
- [ ] Doporučení engine (z `paradox_resolver.py`)

### Den 5-6: OVZCalculator krok-po-kroku
- [ ] Vytvořit `OVZCalculator.vue`
- [ ] Formulář pro každý rok (příjem + koeficient)
- [ ] Řádková kalkulace (Excel-like tabulka)
- [ ] Chart.js graf (průběh OVZ v čase)

### Den 7-8: Integrace kompletního enginu
- [ ] Ověřit všechny 4 enginy (`ovz_calculator`, `reduction_engine`, `paradox_resolver`, `pension_calculator`)
- [ ] Přidat error handling (špatné vstupy)
- [ ] Optimalizace (caching výsledků v Pinia)

---

## 🚀 CO BUDEME DĚLAT TEĎ?

**Moje doporučení:**
1. ✅ **Fáze 2.1** - Hned teď vytvořit `EarlyRetirement.vue` (předčasný důchod)
2. ✅ **Fáze 2.2** - Otestovat všechny API endpoints na Railway
3. ✅ **Fáze 2.3** - Přidat Chart.js pro vizualizace

**Chceš, abych:**

**A)** Začal implementovat `EarlyRetirement.vue` (Fáze 2.1)  
**B)** Vytvořil `ParadoxResolver.vue` s D3.js vizualizací (Fáze 2.2)  
**C)** Rozšířil `App.vue` o nové záložky (Early Ret., Paradox, OVZ detail)  
**D)** Něco jiného?

*Jsem připraven pokračovat! 🚀*
