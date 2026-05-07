"""
Unit tests for paradox_resolver.py
"""

import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "backend", "engine")
)

from paradox_resolver import resolve_paradox


def test_resolve_paradox_include():
    """Test paradox resolution - include substitute period."""
    result = resolve_paradox(
        annual_incomes=[38000 * 12],
        coefficients=[1.0581],
        total_days=365 * 45,
        substitute_days=365,
    )
    assert "include_substitute_period" in result
    assert "ovz_with_inclusion" in result
    assert "ovz_with_exclusion" in result


def test_resolve_paradox_recommendation():
    """Test that recommendation is provided."""
    result = resolve_paradox(
        annual_incomes=[35000 * 12],
        coefficients=[1.0581],
        total_days=365 * 40,
        substitute_days=180,
    )
    assert result["recommendation"] in [
        "Zahrnout náhradní dobu",
        "Vyloučit náhradní dobu",
    ]


if __name__ == "__main__":
    test_resolve_paradox_include()
    print("test_resolve_paradox_include passed")
    test_resolve_paradox_recommendation()
    print("test_resolve_paradox_recommendation passed")
    print("\nAll paradox resolver tests completed")
