import os
import sys
import pandas as pd


# ============================================================
# PROJECT PATH
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

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# FILE PATHS
# ============================================================

PROFIT_LOSS_FILE = os.path.join(
    DATA_DIR,
    "profitandloss.xlsx"
)

BALANCE_SHEET_FILE = os.path.join(
    DATA_DIR,
    "balancesheet.xlsx"
)

COMPANIES_FILE = os.path.join(
    DATA_DIR,
    "companies.xlsx"
)

RATIO_OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "ratio_analysis.csv"
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_numeric(series):
    """
    Convert a pandas Series to numeric values.

    Invalid values are converted to NaN.
    """

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def safe_divide(numerator, denominator):
    """
    Safely divide two values.

    Returns None when denominator is zero,
    missing, or invalid.
    """

    try:

        if pd.isna(numerator):
            return None

        if pd.isna(denominator):
            return None

        if denominator == 0:
            return None

        return numerator / denominator

    except (TypeError, ValueError):

        return None


# ============================================================
# INDIVIDUAL RATIO FUNCTIONS
# ============================================================

def net_profit_margin(
    net_profit,
    sales
):
    """
    Net Profit Margin
    = (Net Profit / Sales) * 100
    """

    result = safe_divide(
        net_profit,
        sales
    )

    if result is None:
        return None

    return result * 100


def operating_profit_margin(
    operating_profit,
    sales
):
    """
    Operating Profit Margin
    = (Operating Profit / Sales) * 100
    """

    result = safe_divide(
        operating_profit,
        sales
    )

    if result is None:
        return None

    return result * 100


def return_on_equity(
    net_profit,
    equity
):
    """
    ROE
    = (Net Profit / Equity) * 100
    """

    try:

        if pd.isna(equity):
            return None

        if equity <= 0:
            return None

        if pd.isna(net_profit):
            return None

        return (
            net_profit /
            equity
        ) * 100

    except (TypeError, ValueError):

        return None


def return_on_assets(
    net_profit,
    total_assets
):
    """
    ROA
    = (Net Profit / Total Assets) * 100
    """

    result = safe_divide(
        net_profit,
        total_assets
    )

    if result is None:
        return None

    return result * 100


def debt_to_equity(
    borrowings,
    equity
):
    """
    Debt to Equity Ratio
    = Borrowings / Equity

    Returns None when equity <= 0.
    """

    try:

        if pd.isna(borrowings):
            return None

        if pd.isna(equity):
            return None

        if equity <= 0:
            return None

        return (
            borrowings /
            equity
        )

    except (TypeError, ValueError):

        return None


def return_on_capital_employed(
    ebit,
    equity,
    borrowings
):
    """
    ROCE
    = EBIT / (Equity + Borrowings) * 100
    """

    try:

        if pd.isna(ebit):
            return None

        if pd.isna(equity):
            return None

        if pd.isna(borrowings):
            return None

        capital_employed = (
            equity +
            borrowings
        )

        if capital_employed <= 0:
            return None

        return (
            ebit /
            capital_employed
        ) * 100

    except (TypeError, ValueError):

        return None


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    = (Operating Profit + Other Income) / Interest

    Returns None when interest is zero.
    """

    try:

        if pd.isna(operating_profit):
            return None

        if pd.isna(other_income):
            other_income = 0

        if pd.isna(interest):
            return None

        if interest == 0:
            return None

        return (
            operating_profit +
            other_income
        ) / interest

    except (TypeError, ValueError):

        return None


def net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    = Borrowings - Investments
    """

    try:

        if pd.isna(borrowings):
            borrowings = 0

        if pd.isna(investments):
            investments = 0

        return (
            borrowings -
            investments
        )

    except (TypeError, ValueError):

        return None


def asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover
    = Sales / Total Assets
    """

    return safe_divide(
        sales,
        total_assets
    )


# ============================================================
# COLUMN VALIDATION
# ============================================================

def find_column(
    df,
    possible_names
):
    """
    Find a column using multiple possible names.

    This makes the module tolerant of small
    differences in Excel column names.
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


