"""Create the project DuckDB database.

Run with:
    .venv/bin/python scripts/create_duckdb.py
"""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "northwind_dw.duckdb"


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    finally:
        con.close()
    print(f"สร้างฐานข้อมูล {DB_PATH}")


if __name__ == "__main__":
    main()
