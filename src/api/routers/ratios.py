import os
import pandas as pd

from fastapi import APIRouter, HTTPException


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/v1/ratios",
    tags=["Ratios"]
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "output"
)

RATIO_FILE = os.path.join(
    OUTPUT_DIR,
    "ratio_analysis.csv"
)


# ============================================================
# LOAD RATIO DATA
# ============================================================

def load_ratio_data():

    if not os.path.exists(RATIO_FILE):

        raise HTTPException(
            status_code=404,
            detail=(
                "Ratio analysis file not found. "
                f"Expected file: {RATIO_FILE}"
            )
        )

    try:

        df = pd.read_csv(
            RATIO_FILE
        )

        if df.empty:

            raise HTTPException(
                status_code=404,
                detail="Ratio analysis file is empty."
            )

        return df

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to read ratio analysis: {error}"
        )


# ============================================================
# CLEAN DATA FOR JSON
# ============================================================

def clean_for_json(df):

    """
    Convert NaN, positive infinity and negative infinity
    into JSON-compatible None values.

    Pandas allows NaN/inf values, but standard JSON does not.
    """

    cleaned = df.copy()

    # Replace positive and negative infinity
    cleaned = cleaned.replace(
        [float("inf"), float("-inf")],
        None
    )

    # Convert NaN / NaT to None
    cleaned = cleaned.astype(object)

    cleaned = cleaned.where(
        pd.notna(cleaned),
        None
    )

    return cleaned.to_dict(
        orient="records"
    )


# ============================================================
# GET ALL RATIOS
# ============================================================

@router.get("/")
def get_all_ratios():

    df = load_ratio_data()

    return {
        "count": len(df),
        "ratios": clean_for_json(df)
    }


# ============================================================
# GET RATIOS FOR ONE COMPANY
# ============================================================

@router.get("/{company_id}")
def get_company_ratios(
    company_id: str
):

    df = load_ratio_data()

    # --------------------------------------------------------
    # Make company_id comparison consistent
    # --------------------------------------------------------

    if "company_id" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail=(
                "company_id column is missing "
                "from ratio_analysis.csv"
            )
        )

    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
    )

    company_id = company_id.strip()

    # --------------------------------------------------------
    # Filter company
    # --------------------------------------------------------

    result = df[
        df["company_id"].str.upper()
        == company_id.upper()
    ]

    # --------------------------------------------------------
    # Company not found
    # --------------------------------------------------------

    if result.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No ratio data found for "
                f"company_id: {company_id}"
            )
        )

    # --------------------------------------------------------
    # Return company ratios
    # --------------------------------------------------------

    return {
        "company_id": company_id,
        "count": len(result),
        "ratios": clean_for_json(result)
    }