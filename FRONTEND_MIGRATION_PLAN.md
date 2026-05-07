# KALKULAČKA PENZÍ PRO - Frontend Migration Plan (Vue 3)

> Detailní plán na migraci z HTML/JS MVP na production-ready Vue 3 aplikaci

---

## 📊 Fáze Overview

| Fáze | Trvání | Cíl | Status |
|------|--------|-----|--------|
| **0. Příprava** | 1 den | Setup + Design System | 📋 TODO |
| **1. Component Base** | 3 dny | Core komponenty | 📋 TODO |
| **2. Form & Calc** | 5 dní | Kalkulátor integraci | 📋 TODO |
| **3. UI/UX Polish** | 3 dny | Design + Responsive | 📋 TODO |
| **4. Testing & Deploy** | 2 dny | E2E + CF Pages | 📋 TODO |

**Celkem:** ~14 dní (2 týdny full-time)

---

## 🎯 Fáze 0: Příprava (1 den)

### 0.1 Vue 3 Project Setup

```bash
# V nadřazené složce PensionCalculator
cd ..
npm create vite@latest pension-calculator-frontend -- --template vue
cd pension-calculator-frontend

# Install dependencies
npm install

# Add UI framework
npm install @headlessui/vue tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install API client + utilities
npm install axios vue-router pinia zod
npm install -D typescript @vue/test-utils vitest
```

### 0.2 Projekt Struktura

```
pension-calculator-frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.vue
│   │   │   ├── Footer.vue
│   │   │   ├── Navigation.vue
│   │   │   ├── Button.vue
│   │   │   ├── Input.vue
│   │   │   └── Card.vue
│   │   ├── calculator/
│   │   │   ├── PensionCalculator.vue
│   │   │   ├── OVZCalculator.vue
│   │   │   ├── ParadoxResolver.vue
│   │   │   └── EarlyRetirement.vue
│   │   └── auth/
│   │       ├── LoginForm.vue
│   │       └── OAuthButtons.vue
│   ├── pages/
│   │   ├── Home.vue
│   │   ├── Calculator.vue
│   │   ├── Dashboard.vue
│   │   ├── Profile.vue
│   │   └── NotFound.vue
│   ├── stores/
│   │   ├── user.ts
│   │   ├── calculator.ts
│   │   └── auth.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── calculator.ts
│   ├── types/
│   │   ├── pension.ts
│   │   ├── user.ts
│   │   └── api.ts
│   ├── styles/
│   │   ├── main.css
│   │   ├── tailwind.css
│   │   └── variables.css
│   ├── App.vue
│   ├── main.ts
│   └── env.d.ts
├── tests/
│   └── unit/
├── .env.example
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

### 0.3 TypeScript Configuration

`vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

### 0.4 Color Palette & Design System

**Primární barvy:**
- Primary: `#3498db` (Modrá - Trust, calming)
- Success: `#27ae60` (Zelená - Positive results)
- Warning: `#e74c3c` (Červená - Important)
- Background: `#f8f9fa` (Světle šedá)
- Text: `#2c3e50` (Tmavě modrá)

**Tailwind config:**
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3498db',
        success: '#27ae60',
        warning: '#e74c3c',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto'],
      },
    },
  },
}
```

---

## 🎨 Fáze 1: Core Components (3 dny)

### 1.1 Common Components

**Button.vue**
```vue
<template>
  <button
    :class="[
      'px-4 py-2 rounded font-medium transition',
      variantClasses,
    ]"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
})

const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-primary text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    success: 'bg-success text-white hover:bg-green-600',
    danger: 'bg-warning text-white hover:bg-red-600',
  }
  return variants[props.variant]
})
</script>
```

**Input.vue**
```vue
<template>
  <div class="form-group">
    <label v-if="label" class="block mb-2 font-medium">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-primary"
    />
    <p v-if="error" class="text-red-500 text-sm mt-1">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  label?: string
  type?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  error?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
```

**Card.vue**
```vue
<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div v-if="title" class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>
```

### 1.2 Layout Components

**Header.vue** - Navigace, logo, user menu
**Footer.vue** - Copyright, links
**Navigation.vue** - Tab-based navigation

### 1.3 Stores (Pinia)

**stores/calculator.ts** - Centrální stav kalkulatoru
**stores/user.ts** - User session & profile
**stores/auth.ts** - Authentication state

---

## 🧮 Fáze 2: Kalkulátor Integraci (5 dní)

### 2.1 API Service Integration

`services/api.ts`:
```typescript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

