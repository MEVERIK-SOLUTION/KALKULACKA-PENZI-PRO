import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { PensionRequest, PensionResponse } from '@/types/pension';
import { calculatorService } from '@/services/calculator';

export const useCalculatorStore = defineStore('calculator', () => {
  const lastResult = ref<PensionResponse | null>(null);
  const history = ref<any[]>([]);
  const loading = ref(false);
  const error = ref('');

  const hasResult = computed(() => lastResult.value !== null);

  async function calculatePension(payload: PensionRequest) {
    loading.value = true;
    error.value = '';
    
    try {
      const response = await calculatorService.calculatePension(payload);
      lastResult.value = response.data;
      history.value.push({
        timestamp: new Date(),
        type: 'pension',
        result: response.data,
      });
      return response.data;
    } catch (err: any) {
      error.value = err.message || 'Chyba při výpočtu';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function clearResult() {
    lastResult.value = null;
    error.value = '';
  }

  return {
    lastResult,
    history,
    loading,
    error,
    hasResult,
    calculatePension,
    clearResult,
  };
});