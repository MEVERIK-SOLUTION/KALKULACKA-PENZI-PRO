import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';
const API_KEY = import.meta.env.VITE_API_KEY || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
  },
});

export interface HistoryEntry {
  calc_type: string;
  input_data: Record<string, any>;
  result: Record<string, any>;
  ovz?: number;
  vz?: number;
  pension_amount?: number;
  insurance_years?: number;
  note?: string;
}

export interface HistoryRecord extends HistoryEntry {
  id: number;
  created_at: string;
  client_ip: string | null;
}

export const historyService = {
  /** Save a calculation result to server history */
  save(entry: HistoryEntry) {
    return api.post<HistoryRecord>('/history/', entry);
  },

  /** List history records with optional filter */
  list(params?: { calc_type?: string; limit?: number; offset?: number }) {
    const search = new URLSearchParams();
    if (params?.calc_type) search.append('calc_type', params.calc_type);
    if (params?.limit) search.append('limit', params.limit.toString());
    if (params?.offset) search.append('offset', params.offset.toString());
    return api.get<HistoryRecord[]>(`/history/?${search}`);
  },

  /** Get a single history record */
  get(id: number) {
    return api.get<HistoryRecord>(`/history/${id}`);
  },

  /** Update a history record */
  update(id: number, entry: HistoryEntry) {
    return api.put<HistoryRecord>(`/history/${id}`, entry);
  },

  /** Delete a history record */
  delete(id: number) {
    return api.delete(`/history/${id}`);
  },

  /** Export history as CSV (returns blob) */
  exportCSV(calcType?: string) {
    const params = calcType ? `?calc_type=${calcType}` : '';
    return api.get(`/history/export/csv${params}`, { responseType: 'blob' });
  },

  /** Export history as PDF (returns blob) */
  exportPDF(calcType?: string) {
    const params = calcType ? `?calc_type=${calcType}` : '';
    return api.get(`/history/export/pdf${params}`, { responseType: 'blob' });
  },
};
