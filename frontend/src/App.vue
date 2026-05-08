<template>
  <div class="min-h-screen py-8" :class="isDark ? 'dark' : ''">
    <div class="container mx-auto px-4 max-w-6xl">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2">KALKULAČKA PENZÍ PRO 2026</h1>
          <p class="text-gray-600 dark:text-gray-300">Expertní ekosystém pro důchodovou analýzu a optimalizaci</p>
        </div>
        
        <button
          @click="toggleDarkMode"
          class="p-2 rounded-lg transition-colors duration-300 hover:scale-105"
          :class="isDark ? 'bg-amber-400 text-gray-900' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          :title="isDark ? 'Přepnout na světlý režim' : 'Přepnout na tmavý režim'"
        >
          <!-- Sun icon for dark mode -->
          <svg v-if="isDark" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9.5-9.5 1-1M21 12h-1M3 12H2m15.5 9.5l-1-1M12 21v-1m0-16v-1m-9.5 9.5-1 1M3 12h1m18 0l-1 1M12 3v1m0 16v1m-9.5-9.5-1 1M21 12h-1" />
          </svg>
          <!-- Moon icon for light mode -->
          <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 1 21 12.79z" />
          </svg>
        </button>
      </div>

      <div class="bg-white dark:bg-[#16213e] rounded-lg shadow-md transition-colors duration-300">
        <div class="flex border-b-2 border-gray-100 dark:border-[#2d3748] overflow-x-auto tab-container">
          <div
            v-for="tab in tabs"
            :key="tab.id"
            class="px-6 py-3 cursor-pointer border-b-2 transition-all duration-300 whitespace-nowrap hover:scale-105"
            :class="[
              activeTab === tab.id
                ? 'border-primary text-primary bg-primary/5'
                : 'border-transparent text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-800/50'
            ]"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </div>
        </div>

        <div class="p-6 text-gray-800 dark:text-gray-100 tab-content">
          <!-- Tab: Důchod -->
          <div v-if="activeTab === 'pension'" class="space-y-4 slide-in">
            <Input
              v-model="pensionForm.monthlyIncome"
              label="Průměrný měsíční příjem (Kč)"
              type="number"
              placeholder="38000"
            />
            <Input
              v-model="pensionForm.insuranceYears"
              label="Počet let pojištění"
              type="number"
              placeholder="45"
              :min="0"
              :max="50"
            />
            <Input
              v-model="pensionForm.excludedDays"
              label="Vyloučené dny (nemoc, péče o dítě)"
              type="number"
              placeholder="0"
              :min="0"
            />
            <Button
              variant="primary"
              :disabled="loading"
              @click="calculatePension"
            >
              {{ loading ? 'Načítání...' : 'Vypočítat důchod' }}
            </Button>

            <div v-if="store.hasResult" class="mt-6 space-y-6 bounce-in">
              <div class="p-6 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 transition-all duration-300 shadow-lg hover:shadow-xl">
                <h3 class="text-lg font-semibold text-green-700 dark:text-green-400 mb-4">Výsledek výpočtu</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="space-y-2">
                    <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
                      <span class="text-gray-700 dark:text-gray-300">OVZ:</span>
                      <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(store.lastResult?.ovz).toFixed(2) }} Kč</span>
                    </div>
                    <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
                      <span class="text-gray-700 dark:text-gray-300">Výpočtový základ:</span>
                      <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(store.lastResult?.vz).toFixed(2) }} Kč</span>
                    </div>
                    <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
                      <span class="text-gray-700 dark:text-gray-300">Základní výměra:</span>
                      <span class="font-medium text-gray-900 dark:text-gray-100">{{ store.lastResult?.base_pension }} Kč</span>
                    </div>
                    <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
                      <span class="text-gray-700 dark:text-gray-300">Procentní sazba:</span>
                      <span class="font-medium text-gray-900 dark:text-gray-100">{{ store.lastResult?.percent_rate }}%</span>
                    </div>
                    <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
                      <span class="text-gray-700 dark:text-gray-300">Pojištění (roky):</span>
                      <span class="font-medium text-gray-900 dark:text-gray-100">{{ store.lastResult?.insurance_years }}</span>
                    </div>
                    <div class="flex justify-between py-2 font-bold text-green-700 dark:text-green-400 text-lg">
                      <span>Celkový důchod:</span>
                      <span>{{ Number(store.lastResult?.pension_amount).toFixed(2) }} Kč</span>
                    </div>
                  </div>
                  <PensionChart
                    :ovz="store.lastResult?.ovz || 0"
                    :vz="store.lastResult?.vz || 0"
                    :basePension="store.lastResult?.base_pension || 0"
                    :percentRate="store.lastResult?.percent_rate || 0"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Předčasný -->
          <EarlyRetirement v-if="activeTab === 'early-retirement'" />

          <!-- Tab: OVZ -->
          <OVZCalculator v-if="activeTab === 'ovz'" />

          <!-- Tab: Paradox -->
          <ParadoxResolver v-if="activeTab === 'paradox'" />

          <!-- Tab: IOLDP -->
          <IOLDPUploader v-if="activeTab === 'iol-dp'" />

          <!-- Tab: Ekonomika -->
          <EconomicIndicators v-if="activeTab === 'economic'" />

          <!-- Tab: Vizualizace -->
          <CalculationVisualization v-if="activeTab === 'visualization'" />

          <!-- Tab: Porovnání -->
          <PensionComparison v-if="activeTab === 'comparison'" />

          <!-- Tab: Historie -->
          <CalculationHistory v-if="activeTab === 'history'" />
        </div>
      </div>

      <div v-if="store.error" class="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>
    </div>
  </div>
