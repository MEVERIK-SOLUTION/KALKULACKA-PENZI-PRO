<template>
  <Card title="Rozhodovací paradox náhradních dob">
    <div class="space-y-4">
      <div class="bg-amber-50 dark:bg-amber-900/20 p-4 rounded border border-amber-200 dark:border-amber-800 transition-colors duration-300">
        <h4 class="font-medium text-amber-800 dark:text-amber-300 mb-2">Co je rozhodovací paradox?</h4>
        <p class="text-sm text-amber-700 dark:text-amber-400">
          Náhradní doba (studium, vojna) zvyšuje jmenovatele (dny), ale ne z čitatele (příjem). 
          To může <strong>snížit OVZ</strong>. Někdy se vyplatí ji vyloučit!
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          v-model="form.annualIncome"
          label="Roční příjem (Kč)"
          type="number"
          placeholder="456000"
        />
        <Input
          v-model="form.coefficient"
          label="Koeficient"
          type="number"
          placeholder="1.0581"
          step="0.0001"
        />
        <Input
          v-model="form.totalDays"
          label="Celkem dní"
          type="number"
          placeholder="16425"
          :min="0"
        />
        <Input
          v-model="form.substituteDays"
          label="Náhradní doby (dny)"
          type="number"
          placeholder="365"
          :min="0"
        />
      </div>

      <Button
        variant="primary"
        :disabled="loading"
        @click="resolveParadox"
      >
        {{ loading ? 'Analyzuji...' : 'Vyřešit paradox' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>

      <div v-if="result" class="mt-6 space-y-4">
        <div class="p-6 bg-white dark:bg-[#16213e] rounded-lg shadow border-2 dark:border-[#2d3748] transition-colors duration-300" :class="recommendationClass">
          <h3 class="text-lg font-semibold mb-4">Rozhodnutí: <span :class="recommendationColor">{{ result.recommendation }}</span></h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <h4 class="font-medium text-gray-700">S náhradní dobou</h4>
              <div class="flex justify-between py-2 border-b">
                <span>OVZ:</span>
                <span class="font-medium">{{ Number(result.ovz_with_inclusion).toFixed(2) }} Kč</span>
              </div>
            </div>
            
            <div class="space-y-2">
              <h4 class="font-medium text-gray-700">Bez náhradní doby</h4>
              <div class="flex justify-between py-2 border-b">
                <span>OVZ:</span>
                <span class="font-medium">{{ Number(result.ovz_with_exclusion).toFixed(2) }} Kč</span>
              </div>
            </div>
          </div>

          <div class="mt-4 p-4 rounded" :class="differenceClass">
            <div class="flex justify-between font-bold text-lg">
              <span>Rozdíl:</span>
              <span>{{ Number(result.difference).toFixed(2) }} Kč</span>
            </div>
            <p class="text-sm mt-2">Náhradní doba {{ result.difference > 0 ? 'zvyšuje' : 'snižuje' }} váš OVZ o {{ Number(Math.abs(result.difference)).toFixed(2) }} Kč</p>
          </div>

          <!-- Vizualizace - jednoduchý bar chart -->
          <div class="mt-6">
            <h4 class="font-medium mb-3">Srovnání OVZ</h4>
            <div class="space-y-3">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>S náhradní dobou</span>
                  <span>{{ Number(result.ovz_with_inclusion).toFixed(2) }} Kč</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-6">
                  <div 
                    class="bg-blue-500 h-6 rounded-full transition-all duration-500" 
                    :style="{ width: inclusionPercent + '%' }"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>Bez náhradní doby</span>
                  <span>{{ Number(result.ovz_with_exclusion).toFixed(2) }} Kč</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-6">
                  <div 
                    class="bg-green-500 h-6 rounded-full transition-all duration-500" 
                    :style="{ width: exclusionPercent + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import { calculatorService } from '@/services/calculator';
import type { ParadoxResponse } from '@/types/pension';
import Card from '@/components/common/Card.vue';
import Input from '@/components/common/Input.vue';
import Button from '@/components/common/Button.vue';

const store = useCalculatorStore();
const loading = ref(false);
const result = ref<ParadoxResponse | null>(null);

const form = ref({
  annualIncome: 456000,
  coefficient: 1.0581,
  totalDays: 16425,
  substituteDays: 365,
});

const inclusionPercent = computed(() => {
  if (!result.value) return 0;
  const max = Math.max(result.value.ovz_with_inclusion, result.value.ovz_with_exclusion);
  return (result.value.ovz_with_inclusion / max) * 100;
});

const exclusionPercent = computed(() => {
  if (!result.value) return 0;
  const max = Math.max(result.value.ovz_with_inclusion, result.value.ovz_with_exclusion);
  return (result.value.ovz_with_exclusion / max) * 100;
});

const recommendationClass = computed(() => {
  if (!result.value) return '';
  return result.value.recommendation.includes('Vyloučit') 
    ? 'border-red-300 bg-red-50' 
    : 'border-green-300 bg-green-50';
});

const recommendationColor = computed(() => {
  if (!result.value) return '';
  return result.value.recommendation.includes('Vyloučit') 
    ? 'text-red-600' 
    : 'text-green-600';
});

const differenceClass = computed(() => {
  if (!result.value) return '';
  return result.value.difference > 0 
    ? 'bg-red-50 text-red-700' 
    : 'bg-green-50 text-green-700';
});

async function resolveParadox() {
  loading.value = true;
  result.value = null;
  
  try {
    const { data } = await calculatorService.resolveParadox({
      annual_incomes: [form.value.annualIncome],
      coefficients: [form.value.coefficient],
      total_days: form.value.totalDays,
      substitute_days: form.value.substituteDays,
    });
    result.value = data;
  } catch (err: any) {
    store.error = err.message || 'Chyba při řešení paradoxu';
  } finally {
    loading.value = false;
  }
}
</script>
