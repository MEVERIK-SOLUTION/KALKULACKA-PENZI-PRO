"""
Pension Calculator - Main calculation engine for old-age pension
"""

from typing import List, Dict, Optional
from ovz_calculator import calculate_ovz, load_config
from reduction_engine import calculate_vz


def calculate_pension(
    annual_incomes: List[float],
    coefficients: List[float],
    insurance_years: int,
    excluded_days: int = 0,
    config: Optional[Dict] = None,
) -> Dict:
    """Calculate old-age pension."""
    if config is None:
        config = load_config()

    total_days = insurance_years * 365
    ovz = calculate_ovz(annual_incomes, coefficients, total_days, excluded_days, config)
    vz = calculate_vz(ovz, config)

    base_pension = config.get("base_pension_amount", 4900)
    percent_rate = config.get("percent_rate_per_year", 1.495)
    pension = base_pension + (vz * percent_rate / 100 * insurance_years)

    return {
        "ovz": ovz,
        "vz": vz,
        "base_pension": base_pension,
        "percent_rate": percent_rate,
        "insurance_years": insurance_years,
        "pension_amount": round(pension, 2),
    }


def calculate_early_retirement(
    pension_amount: float,
    months_before: int,
    config: Optional[Dict] = None,
) -> Dict:
    """Calculate early retirement pension with reduction."""
    if config is None:
        config = load_config()

    reduction_per_90_days = config.get("early_retirement", {}).get(
        "reduction_per_90_days", 1.5
    )
    periods_90_days = months_before / 3
    reduction_percent = periods_90_days * reduction_per_90_days
    reduced_pension = pension_amount * (1 - reduction_percent / 100)

    return {
        "original_pension": pension_amount,
        "months_early": months_before,
        "reduction_percent": reduction_percent,
        "reduced_pension": round(reduced_pension, 2),
    }
