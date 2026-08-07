import pandas as pd
from cashflow_kpis import *

cashflow = pd.read_excel("data/raw/cashflow.xlsx", header=1)
profit = pd.read_excel("data/raw/profitandloss.xlsx", header=1)

records = []

for _, row in cashflow.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    # Match company and year in Profit & Loss
    pl = profit[
        (profit["company_id"] == row["company_id"]) &
        (profit["year"] == row["year"])
    ]

    if len(pl) == 0:
        continue

    sales = pl.iloc[0]["sales"]
    operating_profit = pl.iloc[0]["operating_profit"]
    pat = pl.iloc[0]["net_profit"]

    fcf = free_cash_flow(cfo, cfi)
    quality = cfo_quality(cfo, pat)

    capex = abs(cfi)
    capex_pct = capex_intensity(capex, sales)

    fcf_conversion_pct = fcf_conversion(fcf, operating_profit)

    pattern = capital_allocation(cfo, cfi, cff)

    records.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "free_cash_flow": fcf,
        "cfo_quality": quality,
        "capex_intensity": capex_pct,
        "fcf_conversion": fcf_conversion_pct,
        "capital_allocation": pattern
    })

result = pd.DataFrame(records)

result.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

print(result.head())
print(f"\nGenerated {len(result)} records.")