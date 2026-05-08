import axios from 'axios';
import type { 
  PensionRequest, PensionResponse,
  OVZRequest, OVZResponse,
  ParadoxRequest, ParadoxResponse,
  EarlyRetirementRequest, EarlyRetirementResponse 
} from '@/types/pension';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'dev-key-123', // Development API key
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