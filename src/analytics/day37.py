"""
DAY 37 - CLUSTER PROFILING & STATISTICS
N100 Financial Intelligence Platform

Outputs:
1. Cluster profiling statistics
2. Correlation heatmap
3. Outlier report
4. Portfolio statistics
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "raw" / "companies.xlsx"
CLUSTER_FILE = PROJECT_ROOT / "output" / "cluster_labels.csv"

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("DAY 37 - CLUSTER PROFILING & STATISTICS")
print("=" * 70)

print("\nLoading company data...")

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Companies file not found:\n{DATA_FILE}"
    )

if not CLUSTER_FILE.exists():
    raise FileNotFoundError(
        f"Cluster labels file not found:\n{CLUSTER_FILE}"
    )


# Read Excel
excel_file = pd.ExcelFile(DATA_FILE)

print(f"\nExcel sheets found: {excel_file.sheet_names}")

# Prefer Companies sheet
if "Companies" in excel_file.sheet_names:
    companies = pd.read_excel(DATA_FILE, sheet_name="Companies")
else:
    companies = pd.read_excel(DATA_FILE, sheet_name=excel_file.sheet_names[0])


# Read cluster output
clusters = pd.read_csv(CLUSTER_FILE)


print(f"\nCompanies loaded: {len(companies)}")
print(f"Cluster rows loaded: {len(clusters)}")


# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

companies.columns = (
    companies.columns
    .astype(str)
    .str.strip()
)

clusters.columns = (
    clusters.columns
    .astype(str)
    .str.strip()
)


print("\nCompany columns:")
print(list(companies.columns))

print("\nCluster columns:")
print(list(clusters.columns))


# ============================================================
# 4. STANDARDIZE COMPANY ID
# ============================================================

def find_column(df, candidates):
    """
    Find the first matching column from a list of candidates.
    Matching is case-insensitive.
    """

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:
        key = candidate.lower()

        if key in normalized:
            return normalized[key]

    return None


company_id_companies = find_column(
    companies,
    [
        "company_id",
        "company id",
        "id"
    ]
)

company_id_clusters = find_column(
    clusters,
    [
        "company_id",
        "company id",
        "id"
    ]
)


if company_id_companies is None:
    raise KeyError(
        "Could not find company_id in companies.xlsx"
    )

if company_id_clusters is None:
    raise KeyError(
        "Could not find company_id in cluster_labels.csv"
    )


companies = companies.rename(
    columns={company_id_companies: "company_id"}
)

clusters = clusters.rename(
    columns={company_id_clusters: "company_id"}
)


companies["company_id"] = (
    companies["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

clusters["company_id"] = (
    clusters["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ============================================================
# 5. REMOVE DUPLICATE COMPANY IDS
# ============================================================

companies = companies.drop_duplicates(
    subset=["company_id"],
    keep="first"
)

clusters = clusters.drop_duplicates(
    subset=["company_id"],
    keep="first"
)


print("\nUnique companies:", companies["company_id"].nunique())
print("Unique clustered companies:", clusters["company_id"].nunique())


# ============================================================
# 6. MERGE CLUSTER INFORMATION
# ============================================================

cluster_columns = [
    col for col in [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
    if col in clusters.columns
]

cluster_data = clusters[cluster_columns].copy()

df = companies.merge(
    cluster_data,
    on="company_id",
    how="inner"
)


print("\nMerged dataset:")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 7. CHECK CLUSTER DISTRIBUTION
# ============================================================

if "cluster_id" not in df.columns:
    raise KeyError(
        "cluster_id is missing from cluster_labels.csv"
    )

print("\n" + "=" * 70)
print("CLUSTER DISTRIBUTION")
print("=" * 70)

cluster_counts = (
    df.groupby(
        ["cluster_id", "cluster_name"],
        dropna=False
    )
    .size()
    .reset_index(name="company_count")
)

print(cluster_counts.to_string(index=False))


# ============================================================
# 8. IDENTIFY BROAD SECTOR
# ============================================================

sector_column = find_column(
    df,
    [
        "broad_sector",
        "broad sector",
        "sector"
    ]
)

if sector_column is not None:
    if sector_column != "broad_sector":
        df = df.rename(
            columns={sector_column: "broad_sector"}
        )

    df["broad_sector"] = (
        df["broad_sector"]
        .astype(str)
        .str.strip()
    )

    print("\nBroad sector column:", "broad_sector")

else:
    print(
        "\nWARNING: broad_sector column not found."
    )


# ============================================================
# 9. CONVERT NUMERIC COLUMNS
# ============================================================

for column in df.columns:

    if column in [
        "company_id",
        "company_name",
        "cluster_name",
        "broad_sector"
    ]:
        continue

    # Try numeric conversion
    converted = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    # Keep numeric conversion if it contains useful values
    if converted.notna().sum() > 0:
        df[column] = converted


# ============================================================
# 10. IDENTIFY FINANCIAL KPI COLUMNS
# ============================================================

# Columns that should NOT be treated as KPIs
EXCLUDED_COLUMNS = {
    "company_id",
    "company_name",
    "cluster_id",
    "cluster_name",
    "distance_from_centroid",
    "broad_sector",
    "sector",
    "industry"
}


numeric_columns = df.select_dtypes(
    include=[np.number]
).columns.tolist()


candidate_kpis = [
    col for col in numeric_columns
    if col not in EXCLUDED_COLUMNS
]


print("\nNumeric KPI candidates:")
for col in candidate_kpis:
    print(" -", col)


# ============================================================
# 11. CLUSTER PROFILE
# ============================================================

print("\n" + "=" * 70)
print("CLUSTER PROFILING")
print("=" * 70)


# Use financial numeric variables for profiling.
# Exclude cluster_id and distance.
profile_columns = [
    col for col in candidate_kpis
    if col != "cluster_id"
    and col != "distance_from_centroid"
]


if not profile_columns:
    raise ValueError(
        "No numeric financial columns found for cluster profiling."
    )


# Mean
cluster_mean = (
    df.groupby(
        ["cluster_id", "cluster_name"],
        dropna=False
    )[profile_columns]
    .mean()
    .round(4)
)


# Median
cluster_median = (
    df.groupby(
        ["cluster_id", "cluster_name"],
        dropna=False
    )[profile_columns]
    .median()
    .round(4)
)


# Save mean profile
mean_file = OUTPUT_DIR / "cluster_profile_mean.csv"

cluster_mean.to_csv(mean_file)


# Save median profile
median_file = OUTPUT_DIR / "cluster_profile_median.csv"

cluster_median.to_csv(median_file)


print("\nCluster mean profile:")
print(cluster_mean.to_string())


print("\nCluster median profile:")
print(cluster_median.to_string())


# ============================================================
# 12. CLUSTER PROFILE COMBINED FILE
# ============================================================

combined_profile = []

for index, row in cluster_mean.reset_index().iterrows():

    cluster_id = row["cluster_id"]
    cluster_name = row["cluster_name"]

    company_count = len(
        df[df["cluster_id"] == cluster_id]
    )

    result = {
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "company_count": company_count
    }

    for column in profile_columns:
        result[f"{column}_mean"] = row[column]

    median_row = cluster_median.reset_index()

    median_match = median_row[
        median_row["cluster_id"] == cluster_id
    ]

    if not median_match.empty:

        median_values = median_match.iloc[0]

        for column in profile_columns:
            result[f"{column}_median"] = (
                median_values[column]
            )

    combined_profile.append(result)


combined_profile_df = pd.DataFrame(
    combined_profile
)

combined_profile_file = (
    OUTPUT_DIR / "cluster_profile.csv"
)

combined_profile_df.to_csv(
    combined_profile_file,
    index=False
)


print(
    f"\nSaved cluster profile:\n"
    f"{combined_profile_file}"
)


# ============================================================
# 13. CORRELATION HEATMAP
# ============================================================

print("\n" + "=" * 70)
print("CORRELATION HEATMAP")
print("=" * 70)


# Use financial numeric variables only
correlation_columns = [
    col for col in candidate_kpis
    if col != "cluster_id"
    and col != "distance_from_centroid"
]


correlation_df = df[
    correlation_columns
].copy()


# Remove columns containing no usable data
correlation_df = correlation_df.dropna(
    axis=1,
    how="all"
)


# Pearson correlation
correlation_matrix = correlation_df.corr(
    method="pearson"
)


correlation_file = (
    OUTPUT_DIR / "correlation_matrix.csv"
)

correlation_matrix.to_csv(
    correlation_file
)


# Create heatmap
plt.figure(
    figsize=(14, 11)
)

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    square=False,
    linewidths=0.5,
    cbar=True
)

plt.title(
    "Financial KPI Correlation Heatmap",
    fontsize=16,
    pad=15
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.yticks(
    rotation=0
)

plt.tight_layout()


heatmap_file = (
    REPORT_DIR / "correlation_heatmap.png"
)

plt.savefig(
    heatmap_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print(
    f"Correlation heatmap saved:\n"
    f"{heatmap_file}"
)


# ============================================================
# 14. OUTLIER DETECTION
# ============================================================

print("\n" + "=" * 70)
print("OUTLIER DETECTION")
print("=" * 70)


def calculate_zscore(series):

    """
    Calculate Z-score.

    Uses sample standard deviation.
    """

    mean = series.mean()
    std = series.std()

    if pd.isna(std) or std == 0:
        return pd.Series(
            np.zeros(len(series)),
            index=series.index
        )

    return (series - mean) / std


outlier_records = []


# Broad-sector based Z-score
if "broad_sector" in df.columns:

    grouped = df.groupby(
        "broad_sector",
        dropna=False
    )

    for sector_name, sector_group in grouped:

        for metric in profile_columns:

            if metric not in sector_group.columns:
                continue

            values = pd.to_numeric(
                sector_group[metric],
                errors="coerce"
            )

            z_scores = calculate_zscore(values)

            for idx, z_score in z_scores.items():

                if pd.isna(z_score):
                    continue

                if abs(z_score) > 3:

                    outlier_records.append({
                        "company_id": df.loc[
                            idx, "company_id"
                        ],

                        "company_name": df.loc[
                            idx, "company_name"
                        ]
                        if "company_name" in df.columns
                        else "",

                        "broad_sector": sector_name,

                        "metric": metric,

                        "value": df.loc[
                            idx, metric
                        ],

                        "z_score": round(
                            z_score,
                            4
                        ),

                        "outlier_type": (
                            "High"
                            if z_score > 3
                            else "Low"
                        )
                    })

else:

    print(
        "WARNING: broad_sector not available."
    )

    print(
        "Sector-based outlier detection skipped."
    )


outlier_report = pd.DataFrame(
    outlier_records
)


# Ensure columns exist even if there are zero outliers
if outlier_report.empty:

    outlier_report = pd.DataFrame(
        columns=[
            "company_id",
            "company_name",
            "broad_sector",
            "metric",
            "value",
            "z_score",
            "outlier_type"
        ]
    )


outlier_file = (
    OUTPUT_DIR / "outlier_report.csv"
)

outlier_report.to_csv(
    outlier_file,
    index=False
)


print(
    f"\nOutliers detected: "
    f"{len(outlier_report)}"
)

print(
    f"Outlier report saved:\n"
    f"{outlier_file}"
)


# ============================================================
# 15. PORTFOLIO STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("PORTFOLIO STATISTICS")
print("=" * 70)


portfolio_records = []


for metric in profile_columns:

    series = pd.to_numeric(
        df[metric],
        errors="coerce"
    ).dropna()


    if series.empty:
        continue


    record = {
        "metric": metric,

        "P10": series.quantile(0.10),

        "P25": series.quantile(0.25),

        "P50": series.quantile(0.50),

        "P75": series.quantile(0.75),

        "P90": series.quantile(0.90),

        "mean": series.mean(),

        "std": series.std(),

        "count": series.count()
    }


    portfolio_records.append(record)


portfolio_stats = pd.DataFrame(
    portfolio_records
)


# Round numerical values
numeric_stat_columns = [
    "P10",
    "P25",
    "P50",
    "P75",
    "P90",
    "mean",
    "std"
]


for column in numeric_stat_columns:

    if column in portfolio_stats.columns:

        portfolio_stats[column] = (
            portfolio_stats[column]
            .round(4)
        )


portfolio_stats_file = (
    OUTPUT_DIR / "portfolio_stats.csv"
)


portfolio_stats.to_csv(
    portfolio_stats_file,
    index=False
)


print(
    "\nPortfolio statistics:"
)

print(
    portfolio_stats.to_string(
        index=False
    )
)


print(
    f"\nSaved portfolio statistics:\n"
    f"{portfolio_stats_file}"
)


# ============================================================
# 16. FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("DAY 37 COMPLETE")
print("=" * 70)


print("\nINPUT FILES:")
print(f"Companies: {DATA_FILE}")
print(f"Clusters:  {CLUSTER_FILE}")


print("\nOUTPUT FILES:")

print(
    "1.",
    OUTPUT_DIR / "cluster_profile.csv"
)

print(
    "2.",
    OUTPUT_DIR / "cluster_profile_mean.csv"
)

print(
    "3.",
    OUTPUT_DIR / "cluster_profile_median.csv"
)

print(
    "4.",
    REPORT_DIR / "correlation_heatmap.png"
)

print(
    "5.",
    OUTPUT_DIR / "correlation_matrix.csv"
)

print(
    "6.",
    OUTPUT_DIR / "outlier_report.csv"
)

print(
    "7.",
    OUTPUT_DIR / "portfolio_stats.csv"
)


print("\nCLUSTER COUNTS:")

print(
    df.groupby(
        ["cluster_id", "cluster_name"]
    )
    .size()
    .to_string()
)


print("\nTOTAL COMPANIES:", len(df))

print(
    "\nDAY 37 COMPLETE"
)

print("=" * 70)