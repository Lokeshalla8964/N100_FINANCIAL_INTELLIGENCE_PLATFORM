import matplotlib.pyplot as plt

def profit_distribution(net_profit, operating_profit):

    plt.figure(figsize=(5,5))

    plt.pie(
        [net_profit, operating_profit],
        labels=["Net Profit","Operating Profit"],
        autopct="%1.1f%%"
    )

    plt.title("Profit Distribution")

    plt.show()