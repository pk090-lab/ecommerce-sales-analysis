from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "02_analysis_queries.sql"

if not SQL_PATH.exists():
    raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

print("Running SQL business analysis...")

with sqlite3.connect(DB_PATH) as conn:
    sql_text = SQL_PATH.read_text(encoding="utf-8")

    statements = []
    buffer = ""

    # Split SQL into complete statements
    for line in sql_text.splitlines():
        buffer += line + "\n"

        if sqlite3.complete_statement(buffer):
            if buffer.strip():
                statements.append(buffer.strip())
            buffer = ""

    # Execute each query and display its results
    query_number = 0

    for statement in statements:
        cursor = conn.execute(statement)

        if cursor.description:
            query_number += 1
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = pd.DataFrame(rows, columns=columns)

            print("\n" + "=" * 65)
            print(f"QUERY {query_number}")
            print("=" * 65)
            print(results.to_string(index=False))

print("\nSQL analysis completed successfully!")