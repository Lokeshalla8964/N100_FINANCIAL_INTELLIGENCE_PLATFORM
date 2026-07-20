import matplotlib.pyplot as plt

def revenue_growth_chart(start_revenue, end_revenue):

    labels = ["Start Revenue", "End Revenue"]
    values = [start_revenue, end_revenue]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)

    plt.title("Revenue Growth")
    plt.ylabel("Revenue")

    plt.show()