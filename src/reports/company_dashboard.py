def display_dashboard(company, sales, net_profit, roe, debt_equity):
    print("\n========== COMPANY DASHBOARD ==========")
    print("Company        :", company)
    print("Sales          :", sales)
    print("Net Profit     :", net_profit)
    print("ROE            :", round(roe, 2), "%")
    print("Debt to Equity :", debt_equity)
    print("=======================================\n")