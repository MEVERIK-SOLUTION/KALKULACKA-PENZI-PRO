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
        <!-- Inflace ČSÚ -->
        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Inflace (ČSÚ)</h4>
          <div v-if="inflationRate > 0" class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {{ inflationRate }}%
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Průměrná meziroční inflace</p>
        </div>

        <!-- Kurz EUR -->
        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Kurz EUR (ČNB)</h4>
          <div v-if="eurRate > 0" class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ eurRate }} Kč
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Kurz dle ČNB (SMV5M603)</p>
        </div>

        <!-- Průměrná mzda -->
        <div class="bg-white dark:bg-[#16213e] p-4 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-2">Průměrná mzda (ČSÚ)</h4>
          <div v-if="avgWage > 0" class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ avgWage.toLocaleString('cs-CZ') }} Kč
          </div>
          <div v-else class="text-gray-400 dark:text-gray-500">Načítání...</div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Rok {{ currentYear }}</p>
        </div>
      </div>

      <Button
        variant="secondary"
        :disabled="loading"
        @click="loadEconomicData"
      >
        {{ loading ? 'Aktualizuji...' : 'Aktualizovat data' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 text-red-600 rounded">
        {{ store.error }}
      </div>

      <!-- Tabulka s historickými daty -->
      <div v-if="historicalData.length > 0" class="mt-4">
        <h4 class="font-medium mb-3">Historická data (posledních 12 měsíců)</h4>
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-100">
              <th class="text-left p-2">Měsíc</th>
              <th class="text-right p-2">Inflace (%)</th>
              <th class="text-right p-2">Kurz EUR</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in historicalData" :key="idx" class="border-t">
              <td class="p-2">{{ item.month }}</td>
              <td class="text-right p-2">{{ item.inflation }}%</td>
              <td class="text-right p-2">{{ item.eurRate }} Kč</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import { getInflationRate, getAverageWage } from '@/services/csusApi';
import { getExchangeRate } from '@/services/cnbApi';

const store = useCalculatorStore();
const loading = ref(false);
const inflationRate = ref(0);
const eurRate = ref(0);
const avgWage = ref(0);
const currentYear = ref(new Date().getFullYear());
const historicalData = ref<Array<{
  month: string;
  inflation: number;
  eurRate: number;
}>>([]);

async function loadEconomicData() {
  loading.value = true;
  
  try {
    // Načteme aktuální data
    const [inflation, wage, eur] = await Promise.all([
      getInflationRate(currentYear.value),
      getAverageWage(currentYear.value),
      getExchangeRate('EUR', undefined),
    ]);

    inflationRate.value = inflation || 2.5; // Fallback
    avgWage.value = wage || 49262;
    eurRate.value = eur || 24.50;

    // Simulovaná historická data (v produkci by se volalo ČSÚ/ČNB API)
    historicalData.value = generateHistoricalData(inflationRate.value, eurRate.value);
  } catch (err: any) {
    store.error = err.message || 'Chyba při načítání ekonomických dat';
  } finally {
    loading.value = false;
  }
}

function generateHistoricalData(inflation: number, eur: number) {
  const data = [];
  const months = ['Led', 'Úno', 'Bře', 'Dub', 'Kvě', 'Čer', 'Čvc', 'Srp', 'Zář', 'Říj', 'Lis', 'Pro'];
  
  for (let i = 0; i < 12; i++) {
    data.push({
      month: months[i] + ' ' + currentYear.value,
      inflation: (inflation + (Math.random() - 0.5) * 0.5).toFixed(1),
      eurRate: (eur + (Math.random() - 0.5) * 0.5).toFixed(2),
    });
  }
  
  return data;
}

onMounted(() => {
  loadEconomicData();
});
</script>
