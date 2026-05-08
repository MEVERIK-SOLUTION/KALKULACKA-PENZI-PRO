<template>
  <Card title="Porovnání scénářů důchodu">
    <div class="space-y-6">
      <div class="bg-amber-50 dark:bg-amber-900/20 p-4 rounded border border-amber-200 dark:border-amber-800 transition-colors duration-300">
        <h4 class="font-medium text-amber-800 dark:text-amber-300 mb-2">Porovnejte různé scénáře</h4>
        <p class="text-sm text-amber-600 dark:text-amber-400">
          Vytvořte až 3 scénáře s různými příjmy, odpracovanými roky nebo vyloučenými dny
          a porovnejte jejich výsledky vedle sebe.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="(sc, idx) in scenarios" :key="idx" class="border border-gray-200 dark:border-[#2d3748] rounded-lg p-4 bg-white dark:bg-[#16213e] transition-colors duration-300">
          <div class="flex justify-between items-center mb-3">
            <h4 class="font-medium text-gray-700 dark:text-gray-300">Scénář {{ idx + 1 }}</h4>
            <button v-if="scenarios.length > 2" @click="removeScenario(idx)" class="text-red-500 hover:text-red-700 text-sm">
              ✕
            </button>
          </div>
          <div class="space-y-3">
            <Input
              v-model="sc.monthlyIncome"
              :label="'Měsíční příjem (Kč)'"
              type="number"
              :placeholder="String(35000 + idx * 5000)"
            />
            <Input
              v-model="sc.insuranceYears"
              label="Roky pojištění"
              type="number"
              :placeholder="String(40 + idx * 5)"
              :min="0"
              :max="50"
            />
            <Input
              v-model="sc.excludedDays"
              label="Vyloučené dny"
              type="number"
              placeholder="0"
              :min="0"
            />
            <Button
              variant="primary"
              :disabled="loading[idx]"
              @click="calculateScenario(idx)"
            >
              {{ loading[idx] ? '...' : 'Vypočítat' }}
            </Button>
          </div>
          <div v-if="results[idx]" class="mt-4 p-3 bg-green-50 dark:bg-green-900/20 rounded border border-green-200 dark:border-green-800">
            <div class="text-sm space-y-1">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Důchod:</span>
                <span class="font-bold text-green-700 dark:text-green-400">{{ results[idx].pension_amount.toLocaleString('cs-CZ', { minimumFractionDigits: 0 }) }} Kč</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">OVZ:</span>
                <span class="text-gray-800 dark:text-gray-200">{{ results[idx].ovz.toLocaleString('cs-CZ', { minimumFractionDigits: 0 }) }} Kč</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Základ:</span>
                <span class="text-gray-800 dark:text-gray-200">{{ results[idx].vz.toLocaleString('cs-CZ', { minimumFractionDigits: 0 }) }} Kč</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Sazba:</span>
                <span class="text-gray-800 dark:text-gray-200">{{ results[idx].percent_rate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center">
        <Button
          v-if="scenarios.length < 3"
          variant="secondary"
          @click="addScenario"
        >
          + Přidat scénář
        </Button>
      </div>

      <!-- Comparison chart when 2+ results -->
      <div v-if="completedCount >= 2" class="mt-8">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4 text-center">Srovnání výsledků</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-100 dark:bg-[#1a1a2e]">
                <th class="text-left p-2 text-gray-700 dark:text-gray-300">Parametr</th>
                <th v-for="(_, idx) in results" :key="idx" class="text-right p-2 text-gray-700 dark:text-gray-300">
                  Scénář {{ idx + 1 }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-t border-gray-200 dark:border-[#2d3748]">
                <td class="p-2 font-medium text-gray-700 dark:text-gray-300">Měsíční příjem</td>
                <td v-for="(_, idx) in validResults" :key="idx" class="text-right p-2 text-gray-800 dark:text-gray-200">
                  {{ scenarios[idx].monthlyIncome.toLocaleString('cs-CZ') }} Kč
                </td>
              </tr>
              <tr class="border-t border-gray-200 dark:border-[#2d3748]">
                <td class="p-2 font-medium text-gray-700 dark:text-gray-300">Pojištění</td>
                <td v-for="(_, idx) in validResults" :key="idx" class="text-right p-2 text-gray-800 dark:text-gray-200">
                  {{ scenarios[idx].insuranceYears }} let
                </td>
              </tr>
              <tr class="border-t border-gray-200 dark:border-[#2d3748] bg-green-50 dark:bg-green-900/10">
                <td class="p-2 font-bold text-green-700 dark:text-green-400">Důchod</td>
                <td v-for="(r, idx) in validResults" :key="idx" class="text-right p-2 font-bold text-green-700 dark:text-green-400">
                  {{ r.pension_amount.toLocaleString('cs-CZ', { minimumFractionDigits: 0 }) }} Kč
                </td>
              </tr>
              <tr class="border-t border-gray-200 dark:border-[#2d3748]">
                <td class="p-2 font-medium text-gray-700 dark:text-gray-300">OVZ</td>
                <td v-for="(r, idx) in validResults" :key="idx" class="text-right p-2 text-gray-800 dark:text-gray-200">
                  {{ r.ovz.toLocaleString('cs-CZ', { minimumFractionDigits: 0 }) }} Kč
                </td>
              </tr>
              <tr class="border-t border-gray-200 dark:border-[#2d3748]">
                <td class="p-2 font-medium text-gray-700 dark:text-gray-300">Procentní sazba</td>
                <td v-for="(r, idx) in validResults" :key="idx" class="text-right p-2 text-gray-800 dark:text-gray-200">
                  {{ r.percent_rate }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Bar chart comparison -->
        <div class="mt-6">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { calculatorService } from '@/services/calculator';
import Button from '@/components/common/Button.vue';
import Input from '@/components/common/Input.vue';
import Card from '@/components/common/Card.vue';
import type { PensionResponse } from '@/types/pension';

Chart.register(...registerables);

interface Scenario {
  monthlyIncome: number;
  insuranceYears: number;
  excludedDays: number;
}

const scenarios = ref<Scenario[]>([
  { monthlyIncome: 35000, insuranceYears: 40, excludedDays: 0 },
  { monthlyIncome: 45000, insuranceYears: 45, excludedDays: 0 },
]);

const results = ref<(PensionResponse | null)[]>([null, null]);
const loading = ref([false, false]);
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const completedCount = computed(() => results.value.filter(r => r !== null).length);
const validResults = computed(() => results.value.filter((r): r is PensionResponse => r !== null));

function addScenario() {
  if (scenarios.value.length < 3) {
    scenarios.value.push({ monthlyIncome: 55000, insuranceYears: 50, excludedDays: 0 });
    results.value.push(null);
    loading.value.push(false);
  }
}

function removeScenario(idx: number) {
  scenarios.value.splice(idx, 1);
  results.value.splice(idx, 1);
  loading.value.splice(idx, 1);
}

async function calculateScenario(idx: number) {
  loading.value[idx] = true;
  try {
    const { data } = await calculatorService.calculatePension({
      annual_incomes: [scenarios.value[idx].monthlyIncome * 12],
      coefficients: [1.0581],
      insurance_years: scenarios.value[idx].insuranceYears,
      excluded_days: scenarios.value[idx].excludedDays,
    });
    results.value[idx] = data;
  } catch (err: any) {
    results.value[idx] = null;
  } finally {
    loading.value[idx] = false;
  }
}

function renderChart() {
  if (!chartCanvas.value) return;
  const valid = validResults.value;
  if (valid.length < 2) return;

  if (chartInstance) chartInstance.destroy();

  const labels = valid.map((_, i) => `Scénář ${i + 1}`);
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Důchod (Kč)',
          data: valid.map(r => r.pension_amount),
          backgroundColor: 'rgba(34, 197, 94, 0.7)',
          borderColor: 'rgb(34, 197, 94)',
          borderWidth: 1,
        },
        {
          label: 'OVZ (Kč)',
          data: valid.map(r => r.ovz),
          backgroundColor: 'rgba(59, 130, 246, 0.7)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 1,
        },
        {
          label: 'Výpočtový základ (Kč)',
          data: valid.map(r => r.vz),
          backgroundColor: 'rgba(168, 85, 247, 0.7)',
          borderColor: 'rgb(168, 85, 247)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: (v) => Number(v).toLocaleString('cs-CZ') + ' Kč',
          },
        },
      },
    },
  });
}

watch(completedCount, async (count) => {
  if (count >= 2) {
    await nextTick();
    renderChart();
  }
});
</script>
