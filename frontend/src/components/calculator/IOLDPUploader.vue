<template>
  <Card title="IOLDP Nahrání - ePortál ČSSZ">
    <div class="space-y-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded border border-blue-200 dark:border-blue-800 transition-colors duration-300">
        <h4 class="font-medium text-blue-800 dark:text-blue-300 mb-2">Jak na to?</h4>
        <ol class="text-sm text-blue-700 dark:text-blue-400 list-decimal pl-4 space-y-1">
          <li>Stáhněte svůj IOLDP z <a href="https://eportal.cssz.cz" target="_blank" class="underline text-blue-600 dark:text-blue-400">ePortálu ČSSZ</a></li>
          <li>Formát: XML (strukturovaná data) nebo PDF (skenovaný dokument)</li>
          <li>Klikněte na "Vybrat soubor" a nahrajte IOLDP</li>
          <li>Systém automaticky extrahuje: příjmy, koeficienty, dobu pojištění</li>
        </ol>
      </div>

      <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded p-6 text-center transition-colors duration-300">
        <input
          type="file"
          id="iol-dp-file"
          accept=".xml,.pdf"
          class="hidden"
          @change="handleFileUpload"
        />
        <label
          for="iol-dp-file"
          class="cursor-pointer text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
        >
          <div class="space-y-2">
            <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4.97 4.97 0 0 1 1.9-1.44 4.97 4.97 0 0 1 1.9 1.44m6 2 1.01-5.8m-5.8 5.8h-.2c-.98 0-1.97-.24-2.87-.75L3 19.78V22h2.4l-.7-3.6c-1.45.55-2.93.87-4.45.87-.36-.33-.7-.7-1.04-1.1l-3.6.7H2v-2.4l3.6-.7c.15-1.52.47-3 .87-4.45l-.7-3.6a7.029 7.029 0 0 1-.75-2.87V5.2H.5C.24 5.2 0 4.96 0 4.7V3.5c0-.98.37-1.91 1-1.1l3.6.7c.52-.93 1.17-1.8 1.9-2.6L5.5.5h2.4l.7 3.6c1.45-.55 2.93-.87 4.45-.87.36.33.7.7 1.04 1.1l3.6-.7H14v2.4l-3.6.7c-.15 1.52-.47 3-.87 4.45l.7 3.6c.33.36.7.7 1.1 1.04l3.6-.7v2.4h-2.4l-.7 3.6z"/>
            </svg>
            <span class="block text-sm font-medium">Klikněte pro výběr souboru</span>
            <span class="text-xs text-gray-500 dark:text-gray-400">Podporované formáty: XML, PDF</span>
          </div>
        </label>
      </div>

      <div v-if="uploadedFileName" class="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded flex items-center justify-between transition-colors duration-300">
        <div class="flex items-center space-x-2">
          <svg class="h-5 w-5 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/>
          </svg>
          <span class="text-sm font-medium text-green-800 dark:text-green-300">{{ uploadedFileName }}</span>
        </div>
        <button
          @click="clearFile"
          class="text-green-700 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <Button
        variant="primary"
        :disabled="!uploadedFileName || loading"
        @click="parseFile"
      >
        {{ loading ? 'Analyzuji...' : 'Analyzovat IOLDP' }}
      </Button>

      <div v-if="store.error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded transition-colors duration-300">
        {{ store.error }}
      </div>

      <div v-if="parsedData" class="mt-6 space-y-6 fade-in">
        <div class="p-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg transition-colors duration-300">
          <h3 class="text-lg font-semibold text-green-700 dark:text-green-400 mb-4">Rozpoznání data</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div class="bg-white dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
              <p class="text-sm text-gray-600 dark:text-gray-400">Jméno</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ parsedData.fullName }}</p>
            </div>
            <div class="bg-white dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
              <p class="text-sm text-gray-600 dark:text-gray-400">Datum narození</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ parsedData.birthDate }}</p>
            </div>
            <div class="bg-white dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
              <p class="text-sm text-gray-600 dark:text-gray-400">Doba pojištění</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ parsedData.insuranceYears }} let</p>
            </div>
            <div class="bg-white dark:bg-[#16213e] p-3 rounded border border-gray-200 dark:border-[#2d3748] transition-colors duration-300">
              <p class="text-sm text-gray-600 dark:text-gray-400">Vyloučené dny</p>
              <p class="font-medium text-gray-900 dark:text-gray-100">{{ parsedData.excludedDays }} dní</p>
            </div>
          </div>

          <div v-if="parsedData.annualIncomes.length > 0">
            <h4 class="font-medium mb-3 text-gray-800 dark:text-gray-200">Roční příjmy ({{ parsedData.annualIncomes.length }} let)</h4>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="bg-gray-100 dark:bg-[#1a1a2e]">
                    <th class="text-left p-2 text-gray-700 dark:text-gray-300">Rok</th>
                    <th class="text-right p-2 text-gray-700 dark:text-gray-300">Příjem</th>
                    <th class="text-right p-2 text-gray-700 dark:text-gray-300">Koeficient</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(item, idx) in parsedData.annualIncomes"
                    :key="idx"
                    class="border-t border-gray-200 dark:border-[#2d3748]"
                  >
                    <td class="p-2 text-gray-800 dark:text-gray-200">{{ item.year }}</td>
                    <td class="text-right p-2 text-gray-800 dark:text-gray-200">{{ Number(item.income).toLocaleString('cs-CZ') }} Kč</td>
                    <td class="text-right p-2 text-gray-800 dark:text-gray-200">{{ item.coefficient }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <Button
          variant="primary"
          @click="applyToCalculator"
        >
          Použít data v kalkulačce
        </Button>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useCalculatorStore } from '@/stores/calculator';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import { parseIOLDPXML, parseIOLDPPDF, mapToCalculatorInput } from '@/services/iolDPParser';
