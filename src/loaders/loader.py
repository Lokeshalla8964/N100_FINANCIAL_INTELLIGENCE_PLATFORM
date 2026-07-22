import pandas as pd
from analytics.ratios import *
from analytics.cagr import *
from analytics.cashflow_kpis import *
from analytics.health_score import *
from analytics.company_profile import *
from reports.company_dashboard import display_dashboard
from analytics.investment_screener import screen_company
from analytics.sector_analytics import sector_rating
from reports.report_generator import generate_report
from reports.charts import sales_profit_chart
from reports.growth_chart import revenue_growth_chart
from reports.profit_chart import profit_distribution
from screener.engine import screen_companies
from export.excel_export import export_screener
from analytics.peer import calculate_peer_rank
from reports.radar_chart import radar_chart
from export.peer_export import export_peer_comparison


from config.config import (
    ANALYSIS_FILE,
    BALANCE_SHEET_FILE,
    CASHFLOW_FILE,
    COMPANIES_FILE,
    DOCUMENTS_FILE,
    PROFIT_LOSS_FILE,
    PROS_CONS_FILE,
)

analysis = pd.read_excel(ANALYSIS_FILE)
balance_sheet = pd.read_excel(BALANCE_SHEET_FILE)
cashflow = pd.read_excel(CASHFLOW_FILE)
companies = pd.read_excel(COMPANIES_FILE, header=1)
documents = pd.read_excel(DOCUMENTS_FILE)
profit_loss = pd.read_excel(PROFIT_LOSS_FILE, header=1)
pros_cons = pd.read_excel(PROS_CONS_FILE)

print("All datasets loaded successfully!")
print(profit_loss.columns.tolist())
# =========================
# TESTING SECTION
# =========================
row = profit_loss.iloc[0]

sales = row["sales"]
net_profit = row["net_profit"]
operating_profit = row["operating_profit"]
npm = net_profit_margin(net_profit, sales)
print("Net Profit Margin:", round(npm, 2), "%")

print("Sales:", sales)
print("Net Profit:", net_profit)
print("Operating Profit:", operating_profit)

print("Net Profit Margin:", net_profit_margin(net_profit, sales))
print("Operating Profit Margin:", operating_profit_margin(operating_profit, sales))
equity = 1000

roe = return_on_equity(net_profit, equity)
print("Return on Equity:", roe)
borrowings = 500
investments = 100
interest = 20
other_income = 30
total_assets = 2000

debt_to_equity = debt_to_equity(borrowings, equity)
print("Debt to Equity:", debt_to_equity)
print("Interest Coverage:", interest_coverage_ratio(operating_profit, other_income, interest))
print("Net Debt:", net_debt(borrowings, investments))
print("Asset Turnover:", asset_turnover(sales, total_assets))
# ---------- CAGR TEST ----------

start_revenue = 1000
end_revenue = 1500
years = 5

cagr_value, status = calculate_cagr(start_revenue, end_revenue, years)

print("Revenue CAGR:", cagr_value)
print("Status:", status)
print("\n===== CAGR EDGE CASE TESTS =====")

print(calculate_cagr(0, 1500, 5))          # ZERO_BASE
print(calculate_cagr(-1000, 1500, 5))      # TURNAROUND
print(calculate_cagr(1000, -500, 5))       # DECLINE_TO_LOSS
print(calculate_cagr(-1000, -500, 5))      # BOTH_NEGATIVE
print(calculate_cagr(1000, 1500, 0))       # INVALID_YEARS
# ---------- CASH FLOW KPI TEST ----------

cfo = 500
cfi = -150
cff = -100
pat = 145
capex = -120
sales = 1653
operating_profit = 202

fcf = free_cash_flow(cfo, cfi)

print("\n===== CASH FLOW KPI TEST =====")
print("Free Cash Flow:", fcf)
print("CFO Quality:", cfo_quality(cfo, pat))
print("CapEx Intensity:", capex_intensity(capex, sales))
print("FCF Conversion:", fcf_conversion(fcf, operating_profit))
print("Capital Allocation:", capital_allocation(cfo, cfi, cff))
print("Financial health:", financial_health_score(85))

profile = company_profile("Reliance", "Energy", 2100000)

print("\nCompany Profile")
print(profile)

display_dashboard(
    company=row["company_id"],
    sales=sales,
    net_profit=net_profit,
    roe=roe,
    debt_equity=debt_to_equity
)

recommendation = screen_company(
    roe=roe,
    debt_equity=debt_to_equity,
    net_profit_margin=npm
)

print("Investment Recommendation:", recommendation)

sector = sector_rating(roe)
print("Sector Rating:", sector)

generate_report(
    company=row["company_id"],
    sales=sales,
    net_profit=net_profit,
    roe=roe,
    debt_equity=debt_to_equity,
    recommendation=recommendation,
    sector=sector
)

sales_profit_chart(sales, net_profit)

revenue_growth_chart(start_revenue, end_revenue)

profit_distribution(net_profit, operating_profit)

screen_companies(companies)

export_screener(companies)

calculate_peer_rank(companies)

radar_chart(companies, "Abbott India Ltd")

export_peer_comparison(companies)