</template>

<style>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes bounceIn {
  0% { opacity: 0; transform: scale(0.3); }
  50% { opacity: 1; transform: scale(1.05); }
  70% { transform: scale(0.9); }
  100% { opacity: 1; transform: scale(1); }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}

.slide-in {
  animation: slideIn 0.4s ease-out;
}

.bounce-in {
  animation: bounceIn 0.5s ease-out;
}

.tab-content {
  animation: fadeIn 0.3s ease-out;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .tab-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .tab-container::-webkit-scrollbar {
    display: none;
  }
}

/* Custom scrollbar for webkit browsers */
.tab-container::-webkit-scrollbar {
  height: 4px;
}

.tab-container::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.tab-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.tab-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import { calculatorService } from '@/services/calculator';
import { pensionFormSchema, type PensionFormData } from '@/types/pension';
import Button from '@/components/common/Button.vue';
import Input from '@/components/common/Input.vue';
import PensionChart from '@/components/PensionChart.vue';
import EarlyRetirement from '@/components/calculator/EarlyRetirement.vue';
import OVZCalculator from '@/components/calculator/OVZCalculator.vue';
import ParadoxResolver from '@/components/calculator/ParadoxResolver.vue';
import IOLDPUploader from '@/components/calculator/IOLDPUploader.vue';
import EconomicIndicators from '@/components/calculator/EconomicIndicators.vue';
import CalculationVisualization from '@/components/calculator/CalculationVisualization.vue';
import PensionComparison from '@/components/calculator/PensionComparison.vue';
import CalculationHistory from '@/components/calculator/CalculationHistory.vue';

const store = useCalculatorStore();
const loading = ref(false);
const activeTab = ref('pension');
const isDark = ref(false);

const tabs = [
  { id: 'pension', label: 'Důchod' },
  { id: 'early-retirement', label: 'Předčasný' },
  { id: 'ovz', label: 'OVZ' },
  { id: 'paradox', label: 'Paradox' },
  { id: 'iol-dp', label: 'IOLDP' },
  { id: 'economic', label: 'Ekonomika' },
  { id: 'visualization', label: 'Vizualizace' },
  { id: 'comparison', label: 'Porovnání' },
  { id: 'history', label: 'Historie' },
];

// Load pension form data
const pensionForm = ref({
  monthlyIncome: 38000,
  insuranceYears: 45,
  excludedDays: 0,
});

async function calculatePension() {
  try {
    // Validate form data
    const validatedData = pensionFormSchema.parse(pensionForm.value);
    
    await store.calculatePension({
      annual_incomes: [validatedData.monthlyIncome * 12],
      coefficients: [1.0581],
      insurance_years: validatedData.insuranceYears,
      excluded_days: validatedData.excludedDays || 0,
    });
  } catch (err: any) {
    if (err.name === 'ZodError') {
      store.error = err.errors[0].message;
    } else {
      // Error is handled in store
    }
  }
}

function toggleDarkMode() {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
}

onMounted(() => {
  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDark.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>
