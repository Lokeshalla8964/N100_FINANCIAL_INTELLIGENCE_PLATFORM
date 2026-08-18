from fastapi import APIRouter, HTTPException, Query
import sqlite3
from pathlib import Path


router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"


def get_connection():
    """
    Create a connection to the Nifty 100 SQLite database.
    """

    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Database not found: {DB_PATH}"
        )

    connection = sqlite3.connect(DB_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# 1. GET ALL COMPANIES
# =========================================================

@router.get("")
def get_companies(
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None)
):
    """
    Return N100 companies with latest available KPI information.

    Optional filters:
    - sector
    - market_cap_category
    - search
    """

    connection = get_connection()

    try:

        query = """
            SELECT
                c.id,
                c.company_name,
                s.broad_sector,
                s.sub_sector,
                c.roe_percentage AS roe_pct,
                c.roce_percentage AS roce_pct

            FROM companies c

            LEFT JOIN sectors s
                ON c.id = s.company_id

            WHERE 1 = 1
        """

        parameters = []

        # -------------------------------------------------
        # SECTOR FILTER
        # -------------------------------------------------

        if sector:

            query += """
                AND (
                    LOWER(COALESCE(s.broad_sector, '')) = LOWER(?)
                    OR
                    LOWER(COALESCE(s.sub_sector, '')) = LOWER(?)
                )
            """

            parameters.extend([
                sector,
                sector
            ])

        # -------------------------------------------------
        # SEARCH FILTER
        # -------------------------------------------------

        if search:

            query += """
                AND LOWER(c.company_name) LIKE LOWER(?)
            """

            parameters.append(
                f"%{search}%"
            )

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        query += """
            ORDER BY c.company_name
        """

        rows = connection.execute(
            query,
            parameters
        ).fetchall()

        companies = []

        for row in rows:

            companies.append(dict(row))

        return {
            "count": len(companies),
            "companies": companies
        }

    except sqlite3.Error as error:

        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {error}"
        )

    finally:

        connection.close()


# =========================================================
# 2. GET COMPANY PROFILE
# =========================================================

@router.get("/{company_id}/profile")
def get_company_profile(company_id: str):
    """
    Return detailed profile information for a company.
    """

    connection = get_connection()

    try:

        query = """
            SELECT
                c.id,
                c.company_logo,
                c.company_name,
                c.chart_link,
                c.about_company,
                c.website,
                c.nse_profile,
                c.bse_profile,
                c.face_value,
                c.book_value,
                c.roce_percentage,
                c.roe_percentage,

                s.broad_sector,
                s.sub_sector

            FROM companies c

            LEFT JOIN sectors s
                ON c.id = s.company_id

            WHERE UPPER(c.id) = UPPER(?)

            LIMIT 1
        """

        row = connection.execute(
            query,
            (company_id,)
        ).fetchone()

        # -------------------------------------------------
        # COMPANY NOT FOUND
        # -------------------------------------------------

        if row is None:

            raise HTTPException(
                status_code=404,
                detail=f"Company not found: {company_id}"
            )

        company = dict(row)

        return {
            "company": company
        }

    except HTTPException:

        raise

    except sqlite3.Error as error:

        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {error}"
        )

    finally:

        connection.close()