export interface PensionRequest {
  annual_incomes: number[]
  coefficients: number[]
  insurance_years: number
  excluded_days?: number
}

export interface OVZRequest {
  annual_incomes: number[]
  coefficients: number[]
  total_days: number
  excluded_days?: number
}

export interface PensionResponse {
  pension_amount: number
  vz: number
  ovz: number
  reduction_percent: number
  details: Record<string, any>
}

export const calculatorService = {
  calculatePension(payload: PensionRequest) {
    return api.post<PensionResponse>('/calculate-pension', payload)
  },

  calculateOVZ(payload: OVZRequest) {
    return api.post<number>('/calculate-ovz', payload)
  },

  resolveParadox(payload: ParadoxRequest) {
    return api.post('/resolve-paradox', payload)
  },

  calculateEarlyRetirement(payload: EarlyRetirementRequest) {
    return api.post<EarlyRetirementResponse>('/calculate-early-retirement', payload)
  },
}
```

### 2.2 Kalkulátor Komponenty

**components/calculator/PensionCalculator.vue**
```vue
<template>
  <Card title="Výpočet Starobního Důchodu">
    <form @submit.prevent="calculatePension" class="space-y-4">
      <div>
        <Input
          v-model="form.insurance_years"
          label="Počet let pojištění"
          type="number"
          required
          placeholder="35"
        />
      </div>

      <div>
        <label class="block font-medium mb-2">Roční příjmy</label>
        <div
          v-for="(income, idx) in form.annual_incomes"
          :key="idx"
          class="flex gap-2 mb-2"
        >
          <Input
            :model-value="income"
            @update:model-value="updateIncome(idx, $event)"
            type="number"
            placeholder="30000 Kč"
          />
          <Button
            variant="danger"
            @click="removeIncome(idx)"
            class="px-3"
          >
            Smazat
          </Button>
        </div>
        <Button variant="secondary" @click="addIncome">
          + Přidat rok
        </Button>
      </div>

      <Button variant="primary" type="submit" :disabled="calculating">
        {{ calculating ? 'Počítám...' : 'Vypočítat Důchod' }}
      </Button>
    </form>

    <div v-if="result" class="mt-6 p-4 bg-green-50 rounded">
      <h4 class="font-bold text-success text-lg">Váš Důchod</h4>
      <p class="text-2xl font-bold text-success mt-2">
        {{ result.pension_amount.toLocaleString('cs-CZ') }} Kč
      </p>
      <div class="text-sm text-gray-600 mt-2">
        <p>Osobní vyměřovací základ: {{ result.ovz.toFixed(2) }}</p>
        <p>Redukční procento: {{ result.reduction_percent }}%</p>
      </div>
    </div>

    <div v-if="error" class="mt-4 text-red-600">
      {{ error }}
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCalculatorStore } from '@/stores/calculator'
import Card from '../common/Card.vue'
import Button from '../common/Button.vue'
import Input from '../common/Input.vue'

const store = useCalculatorStore()
const calculating = ref(false)
const error = ref('')

const form = reactive({
  insurance_years: 35,
  annual_incomes: [30000, 32000, 35000],
  coefficients: [0.95, 0.97, 1.0],
  excluded_days: 0,
})

const result = computed(() => store.lastResult)

async function calculatePension() {
  calculating.value = true
  error.value = ''

  try {
    await store.calculatePension(form)
  } catch (err) {
    error.value = 'Chyba při výpočtu. Zkuste znovu.'
    console.error(err)
  } finally {
    calculating.value = false
  }
}

function addIncome() {
  form.annual_incomes.push(0)
  form.coefficients.push(1.0)
}

function removeIncome(idx: number) {
  form.annual_incomes.splice(idx, 1)
  form.coefficients.splice(idx, 1)
}

function updateIncome(idx: number, value: string) {
  form.annual_incomes[idx] = parseFloat(value) || 0
}
</script>
```

### 2.3 Pinia Stores

`stores/calculator.ts`:
```typescript
import { defineStore } from 'pinia'
import { calculatorService, PensionRequest } from '@/services/api'

