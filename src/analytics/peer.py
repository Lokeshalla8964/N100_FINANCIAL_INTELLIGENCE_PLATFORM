import os
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

COMPANIES_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "companies.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

PEER_OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "peer_rankings.csv"
)


# ============================================================
# LOAD COMPANIES DATA
# ============================================================

def load_companies_data():
    print("\n==========================================")
    print("LOADING COMPANIES DATA")
    print("==========================================")

    if not os.path.exists(COMPANIES_FILE):
        raise FileNotFoundError(
            f"Companies file not found:\n{COMPANIES_FILE}"
        )

    # Your Excel files use the second row as the header
    companies = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )

    # Clean column names
    companies.columns = (
        companies.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    print("\nCompanies columns:")
    print(companies.columns.tolist())

    print(
        f"\nCompanies loaded: "
        f"{len(companies)} records"
    )

    return companies


# ============================================================
# FIND COMPANY ID
# ============================================================

def standardize_company_id(df):
    """
    Make sure the dataframe has a standard company_id column.
    """

    df = df.copy()

    if "company_id" in df.columns:
        pass

    elif "id" in df.columns:
        df["company_id"] = df["id"]

    else:
        raise ValueError(
            "Companies data does not contain "
            "'company_id' or 'id'."
        )

    return df


# ============================================================
# CALCULATE PEER RANK
# ============================================================

def calculate_peer_rank(df):

    print("\n==========================================")
    print("PEER PERCENTILE RANKINGS")
    print("==========================================")

    if df is None:
        raise ValueError("Input dataframe is None.")

    if df.empty:
        print("WARNING: Companies dataframe is empty.")
        return pd.DataFrame()

    peer_df = df.copy()

    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    peer_df.columns = (
        peer_df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # Standardize company ID
    # --------------------------------------------------------

    peer_df = standardize_company_id(peer_df)

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = [
        "company_id",
        "company_name",
        "roe_percentage",
        "roce_percentage"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in peer_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Companies data is missing required columns: "
            f"{missing_columns}"
        )

    # --------------------------------------------------------
    # Select only required columns
    # --------------------------------------------------------

    peer_df = peer_df[
        [
            "company_id",
            "company_name",
            "roe_percentage",
            "roce_percentage"
        ]
    ].copy()

    # --------------------------------------------------------
    # Clean company names
    # --------------------------------------------------------

    peer_df["company_name"] = (
        peer_df["company_name"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Convert ROE and ROCE to numeric
    # --------------------------------------------------------

    peer_df["roe_percentage"] = pd.to_numeric(
        peer_df["roe_percentage"],
        errors="coerce"
    )

    peer_df["roce_percentage"] = pd.to_numeric(
        peer_df["roce_percentage"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Show missing values
    # --------------------------------------------------------

    print("\nMissing values:")

    print(
        peer_df[
            [
                "roe_percentage",
                "roce_percentage"
            ]
        ].isna().sum()
    )

    # --------------------------------------------------------
    # Remove rows where both ROE and ROCE are missing
    # --------------------------------------------------------

    peer_df = peer_df.dropna(
        subset=[
            "roe_percentage",
            "roce_percentage"
        ],
        how="all"
    ).copy()

    if peer_df.empty:
        print(
            "WARNING: No valid ROE/ROCE records found."
        )

        return peer_df

    # --------------------------------------------------------
    # Fill individual missing values with median
    # --------------------------------------------------------

    roe_median = peer_df[
        "roe_percentage"
    ].median()

    roce_median = peer_df[
        "roce_percentage"
    ].median()

    if pd.isna(roe_median):
        roe_median = 0

    if pd.isna(roce_median):
        roce_median = 0

    peer_df["roe_percentage"] = (
        peer_df["roe_percentage"]
        .fillna(roe_median)
    )

    peer_df["roce_percentage"] = (
        peer_df["roce_percentage"]
        .fillna(roce_median)
    )

    # --------------------------------------------------------
    # ROE percentile ranking
    # --------------------------------------------------------

    peer_df["roe_rank"] = (
        peer_df[
            "roe_percentage"
        ]
        .rank(
            method="average",
            pct=True
        )
        * 100
    ).round(2)

    # --------------------------------------------------------
    # ROCE percentile ranking
    # --------------------------------------------------------

    peer_df["roce_rank"] = (
        peer_df[
            "roce_percentage"
        ]
        .rank(
            method="average",
            pct=True
        )
        * 100
    ).round(2)

    # --------------------------------------------------------
    # Composite peer score
    # --------------------------------------------------------

    peer_df["peer_score"] = (
        peer_df["roe_rank"]
        +
        peer_df["roce_rank"]
    ) / 2

    peer_df["peer_score"] = (
        peer_df["peer_score"]
        .round(2)
    )

    # --------------------------------------------------------
    # Final peer ranking
    # --------------------------------------------------------

    peer_df["peer_rank"] = (
        peer_df["peer_score"]
        .rank(
            method="min",
            ascending=False
        )
        .astype(int)
    )

    # --------------------------------------------------------
    # Sort results
    # --------------------------------------------------------

    peer_df = peer_df.sort_values(
        by=[
            "peer_score",
            "roe_percentage",
            "roce_percentage"
        ],
        ascending=[
            False,
            False,
            False
        ]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("\n========== PEER RANKING RESULTS ==========\n")

    print(
        peer_df[
            [
                "company_id",
                "company_name",
                "roe_percentage",
                "roce_percentage",
                "roe_rank",
                "roce_rank",
                "peer_score",
                "peer_rank"
            ]
        ].head(20).to_string(index=False)
    )

    print(
        "\n=========================================="
    )

    print("PEER RANKING COMPLETED")

    print(
        "=========================================="
    )

    return peer_df


# ============================================================
# SAVE PEER RESULTS
# ============================================================

def save_peer_rankings(peer_df):

    if peer_df is None or peer_df.empty:
        print(
            "\nWARNING: No peer rankings to save."
        )
        return None

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    peer_df.to_csv(
        PEER_OUTPUT_FILE,
        index=False
    )

    print(
        f"\nPeer rankings saved to:\n"
        f"{PEER_OUTPUT_FILE}"
    )

    return PEER_OUTPUT_FILE


# ============================================================
# GET TOP PEERS
# ============================================================

def get_top_peers(
    peer_df,
    n=10
):

    if peer_df is None or peer_df.empty:
        return pd.DataFrame()

    return (
        peer_df
        .sort_values(
            by="peer_score",
            ascending=False
        )
        .head(n)
        .reset_index(drop=True)
    )


# ============================================================
# FIND PEERS FOR A COMPANY
# ============================================================

def find_company_peers(
    peer_df,
    company_id,
    n=5
):

    if peer_df is None or peer_df.empty:
        return pd.DataFrame()

    company_id = str(company_id)

    selected = peer_df[
        peer_df["company_id"]
        .astype(str)
        == company_id
    ]

    if selected.empty:
        print(
            f"Company ID {company_id} "
            "not found."
        )

        return pd.DataFrame()

    selected_score = (
        selected.iloc[0]["peer_score"]
    )

    peers = peer_df.copy()

    # Calculate similarity in peer score
    peers["score_difference"] = (
        peers["peer_score"]
        -
        selected_score
    ).abs()

    # Remove selected company
    peers = peers[
        peers["company_id"]
        .astype(str)
        != company_id
    ]

    peers = peers.sort_values(
        by="score_difference",
        ascending=True
    )

    return (
        peers
        .head(n)
        .reset_index(drop=True)
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("==========================================")
    print("      N100 FINANCIAL INTELLIGENCE")
    print("             PEER ANALYSIS")
    print("==========================================")

    try:

        # ----------------------------------------------------
        # 1. Load real Companies Excel file
        # ----------------------------------------------------

        companies = load_companies_data()

        # ----------------------------------------------------
        # 2. Calculate peer rankings
        # ----------------------------------------------------

        peer_results = calculate_peer_rank(
            companies
        )

        # ----------------------------------------------------
        # 3. Save results
        # ----------------------------------------------------

        save_peer_rankings(
            peer_results
        )

        # ----------------------------------------------------
        # 4. Display top 10 companies
        # ----------------------------------------------------

        print("\n========== TOP 10 COMPANIES ==========\n")

        top_companies = get_top_peers(
            peer_results,
            n=10
        )

        print(
            top_companies.to_string(
                index=False
            )
        )

        # ----------------------------------------------------
        # 5. Example company peer search
        # ----------------------------------------------------

        if not peer_results.empty:

            first_company_id = (
                peer_results.iloc[0]["company_id"]
            )

            print(
                "\n========== PEERS FOR COMPANY "
                f"{first_company_id} ==========\n"
            )

            company_peers = find_company_peers(
                peer_results,
                first_company_id,
                n=5
            )

            print(
                company_peers.to_string(
                    index=False
                )
            )

        # ----------------------------------------------------
        # 6. Finished
        # ----------------------------------------------------

        print("\n")
        print("==========================================")
        print("PEER ANALYSIS COMPLETED SUCCESSFULLY")
        print("==========================================")

    except Exception as e:

        print("\n")
        print("==========================================")
        print("PEER ANALYSIS FAILED")
        print("==========================================")

        print(
            f"\nError: {type(e).__name__}"
        )

        print(
            f"Details: {e}"
        )