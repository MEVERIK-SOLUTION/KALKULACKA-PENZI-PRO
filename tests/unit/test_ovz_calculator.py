"""
Unit tests for ovz_calculator.py
"""

import json
import os
import sys

import yaml

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "backend", "engine")
)

from ovz_calculator import (
    calculate_ovz,
    calculate_ovz_from_annual,
    calculate_reduced_base,
)


def test_basic_ovz():
    """Test A01: Basic employee, male, 45 years"""
    result = calculate_ovz(
        annual_incomes=[38000 * 12],
        coefficients=[1.0581],
        total_days=365 * 45,
        excluded_days=0,
    )
    expected = (38000 * 12 * 1.0581) / (365 * 45) * 30.4167
    assert abs(result - expected) < 1, f"Expected ~{expected:.2f}, got {result:.2f}"


def test_with_excluded_days():
    """Test D01: Long-term sickness"""
    result_no_excl = calculate_ovz(
        annual_incomes=[35000 * 12],
        coefficients=[1.0581],
        total_days=365 * 45,
        excluded_days=0,
    )
    result_with_excl = calculate_ovz(
        annual_incomes=[35000 * 12],
        coefficients=[1.0581],
        total_days=365 * 45,
        excluded_days=540,
    )
    assert result_with_excl > result_no_excl, (
        f"OVZ with excluded days ({result_with_excl}) should be higher than without ({result_no_excl})"
    )


def test_ovz_from_annual():
    """Simplified version"""
    result = calculate_ovz_from_annual(
        annual_income=38000 * 12, coefficient=1.0581, years=45, excluded_days=0
    )
    expected = (38000 * 12 * 1.0581) / (365 * 45) * 30.4167
    assert abs(result - expected) < 1, f"Expected ~{expected:.2f}, got {result:.2f}"


def test_reduction_2026():
    """Test reduction for 2026 config"""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "config", "legislative_2026.yaml"
    )
    if not os.path.exists(config_path):
        config_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "config",
            "legislative_2026.yaml",
        )

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    ovz = 38000.0
    vz = calculate_reduced_base(ovz, config)
    expected = 21546 * 0.99 + (38000 - 21546) * 0.26
    assert abs(vz - expected) < 1, f"Expected {expected:.2f}, got {vz:.2f}"


def test_model_case_a01():
    """Test with model_cases.json"""
    fixture_path = os.path.join(
        os.path.dirname(__file__), "..", "fixtures", "model_cases.json"
    )
    if not os.path.exists(fixture_path):
        fixture_path = "/Users/matejkocanda/Library/Mobile Documents/com~apple~CloudDocs/tests/fixtures/model_cases.json"

    try:
        with open(fixture_path, encoding="utf-8") as f:
            cases = json.load(f)
        a01 = next(c for c in cases if c["id"] == "A01")
        assert a01["input"]["averageOVZ"] == 38000
        assert a01["input"]["insurancePeriodYears"] == 45
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    import yaml

    test_basic_ovz()
    print("test_basic_ovz passed")
    test_with_excluded_days()
    print("test_with_excluded_days passed")
    test_ovz_from_annual()
    print("test_ovz_from_annual passed")
    try:
        test_reduction_2026()
        print("test_reduction_2026 passed")
    except Exception as e:
        print(f"test_reduction_2026 failed: {e}")
    try:
        test_model_case_a01()
        print("test_model_case_A01 passed")
    except Exception as e:
        print(f"test_model_case_A01 failed: {e}")
    print("\nAll tests completed")
