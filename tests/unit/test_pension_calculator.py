"""
Unit tests for pension_calculator.py
"""

import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "backend", "engine")
)

from pension_calculator import calculate_early_retirement, calculate_pension


def test_calculate_pension_basic():
    """Test basic pension calculation."""
    result = calculate_pension(
        annual_incomes=[38000 * 12],
        coefficients=[1.0581],
        insurance_years=45,
        excluded_days=0,
    )
    assert "pension_amount" in result
    assert result["insurance_years"] == 45
    assert result["pension_amount"] > 0


def test_calculate_pension_components():
    """Test that all components are returned."""
    result = calculate_pension(
        annual_incomes=[38000 * 12],
        coefficients=[1.0581],
        insurance_years=45,
    )
    assert "ovz" in result
    assert "vz" in result
    assert "base_pension" in result
    assert "percent_rate" in result


def test_calculate_early_retirement():
    """Test early retirement calculation."""
    result = calculate_early_retirement(
        pension_amount=20000.0,
        months_before=12,
    )
    assert "reduced_pension" in result
    assert result["reduced_pension"] < 20000.0
    assert result["months_early"] == 12


if __name__ == "__main__":
    test_calculate_pension_basic()
    print("test_calculate_pension_basic passed")
    test_calculate_pension_components()
    print("test_calculate_pension_components passed")
    test_calculate_early_retirement()
    print("test_calculate_early_retirement passed")
    print("\nAll pension calculator tests completed")
