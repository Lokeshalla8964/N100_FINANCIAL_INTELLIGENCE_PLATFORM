def generate_report(company, sales, net_profit, roe, debt_equity, recommendation, sector):

    print("\n========== FINAL COMPANY REPORT ==========")
    print(f"Company                  : {company}")
    print(f"Sales                    : {sales}")
    print(f"Net Profit               : {net_profit}")
    print(f"Return on Equity (ROE)   : {roe:.2f}%")
    print(f"Debt to Equity           : {debt_equity}")
    print(f"Investment Recommendation: {recommendation}")
    print(f"Sector Rating            : {sector}")
    print("==========================================")