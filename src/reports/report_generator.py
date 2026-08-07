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

if __name__ == "__main__":
    generate_report(
        company="ABB",
        sales=25000,
        net_profit=4200,
        roe=18.75,
        debt_equity=0.35,
        recommendation="BUY",
        sector="Strong"
    )