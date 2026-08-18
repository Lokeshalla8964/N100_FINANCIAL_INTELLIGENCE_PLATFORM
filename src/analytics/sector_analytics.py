"""
SECTOR ANALYTICS
================

Uses:
    data/raw/companies.xlsx
    data/raw/sectors.xlsx
    output/ratio_analysis.csv

Generates:
    output/sector_analysis.csv
"""

import os
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "output"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# FILES
# ============================================================

COMPANIES_FILE = os.path.join(
    DATA_DIR,
    "companies.xlsx"
)

SECTORS_FILE = os.path.join(
    DATA_DIR,
    "sectors.xlsx"
)

RATIO_FILE = os.path.join(
    OUTPUT_DIR,
    "ratio_analysis.csv"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "sector_analysis.csv"
)


# ============================================================
# HELPER
# ============================================================

def clean_numeric(series):

    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


def find_column(df, possible_names):

    normalized = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        key = name.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# SECTOR RATING
# ============================================================

def sector_rating(roe):

    if pd.isna(roe):
        return "Not Available"

    if roe >= 20:
        return "Excellent"

    elif roe >= 15:
        return "Very Good"

    elif roe >= 10:
        return "Good"

    else:
        return "Needs Improvement"


# ============================================================
# LOAD COMPANIES
# ============================================================

def load_companies():

    print("\n" + "=" * 70)
    print("LOADING COMPANIES")
    print("=" * 70)

    if not os.path.exists(COMPANIES_FILE):

        raise FileNotFoundError(
            f"Companies file not found:\n{COMPANIES_FILE}"
        )

    companies = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )

    companies = companies.dropna(
        how="all"
    )

    companies.columns = [
        str(column).strip()
        for column in companies.columns
    ]

    print(
        "\nCompanies columns:"
    )

    print(
        list(companies.columns)
    )

    return companies


# ============================================================
# LOAD SECTORS
# ============================================================

def load_sectors():

    print("\n" + "=" * 70)
    print("LOADING SECTOR DATA")
    print("=" * 70)

    if not os.path.exists(SECTORS_FILE):

        raise FileNotFoundError(
            f"Sectors file not found:\n{SECTORS_FILE}"
        )

    sectors = pd.read_excel(
        SECTORS_FILE,
        header=0
    )

    sectors = sectors.dropna(
        how="all"
    )

    sectors.columns = [
        str(column).strip()
        for column in sectors.columns
    ]

    print(
        "\nSectors columns:"
    )

    print(
        list(sectors.columns)
    )

    return sectors


# ============================================================
# LOAD RATIO ANALYSIS
# ============================================================

def load_ratios():

    print("\n" + "=" * 70)
    print("LOADING RATIO ANALYSIS")
    print("=" * 70)

    if not os.path.exists(RATIO_FILE):

        print(
            "\nWARNING:"
        )

        print(
            "ratio_analysis.csv not found."
        )

        return None

    ratios = pd.read_csv(
        RATIO_FILE
    )

    ratios.columns = [
        str(column).strip()
        for column in ratios.columns
    ]

    print(
        "\nRatio columns:"
    )

    print(
        list(ratios.columns)
    )

    print(
        f"\nRows loaded: {len(ratios)}"
    )

    return ratios


# ============================================================
# PREPARE COMPANY DATA
# ============================================================

def prepare_companies(companies):

    company_id = find_column(
        companies,
        [
            "company_id",
            "id"
        ]
    )

    company_name = find_column(
        companies,
        [
            "company_name",
            "name"
        ]
    )

    if company_id is None:

        raise ValueError(
            "\nCompany ID column not found "
            "in companies.xlsx."
        )

    rename_map = {
        company_id: "company_id"
    }

    if company_name is not None:

        rename_map[
            company_name
        ] = "company_name"

    companies = companies.rename(
        columns=rename_map
    )

    companies["company_id"] = (
        companies["company_id"]
        .astype(str)
        .str.strip()
    )

    return companies


# ============================================================
# PREPARE SECTOR DATA
# ============================================================

