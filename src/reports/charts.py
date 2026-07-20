import matplotlib.pyplot as plt

def sales_profit_chart(sales, net_profit):

    labels = ["Sales", "Net Profit"]
    values = [sales, net_profit]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)

    plt.title("Sales vs Net Profit")
    plt.ylabel("Amount")

    plt.show()