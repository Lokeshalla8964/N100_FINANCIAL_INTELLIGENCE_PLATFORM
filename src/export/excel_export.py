import os
import pandas as pd


def export_screener(df):

    os.makedirs("output", exist_ok=True)

    output_file = "output/screener_output.xlsx"

    # Convert to numeric
    df["roe_percentage"] = pd.to_numeric(df["roe_percentage"], errors="coerce")
    df["roce_percentage"] = pd.to_numeric(df["roce_percentage"], errors="coerce")

    # Composite Score
    df["composite_score"] = (
        df["roe_percentage"] +
        df["roce_percentage"]
    ) / 2

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        # Sheet 1
        high_roe = df[df["roe_percentage"] > 15]
        high_roe.to_excel(writer, sheet_name="High ROE", index=False)

        # Sheet 2
        high_roce = df[df["roce_percentage"] > 20]
        high_roce.to_excel(writer, sheet_name="High ROCE", index=False)

        # Sheet 3
        top_score = df.sort_values(
            "composite_score",
            ascending=False
        )
        top_score.to_excel(
            writer,
            sheet_name="Top Composite",
            index=False
        )

        quality = df[
            (df["roe_percentage"] > 15) &
            (df["roce_percentage"] > 20)
        ]
        quality.to_excel(
            writer,
            sheet_name="Quality",
            index=False
        )

        # Sheet 4
        df.to_excel(
            writer,
            sheet_name="All Companies",
            index=False
        )

    print("\nExcel exported successfully.")
    print(output_file)

         # sheet 5
    high_performers = df[
    (df["roe_percentage"] > 20) &
    (df["roce_percentage"] > 25)
        ]

    high_performers.to_excel(
    writer,
    sheet_name="High Performers",
    index=False
        )
    
    # sheet 6
    df.to_excel(
    writer,
    sheet_name="All Companies",
    index=False
        )
