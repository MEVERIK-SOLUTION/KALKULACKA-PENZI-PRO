"""
Reduction Engine - Application of reduction limits (§ 15 ZDP)
"""



def apply_reduction_limits(ovz: float, reduction_limits: list[dict]) -> float:
    """Apply reduction limits to OVZ."""
    sorted_limits = sorted(
        reduction_limits, key=lambda x: x.get("threshold") or float("inf")
    )

    vz = 0.0
    remaining = ovz

    for i, limit in enumerate(sorted_limits):
        threshold = limit.get("threshold")
        rate = limit.get("rate", 0.0)

        if threshold is None:
            vz += remaining * rate
            remaining = 0
            break

        if i == 0:
            if remaining <= threshold:
                vz += remaining * rate
                remaining = 0
                break
            vz += threshold * rate
            remaining -= threshold
        else:
            prev_threshold = sorted_limits[i - 1].get("threshold") or 0
            bracket = threshold - prev_threshold
            if remaining <= bracket:
                vz += remaining * rate
                remaining = 0
                break
            vz += bracket * rate
            remaining -= bracket

    return round(vz, 2)


def calculate_vz(ovz: float, config: dict) -> float:
    """Calculate Výpočtový základ from OVZ using config."""
    reduction_limits = config.get("reduction_limits", [])
    return apply_reduction_limits(ovz, reduction_limits)
