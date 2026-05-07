"""
FastAPI application for Pension Calculator
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src", "backend", "engine")
)

from ovz_calculator import calculate_ovz, calculate_ovz_from_annual
from reduction_engine import calculate_vz
from pension_calculator import calculate_pension, calculate_early_retirement
from paradox_resolver import resolve_paradox

app = FastAPI(title="Pension Calculator API", version="1.0.0")


class OVZRequest(BaseModel):
    annual_incomes: List[float]
    coefficients: List[float]
    total_days: int
    excluded_days: int = 0


class PensionRequest(BaseModel):
    annual_incomes: List[float]
    coefficients: List[float]
    insurance_years: int
    excluded_days: int = 0


class EarlyRetirementRequest(BaseModel):
    pension_amount: float
    months_before: int


class ParadoxRequest(BaseModel):
    annual_incomes: List[float]
    coefficients: List[float]
    total_days: int
    substitute_days: int


@app.get("/")
async def root():
    return {"message": "Pension Calculator API", "version": "1.0.0"}


@app.post("/calculate-ovz")
async def api_calculate_ovz(request: OVZRequest):
    """Calculate Osobní vyměřovací základ."""
    try:
        ovz = calculate_ovz(
            request.annual_incomes,
            request.coefficients,
            request.total_days,
            request.excluded_days,
        )
        return {"ovz": ovz}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calculate-pension")
async def api_calculate_pension(request: PensionRequest):
    """Calculate old-age pension."""
    try:
        result = calculate_pension(
            request.annual_incomes,
            request.coefficients,
            request.insurance_years,
            request.excluded_days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calculate-early-retirement")
async def api_calculate_early_retirement(request: EarlyRetirementRequest):
    """Calculate early retirement pension."""
    try:
        result = calculate_early_retirement(
            request.pension_amount, request.months_before
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/resolve-paradox")
async def api_resolve_paradox(request: ParadoxRequest):
    """Resolve the decision paradox for substitute periods."""
    try:
        result = resolve_paradox(
            request.annual_incomes,
            request.coefficients,
            request.total_days,
            request.substitute_days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
