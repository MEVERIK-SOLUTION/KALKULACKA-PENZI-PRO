<template>
  <div class="bg-white dark:bg-[#16213e] rounded-lg p-6 shadow-md transition-colors duration-300">
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Vývoj důchodu v čase</h3>
    <div class="h-64">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

interface Props {
  ovz: number
  vz: number
  basePension: number
  percentRate: number
}

const props = defineProps<Props>()

const chartData = computed(() => ({
  labels: ['Základní výměra', 'Procentní výměra'],
  datasets: [{
    data: [props.basePension, props.vz * (props.percentRate / 100)],
    backgroundColor: [
      '#3B82F6', // blue
      '#10B981', // green
    ],
    borderColor: [
      '#2563EB',
      '#059669',
    ],
    borderWidth: 2,
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: 'rgb(156 163 175)', // gray-400
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const value = context.parsed
          return `${context.label}: ${value.toFixed(2)} Kč`
        }
      }
    }
  }
}
</script>