"""Load Northwind raw CSV files into DuckDB.

Run with:
    .venv/bin/python scripts/load_raw.py
"""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "raw_data"
DB_PATH = ROOT / "northwind_dw.duckdb"

SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "order_details": "raw/order_details.csv",
    "orders": "raw/orders.csv",
    "products": "raw/products.csv",
    "shippers": "raw/shippers.csv",
    "suppliers": "raw/suppliers.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        print(f"กำลังโหลดข้อมูลเข้า {DB_PATH.name}")

        for table, relative_path in SOURCES.items():
            csv_path = DATA_DIR / relative_path
            if not csv_path.is_file():
                raise FileNotFoundError(f"ไม่พบไฟล์ {csv_path}")

            con.execute(
                f"""
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT *
                FROM read_csv(?, header = true)
                """,
                [str(csv_path)],
            )
            row_count = con.execute(
                f"SELECT COUNT(*) FROM raw.{table}"
            ).fetchone()[0]
            print(f" raw.{table:<22} {row_count:>6,} แถว")
    finally:
        con.close()

    print("โหลดเสร็จแล้ว")


if __name__ == "__main__":
    main()
