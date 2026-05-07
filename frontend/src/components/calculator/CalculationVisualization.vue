<template>
  <Card title="Vizualizace OVZ - Průběh výpočtu">
    <div class="space-y-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded border border-blue-200 dark:border-blue-800 transition-colors duration-300">
        <h4 class="font-medium text-blue-800 dark:text-blue-300 mb-2">Jak se počítá OVZ?</h4>
        <p class="text-sm text-blue-600 dark:text-blue-400">
          OVZ = Σ(Roční příjem × Koeficient) ÷ (Dny - Vyloučené dny) × 30,4167
        </p>
      </div>

      <!-- Krok 1: Roční příjmy -->
      <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">
          <span class="inline-block w-6 h-6 bg-blue-500 text-white text-center rounded-full text-xs mr-2">1</span>
          Roční příjmy a koeficienty
        </h4>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-100 dark:bg-[#1a1a2e]">
                <th class="text-left p-2 text-gray-700 dark:text-gray-300">Rok</th>
                <th class="text-right p-2 text-gray-700 dark:text-gray-300">Příjem (Kč)</th>
                <th class="text-right p-2 text-gray-700 dark:text-gray-300">Koeficient</th>
                <th class="text-right p-2 text-gray-700 dark:text-gray-300">Vyměřovací základ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in breakdown.years" :key="idx" class="border-t border-gray-200 dark:border-[#2d3748]">
                <td class="p-2 text-gray-800 dark:text-gray-200">{{ idx + 1 }}.</td>
                <td class="text-right p-2 text-gray-800 dark:text-gray-200">{{ Number(item.income).toLocaleString('cs-CZ') }}</td>
                <td class="text-right p-2 text-gray-800 dark:text-gray-200">{{ item.coefficient }}</td>
                <td class="text-right p-2 font-medium text-gray-900 dark:text-gray-100">
                  {{ calculateYearlyVZ(item.income, item.coefficient).toFixed(2) }} Kč
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="bg-gray-50 dark:bg-[#1a1a2e] font-medium">
                <td class="p-2 text-gray-700 dark:text-gray-300" colspan="3">Součet (Σ)</td>
                <td class="text-right p-2 text-gray-900 dark:text-gray-100">{{ Number(breakdown.totalIncome).toLocaleString('cs-CZ') }} Kč</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      <!-- Krok 2: OVZ výpočet -->
      <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">
          <span class="inline-block w-6 h-6 bg-blue-500 text-white text-center rounded-full text-xs mr-2">2</span>
          Výpočet OVZ
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <div class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm text-gray-600 dark:text-gray-400">Σ (Příjem × Koeficient):</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(breakdown.totalWeighted).toLocaleString('cs-CZ') }} Kč</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm text-gray-600 dark:text-gray-400">Dny celkem:</span>
              <span class="font-medium">{{ breakdown.totalDays }}</span>
            </div>
            <div class="flex justify-between py-2 border-b">
              <span class="text-sm text-gray-600">Vyloučené dny:</span>
              <span class="font-medium text-red-600">- {{ breakdown.excludedDays }}</span>
            </div>
            <div class="flex justify-between py-2 border-b">
              <span class="text-sm text-gray-600">Dny pro výpočet:</span>
              <span class="font-medium">{{ breakdown.totalDays - breakdown.excludedDays }}</span>
            </div>
            <div class="flex justify-between py-2 border-b">
              <span class="text-sm text-gray-600">Koeficient (30,4167):</span>
              <span class="font-medium">× 30,4167</span>
            </div>
            <div class="flex justify-between py-2 font-bold text-lg border-t-2 border-blue-500">
              <span>OVZ:</span>
              <span class="text-blue-600">{{ Number(breakdown.ovz).toFixed(2) }} Kč</span>
            </div>
          </div>

          <!-- Chart.js Graf: OVZ po letech -->
          <div>
            <canvas ref="ovzChartRef" class="w-full h-48"></canvas>
          </div>
        </div>
      </div>

      <!-- Krok 3: Redukční meze -->
      <div v-if="reductionData" class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">
          <span class="inline-block w-6 h-6 bg-green-500 text-white text-center rounded-full text-xs mr-2">3</span>
          Redukční meze (§ 15 ZDP)
        </h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <div class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm text-gray-600 dark:text-gray-400">OVZ:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(reductionData.ovz).toFixed(2) }} Kč</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm text-gray-600 dark:text-gray-400">1. hranice (21 546 Kč):</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ reductionData.limit1 }} Kč</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm text-gray-600 dark:text-gray-400">2. hranice (195 868 Kč):</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ reductionData.limit2 }} Kč</span>
            </div>
            <div v-for="(item, idx) in reductionData.brackets" :key="idx" 
                 class="flex justify-between py-2 border-b border-gray-200 dark:border-[#2d3748]">
              <span class="text-sm" :class="item.rate === 0 ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'">
                {{ item.description }}:
              </span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(item.amount).toFixed(2) }} Kč ({{ item.rate * 100 }}%)</span>
            </div>
            <div class="flex justify-between py-2 font-bold text-lg border-t-2 border-green-500">
              <span class="text-gray-900 dark:text-gray-100">Výpočtový základ (VZ):</span>
              <span class="text-green-600 dark:text-green-400">{{ Number(reductionData.vz).toFixed(2) }} Kč</span>
            </div>
          </div>
          
          <!-- Redukční graf -->
          <div>
            <canvas ref="reductionChartRef" class="w-full h-48"></canvas>
          </div>
        </div>
      </div>

      <!-- Krok 4: Výsledek důchodu -->
      <div v-if="pensionResult" class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border-2 border-green-300 dark:border-green-800 transition-colors duration-300">
        <h4 class="font-medium text-green-800 dark:text-green-300 mb-4">
          <span class="inline-block w-6 h-6 bg-green-600 text-white text-center rounded-full text-xs mr-2">4</span>
          Výpočet důchodu
        </h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
              <span class="text-gray-700 dark:text-gray-300">Základní výměra (§ 4):</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ pensionResult.base_pension }} Kč</span>
            </div>
            <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
              <span class="text-gray-700 dark:text-gray-300">VZ po redukci:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ Number(pensionResult.vz).toFixed(2) }} Kč</span>
            </div>
            <div class="flex justify-between py-2 border-b border-green-200 dark:border-green-800">
              <span class="text-gray-700 dark:text-gray-300">Procentní sazba ({{ pensionResult.insurance_years }} let × {{ pensionResult.percent_rate }}%):</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ (pensionResult.vz * pensionResult.percent_rate / 100 * pensionResult.insurance_years).toFixed(2) }} Kč</span>
            </div>
            <div class="flex justify-between py-2 font-bold text-xl border-t-2 border-green-500">
              <span class="text-gray-900 dark:text-gray-100">Celkový důchod:</span>
              <span class="text-green-600 dark:text-green-400">{{ Number(pensionResult.pension_amount).toFixed(2) }} Kč</span>
            </div>
          </div>
          
          <!-- Pao Chart - rozložení důchodu -->
          <div>
            <canvas ref="pensionChartRef" class="w-full h-48"></canvas>
          </div>
        </div>
      </div>

      <!-- Tlačítko pro spuštění výpočtu -->
      <Button
        variant="primary"
        :disabled="loading || !hasData"
        @click="calculateAll"
      >
        {{ loading ? 'Počítám...' : 'Spočítat krok po kroku' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import type { OVZResponse, PensionResponse } from '@/types/pension';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import { Chart, registerables } from 'chart.js';
import { Pie, Bar } from 'vue-chartjs';

// Register Chart.js components
registerables();

const store = useCalculatorStore();
const loading = ref(false);
const ovzChartRef = ref<HTMLCanvasElement | null>(null);
const reductionChartRef = ref<HTMLCanvasElement | null>(null);
const pensionChartRef = ref<HTMLCanvasElement | null>(null);

const breakdown = ref({
  years: [] as Array<{ income: number; coefficient: number }>,
  totalIncome: 0,
  totalWeighted: 0,
  totalDays: 0,
  excludedDays: 0,
  ovz: 0,
});

const reductionData = ref<null | {
  ovz: number;
  limit1: number;
  limit2: number;
  brackets: Array<{ description: string; amount: number; rate: number }>;
  vz: number;
}>(null);

const pensionResult = ref<PensionResponse | null>(null);

const form = ref({
  years: [{ income: 456000, coefficient: 1.0581 }],
  totalDays: 16425,
  excludedDays: 0,
  insuranceYears: 45,
});

const hasData = computed(() => form.value.years.length > 0);

function calculateYearlyVZ(income: number, coefficient: number): number {
  const weighted = income * coefficient;
  const days = form.value.totalDays - form.value.excludedDays;
  return (weighted / days) * 30.4167;
}

async function calculateAll() {
  loading.value = true;
  breakdown.value.years = [];
  reductionData.value = null;
  pensionResult.value = null;

  try {
    // Krok 1: Calculate OVZ
    const { data: ovzData } = await calculatorService.calculateOVZ({
      annual_incomes: form.value.years.map(y => y.income),
      coefficients: form.value.years.map(y => y.coefficient),
      total_days: form.value.totalDays,
      excluded_days: form.value.excludedDays,
    });

    // Build breakdown
    const totalWeighted = form.value.years.reduce((sum, y) => sum + (y.income * y.coefficient), 0);
    breakdown.value = {
      years: form.value.years.map(y => ({ ...y })),
      totalIncome: form.value.years.reduce((sum, y) => sum + y.income, 0),
      totalWeighted,
      totalDays: form.value.totalDays,
      excludedDays: form.value.excludedDays,
      ovz: ovzData.ovz,
    };

    await nextTick();
    renderOVZChart();

    // Krok 3: Reduction
    const config = {
      reduction_limits: [
        { threshold: 21546, rate: 0.99 },
        { threshold: 195868, rate: 0.26 },
        { threshold: null, rate: 0 },
      ],
    };
    
    const vz = calculateVZ(ovzData.ovz, config);
    
    reductionData.value = {
      ovz: ovzData.ovz,
      limit1: 21546,
      limit2: 195868,
      brackets: [
        { description: '1. hranice (99%)', amount: Math.min(ovzData.ovz, 21546) * 0.99, rate: 0.99 },
        { description: 'Nad 1. hranici (26%)', amount: Math.max(0, Math.min(ovzData.ovz, 195868) - 21546) * 0.26, rate: 0.26 },
        { description: 'Nad 2. hranici (0%)', amount: Math.max(0, ovzData.ovz - 195868) * 0, rate: 0 },
      ],
      vz,
    };

    await nextTick();
    renderReductionChart();

    // Krok 4: Pension
    const { data: pensionData } = await calculatorService.calculatePension({
      annual_incomes: form.value.years.map(y => y.income),
      coefficients: form.value.years.map(y => y.coefficient),
      insurance_years: form.value.insuranceYears,
      excluded_days: form.value.excludedDays,
    });

    pensionResult.value = pensionData;
    
    await nextTick();
    renderPensionChart();
  } catch (err: any) {
    store.error = err.message || 'Chyba při výpočtu';
  } finally {
    loading.value = false;
  }
}

function calculateVZ(ovz: number, config: any): number {
  // Simplified reduction calculation
  if (ovz <= 21546) return ovz * 0.99;
  if (ovz <= 195868) return 21546 * 0.99 + (ovz - 21546) * 0.26;
  return 21546 * 0.99 + (195868 - 21546) * 0.26;
}

function renderOVZChart() {
  if (!ovzChartRef.value) return;
  
  const ctx = ovzChartRef.value.getContext('2d');
  if (!ctx) return;

  const isDarkMode = document.documentElement.classList.contains('dark');
  const textColor = isDarkMode ? '#cbd5e1' : '#374151';
  const gridColor = isDarkMode ? '#334155' : '#e5e7eb';
  
  const years = breakdown.value.years;
  const labels = years.map((_, idx) => `Rok ${idx + 1}`);
  const incomes = years.map(y => y.income);
  const ovzValues = years.map(y => calculateYearlyVZ(y.income, y.coefficient));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Roční příjem',
          data: incomes,
          backgroundColor: 'rgba(59, 130, 246, 0.5)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 1,
        },
        {
          label: 'OVZ na rok',
          data: ovzValues,
          backgroundColor: 'rgba(16, 185, 129, 0.5)',
          borderColor: 'rgb(16, 185, 129)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { 
          position: 'top',
          labels: { color: textColor }
        },
        title: { 
          display: true, 
          text: 'OVZ po letech',
          color: textColor
        },
      },
      scales: {
        x: {
          ticks: { color: textColor },
          grid: { color: gridColor }
        },
        y: {
          ticks: { color: textColor },
          grid: { color: gridColor }
        }
      }
    },
  });
}

