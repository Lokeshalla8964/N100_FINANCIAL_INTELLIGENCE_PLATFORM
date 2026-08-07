import pandas as pd
import re

analysis = pd.read_excel("data/raw/analysis.xlsx", header=1)

pros_cons = []

def extract_value(text):
    match = re.search(r"(-?\d+\.?\d*)%", str(text))
    if match:
        return float(match.group(1))
    return None

for _, row in analysis.iterrows():

    company = row["company_id"]

    roe = extract_value(row["roe"])
    sales = extract_value(row["compounded_sales_growth"])

    if roe is not None:
        if roe >= 20:
            pros_cons.append({
                "company_id": company,
                "type": "Pro",
                "text": "High Return on Equity"
            })
        else:
            pros_cons.append({
                "company_id": company,
                "type": "Con",
                "text": "Low Return on Equity"
            })

    if sales is not None:
        if sales >= 15:
            pros_cons.append({
                "company_id": company,
                "type": "Pro",
                "text": "Strong Sales Growth"
            })
        else:
            pros_cons.append({
                "company_id": company,
                "type": "Con",
                "text": "Weak Sales Growth"
            })

result = pd.DataFrame(pros_cons)

result.to_csv("output/pros_cons_generated.csv", index=False)

print(result.head())

print(f"\nGenerated {len(result)} Pros & Cons.")