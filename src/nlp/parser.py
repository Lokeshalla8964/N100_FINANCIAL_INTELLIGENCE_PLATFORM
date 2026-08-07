import re
import pandas as pd

analysis = pd.read_excel("data/raw/analysis.xlsx", header=1)

pattern = r"(\d+)\s*Years?:\s*(-?\d+\.?\d*)%"

records = []

for _, row in analysis.iterrows():

    company_id = row["company_id"]

    for metric in [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]:

        text = str(row[metric])

        match = re.search(pattern, text)

        if match:
            records.append({
                "company_id": company_id,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })

parsed = pd.DataFrame(records)

parsed.to_csv("output/analysis_parsed.csv", index=False)

print(parsed.head())
print(f"\nTotal Parsed Records: {len(parsed)}")