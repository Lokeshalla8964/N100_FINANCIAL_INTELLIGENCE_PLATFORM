import numpy as np
import matplotlib.pyplot as plt
import os


def radar_chart(df, company_name):
    company = df[df["company_name"] == company_name]

    if company.empty:
        print("Company not found.")
        return

    metrics = [
        "roe_percentage",
        "roce_percentage"
    ]

    values = []

    for metric in metrics:
        value = company.iloc[0][metric]

        try:
            value = float(value)
        except:
            value = 0

        values.append(value)

    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([
        "ROE",
        "ROCE"
    ])

    ax.set_title(company_name)

    os.makedirs("reports/radar_charts", exist_ok=True)

    filename = (
        "reports/radar_charts/"
        + company_name.replace(" ", "_")
        + "_radar.png"
    )

    plt.savefig(filename)

    plt.close()

    print(f"Radar chart saved: {filename}")