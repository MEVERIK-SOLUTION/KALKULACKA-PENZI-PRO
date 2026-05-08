"""
Paradox Resolver - Resolves the "decision paradox" of substitute periods
"""


from ovz_calculator import calculate_ovz


def calculate_with_exclusion(
    annual_incomes: list[float],
    coefficients: list[float],
    total_days: int,
    excluded_days: int,
    config: dict | None = None,
) -> tuple[float, float]:
    """Calculate OVZ with and without excluded days."""
    ovz_with = calculate_ovz(
        annual_incomes, coefficients, total_days, excluded_days=0, config=config
    )
    ovz_without = calculate_ovz(
        annual_incomes,
        coefficients,
        total_days,
        excluded_days=excluded_days,
        config=config,
    )
    return ovz_with, ovz_without


def resolve_paradox(
    annual_incomes: list[float],
    coefficients: list[float],
    total_days: int,
    substitute_days: int,
    config: dict | None = None,
) -> dict:
    """
    Resolve whether to include or exclude substitute periods.
    Returns recommendation with both OVZ values.
    """
    ovz_with, ovz_without = calculate_with_exclusion(
        annual_incomes, coefficients, total_days, substitute_days, config
    )

    include = ovz_with >= ovz_without

    return {
        "include_substitute_period": include,
        "ovz_with_inclusion": ovz_with,
        "ovz_with_exclusion": ovz_without,
        "difference": abs(ovz_with - ovz_without),
        "recommendation": "Zahrnout náhradní dobu"
        if include
        else "Vyloučit náhradní dobu",
    }
