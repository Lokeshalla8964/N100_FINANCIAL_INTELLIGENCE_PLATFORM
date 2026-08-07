import pandas as pd

pl = pd.read_excel("data/raw/profitandloss.xlsx", header=1)

print(pl.head())

print("\nColumns:")
for col in pl.columns:
    print(col)