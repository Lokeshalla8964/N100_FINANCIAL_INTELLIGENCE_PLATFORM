import pandas as pd

df = pd.read_excel("output/cashflow_intelligence.xlsx")

latest = df.sort_values("year").groupby("company_id").tail(1)

summary = (
    latest.groupby("capital_allocation")
    .size()
    .reset_index(name="company_count")
)

summary.to_csv(
    "output/capital_allocation_summary.csv",
    index=False
)

print(summary)
print("\nCapital Allocation Summary Generated.")