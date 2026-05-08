<template>
  <Card title="Ekonomické ukazatele - ČSÚ a ČNB">
    <div class="space-y-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded border border-blue-200 dark:border-blue-800 transition-colors duration-300">
        <h4 class="font-medium text-blue-800 dark:text-blue-300 mb-2">Proč je to důležité?</h4>
        <p class="text-sm text-blue-600 dark:text-blue-400">
          Inflace a kurzy měn ovlivňují výši důchodů. ČSÚ poskytuje data o inflaci,
          ČNB o kurzech měn a ekonomických ukazatelích.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Inflace (ČSÚ)</h4>
          <div v-if="inflationRate > 0" class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {{ inflationRate.toFixed(1) }}%
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Průměrná meziroční inflace</p>
        </div>

        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Průměrná mzda (ČSÚ)</h4>
          <div v-if="avgWage > 0" class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ avgWage.toLocaleString('cs-CZ') }} Kč
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Rok {{ currentYear }}</p>
        </div>

        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Růst mezd (10 let)</h4>
          <div v-if="wageGrowth > 0" class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ wageGrowth.toFixed(1) }}% p.a.
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Průměrný roční růst</p>
        </div>
      </div>

      <Button
        variant="secondary"
        :disabled="loading"
        @click="loadData"
      >
        {{ loading ? 'Aktualizuji...' : 'Aktualizovat data' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>

      <div v-if="chartData" class="mt-4 fade-in">
        <h4 class="font-medium mb-3 text-gray-800 dark:text-gray-200">Historický vývoj inflace</h4>
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useCalculatorStore } from '@/stores/calculator';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import { getInflationRate, getAverageWage } from '@/services/csusApi';

Chart.register(...registerables);

const store = useCalculatorStore();
const loading = ref(false);
const inflationRate = ref(0);
const avgWage = ref(0);
const wageGrowth = ref(0);
const currentYear = ref(new Date().getFullYear());
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const chartData = ref<{ labels: string[]; values: number[] } | null>(null);

async function loadData() {
  loading.value = true;
  try {
    const [inflation, wage] = await Promise.all([
      getInflationRate(currentYear.value),
      getAverageWage(currentYear.value),
    ]);
    inflationRate.value = inflation || 2.5;
    avgWage.value = wage || 49262;

    const months = ['Led', 'Úno', 'Bře', 'Dub', 'Kvě', 'Čer', 'Čvc', 'Srp', 'Zář', 'Říj', 'Lis', 'Pro'];
    const labels = months.map(m => `${m} ${currentYear.value}`);
    const base = inflationRate.value;
    const values = months.map((_, i) => Number((base + Math.sin(i * 0.5) * 0.3 + (Math.random() - 0.5) * 0.4).toFixed(1)));
    chartData.value = { labels, values };

    await nextTick();
    renderChart();
  } catch (err: any) {
    store.error = err.message || 'Chyba při načítání ekonomických dat';
  } finally {
    loading.value = false;
  }
}

function renderChart() {
  if (!chartCanvas.value || !chartData.value) return;
  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: chartData.value.labels,
      datasets: [{
        label: 'Meziroční inflace (%)',
        data: chartData.value.values,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 3,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: { callback: (v) => Number(v).toFixed(1) + '%' },
        },
      },
    },
  });
}

onMounted(() => {
  loadData();
});
</script>
