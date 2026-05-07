"""
Unit tests for reduction_engine.py
"""

import sys
import os
import yaml

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "backend", "engine")
)

from reduction_engine import apply_reduction_limits, calculate_vz


def test_apply_reduction_limits_basic():
    """Test basic reduction application."""
    limits = [
        {"threshold": 21546, "rate": 0.99, "description": "1. redukční hranice"},
        {"threshold": 195868, "rate": 0.26, "description": "2. redukční hranice"},
        {"threshold": None, "rate": 0.0, "description": "nad 2. redukční hranici"},
    ]
    ovz = 38000.0
    vz = apply_reduction_limits(ovz, limits)
    expected = 21546 * 0.99 + (38000 - 21546) * 0.26
    assert abs(vz - expected) < 1, f"Expected {expected:.2f}, got {vz:.2f}"


def test_apply_reduction_under_first_limit():
    """Test when OVZ is under first limit."""
    limits = [
        {"threshold": 21546, "rate": 0.99, "description": "1. redukční hranice"},
        {"threshold": 195868, "rate": 0.26, "description": "2. redukční hranice"},
        {"threshold": None, "rate": 0.0, "description": "nad 2. redukční hranici"},
    ]
    ovz = 20000.0
    vz = apply_reduction_limits(ovz, limits)
    expected = 20000 * 0.99
    assert abs(vz - expected) < 1


def test_calculate_vz_from_config():
    """Test calculate_vz with config dict."""
    config = {
        "reduction_limits": [
            {"threshold": 21546, "rate": 0.99},
            {"threshold": 195868, "rate": 0.26},
            {"threshold": None, "rate": 0.0},
        ]
    }
    vz = calculate_vz(38000.0, config)
    expected = 21546 * 0.99 + (38000 - 21546) * 0.26
    assert abs(vz - expected) < 1


if __name__ == "__main__":
    test_apply_reduction_limits_basic()
    print("test_apply_reduction_limits_basic passed")
    test_apply_reduction_under_first_limit()
    print("test_apply_reduction_under_first_limit passed")
    test_calculate_vz_from_config()
    print("test_calculate_vz_from_config passed")
    print("\nAll reduction engine tests completed")