export const useCalculatorStore = defineStore('calculator', {
  state: () => ({
    lastResult: null as any,
    history: [] as any[],
    loading: false,
  }),

  actions: {
    async calculatePension(payload: PensionRequest) {
      this.loading = true
      try {
        const response = await calculatorService.calculatePension(payload)
        this.lastResult = response.data
        this.history.push({
          timestamp: new Date(),
          type: 'pension',
          result: response.data,
        })
        return response.data
      } finally {
        this.loading = false
      }
    },
  },
})
```

---

## 🎨 Fáze 3: UI/UX Polish (3 dny)

### 3.1 Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Tailwind responsive utilities

### 3.2 Accessibility
- ARIA labels
- Keyboard navigation
- Color contrast (WCAG AA)
- Screen reader support

### 3.3 Dark Mode Support
```vue
<template>
  <div :class="{ 'dark': isDarkMode }">
    <!-- Content -->
  </div>
</template>

<script setup>
const isDarkMode = ref(false)
</script>
```

### 3.4 Loading & Error States
- Skeleton loaders
- Error boundaries
- Toast notifications (vue-toastification)

---

## ✅ Fáze 4: Testing & Deployment (2 dny)

### 4.1 Unit Tests (Vitest)
```typescript
// tests/PensionCalculator.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PensionCalculator from '@/components/calculator/PensionCalculator.vue'

describe('PensionCalculator', () => {
  it('renders form', () => {
    const wrapper = mount(PensionCalculator)
    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('calculates pension correctly', async () => {
    // Mock API
    // Test calculation flow
  })
})
```

### 4.2 E2E Tests (Playwright)
```typescript
// e2e/pension-calculator.spec.ts
import { test, expect } from '@playwright/test'

test('Full pension calculation flow', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await page.fill('input[placeholder="35"]', '35')
  await page.click('button:has-text("Vypočítat Důchod")')
  
  const result = await page.locator('.text-success').textContent()
  expect(result).toContain('Kč')
})
```

### 4.3 Cloudflare Pages Deployment

`wrangler.toml`:
```toml
name = "pension-calculator-frontend"
type = "javascript"
account_id = "your-account-id"
workers_dev = true
route = ""
zone_id = ""

[env.production]
route = "https://pension-calculator-pro.app/*"
zone_id = "your-zone-id"

[build]
command = "npm install && npm run build"
cwd = "./"
watch_paths = ["src/**/*.{ts,tsx,js,jsx,css}"]

[build.upload]
dir = "dist"
format = "service-worker"
```

---

## 📋 Implementation Checklist

### ✅ Setup (Den 1)
- [ ] `npm create vite` + install
- [ ] Tailwind konfiguraci
- [ ] TypeScript setup
- [ ] .env.example vytvořit

### ✅ Components (Den 2-3)
- [ ] Button, Input, Card komponenty
- [ ] Header, Footer, Navigation
- [ ] PensionCalculator komponenta
- [ ] OVZCalculator komponenta
- [ ] ParadoxResolver komponenta

### ✅ Integration (Den 4-5)
- [ ] API service (axios)
- [ ] Pinia stores
- [ ] Calculator logika
- [ ] Form validation (Zod)

### ✅ Polish (Den 6-7)
- [ ] Mobile responsive
- [ ] Dark mode
- [ ] Error handling
- [ ] Loading states

### ✅ Testing (Den 8)
- [ ] Unit testy (Vitest)
- [ ] E2E testy (Playwright)
- [ ] Performance audit (Lighthouse)

### ✅ Deploy (Den 9)
- [ ] Wrangler config
- [ ] GitHub Actions workflow
- [ ] Cloudflare Pages publish
- [ ] Domain setup

---

## 🚀 Git Workflow During Migration

```bash
# Main branch - stable
# develop branch - work in progress

git checkout -b feature/frontend-vue3
git add src/components/...
git commit -m "feat: Add Button component"
git push origin feature/frontend-vue3

# Create PR, wait for CI/CD
# Merge to develop
# Weekly merge to main
```

---

## 📞 Zajímavé Library Alternativy

| Library | Purpose | Alternative |
|---------|---------|--------------|
| Tailwind CSS | Styling | Bootstrap Vue 3, shadcn/vue |
| Pinia | State | Vuex 4 |
| Vue Router | Routing | - |
| Axios | HTTP Client | Fetch API, TanStack Query |
| Zod | Validation | Valibot, Yup |
| Vitest | Unit Tests | Jest, Mocha |
| Playwright | E2E Tests | Cypress, Nightwatch |

---

**Status:** Ready for implementation  
**Čekám na:** Go-ahead a tvé design feedback
