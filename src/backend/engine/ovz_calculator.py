"""
OVZ Calculator - Osobní vyměřovací základ (§ 15 ZDP)
"""

from pathlib import Path

import yaml


def load_config(year: int = 2026) -> dict:
    """Load legislative config for given year."""
    current_file = Path(__file__)

    # Build search directories - go up to find project root
    search_dirs = [
        Path.cwd() / "config",  # CWD/config/
        current_file.parent / "config",  # engine/config/
        current_file.parent.parent / "config",  # backend/config/
        current_file.parent.parent.parent / "config",  # src/config/
        current_file.parent.parent.parent.parent / "config",  # project/config/
        current_file.parent.parent.parent.parent.parent / "config",  # if nested deeper
    ]

    possible_names = [
        f"legislative_{year}.yaml",
        f"legislative_config_{year}.yaml",
    ]

    for directory in search_dirs:
        for name in possible_names:
            config_path = directory / name
            if config_path.exists():
                with open(config_path, encoding="utf-8") as f:
                    return yaml.safe_load(f)

    raise FileNotFoundError(
        f"Config for year {year} not found. Searched in: {[str(d) for d in search_dirs]}"
    )


def calculate_ovz(
    annual_incomes: list[float],
    coefficients: list[float],
    total_days: int,
    excluded_days: int = 0,
    config: dict | None = None,
) -> float:
    """Calculate Osobní vyměřovací základ (OVZ)."""
    if config is None:
        config = load_config()

    if len(annual_incomes) != len(coefficients):
        raise ValueError("annual_incomes and coefficients must have same length")

    sum_weighted = sum(inc * coef for inc, coef in zip(annual_incomes, coefficients, strict=True))

    denominator_days = total_days - excluded_days
    if denominator_days <= 0:
        raise ValueError("Denominator must be positive")

    ovz = (sum_weighted / denominator_days) * 30.4167
    return round(ovz, 2)


def calculate_ovz_from_annual(
    annual_income: float, coefficient: float, years: int, excluded_days: int = 0
) -> float:
    """Simplified OVZ calculation for single annual income."""
    total_days = 365 * years
    return calculate_ovz(
        annual_incomes=[annual_income],
        coefficients=[coefficient],
        total_days=total_days,
        excluded_days=excluded_days,
    )


def calculate_reduced_base(ovz: float, config: dict | None = None) -> float:
    """Apply reduction limits to OVZ (§ 15 ZDP)."""
    if config is None:
        config = load_config()

    reduction_limits = config.get("reduction_limits", [])
    reduction_limits = sorted(
        reduction_limits, key=lambda x: x.get("threshold") or float("inf")
    )

    vz = 0.0
    remaining_ovz = ovz

    for i, limit in enumerate(reduction_limits):
        threshold = limit.get("threshold")
        rate = limit.get("rate", 0.0)

        if threshold is None:
            break

        if i == 0:
            if remaining_ovz <= threshold:
                vz += remaining_ovz * rate
                remaining_ovz = 0
                break
            vz += threshold * rate
            remaining_ovz -= threshold
        else:
            prev_threshold = reduction_limits[i - 1].get("threshold") or 0
            bracket = threshold - prev_threshold
            if remaining_ovz <= bracket:
                vz += remaining_ovz * rate
                remaining_ovz = 0
                break
            vz += bracket * rate
            remaining_ovz -= bracket

    return round(vz, 2)


if __name__ == "__main__":
    test_ovz = calculate_ovz_from_annual(
        annual_income=38000 * 12, coefficient=1.0581, years=45, excluded_days=0
    )
    print(f"OVZ: {test_ovz:,.2f} Kč")

    test_vz = calculate_reduced_base(test_ovz)
    print(f"Výpočtový základ (after reduction): {test_vz:,.2f} Kč")
