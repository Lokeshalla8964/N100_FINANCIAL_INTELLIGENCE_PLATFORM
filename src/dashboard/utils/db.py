print("DB.PY LOADED")
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "raw"

def load_excel(file_name):
    df = pd.read_excel(DATA_PATH / file_name, header=None)
    df.columns = df.iloc[1]          # row 1 has the real headers
    df = df.iloc[2:].reset_index(drop=True)   # remove title row + header row
    return df

def get_companies():
    return load_excel("companies.xlsx")

def get_analysis():
    return load_excel("analysis.xlsx")

def get_profit_loss():
    return load_excel("profitandloss.xlsx")

def get_balance_sheet():
    return load_excel("balancesheet.xlsx")

def get_cash_flow():
    return load_excel("cashflow.xlsx")

def get_pros_cons():
    return load_excel("prosandcons.xlsx")

def get_documents():
    return load_excel("documents.xlsx")

def get_sectors():
    return pd.read_excel(DATA_PATH / "sectors.xlsx")
