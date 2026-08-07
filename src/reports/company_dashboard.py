def display_dashboard(company, sales, net_profit, roe, debt_equity):
    print("\n========== COMPANY DASHBOARD ==========")
    print("Company        :", company)
    print("Sales          :", sales)
    print("Net Profit     :", net_profit)
    print("ROE            :", round(roe, 2), "%")
    print("Debt to Equity :", debt_equity)
    print("=======================================\n")

if __name__ == "__main__":
    display_dashboard(
        company="ABB",
        sales=25000,
        net_profit=4200,
        roe=18.75,
        debt_equity=0.35,
    )