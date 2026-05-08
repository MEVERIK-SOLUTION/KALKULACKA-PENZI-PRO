export interface PensionRequest {
  annual_incomes: number[];
  coefficients: number[];
  insurance_years: number;
  excluded_days?: number;
}

export interface OVZRequest {
  annual_incomes: number[];
  coefficients: number[];
  total_days: number;
  excluded_days?: number;
}

export interface ParadoxRequest {
  annual_incomes: number[];
  coefficients: number[];
  total_days: number;
  substitute_days: number;
}

export interface EarlyRetirementRequest {
  pension_amount: number;
  months_before: number;
}

export interface EarlyRetirementResponse {
  original_pension: number;
  months_early: number;
  reduction_percent: number;
  reduced_pension: number;
}

export interface PensionResponse {
  ovz: number;
  vz: number;
  base_pension: number;
  percent_rate: number;
  insurance_years: number;
  pension_amount: number;
}

export interface OVZResponse {
  ovz: number;
}

export interface ParadoxResponse {
  recommendation: string;
  ovz_with_inclusion: number;
  ovz_with_exclusion: number;
  difference: number;
}

import { z } from 'zod';

export const pensionFormSchema = z.object({
  monthlyIncome: z.coerce.number()
    .min(1000, 'Příjem musí být alespoň 1 000 Kč')
    .max(500000, 'Příjem nesmí překročit 500 000 Kč'),
  insuranceYears: z.coerce.number()
    .min(1, 'Pojištění musí být alespoň 1 rok')
    .max(50, 'Pojištění nesmí překročit 50 let'),
  excludedDays: z.coerce.number()
    .min(0, 'Vyloučené dny nesmí být záporné')
    .max(365 * 50, 'Vyloučené dny nesmí překročit celkovou dobu pojištění')
    .optional(),
});

export type PensionFormData = z.infer<typeof pensionFormSchema>;