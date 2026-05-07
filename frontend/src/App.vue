<template>
  <div class="min-h-screen bg-gray-100 py-8">
    <div class="container mx-auto px-4 max-w-4xl">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Penzijní Kalkulátor 2026</h1>
      <p class="text-gray-600 mb-8">Výpočet starobního důchodu podle zákona 155/1995 Sb.</p>

      <div class="bg-white rounded-lg shadow-md">
        <div class="flex border-b-2 border-gray-100">
          <div
            v-for="tab in tabs"
            :key="tab.id"
            class="px-6 py-3 cursor-pointer border-b-2 transition-colors"
            :class="[
              activeTab === tab.id
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            ]"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </div>
        </div>

        <div class="p-6">
          <div v-if="activeTab === 'pension'" class="space-y-4">
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
          </div>

          <div v-if="activeTab === 'ovz'" class="space-y-4">
            <Input
              v-model="ovzForm.annualIncome"
              label="Roční příjem (Kč)"
              type="number"
              placeholder="456000"
            />
            <Input
              v-model="ovzForm.coefficient"
              label="Koeficient (2026: 1.0581)"
              type="number"
              placeholder="1.0581"
              step="0.0001"
            />
            <Input
              v-model="ovzForm.totalDays"
              label="Celkem dní"
              type="number"
              placeholder="16425"
              :min="0"
            />
            <Button variant="primary" @click="calculateOVZ">
              Vypočítat OVZ
            </Button>
          </div>

          <div v-if="activeTab === 'paradox'" class="space-y-4">
            <Input
              v-model="paradoxForm.annualIncome"
              label="Roční příjem (Kč)"
              type="number"
              placeholder="456000"
            />
            <Input
              v-model="paradoxForm.coefficient"
              label="Koeficient"
              type="number"
              placeholder="1.0581"
              step="0.0001"
            />
            <Input
              v-model="paradoxForm.totalDays"
              label="Celkem dní"
              type="number"
              placeholder="16425"
              :min="0"
            />
            <Input
              v-model="paradoxForm.substituteDays"
              label="Náhradní doby (dny)"
              type="number"
              placeholder="365"
              :min="0"
            />
            <Button variant="primary" @click="resolveParadox">
              Vyřešit paradox
            </Button>
          </div>

          <div v-if="error" class="mt-4 p-4 bg-red-50 text-red-600 rounded">
            {{ error }}
          </div>

          <div v-if="store.hasResult" class="mt-6 p-6 bg-green-50 rounded">
            <h3 class="text-lg font-semibold text-green-700 mb-4">Výsledek výpočtu</h3>
            <div class="space-y-2">
              <div class="flex justify-between py-2 border-b border-green-200">
                <span>OVZ:</span>
                <span class="font-medium">{{ Number(store.lastResult?.ovz).toFixed(2) }} Kč</span>
              </div>
              <div class="flex justify-between py-2 border-b border-green-200">
                <span>Výpočtový základ:</span>
                <span class="font-medium">{{ Number(store.lastResult?.vz).toFixed(2) }} Kč</span>
              </div>
              <div class="flex justify-between py-2 border-b border-green-200">
                <span>Základní výměra:</span>
                <span class="font-medium">{{ store.lastResult?.base_pension }} Kč</span>
              </div>
              <div class="flex justify-between py-2 border-b border-green-200">
                <span>Procentní sazba:</span>
                <span class="font-medium">{{ store.lastResult?.percent_rate }}%</span>
              </div>
              <div class="flex justify-between py-2 border-b border-green-200">
                <span>Pojištění (roky):</span>
                <span class="font-medium">{{ store.lastResult?.insurance_years }}</span>
              </div>
              <div class="flex justify-between py-2 font-bold text-green-700 text-lg">
                <span>Celkový důchod:</span>
                <span>{{ Number(store.lastResult?.pension_amount).toFixed(2) }} Kč</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import Button from '@/components/common/Button.vue';
import Input from '@/components/common/Input.vue';

const store = useCalculatorStore();
const loading = ref(false);
const error = ref('');

const activeTab = ref('pension');

const tabs = [
  { id: 'pension', label: 'Důchod' },
  { id: 'ovz', label: 'OVZ' },
  { id: 'paradox', label: 'Paradox' },
];

const pensionForm = ref({
  monthlyIncome: 38000,
  insuranceYears: 45,
  excludedDays: 0,
});

const ovzForm = ref({
  annualIncome: 456000,
  coefficient: 1.0581,
  totalDays: 16425,
  excludedDays: 0,
});

const paradoxForm = ref({
  annualIncome: 456000,
  coefficient: 1.0581,
  totalDays: 16425,
  substituteDays: 365,
});

async function calculatePension() {
  loading.value = true;
  error.value = '';
  
  try {
    await store.calculatePension({
      annual_incomes: [pensionForm.value.monthlyIncome * 12],
      coefficients: [1.0581],
      insurance_years: pensionForm.value.insuranceYears,
      excluded_days: pensionForm.value.excludedDays,
    });
  } catch (err: any) {
    error.value = err.message || 'Chyba při výpočtu';
  } finally {
    loading.value = false;
  }
}

async function calculateOVZ() {
  error.value = '';
  try {
    const { data } = await calculatorService.calculateOVZ({
      annual_incomes: [ovzForm.value.annualIncome],
      coefficients: [ovzForm.value.coefficient],
      total_days: ovzForm.value.totalDays,
      excluded_days: ovzForm.value.excludedDays,
    });
    error.value = `OVZ: ${Number(data.ovz).toFixed(2)} Kč`;
  } catch (err: any) {
    error.value = err.message || 'Chyba při výpočtu OVZ';
  }
}

async function resolveParadox() {
  error.value = '';
  try {
    const { data } = await calculatorService.resolveParadox({
      annual_incomes: [paradoxForm.value.annualIncome],
      coefficients: [paradoxForm.value.coefficient],
      total_days: paradoxForm.value.totalDays,
      substitute_days: paradoxForm.value.substituteDays,
    });
    error.value = `Doporučení: ${data.recommendation}`;
  } catch (err: any) {
    error.value = err.message || 'Chyba při řešení paradoxu';
  }
}
</script>