from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA = BASE_DIR / "data" / "raw"

ANALYSIS_FILE = RAW_DATA / "analysis.xlsx"
BALANCE_SHEET_FILE = RAW_DATA / "balancesheet.xlsx"
CASHFLOW_FILE = RAW_DATA / "cashflow.xlsx"
COMPANIES_FILE = RAW_DATA / "companies.xlsx"
DOCUMENTS_FILE = RAW_DATA / "documents.xlsx"
PROFIT_LOSS_FILE = RAW_DATA / "profitandloss.xlsx"
PROS_CONS_FILE = RAW_DATA / "prosandcons.xlsx"