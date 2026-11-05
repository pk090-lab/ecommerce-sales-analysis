from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "clean_sales.csv"
DB_PATH = BASE_DIR / "ecommerce.db"

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Cleaned dataset not found: {CSV_PATH}")

print("Loading cleaned sales data...")

df = pd.read_csv(CSV_PATH)

with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_invoice_date ON sales(invoice_date)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_customer_id ON sales(customer_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_stock_code ON sales(stock_code)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_country ON sales(country)"
    )

    count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]

print("\nDatabase created successfully!")
print(f"Database location: {DB_PATH}")
print(f"Records imported: {count:,}")