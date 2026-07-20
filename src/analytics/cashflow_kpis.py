def free_cash_flow(cfo, cfi):
    """
    Free Cash Flow = CFO + CFI
    (CFI is usually negative)
    """
    return cfo + cfi


def cfo_quality(cfo, pat):
    """
    CFO Quality = CFO / PAT
    Returns None if PAT is 0.
    """
    if pat == 0:
        return None

    return cfo / pat


def capex_intensity(capex, sales):
    """
    CapEx Intensity = |CapEx| / Sales * 100
    Returns None if sales is 0.
    """
    if sales == 0:
        return None

    return abs(capex) / sales * 100


def fcf_conversion(fcf, operating_profit):
    """
    FCF Conversion = FCF / Operating Profit * 100
    Returns None if operating_profit is 0.
    """
    if operating_profit == 0:
        return None

    return fcf / operating_profit * 100
def capital_allocation(cfo, cfi, cff):
    """
    Capital Allocation Pattern
    """

    if cfo > 0 and cfi < 0 and cff < 0:
        return "Reinvestor"

    elif cfo > 0 and cfi < 0 and cff > 0:
        return "Growth Funded by Debt"

    elif cfo > 0 and cfi > 0 and cff < 0:
        return "Shareholder Returns"

    elif cfo > 0 and cfi > 0 and cff > 0:
        return "Cash Accumulator"

    else:
        return "Mixed"