def prepare_sectors(sectors):

    company_id = find_column(
        sectors,
        [
            "company_id",
            "id"
        ]
    )

    sector = find_column(
        sectors,
        [ 
            "broad_sector",
            "sector",
            "sector_name",
            "industry",
            "industry_name"
        ]
    )

    if company_id is None:

        raise ValueError(
            "\nCompany ID column not found "
            "in sectors.xlsx.\n"
            f"Available columns: {list(sectors.columns)}"
        )

    if sector is None:

        raise ValueError(
            "\nBroad sector column not found "
            "in sectors.xlsx.\n"
            f"Available columns: {list(sectors.columns)}"
        )

    sectors = sectors.rename(
        columns={
            company_id: "company_id",
            sector: "sector"
        }
    )

    sectors["company_id"] = (
        sectors["company_id"]
        .astype(str)
        .str.strip()
    )

    sectors["sector"] = (
        sectors["sector"]
        .astype(str)
        .str.strip()
    )

    sectors = sectors[
        sectors["sector"].notna()
    ]

    sectors = sectors[
        sectors["sector"].str.lower()
        != "nan"
    ]

    sectors = sectors[
        [
            "company_id",
            "sector"
        ]
    ]

    sectors = sectors.drop_duplicates(
        subset=["company_id"]
    )

    return sectors


# ============================================================
# PREPARE RATIOS
# ============================================================

