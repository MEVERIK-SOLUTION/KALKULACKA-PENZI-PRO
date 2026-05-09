import axios from 'axios';
import type { 
  PensionRequest, PensionResponse,
  OVZRequest, OVZResponse,
  ParadoxRequest, ParadoxResponse,
  EarlyRetirementRequest, EarlyRetirementResponse 
} from '@/types/pension';

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

export const calculatorService = {
  calculatePension(payload: PensionRequest) {
    return api.post<PensionResponse>('/calculate-pension', payload);
  },

  calculateOVZ(payload: OVZRequest) {
    return api.post<OVZResponse>('/calculate-ovz', payload);
  },

  resolveParadox(payload: ParadoxRequest) {
    return api.post<ParadoxResponse>('/resolve-paradox', payload);
  },

  calculateEarlyRetirement(payload: EarlyRetirementRequest) {
    return api.post<EarlyRetirementResponse>('/calculate-early-retirement', payload);
  },
};