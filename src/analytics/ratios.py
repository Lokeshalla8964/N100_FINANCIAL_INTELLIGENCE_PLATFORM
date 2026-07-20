def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = (Net Profit / Sales) * 100
    Returns None if sales is 0.
    """
    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = (Operating Profit / Sales) * 100
    Returns None if sales is 0.
    """
    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def return_on_equity(net_profit, equity):
    """
    ROE = (Net Profit / Equity) * 100
    Returns None if equity <= 0.
    """
    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_assets(net_profit, total_assets):
    """
    ROA = (Net Profit / Total Assets) * 100
    Returns None if total_assets is 0.
    """
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def debt_to_equity(borrowings, equity):
    """
    Debt to Equity Ratio
    Returns 0 if borrowings is 0.
    Returns None if equity <= 0.
    """
    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return borrowings / equity
def return_on_capital_employed(ebit, equity, borrowings):
    """
    ROCE = EBIT / (Equity + Borrowings) * 100
    Returns None if denominator <= 0.
    """
    capital_employed = equity + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio = (Operating Profit + other income) / Interest
    Returns None if interest is 0.
    """
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def net_debt(borrowings, investments):
    """
    Net Debt = Borrowings - Investments
    """
    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover = Sales / Total Assets
    Returns None if total_assets is 0.
    """
    if total_assets == 0:
        return None

    return sales / total_assets