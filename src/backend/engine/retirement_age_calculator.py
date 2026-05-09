"""Modul pro výpočet důchodového věku dle zákona 155/1995 Sb.

Podporuje:
- Muže (dle ročníku narození)
- Ženy (dle ročníku narození + počtu vychovaných dětí)
- Výpočet v měsících i přepočet na roky + měsíce

Zdroj: config/legislative_2026.yaml → retirement_age
"""
from __future__ import annotations
from typing import NamedTuple

import yaml
import os


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "legislative_2026.yaml")


class RetirementAge(NamedTuple):
    """Výsledek výpočtu důchodového věku."""
    months: int        # celkový věk v měsících
    years: int         # celé roky
    remaining: int     # zbylé měsíce
    description: str   # popis pravidla


def load_config(path: str | None = None) -> dict:
    config_path = path or CONFIG_PATH
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _get_male_retirement_months(birth_year: int, config: dict) -> int:
    """Vrátí důchodový věk muže v měsících dle ročníku narození."""
    male_cfg = config.get("retirement_age", {}).get("male", {})

    if birth_year < 1960:
        return male_cfg.get("born_before_1960", 720)
    elif birth_year >= 1966:
        return male_cfg.get("born_1966_and_later", 780)
    else:
        key = f"born_{birth_year}"
        return male_cfg.get(key, 780)  # fallback na 65 let


def _get_female_retirement_months(birth_year: int, children: int, config: dict) -> int:
    """Vrátí důchodový věk ženy v měsících dle ročníku narození a počtu dětí.

    Pro ženy se použije mužský základ a odečte se redukce za děti.
    """
    female_cfg = config.get("retirement_age", {}).get("female", {})
    max_children = female_cfg.get("max_children_for_reduction", 5)

    # Základ = mužský věk
    base_months = _get_male_retirement_months(birth_year, config)

    # Redukce za děti
    child_reduction = female_cfg.get("child_reduction_months", {})
    effective_children = min(children, max_children)
    reduction = child_reduction.get(effective_children, 0)

    return max(base_months - reduction, 0)


def calculate_retirement_age(
    birth_year: int,
    gender: str = "male",
    children: int = 0,
    config: dict | None = None,
) -> RetirementAge:
    """Spočítá důchodový věk na základě ročníku narození, pohlaví a počtu dětí.

    Args:
        birth_year: Rok narození (např. 1965)
        gender: "male" nebo "female"
        children: Počet vychovaných dětí (relevantní pro ženy)
        config: Legislativní konfigurace. Načte se automaticky pokud není zadána.

    Returns:
        RetirementAge s věkem v měsících, letech a zbytkovými měsíci.
    """
    if config is None:
        config = load_config()

    if gender == "female":
        total_months = _get_female_retirement_months(birth_year, children, config)
        desc = f"Žena, nar. {birth_year}, {children} dětí"
    else:
        total_months = _get_male_retirement_months(birth_year, config)
        desc = f"Muž, nar. {birth_year}"

    years = total_months // 12
    remaining = total_months % 12

    return RetirementAge(
        months=total_months,
        years=years,
        remaining=remaining,
        description=f"{desc} → {years} let {remaining} měs.",
    )


def calculate_months_until_retirement(
    birth_year: int,
    birth_month: int,
    current_year: int,
    current_month: int,
    gender: str = "male",
    children: int = 0,
    config: dict | None = None,
) -> dict:
    """Spočítá kolik měsíců zbývá do důchodu.

    Returns:
        dict s retirement_age, retirement_date, months_remaining
    """
    if config is None:
        config = load_config()

    ra = calculate_retirement_age(birth_year, gender, children, config)

    # Datum dosažení důchodového věku
    retirement_month_abs = (birth_year * 12 + birth_month - 1) + ra.months
    ret_year = retirement_month_abs // 12
    ret_month = retirement_month_abs % 12 + 1

    # Kolik zbývá
    current_abs = current_year * 12 + current_month
    retirement_abs = ret_year * 12 + ret_month
    months_remaining = retirement_abs - current_abs

    return {
        "retirement_age": {
            "months": ra.months,
            "years": ra.years,
            "remaining_months": ra.remaining,
            "description": ra.description,
        },
        "retirement_date": {
            "year": ret_year,
            "month": ret_month,
        },
        "months_remaining": months_remaining,
        "already_retired": months_remaining <= 0,
    }


if __name__ == "__main__":
    # Quick test
    tests = [
        ("Muž 1955", 1955, "male", 0),
        ("Muž 1965", 1965, "male", 0),
        ("Muž 1970", 1970, "male", 0),
        ("Žena 1965, 0 dětí", 1965, "female", 0),
        ("Žena 1965, 2 děti", 1965, "female", 2),
        ("Žena 1965, 5 dětí", 1965, "female", 5),
    ]

    for label, by, g, c in tests:
        ra = calculate_retirement_age(by, g, c)
        print(f"{label}: {ra.description}")