def rename_matching_columns(
    df,
    mapping
):
    """
    Rename columns using possible
    column-name variations.
    """

    rename_dict = {}

    for standard_name, possible_names in mapping.items():

        found = find_column(
            df,
            possible_names
        )

        if found is not None:

            rename_dict[
                found
            ] = standard_name

    return df.rename(
        columns=rename_dict
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("\n" + "=" * 60)
    print("LOADING FINANCIAL DATA")
    print("=" * 60)

    # --------------------------------------------------------
    # Check Profit & Loss
    # --------------------------------------------------------

    if not os.path.exists(
        PROFIT_LOSS_FILE
    ):

        raise FileNotFoundError(
            f"\nProfit & Loss file not found:\n"
            f"{PROFIT_LOSS_FILE}\n"
            f"\nMake sure profitandloss.xlsx exists inside:"
            f"\ndata/raw/"
        )

    # --------------------------------------------------------
    # Check Balance Sheet
    # --------------------------------------------------------

    if not os.path.exists(
        BALANCE_SHEET_FILE
    ):

        raise FileNotFoundError(
            f"\nBalance Sheet file not found:\n"
            f"{BALANCE_SHEET_FILE}\n"
            f"\nMake sure balancesheet.xlsx exists inside:"
            f"\ndata/raw/"
        )

    # --------------------------------------------------------
    # Read Excel files
    # --------------------------------------------------------

    profit_loss = pd.read_excel(
        PROFIT_LOSS_FILE,
        header=1
    )

    balance_sheet = pd.read_excel(
        BALANCE_SHEET_FILE,
        header=1
    )

    # --------------------------------------------------------
    # Display columns
    # --------------------------------------------------------

    print(
        "\nProfit & Loss columns:"
    )

    print(
        list(
            profit_loss.columns
        )
    )

    print(
        "\nBalance Sheet columns:"
    )

    print(
        list(
            balance_sheet.columns
        )
    )

    return (
        profit_loss,
        balance_sheet
    )


# ============================================================
# STANDARDIZE PROFIT & LOSS
# ============================================================

def prepare_profit_loss(
    df
):

    mapping = {

        "company_id": [
            "company_id",
            "company id",
            "id"
        ],

        "year": [
            "year",
            "financial_year",
            "financial year"
        ],

        "sales": [
            "sales",
            "revenue",
            "total_revenue"
        ],

        "operating_profit": [
            "operating_profit",
            "operating profit"
        ],

        "net_profit": [
            "net_profit",
            "net profit"
        ],

        "other_income": [
            "other_income",
            "other income"
        ],

        "interest": [
            "interest",
            "interest_expense",
            "interest expense"
        ]
    }

    df = rename_matching_columns(
        df,
        mapping
    )

    return df


# ============================================================
# STANDARDIZE BALANCE SHEET
# ============================================================

def prepare_balance_sheet(
    df
):

    mapping = {

        "company_id": [
            "company_id",
            "company id",
            "id"
        ],

        "year": [
            "year",
            "financial_year",
            "financial year"
        ],

        "equity": [
            "equity_capital",
            "equity capital",
            "equity"
        ],

        "borrowings": [
            "borrowings",
            "debt",
            "total_debt"
        ],

        "total_assets": [
            "total_assets",
            "total assets"
        ],

        "investments": [
            "investments",
            "investment"
        ]
    }

    df = rename_matching_columns(
        df,
        mapping
    )

    return df


# ============================================================
# CALCULATE RATIOS
# ============================================================

def calculate_ratios(
    profit_loss,
    balance_sheet
):

    print("\n" + "=" * 60)
    print("CALCULATING FINANCIAL RATIOS")
    print("=" * 60)

    # --------------------------------------------------------
    # Standardize columns
    # --------------------------------------------------------

    profit_loss = prepare_profit_loss(
        profit_loss
    )

    balance_sheet = prepare_balance_sheet(
        balance_sheet
    )

    print(
        "\nPrepared Profit & Loss columns:"
    )

    print(
        list(
            profit_loss.columns
        )
    )

    print(
        "\nPrepared Balance Sheet columns:"
    )

    print(
        list(
            balance_sheet.columns
        )
    )

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_pl = [
        "company_id",
        "year",
        "sales",
        "operating_profit",
        "net_profit",
        "other_income",
        "interest"
    ]

    required_bs = [
        "company_id",
        "year",
        "equity",
        "borrowings",
        "total_assets",
        "investments"
    ]

    missing_pl = [
        column
        for column in required_pl
        if column not in profit_loss.columns
    ]

    missing_bs = [
        column
        for column in required_bs
        if column not in balance_sheet.columns
    ]

    if missing_pl:

        raise ValueError(
            "Profit & Loss is missing "
            "required columns: "
            + str(missing_pl)
        )

    if missing_bs:

        raise ValueError(
            "Balance Sheet is missing "
            "required columns: "
            + str(missing_bs)
        )

    # --------------------------------------------------------
    # Clean numeric columns
    # --------------------------------------------------------

    pl_numeric = [
        "sales",
        "operating_profit",
        "net_profit",
        "other_income",
        "interest"
    ]

    bs_numeric = [
        "equity",
        "borrowings",
        "total_assets",
        "investments"
    ]

    for column in pl_numeric:

        profit_loss[
            column
        ] = clean_numeric(
            profit_loss[column]
        )

    for column in bs_numeric:

        balance_sheet[
            column
        ] = clean_numeric(
            balance_sheet[column]
        )

    # --------------------------------------------------------
    # Clean company ID and year
    # --------------------------------------------------------

    profit_loss[
        "company_id"
    ] = (
        profit_loss["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    balance_sheet[
        "company_id"
    ] = (
        balance_sheet["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    profit_loss[
        "year"
    ] = profit_loss[
        "year"
    ].astype(str).str.strip()

    balance_sheet[
        "year"
    ] = balance_sheet[
        "year"
    ].astype(str).str.strip()

    # --------------------------------------------------------
    # Merge datasets
    # --------------------------------------------------------

    merge_columns = [
        "company_id",
        "year"
    ]

    ratios = pd.merge(
        profit_loss[
            merge_columns +
            pl_numeric
        ],
        balance_sheet[
            merge_columns +
            bs_numeric
        ],
        on=merge_columns,
        how="inner"
    )

    if ratios.empty:

        raise ValueError(
            "\nNo matching records found between "
            "Profit & Loss and Balance Sheet.\n"
            "Check company_id and year values."
        )

    print(
        f"\nMatching financial records: "
        f"{len(ratios)}"
    )

    # --------------------------------------------------------
    # Calculate ratios
    # --------------------------------------------------------

    ratios[
        "net_profit_margin"
    ] = ratios.apply(
        lambda row:
        net_profit_margin(
            row["net_profit"],
            row["sales"]
        ),
        axis=1
    )

    ratios[
        "operating_profit_margin"
    ] = ratios.apply(
        lambda row:
        operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        ),
        axis=1
    )

    ratios[
        "roe_percentage"
    ] = ratios.apply(
        lambda row:
        return_on_equity(
            row["net_profit"],
            row["equity"]
        ),
        axis=1
    )

    ratios[
        "roa_percentage"
    ] = ratios.apply(
        lambda row:
        return_on_assets(
            row["net_profit"],
            row["total_assets"]
        ),
        axis=1
    )

    ratios[
        "debt_to_equity"
    ] = ratios.apply(
        lambda row:
        debt_to_equity(
            row["borrowings"],
            row["equity"]
        ),
        axis=1
    )

    ratios[
        "roce_percentage"
    ] = ratios.apply(
        lambda row:
        return_on_capital_employed(
            row["operating_profit"],
            row["equity"],
            row["borrowings"]
        ),
        axis=1
    )

    ratios[
        "interest_coverage_ratio"
    ] = ratios.apply(
        lambda row:
        interest_coverage_ratio(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        ),
        axis=1
    )

    ratios[
        "net_debt"
    ] = ratios.apply(
        lambda row:
        net_debt(
            row["borrowings"],
            row["investments"]
        ),
        axis=1
    )

    ratios[
        "asset_turnover"
    ] = ratios.apply(
        lambda row:
        asset_turnover(
            row["sales"],
            row["total_assets"]
        ),
        axis=1
    )

    # --------------------------------------------------------
    # Round calculated values
    # --------------------------------------------------------

    ratio_columns = [
        "net_profit_margin",
        "operating_profit_margin",
        "roe_percentage",
        "roa_percentage",
        "debt_to_equity",
        "roce_percentage",
        "interest_coverage_ratio",
        "net_debt",
        "asset_turnover"
    ]

    for column in ratio_columns:

        ratios[
            column
        ] = pd.to_numeric(
            ratios[column],
            errors="coerce"
        ).round(2)

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    ratios = ratios.sort_values(
        by=[
            "year",
            "company_id"
        ]
    )

    return ratios


# ============================================================
# GET COMPANY RATIOS
# ============================================================

def get_company_ratios(
    ratios,
    company_id
):
    """
    Return the latest available ratio record
    for a specific company.
    """

    if ratios is None or ratios.empty:
        return None

    company_id = (
        str(company_id)
        .strip()
        .upper()
    )

    company_data = ratios[
        ratios["company_id"] == company_id
    ].copy()

    if company_data.empty:
        return None

    # --------------------------------------------------------
    # Sort by year so latest record is selected
    # --------------------------------------------------------

    company_data = company_data.sort_values(
        by="year"
    )

    row = company_data.iloc[-1]

    return {
        "company_id": row["company_id"],
        "year": row["year"],
        "net_profit_margin": row[
            "net_profit_margin"
        ],
        "operating_profit_margin": row[
            "operating_profit_margin"
        ],
        "roe_percentage": row[
            "roe_percentage"
        ],
        "roa_percentage": row[
            "roa_percentage"
        ],
        "debt_to_equity": row[
            "debt_to_equity"
        ],
        "roce_percentage": row[
            "roce_percentage"
        ],
        "interest_coverage_ratio": row[
            "interest_coverage_ratio"
        ],
        "net_debt": row[
            "net_debt"
        ],
        "asset_turnover": row[
            "asset_turnover"
        ]
    }


# ============================================================
# MAIN ANALYSIS
# ============================================================

def run_ratio_analysis():

    print("\n")

    print("=" * 70)
    print("          FINANCIAL RATIO ANALYSIS")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # Load
        # ----------------------------------------------------

        profit_loss, balance_sheet = load_data()

        # ----------------------------------------------------
        # Calculate
        # ----------------------------------------------------

        ratios = calculate_ratios(
            profit_loss,
            balance_sheet
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_columns = [
            "company_id",
            "year",
            "net_profit_margin",
            "operating_profit_margin",
            "roe_percentage",
            "roa_percentage",
            "debt_to_equity",
            "roce_percentage",
            "interest_coverage_ratio",
            "net_debt",
            "asset_turnover"
        ]

        print(
            "\n========== RATIO ANALYSIS RESULTS ==========\n"
        )

        print(
            ratios[
                display_columns
            ].to_string(
                index=False
            )
        )

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        ratios.to_csv(
            RATIO_OUTPUT_FILE,
            index=False
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "RATIO ANALYSIS COMPLETED SUCCESSFULLY"
        )

        print(
            "=" * 70
        )

        print(
            "\nOutput file:"
        )

        print(
            RATIO_OUTPUT_FILE
        )

        print(
            f"\nRows generated: "
            f"{len(ratios)}"
        )

        print(
            "\nRatio columns generated:"
        )

        for column in display_columns[2:]:

            print(
                f"  - {column}"
            )

        return ratios

    except Exception as error:

        print(
            "\n" + "=" * 70
        )

        print(
            "RATIO ANALYSIS FAILED"
        )

        print(
            "=" * 70
        )

        print(
            f"\nError: {error}"
        )

        raise


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    run_ratio_analysis()