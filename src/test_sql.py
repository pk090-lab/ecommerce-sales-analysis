from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "ecommerce.db"

query = """
SELECT
    country,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders
FROM sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;
"""

with sqlite3.connect(DB_PATH) as conn:
    results = pd.read_sql_query(query, conn)

print("\nTOP 10 COUNTRIES BY REVENUE\n")
print(results.to_string(index=False))