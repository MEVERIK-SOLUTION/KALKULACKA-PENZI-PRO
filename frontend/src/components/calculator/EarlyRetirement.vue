<template>
  <Card title="Předčasný důchod - Krácení">
    <div class="space-y-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded border border-blue-200 dark:border-blue-800 transition-colors duration-300">
        <h4 class="font-medium text-blue-800 dark:text-blue-300 mb-2">Parametry krácení (§ 31 ZDP)</h4>
        <p class="text-sm text-blue-600 dark:text-blue-400">
          Krácení činí <strong>1,5 % za každých započtených 90 dní</strong> před dosažením důchodového věku.
        </p>
      </div>

      <Input
        v-model="form.pensionAmount"
        label="Důchod (Kč - před krácením)"
        type="number"
        placeholder="20000"
      />

      <Input
        v-model="form.monthsBefore"
        label="Počet měsíců předčasnosti"
        type="number"
        placeholder="36"
        :min="0"
        :max="1080"
      />

      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <p class="text-sm text-gray-600 dark:text-gray-300">Počet 90denních období</p>
          <p class="text-xl font-bold text-gray-800 dark:text-gray-100">{{ periods90Days }}</p>
        </div>
        <div class="bg-gray-50 dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
          <p class="text-sm text-gray-600 dark:text-gray-300">Celkové krácení</p>
          <p class="text-xl font-bold text-red-600 dark:text-red-400">{{ reductionPercent }}%</p>
        </div>
      </div>

      <Button
        variant="primary"
        :disabled="loading"
        @click="calculateEarlyRetirement"
      >
        {{ loading ? 'Načítání...' : 'Vypočítat krácení' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>

      <div v-if="result" class="mt-6 p-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded transition-colors duration-300">
        <h3 class="text-lg font-semibold text-green-700 mb-4">Výsledek předčasného důchodu</h3>
        <div class="space-y-2">
          <div class="flex justify-between py-2 border-b border-green-200">
            <span>Původní důchod:</span>
            <span class="font-medium">{{ Number(result.original_pension).toFixed(2) }} Kč</span>
          </div>
          <div class="flex justify-between py-2 border-b border-green-200">
            <span>Měsíce předčasnosti:</span>
            <span class="font-medium">{{ result.months_early }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-green-200">
            <span>Krácení celkem:</span>
            <span class="font-medium text-red-600">{{ Number(result.reduction_percent).toFixed(2) }}%</span>
          </div>
          <div class="flex justify-between py-2 font-bold text-green-700 text-lg">
            <span><strong>Předčasný důchod:</strong></span>
            <span><strong>{{ Number(result.reduced_pension).toFixed(2) }} Kč</strong></span>
          </div>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import type { EarlyRetirementResponse } from '@/types/pension';
import Card from '@/components/common/Card.vue';
import Input from '@/components/common/Input.vue';
import Button from '@/components/common/Button.vue';

const store = useCalculatorStore();
const loading = ref(false);
const result = ref<EarlyRetirementResponse | null>(null);

const form = ref({
  pensionAmount: 20000,
  monthsBefore: 36,
});

const periods90Days = computed(() => {
  return Math.floor(form.value.monthsBefore / 3);
});

const reductionPercent = computed(() => {
  return (periods90Days.value * 1.5).toFixed(2);
});

async function calculateEarlyRetirement() {
  loading.value = true;
  result.value = null;
  
  try {
    const { data } = await calculatorService.calculateEarlyRetirement({
      pension_amount: form.value.pensionAmount,
      months_before: form.value.monthsBefore,
    });
    result.value = data;
  } catch (err: any) {
    store.error = err.message || 'Chyba při výpočtu';
  } finally {
    loading.value = false;
  }
}
</script>
