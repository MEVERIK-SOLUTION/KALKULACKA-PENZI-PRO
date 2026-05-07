<template>
  <Card title="OVZ - Osobní vyměřovací základ">
    <div class="space-y-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded border border-blue-200 dark:border-blue-800 transition-colors duration-300">
        <h4 class="font-medium text-blue-800 dark:text-blue-300 mb-2">Jak se počítá OVZ? (§ 15 ZDP)</h4>
        <p class="text-sm text-blue-600 dark:text-blue-400">
          OVZ = Σ(Roční příjem × Koeficient) ÷ (Dny - Vyloučené doby) × 30,4167
        </p>
      </div>

      <!-- Formulář pro každý rok -->
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <h4 class="font-medium text-gray-800 dark:text-gray-200">Roční příjmy a koeficienty</h4>
          <Button variant="secondary" size="sm" @click="addYear">
            + Přidat rok
          </Button>
        </div>

        <div v-for="(item, index) in form.years" :key="index" 
             class="grid grid-cols-1 md:grid-cols-3 gap-3 p-3 bg-gray-50 dark:bg-[#16213e] rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <Input
            v-model="item.income"
            :label="`Rok ${index + 1} - Příjem (Kč)`"
            type="number"
            placeholder="456000"
          />
          <Input
            v-model="item.coefficient"
            :label="`Koeficient ${index + 1}`"
            type="number"
            placeholder="1.0581"
            step="0.0001"
          />
          <div class="flex items-end">
            <Button 
              variant="danger" 
              size="sm"
              :disabled="form.years.length <= 1"
              @click="removeYear(index)"
            >
              Odebrat
            </Button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Input
            v-model="form.totalDays"
            label="Celkem dní (rozhodné období)"
            type="number"
            placeholder="16425"
            :min="0"
          />
          <Input
            v-model="form.excludedDays"
            label="Vyloučené doby (dny)"
            type="number"
            placeholder="0"
            :min="0"
          />
        </div>
      </div>

      <Button
        variant="primary"
        :disabled="loading"
        @click="calculateOVZ"
      >
        {{ loading ? 'Počítám...' : 'Vypočítat OVZ' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 text-red-600 rounded">
        {{ store.error }}
      </div>

      <!-- Výsledek s vizualizací -->
      <div v-if="result" class="mt-6 space-y-6">
        <div class="p-6 bg-green-50 rounded-lg">
          <h3 class="text-lg font-semibold text-green-700 mb-4">Výsledek OVZ</h3>
          <div class="space-y-2">
            <div class="flex justify-between py-2 border-b border-green-200">
              <span>OVZ:</span>
              <span class="font-medium">{{ Number(result.ovz).toFixed(2) }} Kč</span>
            </div>
          </div>
        </div>

        <!-- Jednoduchý progress bar - vizualizace -->
        <div v-if="ovzProgress > 0" class="space-y-2">
          <h4 class="font-medium">Vizualizace OVZ</h4>
          <div class="w-full bg-gray-200 rounded-full h-8">
            <div 
              class="bg-gradient-to-r from-blue-400 to-green-500 h-8 rounded-full transition-all duration-700 flex items-center justify-center"
              :style="{ width: ovzProgress + '%' }"
            >
              <span v-if="ovzProgress > 10" class="text-white text-sm font-bold">
                {{ Number(result.ovz).toFixed(0) }} Kč
              </span>
            </div>
          </div>
          <p class="text-sm text-gray-600 text-center">
            OVZ vůči průměrné mzdě ({{ avgSalary2026 }} Kč)
          </p>
        </div>

        <!-- Tabulka s roky (Excel-like) -->
        <div v-if="form.years.length > 0" class="mt-4">
          <h4 class="font-medium mb-3">Přehled po letech</h4>
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-100">
                <th class="text-left p-2">Rok</th>
                <th class="text-right p-2">Příjem (Kč)</th>
                <th class="text-right p-2">Koeficient</th>
                <th class="text-right p-2">Vyměřovací základ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in form.years" :key="idx" class="border-t">
                <td class="p-2">{{ idx + 1 }}.</td>
                <td class="text-right p-2">{{ Number(item.income).toLocaleString('cs-CZ') }}</td>
                <td class="text-right p-2">{{ item.coefficient }}</td>
                <td class="text-right p-2 font-medium">
                  {{ calculateYearlyVZ(item.income, item.coefficient).toFixed(2) }} Kč
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import type { OVZResponse } from '@/types/pension';
import Card from '@/components/common/Card.vue';
import Input from '@/components/common/Input.vue';
import Button from '@/components/common/Button.vue';

const store = useCalculatorStore();
const loading = ref(false);
const result = ref<OVZResponse | null>(null);

const avgSalary2026 = 49262; // Průměrná mzda 2026

const form = ref({
  years: [
    { income: 456000, coefficient: 1.0581 },
  ],
  totalDays: 16425,
  excludedDays: 0,
});

const ovzProgress = computed(() => {
  if (!result.value) return 0;
  const maxOVZ = avgSalary2026 * 3; // 3x průměrná mzda jako maximum
  return Math.min((result.value.ovz / maxOVZ) * 100, 100);
});

function addYear() {
  form.value.years.push({ income: 0, coefficient: 1.0581 });
}

function removeYear(index: number) {
  form.value.years.splice(index, 1);
}

function calculateYearlyVZ(income: number, coefficient: number): number {
  // Zjednodušený výpočet pro vizualizaci
  return (income * coefficient) / (form.value.totalDays - form.value.excludedDays) * 30.4167;
}

async function calculateOVZ() {
  loading.value = true;
  result.value = null;
  
  try {
    const { data } = await calculatorService.calculateOVZ({
      annual_incomes: form.value.years.map(y => y.income),
      coefficients: form.value.years.map(y => y.coefficient),
      total_days: form.value.totalDays,
      excluded_days: form.value.excludedDays,
    });
    result.value = data;
  } catch (err: any) {
    store.error = err.message || 'Chyba při výpočtu OVZ';
  } finally {
    loading.value = false;
  }
}
</script>
