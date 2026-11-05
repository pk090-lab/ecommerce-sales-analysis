from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "powerbi"

OUTPUT_DIR.mkdir(exist_ok=True)

# CSV files and corresponding Excel worksheet names
files = {
    "Monthly Sales": "monthly_sales.csv",
    "Product Performance": "product_performance.csv",
    "Country Performance": "country_performance.csv",
    "Customer Performance": "customer_performance.csv",
    "Data Quality": "data_quality_summary.csv",
    "KPI Summary": "project_kpi_summary.csv",
}

output_file = OUTPUT_DIR / "ecommerce_dashboard_data.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for sheet_name, filename in files.items():
        csv_path = DATA_DIR / filename

        if not csv_path.exists():
            raise FileNotFoundError(f"Missing file: {csv_path}")

        df = pd.read_csv(csv_path)
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        print(f"Added {sheet_name}: {len(df):,} rows")

print("\nPower BI workbook created successfully!")
print(f"Location: {output_file}")