import type { IOLDPData } from '@/services/iolDPParser';

const store = useCalculatorStore();
const loading = ref(false);
const uploadedFileName = ref('');
const parsedData = ref<IOLDPData | null>(null);
const fileContent = ref('');

function handleFileUpload(event: Event) {
  const fileInput = event.target as HTMLInputElement;
  const file = fileInput.files?.[0];
  if (!file) return;

  uploadedFileName.value = file.name;
  const reader = new FileReader();
  
  reader.onload = (e) => {
    const text = e.target?.result as string;
    fileContent.value = text;
  };
  
  if (file.name.endsWith('.xml')) {
    reader.readAsText(file);
  } else if (file.name.endsWith('.pdf')) {
    // Note: Real PDF parsing requires server-side or PDF.js library
    reader.readAsText(file); // Simplified - would need PDF.js for production
  }
}

async function parseFile() {
  if (!fileContent.value) return;
  
  loading.value = true;
  parsedData.value = null;
  
  try {
    let result;
    if (uploadedFileName.value.endsWith('.xml')) {
      result = parseIOLDPXML(fileContent.value);
    } else if (uploadedFileName.value.endsWith('.pdf')) {
      result = parseIOLDPPDF(fileContent.value);
    }
    
    if (result && result.success && result.data) {
      parsedData.value = result.data;
    } else {
      store.error = result?.error || 'Neznámá chyba při parsování';
    }
  } catch (err: any) {
    store.error = err.message || 'Chyba při analýze souboru';
  } finally {
    loading.value = false;
  }
}

function useDataForCalculation() {
  if (!parsedData.value) return;
  
  const input = mapToCalculatorInput(parsedData.value);
  
  // Here you would update the calculator forms
  // For now, just show success message
  alert(`Data připravena pro výpočet:\n${JSON.stringify(input, null, 2)}`);
}

function clearFile() {
  uploadedFileName.value = '';
  parsedData.value = null;
  fileContent.value = '';
}
</script>
