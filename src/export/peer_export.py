import os
import pandas as pd


def export_peer_comparison(df):
    # Create output folder
    os.makedirs("output", exist_ok=True)

    # Copy dataframe
    peer_df = df.copy()

    # Convert numeric columns
    peer_df["roe_percentage"] = pd.to_numeric(
        peer_df["roe_percentage"], errors="coerce"
    )

    peer_df["roce_percentage"] = pd.to_numeric(
        peer_df["roce_percentage"], errors="coerce"
    )

    # Calculate percentile ranks
    peer_df["roe_rank"] = (
        peer_df["roe_percentage"].rank(pct=True) * 100
    ).round(2)

    peer_df["roce_rank"] = (
        peer_df["roce_percentage"].rank(pct=True) * 100
    ).round(2)

    # Composite score
    peer_df["peer_score"] = (
        peer_df["roe_rank"] +
        peer_df["roce_rank"]
    ) / 2

    # Sort
    peer_df = peer_df.sort_values(
        by="peer_score",
        ascending=False
    )

    output_file = "output/peer_comparison.xlsx"

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        peer_df.to_excel(
            writer,
            sheet_name="Peer Comparison",
            index=False
        )

    print("\nPeer Comparison Excel exported successfully.")
    print(f"Location: {output_file}")