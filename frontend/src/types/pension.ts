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

export interface EarlyRetirementResponse {
  original_pension: number;
  months_early: number;
  reduction_percent: number;
  reduced_pension: number;
}