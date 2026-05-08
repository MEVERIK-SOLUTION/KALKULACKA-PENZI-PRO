<template>
  <div class="bg-white dark:bg-[#16213e] rounded-lg shadow-md transition-colors duration-300">
    <div class="p-6">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Historie výpočtů</h3>
        <div class="flex gap-2">
          <button
            @click="exportCSV"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            :disabled="loading"
          >
            Export CSV
          </button>
          <button
            @click="exportPDF"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            :disabled="loading"
          >
            Export PDF
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="mb-4 flex gap-4">
        <select
          v-model="filterType"
          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          @change="loadHistory"
        >
          <option value="">Všechny typy</option>
          <option value="pension">Důchod</option>
          <option value="ovz">OVZ</option>
          <option value="early-retirement">Předčasný</option>
          <option value="paradox">Paradox</option>
        </select>
      </div>

      <!-- History Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th class="px-6 py-3">ID</th>
              <th class="px-6 py-3">Typ</th>
              <th class="px-6 py-3">OVZ</th>
              <th class="px-6 py-3">VZ</th>
              <th class="px-6 py-3">Důchod</th>
              <th class="px-6 py-3">Roky</th>
              <th class="px-6 py-3">Vytvořeno</th>
              <th class="px-6 py-3">Akce</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="record in history"
              :key="record.id"
              class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ record.id }}</td>
              <td class="px-6 py-4">{{ getTypeLabel(record.calc_type) }}</td>
              <td class="px-6 py-4">{{ record.ovz ? record.ovz.toFixed(2) : '-' }}</td>
              <td class="px-6 py-4">{{ record.vz ? record.vz.toFixed(2) : '-' }}</td>
              <td class="px-6 py-4">{{ record.pension_amount ? record.pension_amount.toFixed(2) : '-' }}</td>
              <td class="px-6 py-4">{{ record.insurance_years || '-' }}</td>
              <td class="px-6 py-4">{{ formatDate(record.created_at) }}</td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <button
                    @click="viewDetails(record)"
                    class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                    title="Zobrazit detaily"
                  >
                    👁️
                  </button>
                  <button
                    @click="deleteRecord(record.id)"
                    class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                    title="Smazat"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <button
          @click="loadMore"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          :disabled="loading"
        >
          Načíst více
        </button>
        <span class="text-sm text-gray-600 dark:text-gray-400">
          Zobrazeno {{ history.length }} záznamů
        </span>
      </div>

      <!-- Details Modal -->
      <div
        v-if="selectedRecord"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click="selectedRecord = null"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4 max-h-96 overflow-y-auto"
          @click.stop
        >
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-semibold">Detaily výpočtu #{{ selectedRecord.id }}</h4>
            <button @click="selectedRecord = null" class="text-gray-500 hover:text-gray-700">✕</button>
          </div>

          <div class="space-y-4">
            <div><strong>Typ:</strong> {{ getTypeLabel(selectedRecord.calc_type) }}</div>
            <div><strong>Vytvořeno:</strong> {{ formatDate(selectedRecord.created_at) }}</div>
            <div><strong>OVZ:</strong> {{ selectedRecord.ovz ? selectedRecord.ovz.toFixed(2) : 'N/A' }}</div>
            <div><strong>VZ:</strong> {{ selectedRecord.vz ? selectedRecord.vz.toFixed(2) : 'N/A' }}</div>
            <div><strong>Důchod:</strong> {{ selectedRecord.pension_amount ? selectedRecord.pension_amount.toFixed(2) : 'N/A' }}</div>
            <div><strong>Roky pojištění:</strong> {{ selectedRecord.insurance_years || 'N/A' }}</div>

            <div>
              <strong>Vstupní data:</strong>
              <pre class="bg-gray-100 dark:bg-gray-700 p-2 rounded mt-1 text-xs overflow-x-auto">{{ JSON.stringify(selectedRecord.input_data, null, 2) }}</pre>
            </div>

            <div>
              <strong>Výsledek:</strong>
              <pre class="bg-gray-100 dark:bg-gray-700 p-2 rounded mt-1 text-xs overflow-x-auto">{{ JSON.stringify(selectedRecord.result, null, 2) }}</pre>
            </div>

            <div v-if="selectedRecord.note">
              <strong>Poznámka:</strong> {{ selectedRecord.note }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface HistoryRecord {
  id: number
  calc_type: string
  input_data: any
  result: any
  ovz: number | null
  vz: number | null
  pension_amount: number | null
  insurance_years: number | null
  created_at: string
  client_ip: string | null
  note: string | null
}

const history = ref<HistoryRecord[]>([])
const loading = ref(false)
const filterType = ref('')
const selectedRecord = ref<HistoryRecord | null>(null)
const offset = ref(0)
const limit = ref(20)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'dev-key-123',
  },
})

const loadHistory = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filterType.value) params.append('calc_type', filterType.value)
    params.append('limit', limit.value.toString())
    params.append('offset', offset.value.toString())

    const response = await api.get<HistoryRecord[]>(`/history/?${params}`)
    if (offset.value === 0) {
      history.value = response.data
    } else {
      history.value = [...history.value, ...response.data]
    }
  } catch (error) {
    console.error('Error loading history:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  offset.value += limit.value
  loadHistory()
}

const deleteRecord = async (id: number) => {
  if (!confirm('Opravdu chcete smazat tento záznam?')) return

  try {
    await api.delete(`/history/${id}`)
    history.value = history.value.filter(r => r.id !== id)
  } catch (error) {
    console.error('Error deleting record:', error)
  }
}

const exportCSV = async () => {
  try {
    const params = filterType.value ? `?calc_type=${filterType.value}` : ''
    const response = await api.get(`/history/export/csv${params}`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'historie_vypoctu.csv')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error exporting CSV:', error)
  }
}

const exportPDF = async () => {
  try {
    const params = filterType.value ? `?calc_type=${filterType.value}` : ''
    const response = await api.get(`/history/export/pdf${params}`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'historie_vypoctu.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error exporting PDF:', error)
  }
}

const viewDetails = (record: HistoryRecord) => {
  selectedRecord.value = record
}

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'pension': 'Důchod',
    'ovz': 'OVZ',
    'early-retirement': 'Předčasný',
    'paradox': 'Paradox'
  }
  return labels[type] || type
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('cs-CZ')
}

onMounted(() => {
  loadHistory()
})
</script>