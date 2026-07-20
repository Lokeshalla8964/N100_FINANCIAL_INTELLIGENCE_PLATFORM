import pandas as pd

def screen_companies(df,
                     min_roe=0,
                     max_debt_equity=float('inf'),
                     min_profit_margin=0):

    screened = df[
        (df["ROE"] >= min_roe) &
        (df["Debt_to_Equity"] <= max_debt_equity) &
        (df["Net_Profit_Margin"] >= min_profit_margin)
    ]

    return screened
def screen_company(roe, debt_equity, net_profit_margin):
    """
    Returns investment recommendation based on financial ratios.
    """

    if roe >= 15 and debt_equity <= 1 and net_profit_margin >= 10:
        return "Strong Buy"

    elif roe >= 10 and debt_equity <= 2:
        return "Buy"

    elif roe >= 5:
        return "Hold"

    else:
        return "Avoid"