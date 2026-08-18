import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
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

REPORTS_DIR = os.path.join(
    PROJECT_ROOT,
    "src",
    "reports"
)

RADAR_DIR = os.path.join(
    REPORTS_DIR,
    "radar_charts"
)

os.makedirs(
    RADAR_DIR,
    exist_ok=True
)


# ============================================================
# INPUT FILES
# ============================================================

RATIO_FILE = os.path.join(
    OUTPUT_DIR,
    "ratio_analysis.csv"
)

COMPANIES_FILE = os.path.join(
    DATA_DIR,
    "companies.xlsx"
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def find_column(df, possible_names):
    """
    Find a dataframe column using multiple possible names.
    """

    normalized = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        key = name.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


def safe_filename(name):
    """
    Convert company name into a safe filename.
    """

    name = str(name).strip()

    name = re.sub(
        r'[<>:"/\\|?*]',
        "",
        name
    )

    name = re.sub(
        r"\s+",
        "_",
        name
    )

    return name


def clean_numeric(value):
    """
    Convert value to a safe numeric value.
    Invalid, NaN and infinity values become 0.
    """

    try:

        value = float(value)

        if not np.isfinite(value):
            return 0.0

        return value

    except (TypeError, ValueError):

        return 0.0


# ============================================================
# LOAD RATIO DATA
# ============================================================

def load_ratio_data():

    if not os.path.exists(RATIO_FILE):

        raise FileNotFoundError(
            "\nRatio file not found:\n"
            f"{RATIO_FILE}\n\n"
            "Run the ratio analysis first."
        )

    df = pd.read_csv(
        RATIO_FILE
    )

    if df.empty:

        raise ValueError(
            "ratio_analysis.csv is empty."
        )

    print(
        f"Ratio records loaded: {len(df)}"
    )

    print(
        "Ratio columns:"
    )

    print(
        list(df.columns)
    )

    return df


# ============================================================
# LOAD COMPANY DATA
# ============================================================

def load_company_data():

    if not os.path.exists(COMPANIES_FILE):

        raise FileNotFoundError(
            "\nCompanies file not found:\n"
            f"{COMPANIES_FILE}"
        )

    # Your project uses header=1 for the Excel files.
    df = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )

    if df.empty:

        raise ValueError(
            "companies.xlsx is empty."
        )

    print(
        f"\nCompany records loaded: {len(df)}"
    )

    print(
        "Company columns:"
    )

    print(
        list(df.columns)
    )

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(
    ratio_df,
    company_df
):

    # --------------------------------------------------------
    # Find company ID columns
    # --------------------------------------------------------

    ratio_id = find_column(
        ratio_df,
        [
            "company_id",
            "company id",
            "id"
        ]
    )

    company_id = find_column(
        company_df,
        [
            "company_id",
            "company id",
            "id"
        ]
    )

    if ratio_id is None:

        raise ValueError(
            "Could not find company_id in ratio_analysis.csv"
        )

    if company_id is None:

        raise ValueError(
            "Could not find company_id in companies.xlsx"
        )

    # --------------------------------------------------------
    # Find company name column
    # --------------------------------------------------------

    company_name = find_column(
        company_df,
        [
            "company_name",
            "company name",
            "name"
        ]
    )

    if company_name is None:

        raise ValueError(
            "Could not find company_name in companies.xlsx"
        )

    # --------------------------------------------------------
    # Rename important columns
    # --------------------------------------------------------

    company_df = company_df.rename(
        columns={
            company_id: "company_id",
            company_name: "company_name"
        }
    )

    ratio_df = ratio_df.rename(
        columns={
            ratio_id: "company_id"
        }
    )

    # --------------------------------------------------------
    # Normalize IDs
    # --------------------------------------------------------

    ratio_df["company_id"] = (
        ratio_df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    company_df["company_id"] = (
        company_df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # --------------------------------------------------------
    # Locate ROE column
    # --------------------------------------------------------

    roe_column = find_column(
        ratio_df,
        [
            "roe_percentage",
            "roe_pct",
            "roe"
        ]
    )

    # --------------------------------------------------------
    # Locate ROCE column
    # --------------------------------------------------------

    roce_column = find_column(
        ratio_df,
        [
            "roce_percentage",
            "roce_pct",
            "roce"
        ]
    )

    if roe_column is None:

        raise ValueError(
            "ROE column not found in ratio_analysis.csv"
        )

    if roce_column is None:

        raise ValueError(
            "ROCE column not found in ratio_analysis.csv"
        )

    # --------------------------------------------------------
    # Rename metrics
    # --------------------------------------------------------

    ratio_df = ratio_df.rename(
        columns={
            roe_column: "roe_percentage",
            roce_column: "roce_percentage"
        }
    )

    # --------------------------------------------------------
    # Convert year to sortable text/value
    # --------------------------------------------------------

    if "year" in ratio_df.columns:

        ratio_df["_year_sort"] = (
            ratio_df["year"]
            .astype(str)
        )

    else:

        ratio_df["_year_sort"] = ""

    # --------------------------------------------------------
    # Convert metrics to numeric
    # --------------------------------------------------------

    ratio_df["roe_percentage"] = pd.to_numeric(
        ratio_df["roe_percentage"],
        errors="coerce"
    )

    ratio_df["roce_percentage"] = pd.to_numeric(
        ratio_df["roce_percentage"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Keep latest record for each company
    # --------------------------------------------------------

    ratio_df = ratio_df.sort_values(
        [
            "company_id",
            "_year_sort"
        ]
    )

    ratio_latest = (
        ratio_df
        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )
    )

    # --------------------------------------------------------
    # Merge company names + latest ratios
    # --------------------------------------------------------

    merged = pd.merge(
        company_df[
            [
                "company_id",
                "company_name"
            ]
        ],
        ratio_latest[
            [
                "company_id",
                "roe_percentage",
                "roce_percentage"
            ]
        ],
        on="company_id",
        how="inner"
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    merged = merged.drop_duplicates(
        subset=["company_id"]
    )

    return merged


# ============================================================
# GENERATE ONE RADAR CHART
# ============================================================

def radar_chart(
    company_name,
    roe,
    roce
):

    metrics = [
        "ROE",
        "ROCE"
    ]

    values = [
        clean_numeric(roe),
        clean_numeric(roce)
    ]

    # --------------------------------------------------------
    # Close radar polygon
    # --------------------------------------------------------

    values += values[:1]

    # --------------------------------------------------------
    # Angles
    # --------------------------------------------------------

    angles = np.linspace(
        0,
        2 * np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = plt.figure(
        figsize=(6, 6)
    )

    ax = plt.subplot(
        111,
        polar=True
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        metrics
    )

    ax.set_title(
        company_name,
        pad=20
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    filename = (
        safe_filename(company_name)
        + "_radar.png"
    )

    filepath = os.path.join(
        RADAR_DIR,
        filename
    )

    plt.tight_layout()

    plt.savefig(
        filepath,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(
        fig
    )

    return filepath


# ============================================================
# GENERATE ALL RADAR CHARTS
# ============================================================

def generate_all_radar_charts():

    print("\n" + "=" * 70)
    print("GENERATING RADAR CHARTS")
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    ratio_df = load_ratio_data()

    company_df = load_company_data()

    # --------------------------------------------------------
    # Prepare
    # --------------------------------------------------------

    data = prepare_data(
        ratio_df,
        company_df
    )

    print(
        f"\nCompanies available for radar charts: "
        f"{len(data)}"
    )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    generated = 0

    failed = []

    for _, row in data.iterrows():

        company_name = str(
            row["company_name"]
        ).strip()

        try:

            filepath = radar_chart(
                company_name,
                row["roe_percentage"],
                row["roce_percentage"]
            )

            generated += 1

            print(
                f"[{generated}/{len(data)}] "
                f"Created: {os.path.basename(filepath)}"
            )

        except Exception as error:

            failed.append(
                (
                    company_name,
                    str(error)
                )
            )

            print(
                f"FAILED: {company_name}"
            )

            print(
                f"ERROR: {error}"
            )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RADAR CHART GENERATION COMPLETE")
    print("=" * 70)

    print(
        f"\nCharts generated: {generated}"
    )

    print(
        f"Charts failed: {len(failed)}"
    )

    print(
        f"Output directory:\n{RADAR_DIR}"
    )

    # --------------------------------------------------------
    # Failed companies
    # --------------------------------------------------------

    if failed:

        print(
            "\nFailed companies:"
        )

        for company_name, error in failed:

            print(
                f"  - {company_name}: {error}"
            )

    # --------------------------------------------------------
    # Expected count
    # --------------------------------------------------------

    if generated == 92:

        print(
            "\nSUCCESS: All 92 required radar charts "
            "were generated."
        )

    elif generated < 92:

        print(
            "\nWARNING: Fewer than 92 radar charts "
            "were generated."
        )

    else:

        print(
            "\nWARNING: More than 92 radar charts "
            "were generated."
        )

    return generated


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    generate_all_radar_charts()