def prepare_ratios(ratios):

    if ratios is None:
        return None

    company_id = find_column(
        ratios,
        [
            "company_id",
            "id"
        ]
    )

    if company_id is None:

        print(
            "\nWARNING:"
        )

        print(
            "company_id not found in "
            "ratio_analysis.csv."
        )

        return None

    ratios = ratios.rename(
        columns={
            company_id: "company_id"
        }
    )

    ratios["company_id"] = (
        ratios["company_id"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Find ratio columns
    # --------------------------------------------------------

    roe = find_column(
        ratios,
        [
            "roe_percentage",
            "roe",
            "return_on_equity"
        ]
    )

    roce = find_column(
        ratios,
        [
            "roce_percentage",
            "roce",
            "return_on_capital_employed"
        ]
    )

    net_margin = find_column(
        ratios,
        [
            "net_profit_margin",
            "net_margin"
        ]
    )

    operating_margin = find_column(
        ratios,
        [
            "operating_profit_margin",
            "operating_margin"
        ]
    )

    rename_map = {}

    if roe is not None:
        rename_map[roe] = "roe_percentage"

    if roce is not None:
        rename_map[roce] = "roce_percentage"

    if net_margin is not None:
        rename_map[
            net_margin
        ] = "net_profit_margin"

    if operating_margin is not None:
        rename_map[
            operating_margin
        ] = "operating_profit_margin"

    ratios = ratios.rename(
        columns=rename_map
    )

    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    numeric_columns = [
        "roe_percentage",
        "roce_percentage",
        "net_profit_margin",
        "operating_profit_margin"
    ]

    for column in numeric_columns:

        if column in ratios.columns:

            ratios[column] = clean_numeric(
                ratios[column]
            )

    # --------------------------------------------------------
    # Keep latest row per company if year exists
    # --------------------------------------------------------

    if "year" in ratios.columns:

        ratios["year"] = pd.to_numeric(
            ratios["year"],
            errors="coerce"
        )

        ratios = (
            ratios
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )

    else:

        ratios = ratios.drop_duplicates(
            subset=["company_id"],
            keep="last"
        )

    return ratios


# ============================================================
# MERGE DATA
# ============================================================

def merge_data(
    companies,
    sectors,
    ratios
):

    print("\n" + "=" * 70)
    print("MERGING COMPANY + SECTOR + RATIO DATA")
    print("=" * 70)

    # --------------------------------------------------------
    # Company + sector
    # --------------------------------------------------------

    merged = companies.merge(
        sectors,
        on="company_id",
        how="left"
    )

    print(
        f"\nCompanies: {len(companies)}"
    )

    print(
        f"After sector merge: {len(merged)}"
    )

    # --------------------------------------------------------
    # Ratio merge
    # --------------------------------------------------------

    if ratios is not None:

        ratio_columns = [
            "company_id",
            "roe_percentage",
            "roce_percentage",
            "net_profit_margin",
            "operating_profit_margin"
        ]

        available = [
            column
            for column in ratio_columns
            if column in ratios.columns
        ]

        ratio_subset = ratios[
            available
        ].copy()

        merged = merged.merge(
            ratio_subset,
            on="company_id",
            how="left"
        )

        print(
            f"After ratio merge: {len(merged)}"
        )

    return merged


# ============================================================
# SECTOR STATISTICS
# ============================================================

def calculate_sector_statistics(df):

    print("\n" + "=" * 70)
    print("CALCULATING SECTOR STATISTICS")
    print("=" * 70)

    if "sector" not in df.columns:

        raise ValueError(
            "Sector column is missing after merge."
        )

    # --------------------------------------------------------
    # Count companies
    # --------------------------------------------------------

    aggregation = {
        "company_id": "nunique"
    }

    # --------------------------------------------------------
    # Financial metrics
    # --------------------------------------------------------

    if "roe_percentage" in df.columns:

        aggregation[
            "roe_percentage"
        ] = "mean"

    if "roce_percentage" in df.columns:

        aggregation[
            "roce_percentage"
        ] = "mean"

    if "net_profit_margin" in df.columns:

        aggregation[
            "net_profit_margin"
        ] = "mean"

    if "operating_profit_margin" in df.columns:

        aggregation[
            "operating_profit_margin"
        ] = "mean"

    sector_df = (
        df
        .groupby("sector")
        .agg(aggregation)
        .reset_index()
    )

    sector_df = sector_df.rename(
        columns={
            "company_id": "company_count"
        }
    )

    # --------------------------------------------------------
    # Round metrics
    # --------------------------------------------------------

    numeric_columns = [
        "roe_percentage",
        "roce_percentage",
        "net_profit_margin",
        "operating_profit_margin"
    ]

    for column in numeric_columns:

        if column in sector_df.columns:

            sector_df[column] = (
                sector_df[column]
                .round(2)
            )

    # --------------------------------------------------------
    # Sector rating
    # --------------------------------------------------------

    if "roe_percentage" in sector_df.columns:

        sector_df[
            "sector_rating"
        ] = (
            sector_df[
                "roe_percentage"
            ]
            .apply(sector_rating)
        )

    else:

        sector_df[
            "sector_rating"
        ] = "Not Available"

    # --------------------------------------------------------
    # Sector score
    # --------------------------------------------------------

    score_columns = [
        column
        for column in [
            "roe_percentage",
            "roce_percentage",
            "net_profit_margin",
            "operating_profit_margin"
        ]
        if column in sector_df.columns
    ]

    if score_columns:

        sector_df[
            "sector_score"
        ] = (
            sector_df[
                score_columns
            ]
            .mean(axis=1)
            .round(2)
        )

    else:

        sector_df[
            "sector_score"
        ] = None

    # --------------------------------------------------------
    # Sector rank
    # --------------------------------------------------------

    sector_df[
        "sector_rank"
    ] = (
        sector_df[
            "sector_score"
        ]
        .rank(
            ascending=False,
            method="min"
        )
    )

    sector_df[
        "sector_rank"
    ] = (
        sector_df[
            "sector_rank"
        ]
        .astype("Int64")
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    sector_df = (
        sector_df
        .sort_values(
            by="sector_score",
            ascending=False,
            na_position="last"
        )
        .reset_index(drop=True)
    )

    return sector_df


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(sector_df):

    print("\n")
    print("=" * 70)
    print("SECTOR ANALYSIS RESULTS")
    print("=" * 70)

    if sector_df.empty:

        print(
            "\nNo sector records found."
        )

        return

    print(
        sector_df.to_string(
            index=False
        )
    )

    print("\n")
    print("=" * 70)
    print("TOP SECTORS")
    print("=" * 70)

    top_columns = [
        "sector",
        "company_count",
        "roe_percentage",
        "roce_percentage",
        "sector_score",
        "sector_rating",
        "sector_rank"
    ]

    available = [
        column
        for column in top_columns
        if column in sector_df.columns
    ]

    print(
        sector_df[
            available
        ]
        .head(10)
        .to_string(index=False)
    )


# ============================================================
# SAVE
# ============================================================

def save_output(sector_df):

    sector_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n")
    print("=" * 70)
    print("OUTPUT GENERATED")
    print("=" * 70)

    print(
        f"\nFile:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        f"\nRows generated: "
        f"{len(sector_df)}"
    )


# ============================================================
# MAIN
# ============================================================

def run_sector_analysis():

    print("\n")
    print("=" * 70)
    print("N100 FINANCIAL INTELLIGENCE PLATFORM")
    print("SECTOR ANALYTICS")
    print("=" * 70)

    try:

        # STEP 1
        companies = load_companies()

        companies = prepare_companies(
            companies
        )

        # STEP 2
        sectors = load_sectors()

        sectors = prepare_sectors(
            sectors
        )

        # STEP 3
        ratios = load_ratios()

        ratios = prepare_ratios(
            ratios
        )

        # STEP 4
        merged = merge_data(
            companies,
            sectors,
            ratios
        )

        # STEP 5
        sector_df = (
            calculate_sector_statistics(
                merged
            )
        )

        # STEP 6
        print_results(
            sector_df
        )

        # STEP 7
        save_output(
            sector_df
        )

        print("\n")
        print("=" * 70)
        print(
            "SECTOR ANALYSIS COMPLETED SUCCESSFULLY"
        )
        print("=" * 70)

        return sector_df

    except Exception as error:

        print("\n")
        print("=" * 70)
        print("SECTOR ANALYSIS FAILED")
        print("=" * 70)

        print(
            f"\nError: {error}"
        )

        raise


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_sector_analysis()