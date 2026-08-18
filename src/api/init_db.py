from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "nifty100.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# SOURCE FILES
# ============================================================

FILES = {
    "companies": RAW_DIR / "companies.xlsx",
    "sectors": RAW_DIR / "sectors.xlsx",
    "analysis": RAW_DIR / "analysis.xlsx",
    "balance_sheet": RAW_DIR / "balancesheet.xlsx",
    "cashflow": RAW_DIR / "cashflow.xlsx",
    "profit_loss": RAW_DIR / "profitandloss.xlsx",
    "documents": RAW_DIR / "documents.xlsx",
    "pros_cons": RAW_DIR / "prosandcons.xlsx",
}


# ============================================================
# READ EXCEL SAFELY
# ============================================================

def read_excel_file(path: Path, header=0):
    if not path.exists():
        print(f"WARNING: File not found: {path}")
        return None

    print(f"Loading: {path.name}")

    try:
        df = pd.read_excel(path, header=header)

        # Remove completely empty rows/columns.
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        # Clean column names.
        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return df

    except Exception as error:
        print(f"ERROR reading {path.name}: {error}")
        return None


# ============================================================
# LOAD DATA
# ============================================================

def main():

    print("=" * 70)
    print("BUILDING NIFTY 100 SQLITE DATABASE")
    print("=" * 70)

    if DB_PATH.exists():
        print(f"\nExisting database found:")
        print(DB_PATH)

        answer = input(
            "\nReplace existing database? (y/n): "
        ).strip().lower()

        if answer != "y":
            print("Database creation cancelled.")
            return

        DB_PATH.unlink()
        print("Existing database removed.")

    # Companies uses second row as header in your project.
    companies = read_excel_file(
        FILES["companies"],
        header=1
    )

    # Profit & Loss also uses second row as header.
    profit_loss = read_excel_file(
        FILES["profit_loss"],
        header=1
    )

    # Other files use first row as header.
    sectors = read_excel_file(FILES["sectors"], header=0)
    analysis = read_excel_file(FILES["analysis"], header=0)
    balance_sheet = read_excel_file(FILES["balance_sheet"], header=0)
    cashflow = read_excel_file(FILES["cashflow"], header=0)
    documents = read_excel_file(FILES["documents"], header=0)
    pros_cons = read_excel_file(FILES["pros_cons"], header=0)

    datasets = {
        "companies": companies,
        "sectors": sectors,
        "analysis": analysis,
        "balance_sheet": balance_sheet,
        "cashflow": cashflow,
        "profit_loss": profit_loss,
        "documents": documents,
        "pros_cons": pros_cons,
    }

    # ========================================================
    # SHOW LOADED TABLES
    # ========================================================

    print("\n" + "=" * 70)
    print("LOADED DATASETS")
    print("=" * 70)

    for table_name, df in datasets.items():

        if df is None:
            print(f"{table_name:20} -> NOT LOADED")
            continue

        print(
            f"{table_name:20} -> "
            f"{len(df):5} rows | "
            f"{len(df.columns):3} columns"
        )

        print(
            "   Columns:",
            df.columns.tolist()
        )

    # Companies is required for the API.
    if companies is None:
        raise RuntimeError(
            "companies.xlsx could not be loaded."
        )

    # Check the important columns.
    required_company_columns = [
        "id",
        "company_name",
    ]

    missing_company_columns = [
        column
        for column in required_company_columns
        if column not in companies.columns
    ]

    if missing_company_columns:

        raise RuntimeError(
            "companies.xlsx is missing required columns: "
            + str(missing_company_columns)
        )

    # ========================================================
    # CREATE SQLITE DATABASE
    # ========================================================

    print("\n" + "=" * 70)
    print("CREATING SQLITE DATABASE")
    print("=" * 70)

    connection = sqlite3.connect(DB_PATH)

    try:
        for table_name, df in datasets.items():
            if df is None:
                continue

            print(f"\nWriting table: {table_name}")

            try:
                df.to_sql(
                    table_name,
                    connection,
                    if_exists="replace",
                    index=False
                )

                print(f"SUCCESS: {table_name}")

            except Exception as error:
                print(f"FAILED: {table_name}")
                print(f"ERROR: {error}")
                raise

        connection.commit()

    finally:
        connection.close()

    # ========================================================
    # VERIFY DATABASE
    # ========================================================

    print("\n" + "=" * 70)
    print("VERIFYING DATABASE")
    print("=" * 70)

    connection = sqlite3.connect(DB_PATH)

    try:

        tables = pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """,
            connection
        )

        print("\nTables created:")

        for table in tables["name"]:
            print(f"  ✓ {table}")

            count = pd.read_sql_query(
                f'SELECT COUNT(*) AS count FROM "{table}"',
                connection
            ).iloc[0]["count"]

            print(
                f"      Rows: {count}"
            )

    finally:
        connection.close()

    print("\n" + "=" * 70)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"\nDatabase:"
        f"\n{DB_PATH}"
    )


if __name__ == "__main__":
    main()