"""
Data service – propojuje ČSÚ DataStat API s penzijním kalkulátorem.
Poskytuje reálná data pro valorizaci, redukční hranice a projekce.
"""

import sys
from pathlib import Path

import pandas as pd

# Přidání cz_pension_api do cesty
CZ_PENSION_API = Path(__file__).resolve().parent.parent.parent.parent.parent / "Vývoj a rešerše s OpenCode" / "cz_pension_api"
if CZ_PENSION_API.exists():
    sys.path.insert(0, str(CZ_PENSION_API))

from cz_pension_api import DataStatClient  # noqa: E402


class PensionDataService:
    """Service layer for fetching real pension-related data from ČSÚ."""

    def __init__(self, use_cache: bool = True):
        self._client = DataStatClient(use_cache=use_cache)

    def get_latest_inflation_yoy(self) -> float | None:
        """Get latest year-over-year inflation rate."""
        df = self._client.get_inflation_monthly()
        df_yr = df[df["Ukazatel"] == "Stejné období předchozího roku = 100"]
        if df_yr.empty:
            return None
        latest = float(df_yr["Hodnota"].iloc[-1])
        return latest - 100  # převod na procenta

    def get_latest_avg_wage(self) -> float | None:
        """Get latest average gross monthly wage."""
        df = self._client.get_wages_quarterly()
        df_mzda = df[df["Ukazatel"] == "Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč)"]
        if df_mzda.empty:
            return None
        return float(df_mzda["Hodnota"].iloc[-1])

    def get_wage_growth_rate(self, years_back: int = 10) -> float | None:
        """Calculate average annual wage growth rate over N years."""
        df = self._client.get_wages_quarterly()
        df_mzda = df[df["Ukazatel"] == "Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč)"]
        df_mzda = df_mzda.copy()
        df_mzda["Hodnota"] = pd.to_numeric(df_mzda["Hodnota"], errors="coerce")
        if len(df_mzda) < years_back * 4:
            return None
        latest = df_mzda["Hodnota"].iloc[-1]
        prev = df_mzda["Hodnota"].iloc[-(years_back * 4)]
        if prev == 0:
            return None
        return ((latest / prev) ** (1 / years_back) - 1) * 100