function renderReductionChart() {
  if (!reductionChartRef.value || !reductionData.value) return;
  
  const ctx = reductionChartRef.value.getContext('2d');
  if (!ctx) return;

  const isDarkMode = document.documentElement.classList.contains('dark');
  const textColor = isDarkMode ? '#cbd5e1' : '#374151';
  const gridColor = isDarkMode ? '#334155' : '#e5e7eb';
  
  const data = reductionData.value;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.brackets.map(b => b.description),
      datasets: [
        {
          label: 'Částka po redukci',
          data: data.brackets.map(b => b.amount),
          backgroundColor: [
            'rgba(59, 130, 246, 0.5)',
            'rgba(16, 185, 129, 0.5)',
            'rgba(239, 68, 68, 0.5)',
          ],
          borderColor: [
            'rgb(59, 130, 246)',
            'rgb(16, 185, 129)',
            'rgb(239, 68, 68)',
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { 
          display: true, 
          text: 'Redukční meze',
          color: textColor
        },
      },
      scales: {
        x: {
          ticks: { color: textColor },
          grid: { color: gridColor }
        },
        y: {
          ticks: { color: textColor },
          grid: { color: gridColor }
        }
      }
    },
  });
}

function renderPensionChart() {
  if (!pensionChartRef.value || !pensionResult.value) return;
  
  const ctx = pensionChartRef.value.getContext('2d');
  if (!ctx) return;

  const isDarkMode = document.documentElement.classList.contains('dark');
  const textColor = isDarkMode ? '#cbd5e1' : '#374151';
  
  const data = pensionResult.value;
  const baseAmount = data.base_pension;
  const percentAmount = data.vz * data.percent_rate / 100 * data.insurance_years;
  
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Základní výměra', 'Procentní část'],
      datasets: [
        {
          data: [baseAmount, percentAmount],
          backgroundColor: [
            'rgba(59, 130, 246, 0.5)',
            'rgba(16, 185, 129, 0.5)',
          ],
          borderColor: [
            'rgb(59, 130, 246)',
            'rgb(16, 185, 129)',
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { 
          position: 'top',
          labels: { color: textColor }
        },
        title: { 
          display: true, 
          text: 'Rozložení důchodu',
          color: textColor
        },
      },
    },
  });
}
</script>
