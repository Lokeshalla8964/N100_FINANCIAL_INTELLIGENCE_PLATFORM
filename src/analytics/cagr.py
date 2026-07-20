def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR (Compound Annual Growth Rate).

    CAGR = ((End / Start) ** (1 / Years) - 1) * 100
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return cagr, "NORMAL"