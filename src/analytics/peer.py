import pandas as pd


def calculate_peer_rank(df):
    print("\n========== PEER PERCENTILE RANKINGS ==========\n")

    # Make a copy
    peer_df = df.copy()

    # Required columns
    columns = [
        "id",
        "company_name",
        "roe_percentage",
        "roce_percentage"
    ]

    peer_df = peer_df[columns]

    # Convert numeric columns
    peer_df["roe_percentage"] = pd.to_numeric(
        peer_df["roe_percentage"], errors="coerce"
    )

    peer_df["roce_percentage"] = pd.to_numeric(
        peer_df["roce_percentage"], errors="coerce"
    )

    # Percentile Ranking
    peer_df["roe_rank"] = (
        peer_df["roe_percentage"]
        .rank(pct=True) * 100
    ).round(2)

    peer_df["roce_rank"] = (
        peer_df["roce_percentage"]
        .rank(pct=True) * 100
    ).round(2)

    # Composite Peer Score
    peer_df["peer_score"] = (
        peer_df["roe_rank"] +
        peer_df["roce_rank"]
    ) / 2

    peer_df = peer_df.sort_values(
        by="peer_score",
        ascending=False
    )

    print(peer_df.head(20))

    return peer_df