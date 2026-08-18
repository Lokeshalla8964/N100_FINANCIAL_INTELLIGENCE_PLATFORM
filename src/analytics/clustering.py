# ============================================================
# N100 FINANCIAL INTELLIGENCE PLATFORM
# K-MEANS COMPANY CLUSTERING
# DAY 36
# ============================================================

import os
import sys
import re
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


# ============================================================
# 1. PATHS
# ============================================================

CURRENT_FILE = os.path.abspath(__file__)

SRC_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(CURRENT_FILE),
        ".."
    )
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        SRC_DIR,
        ".."
    )
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# 2. CONFIG
# ============================================================

from config.config import (
    ANALYSIS_FILE,
    BALANCE_SHEET_FILE,
    CASHFLOW_FILE,
    COMPANIES_FILE,
    DOCUMENTS_FILE,
    PROFIT_LOSS_FILE,
    PROS_CONS_FILE,
)


# ============================================================
# 3. OUTPUT DIRECTORIES
# ============================================================

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "output"
)

REPORTS_DIR = os.path.join(
    PROJECT_ROOT,
    "reports"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    REPORTS_DIR,
    exist_ok=True
)


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def clean_columns(df):
    """
    Normalize dataframe column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False
        )
        .str.replace(
            "-",
            "_",
            regex=False
        )
    )

    return df


def ensure_company_id(df):
    """
    Ensure company identifier is called company_id.
    """

    df = clean_columns(
        df
    )

    if (
        "company_id" not in df.columns
        and "id" in df.columns
    ):
        df = df.rename(
            columns={
                "id": "company_id"
            }
        )

    if "company_id" not in df.columns:

        for candidate in [
            "company",
            "companyid",
            "company_code",
            "code",
        ]:

            if candidate in df.columns:

                df = df.rename(
                    columns={
                        candidate: "company_id"
                    }
                )

                break

    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(
                r"\.0$",
                "",
                regex=True
            )
        )

        df.loc[
            df["company_id"].isin(
                [
                    "",
                    "NAN",
                    "NONE",
                    "NULL",
                ]
            ),
            "company_id"
        ] = np.nan

    return df


def parse_year(value):
    """
    Convert different year formats into an integer.
    """

    if pd.isna(value):
        return np.nan

    try:

        numeric = float(value)

        if 1900 <= numeric <= 2100:
            return int(numeric)

    except (
        ValueError,
        TypeError
    ):
        pass

    text = str(value)

    match = re.search(
        r"(19|20)\d{2}",
        text
    )

    if match:
        return int(
            match.group(0)
        )

    return np.nan


def normalize_year(df):
    """
    Normalize year values.
    """

    df = df.copy()

    if "year" in df.columns:

        df["year"] = (
            df["year"]
            .apply(parse_year)
        )

    return df


def clean_numeric(series):
    """
    Convert a pandas series to numeric values.
    """

    return pd.to_numeric(
        series
        .astype(str)
        .str.replace(
            ",",
            "",
            regex=False
        )
        .str.replace(
            "%",
            "",
            regex=False
        )
        .str.strip(),
        errors="coerce"
    )


def check_columns(
    df,
    required,
    name
):
    """
    Check that required columns exist.
    """

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"{name} is missing required columns: "
            f"{missing}"
        )


def calculate_cagr(
    start_value,
    end_value,
    years
):
    """
    Calculate standard CAGR percentage.
    """

    try:

        start_value = float(
            start_value
        )

        end_value = float(
            end_value
        )

        years = int(
            years
        )

    except (
        ValueError,
        TypeError
    ):

        return np.nan

    if years <= 0:
        return np.nan

    if pd.isna(start_value):
        return np.nan

    if pd.isna(end_value):
        return np.nan

    # Standard CAGR is not meaningful
    # when starting value is zero/negative.
    if start_value <= 0:
        return np.nan

    # Negative ending value is not supported
    # by standard CAGR.
    if end_value < 0:
        return np.nan

    return (
        (
            end_value / start_value
        ) ** (1 / years)
        - 1
    ) * 100


def calculate_company_cagr(
    df,
    value_column
):
    """
    Calculate approximately five-year CAGR for each company.
    """

    data = ensure_company_id(
        df.copy()
    )

    data = normalize_year(
        data
    )

    check_columns(
        data,
        [
            "company_id",
            "year",
            value_column,
        ],
        f"CAGR source ({value_column})"
    )

    data[value_column] = clean_numeric(
        data[value_column]
    )

    data = data.dropna(
        subset=[
            "company_id",
            "year",
        ]
    )

    results = []

    for company_id, group in data.groupby(
        "company_id"
    ):

        group = (
            group
            .sort_values(
                "year"
            )
            .copy()
        )

        if len(group) < 2:
            continue

        latest = group.iloc[-1]

        latest_year = int(
            latest["year"]
        )

        target_year = (
            latest_year - 5
        )

        group["distance"] = (
            group["year"]
            - target_year
        ).abs()

        previous = (
            group
            .sort_values(
                [
                    "distance",
                    "year",
                ]
            )
            .iloc[0]
        )

        start_year = int(
            previous["year"]
        )

        years = (
            latest_year
            - start_year
        )

        if years <= 0:
            continue

        cagr = calculate_cagr(
            previous[value_column],
            latest[value_column],
            years
        )

        results.append(
            {
                "company_id": company_id,
                f"{value_column}_cagr_5yr": cagr,
            }
        )

    return pd.DataFrame(
        results,
        columns=[
            "company_id",
            f"{value_column}_cagr_5yr",
        ]
    )


# ============================================================
# 5. LOAD DATA
# ============================================================

print()
print("=" * 70)
print("LOADING DATA")
print("=" * 70)


# ------------------------------------------------------------
# Analysis
# ------------------------------------------------------------

analysis = pd.read_excel(
    ANALYSIS_FILE
)

analysis = clean_columns(
    analysis
)


# ------------------------------------------------------------
# Balance Sheet
# ------------------------------------------------------------

balance_sheet = pd.read_excel(
    BALANCE_SHEET_FILE,
    header=1
)

balance_sheet = ensure_company_id(
    balance_sheet
)

balance_sheet = normalize_year(
    balance_sheet
)


# ------------------------------------------------------------
# Cash Flow
# ------------------------------------------------------------

cashflow = pd.read_excel(
    CASHFLOW_FILE,
    header=1
)

cashflow = ensure_company_id(
    cashflow
)

cashflow = normalize_year(
    cashflow
)


# ------------------------------------------------------------
# Companies MASTER DATASET
# ------------------------------------------------------------

companies = pd.read_excel(
    COMPANIES_FILE,
    header=1
)

companies = ensure_company_id(
    companies
)


# ------------------------------------------------------------
# Documents
# ------------------------------------------------------------

documents = pd.read_excel(
    DOCUMENTS_FILE
)

documents = clean_columns(
    documents
)


# ------------------------------------------------------------
# Profit & Loss
# ------------------------------------------------------------

profit_loss = pd.read_excel(
    PROFIT_LOSS_FILE,
    header=1
)

profit_loss = ensure_company_id(
    profit_loss
)

profit_loss = normalize_year(
    profit_loss
)


# ------------------------------------------------------------
# Pros & Cons
# ------------------------------------------------------------

pros_cons = pd.read_excel(
    PROS_CONS_FILE
)

pros_cons = clean_columns(
    pros_cons
)


print()
print("Datasets loaded successfully.")


# ============================================================
# 6. VALIDATE MASTER COMPANY LIST
# ============================================================

check_columns(
    companies,
    [
        "company_id",
    ],
    "Companies"
)


# Remove invalid IDs
companies = companies.dropna(
    subset=[
        "company_id"
    ]
).copy()


# Remove duplicate company IDs
companies = (
    companies
    .drop_duplicates(
        subset=[
            "company_id"
        ],
        keep="first"
    )
    .copy()
)


official_company_ids = (
    companies[
        "company_id"
    ]
    .astype(str)
    .str.strip()
    .str.upper()
)


official_company_ids = set(
    official_company_ids
)


print()
print("=" * 70)
print("OFFICIAL COMPANY MASTER CHECK")
print("=" * 70)

print(
    "Official companies:",
    len(official_company_ids)
)


if len(official_company_ids) != 92:

    raise ValueError(
        "Expected exactly 92 official companies "
        f"but found {len(official_company_ids)}."
    )


# ============================================================
# 7. COLUMN CHECKS
# ============================================================

check_columns(
    profit_loss,
    [
        "company_id",
        "year",
        "sales",
        "operating_profit",
        "net_profit",
    ],
    "Profit Loss"
)


check_columns(
    balance_sheet,
    [
        "company_id",
        "year",
        "equity_capital",
        "reserves",
        "borrowings",
        "total_assets",
    ],
    "Balance Sheet"
)


check_columns(
    cashflow,
    [
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    ],
    "Cash Flow"
)


# ============================================================
# 8. CLEAN NUMERIC COLUMNS
# ============================================================

profit_numeric = [
    "sales",
    "operating_profit",
    "net_profit",
]

for column in profit_numeric:

    profit_loss[column] = clean_numeric(
        profit_loss[column]
    )


balance_numeric = [
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets",
]

for column in balance_numeric:

    balance_sheet[column] = clean_numeric(
        balance_sheet[column]
    )


cashflow_numeric = [
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "net_cash_flow",
]

for column in cashflow_numeric:

    cashflow[column] = clean_numeric(
        cashflow[column]
    )


# ============================================================
# 9. REMOVE INVALID ROWS
# ============================================================

profit_loss = profit_loss.dropna(
    subset=[
        "company_id",
        "year",
    ]
).copy()


balance_sheet = balance_sheet.dropna(
    subset=[
        "company_id",
        "year",
    ]
).copy()


cashflow = cashflow.dropna(
    subset=[
        "company_id",
        "year",
    ]
).copy()


# ============================================================
# 10. CALCULATE OPERATING PROFIT MARGIN
# ============================================================

profit_loss[
    "operating_profit_margin_pct"
] = np.where(
    profit_loss["sales"] != 0,

    (
        profit_loss[
            "operating_profit"
        ]
        /
        profit_loss[
            "sales"
        ]
    ) * 100,

    np.nan
)


# ============================================================
# 11. CALCULATE FREE CASH FLOW
# ============================================================

cashflow[
    "free_cash_flow"
] = (
    cashflow[
        "operating_activity"
    ]
    +
    cashflow[
        "investing_activity"
    ]
)


# ============================================================
# 12. REVENUE CAGR
# ============================================================

print()
print("=" * 70)
print("CALCULATING REVENUE CAGR")
print("=" * 70)


revenue_cagr = calculate_company_cagr(
    profit_loss,
    "sales"
)


revenue_cagr = revenue_cagr.rename(
    columns={
        "sales_cagr_5yr":
        "revenue_cagr_5yr"
    }
)


print(
    "Revenue CAGR companies:",
    len(revenue_cagr)
)


# ============================================================
# 13. FCF CAGR
# ============================================================

print()
print("=" * 70)
print("CALCULATING FREE CASH FLOW CAGR")
print("=" * 70)


fcf_cagr = calculate_company_cagr(
    cashflow,
    "free_cash_flow"
)


fcf_cagr = fcf_cagr.rename(
    columns={
        "free_cash_flow_cagr_5yr":
        "fcf_cagr_5yr"
    }
)


print(
    "FCF CAGR companies:",
    len(fcf_cagr)
)


# ============================================================
# 14. LATEST PROFIT & LOSS RECORD
# ============================================================

profit_latest = (
    profit_loss
    .sort_values(
        "year"
    )
    .groupby(
        "company_id"
    )
    .tail(1)
    .copy()
)


profit_latest = ensure_company_id(
    profit_latest
)


# ============================================================
# 15. LATEST BALANCE SHEET RECORD
# ============================================================

balance_latest = (
    balance_sheet
    .sort_values(
        "year"
    )
    .groupby(
        "company_id"
    )
    .tail(1)
    .copy()
)


balance_latest = ensure_company_id(
    balance_latest
)


# ============================================================
# 16. LATEST CASH FLOW RECORD
# ============================================================

cashflow_latest = (
    cashflow
    .sort_values(
        "year"
    )
    .groupby(
        "company_id"
    )
    .tail(1)
    .copy()
)


cashflow_latest = ensure_company_id(
    cashflow_latest
)


# ============================================================
# 17. CALCULATE ROE AND DEBT/EQUITY
# ============================================================

profit_latest = profit_latest.merge(
    balance_latest[
        [
            "company_id",
            "equity_capital",
            "reserves",
            "borrowings",
            "total_assets",
        ]
    ],
    on="company_id",
    how="left"
)


# ------------------------------------------------------------
# Total Equity
# ------------------------------------------------------------

profit_latest[
    "total_equity"
] = (
    profit_latest[
        "equity_capital"
    ].fillna(0)
    +
    profit_latest[
        "reserves"
    ].fillna(0)
)


# ------------------------------------------------------------
# ROE
# ------------------------------------------------------------

profit_latest[
    "return_on_equity_pct"
] = np.where(

    profit_latest[
        "total_equity"
    ] > 0,

    (
        profit_latest[
            "net_profit"
        ]
        /
        profit_latest[
            "total_equity"
        ]
    ) * 100,

    np.nan
)


# ------------------------------------------------------------
# Debt / Equity
# ------------------------------------------------------------

profit_latest[
    "debt_to_equity"
] = np.where(

    profit_latest[
        "total_equity"
    ] > 0,

    (
        profit_latest[
            "borrowings"
        ].fillna(0)
        /
        profit_latest[
            "total_equity"
        ]
    ),

    np.nan
)


# ============================================================
# 18. BUILD FINANCIAL METRICS
# ============================================================

financial_metrics = profit_latest[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
    ]
].copy()


# ============================================================
# 19. MERGE CASH FLOW METRICS
# ============================================================

cash_selected = cashflow_latest[
    [
        "company_id",
        "free_cash_flow",
        "net_cash_flow",
    ]
].copy()


cash_selected = ensure_company_id(
    cash_selected
)


financial_metrics = pd.merge(
    financial_metrics,
    cash_selected,
    on="company_id",
    how="left"
)


# ============================================================
# 20. MERGE REVENUE CAGR
# ============================================================

revenue_cagr = ensure_company_id(
    revenue_cagr
)


if "revenue_cagr_5yr" not in revenue_cagr.columns:

    revenue_cagr[
        "revenue_cagr_5yr"
    ] = np.nan


financial_metrics = pd.merge(
    financial_metrics,
    revenue_cagr[
        [
            "company_id",
            "revenue_cagr_5yr",
        ]
    ],
    on="company_id",
    how="left"
)


# ============================================================
# 21. MERGE FCF CAGR
# ============================================================

fcf_cagr = ensure_company_id(
    fcf_cagr
)


if "fcf_cagr_5yr" not in fcf_cagr.columns:

    fcf_cagr[
        "fcf_cagr_5yr"
    ] = np.nan


financial_metrics = pd.merge(
    financial_metrics,
    fcf_cagr[
        [
            "company_id",
            "fcf_cagr_5yr",
        ]
    ],
    on="company_id",
    how="left"
)


# ============================================================
# 22. COMPANY INFORMATION
# ============================================================

company_columns = [
    "company_id"
]


if "company_name" in companies.columns:

    company_columns.append(
        "company_name"
    )


if "broad_sector" in companies.columns:

    company_columns.append(
        "broad_sector"
    )


company_info = (
    companies[
        company_columns
    ]
    .drop_duplicates(
        "company_id"
    )
    .copy()
)


# ============================================================
# 23. IMPORTANT:
# USE COMPANIES MASTER AS THE BASE
# ============================================================

cluster_data = company_info.merge(
    financial_metrics,
    on="company_id",
    how="left"
)


# ============================================================
# 24. VERIFY EXACTLY 92 COMPANIES
# ============================================================

print()
print("=" * 70)
print("OFFICIAL COMPANY FILTER")
print("=" * 70)


print(
    "Company master rows:",
    len(company_info)
)


print(
    "Cluster data rows:",
    len(cluster_data)
)


print(
    "Unique company IDs:",
    cluster_data[
        "company_id"
    ].nunique()
)


if len(cluster_data) != 92:

    raise ValueError(
        "Cluster data does not contain exactly 92 companies."
    )


if (
    cluster_data[
        "company_id"
    ].nunique()
    != 92
):

    raise ValueError(
        "Cluster data contains duplicate company IDs."
    )


# ============================================================
# 25. SECTOR
# ============================================================

if "broad_sector" not in cluster_data.columns:

    cluster_data[
        "broad_sector"
    ] = "Unknown"

else:

    cluster_data[
        "broad_sector"
    ] = (
        cluster_data[
            "broad_sector"
        ]
        .fillna(
            "Unknown"
        )
        .astype(str)
        .str.strip()
    )


# ============================================================
# 26. REQUIRED CLUSTERING FEATURES
# ============================================================

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


print()
print("=" * 70)
print("CLUSTERING FEATURES")
print("=" * 70)


for feature in features:

    print(
        feature
    )


# ============================================================
# 27. CLEAN FEATURE VALUES
# ============================================================

for feature in features:

    cluster_data[
        feature
    ] = clean_numeric(
        cluster_data[
            feature
        ]
    )


cluster_data = cluster_data.replace(
    [
        np.inf,
        -np.inf,
    ],
    np.nan
)


# ============================================================
# 28. MISSING VALUES BEFORE IMPUTATION
# ============================================================

print()
print("=" * 70)
print("MISSING VALUES BEFORE IMPUTATION")
print("=" * 70)


print(
    cluster_data[
        features
    ].isna().sum()
)


# ============================================================
# 29. SECTOR-MEDIAN IMPUTATION
# ============================================================

print()
print("=" * 70)
print("SECTOR-MEDIAN IMPUTATION")
print("=" * 70)


for feature in features:

    sector_median = (
        cluster_data
        .groupby(
            "broad_sector"
        )[feature]
        .transform(
            "median"
        )
    )

    cluster_data[
        feature
    ] = (
        cluster_data[
            feature
        ]
        .fillna(
            sector_median
        )
    )

    # Overall median fallback
    overall_median = (
        cluster_data[
            feature
        ]
        .median()
    )

    if pd.isna(
        overall_median
    ):

        overall_median = 0.0

    cluster_data[
        feature
    ] = (
        cluster_data[
            feature
        ]
        .fillna(
            overall_median
        )
    )


# ============================================================
# 30. FINAL MISSING VALUE CHECK
# ============================================================

print()
print("=" * 70)
print("MISSING VALUES AFTER IMPUTATION")
print("=" * 70)


missing_after = (
    cluster_data[
        features
    ].isna().sum()
)


print(
    missing_after
)


if missing_after.sum() > 0:

    raise ValueError(
        "Missing values still exist after imputation."
    )


# ============================================================
# 31. STANDARD SCALER
# ============================================================

print()
print("=" * 70)
print("STANDARD SCALING")
print("=" * 70)


X = cluster_data[
    features
].copy()


scaler = StandardScaler()


X_scaled = scaler.fit_transform(
    X
)


print(
    "Scaling completed."
)


# ============================================================
# 32. ELBOW PLOT
# ============================================================

print()
print("=" * 70)
print("GENERATING ELBOW PLOT")
print("=" * 70)


inertias = []

k_values = range(
    2,
    11
)


for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(
        X_scaled
    )

    inertias.append(
        model.inertia_
    )


plt.figure(
    figsize=(9, 6)
)


plt.plot(
    list(k_values),
    inertias,
    marker="o"
)


plt.xlabel(
    "Number of Clusters (k)"
)


plt.ylabel(
    "Inertia"
)


plt.title(
    "K-Means Elbow Plot"
)


plt.xticks(
    list(k_values)
)


plt.grid(
    True
)


elbow_path = os.path.join(
    REPORTS_DIR,
    "elbow_plot.png"
)


plt.savefig(
    elbow_path,
    dpi=200,
    bbox_inches="tight"
)


plt.close()


print(
    "Saved:",
    elbow_path
)


# ============================================================
# 33. RUN K-MEANS
# ============================================================

N_CLUSTERS = 5


print()
print("=" * 70)
print("RUNNING K-MEANS")
print("=" * 70)


kmeans = KMeans(
    n_clusters=N_CLUSTERS,
    random_state=42,
    n_init=10
)


cluster_data[
    "cluster_id"
] = kmeans.fit_predict(
    X_scaled
)


# ============================================================
# 34. DISTANCE FROM CENTROID
# ============================================================

distances = kmeans.transform(
    X_scaled
)


cluster_data[
    "distance_from_centroid"
] = [
    distances[
        i,
        int(
            cluster_data.iloc[
                i
            ][
                "cluster_id"
            ]
        )
    ]
    for i in range(
        len(cluster_data)
    )
]


# ============================================================
# 35. CLUSTER NAMES
# ============================================================

cluster_names = {
    0: "High-Quality Compounders",
    1: "Defensive Dividend Payers",
    2: "Value Cyclicals",
    3: "Distressed or Turnaround",
    4: "Emerging Growth",
}


cluster_data[
    "cluster_name"
] = (
    cluster_data[
        "cluster_id"
    ].map(
        cluster_names
    )
)


# ============================================================
# 36. VERIFY CLUSTER ASSIGNMENTS
# ============================================================

print()
print("=" * 70)
print("CLUSTER ASSIGNMENT CHECK")
print("=" * 70)


print(
    "Total companies:",
    len(cluster_data)
)


print(
    "Unique company IDs:",
    cluster_data[
        "company_id"
    ].nunique()
)


print(
    "Unique cluster IDs:",
    cluster_data[
        "cluster_id"
    ].nunique()
)


print()
print(
    "Cluster counts:"
)


print(
    cluster_data[
        "cluster_name"
    ].value_counts()
)


if len(cluster_data) != 92:

    raise ValueError(
        "Final clustering output does not contain 92 companies."
    )


if (
    cluster_data[
        "company_id"
    ].nunique()
    != 92
):

    raise ValueError(
        "Final clustering output contains duplicate IDs."
    )


if (
    cluster_data[
        "cluster_id"
    ].isna().any()
):

    raise ValueError(
        "Some companies do not have a cluster assignment."
    )


# ============================================================
# 37. CLUSTER STATISTICS
# ============================================================

summary = (
    cluster_data
    .groupby(
        [
            "cluster_id",
            "cluster_name",
        ]
    )[
        features
    ]
    .agg(
        [
            "mean",
            "median",
        ]
    )
)


# ============================================================
# 38. SAVE CLUSTER LABELS
# ============================================================

cluster_labels_path = os.path.join(
    OUTPUT_DIR,
    "cluster_labels.csv"
)


cluster_data[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]
].to_csv(
    cluster_labels_path,
    index=False
)


# ============================================================
# 39. SAVE CLUSTER STATISTICS
# ============================================================

cluster_stats_path = os.path.join(
    OUTPUT_DIR,
    "cluster_statistics.csv"
)


summary.to_csv(
    cluster_stats_path
)


# ============================================================
# 40. FINAL FILE VALIDATION
# ============================================================

saved_labels = pd.read_csv(
    cluster_labels_path
)


print()
print("=" * 70)
print("FINAL OUTPUT VALIDATION")
print("=" * 70)


print(
    "cluster_labels.csv rows:",
    len(saved_labels)
)


print(
    "cluster_labels.csv unique IDs:",
    saved_labels[
        "company_id"
    ].nunique()
)


print(
    "Cluster IDs:",
    sorted(
        saved_labels[
            "cluster_id"
        ].unique()
    )
)


# Check exact 92
if len(saved_labels) != 92:

    raise ValueError(
        "ERROR: cluster_labels.csv does not contain exactly 92 rows."
    )


# Check unique IDs
if (
    saved_labels[
        "company_id"
    ].nunique()
    != 92
):

    raise ValueError(
        "ERROR: cluster_labels.csv contains duplicate company IDs."
    )


# Check all 5 clusters
if set(
    saved_labels[
        "cluster_id"
    ].unique()
) != {0, 1, 2, 3, 4}:

    raise ValueError(
        "ERROR: Expected cluster IDs 0, 1, 2, 3, 4."
    )


# Check no missing assignments
if saved_labels[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]
].isna().any().any():

    raise ValueError(
        "ERROR: Missing values exist in final cluster labels."
    )


# ============================================================
# 41. PRINT FINAL RESULTS
# ============================================================

print()
print("=" * 70)
print("K-MEANS CLUSTERING COMPLETED SUCCESSFULLY")
print("=" * 70)


print()
print(
    "Companies clustered:",
    len(saved_labels)
)


print(
    "Unique companies:",
    saved_labels[
        "company_id"
    ].nunique()
)


print(
    "Number of clusters:",
    saved_labels[
        "cluster_id"
    ].nunique()
)


print()
print(
    "Cluster counts:"
)


print(
    saved_labels[
        "cluster_name"
    ].value_counts()
)


print()
print(
    "OUTPUT FILES:"
)


print(
    "output/cluster_labels.csv"
)


print(
    "output/cluster_statistics.csv"
)


print(
    "reports/elbow_plot.png"
)


print()
print(
    "CLUSTER NAMES:"
)


for cluster_id, name in cluster_names.items():

    print(
        f"Cluster {cluster_id}: {name}"
    )


print()
print("=" * 70)
print("DAY 36 COMPLETE")
print("=" * 70)
