"""
Pension Calculator - Main calculation engine for old-age pension
"""


from ovz_calculator import calculate_ovz, load_config
from reduction_engine import calculate_vz


def calculate_pension(
    annual_incomes: list[float],
    coefficients: list[float],
    insurance_years: int,
    excluded_days: int = 0,
    config: dict | None = None,
) -> dict:
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
    config: dict | None = None,
) -> dict:
    """Calculate early retirement pension with progressive reduction.

    Uses multi-stage reduction per § 36 zákona 155/1995 Sb.:
      - Stage 1: first 360 days → reduction_per_90_days (e.g. 0.9%)
      - Stage 2: days 361–720 → reduction_per_90_days (e.g. 1.2%)
      - Stage 3: days 721+   → reduction_per_90_days (e.g. 1.5%)

    Falls back to flat rate if stages are not configured (legacy).
    """
    if config is None:
        config = load_config()

    early_cfg = config.get("early_retirement", {})
    stages = early_cfg.get("stages")

    total_days_early = months_before * 30  # approximate days

    if stages:
        # Progressive multi-stage reduction
        reduction_percent = 0.0
        remaining_days = total_days_early
        breakdown = []

        for stage in stages:
            if remaining_days <= 0:
                break

            days_limit = stage.get("days_up_to")
            rate = stage.get("reduction_per_90_days", 0.0)

            if days_limit is None:
                # Unlimited last stage
                periods = remaining_days / 90
                stage_reduction = periods * rate
                breakdown.append({
                    "days": remaining_days,
                    "rate_per_90_days": rate,
                    "reduction_pct": round(stage_reduction, 4),
                })
                reduction_percent += stage_reduction
                remaining_days = 0
            else:
                # Find the bracket size for this stage
                prev_limit = 0
                stage_idx = stages.index(stage)
                if stage_idx > 0:
                    prev_limit = stages[stage_idx - 1].get("days_up_to") or 0
                bracket = days_limit - prev_limit

                applicable_days = min(remaining_days, bracket)
                periods = applicable_days / 90
                stage_reduction = periods * rate
                breakdown.append({
                    "days": applicable_days,
                    "rate_per_90_days": rate,
                    "reduction_pct": round(stage_reduction, 4),
                })
                reduction_percent += stage_reduction
                remaining_days -= applicable_days
    else:
        # Legacy flat rate
        reduction_per_90_days = early_cfg.get("reduction_per_90_days", 1.5)
        periods_90_days = months_before / 3
        reduction_percent = periods_90_days * reduction_per_90_days
        breakdown = [{
            "days": total_days_early,
            "rate_per_90_days": reduction_per_90_days,
            "reduction_pct": round(reduction_percent, 4),
        }]

    reduced_pension = pension_amount * (1 - reduction_percent / 100)

    return {
        "original_pension": pension_amount,
        "months_early": months_before,
        "days_early": total_days_early,
        "reduction_percent": round(reduction_percent, 4),
        "reduction_breakdown": breakdown,
        "reduced_pension": round(reduced_pension, 2),
    }
