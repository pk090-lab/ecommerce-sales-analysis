"""Clean UCI Online Retail data and generate reproducible analysis outputs."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUT = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

RENAME = {
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country",
}

def main():
    if not RAW.exists():
        raise FileNotFoundError(
            f"Missing {RAW}. Run `python src/download_data.py` or download "
            "Online Retail.xlsx from https://archive.ics.uci.edu/dataset/352/online+retail"
        )

    df = pd.read_excel(RAW)
    df = df.rename(columns=RENAME)
    required = list(RENAME.values())
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")

    initial_rows = len(df)
    df["invoice_no"] = df["invoice_no"].astype("string").str.strip()
    df["stock_code"] = df["stock_code"].astype("string").str.strip()
    df["description"] = df["description"].astype("string").str.strip()
    df["country"] = df["country"].astype("string").str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")
    df["revenue"] = df["quantity"] * df["unit_price"]

    # Keep an explicit quality profile before filtering.
    cancelled = df["invoice_no"].str.startswith("C", na=False)
    invalid_date = df["invoice_date"].isna()
    invalid_numeric = df["quantity"].isna() | df["unit_price"].isna()
    nonpositive_quantity = df["quantity"].le(0)
    nonpositive_price = df["unit_price"].le(0)

    quality = pd.DataFrame([
        ("source_rows", initial_rows),
        ("cancelled_or_credit_note_rows", int(cancelled.sum())),
        ("missing_customer_id_rows", int(df["customer_id"].isna().sum())),
        ("invalid_invoice_date_rows", int(invalid_date.sum())),
        ("invalid_quantity_or_price_rows", int(invalid_numeric.sum())),
        ("nonpositive_quantity_rows", int(nonpositive_quantity.sum())),
        ("nonpositive_unit_price_rows", int(nonpositive_price.sum())),
    ], columns=["quality_check", "row_count"])
    quality.to_csv(OUT / "data_quality_summary.csv", index=False)

    # Positive sales fact: exclude cancellations, invalid dates/numbers, returns,
    # and non-positive prices. Missing customer IDs are retained for sales totals.
    valid = (
        ~cancelled
        & ~invalid_date
        & ~invalid_numeric
        & df["quantity"].gt(0)
        & df["unit_price"].gt(0)
        & df["invoice_no"].notna()
        & df["stock_code"].notna()
    )
    sales = df.loc[valid].copy()
    sales["revenue"] = (sales["quantity"] * sales["unit_price"]).round(2)
    sales["invoice_date"] = sales["invoice_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    sales["customer_id"] = sales["customer_id"].astype("string")
    sales.to_csv(OUT / "clean_sales.csv", index=False)

    # Summaries
    sales["invoice_month"] = pd.to_datetime(sales["invoice_date"]).dt.to_period("M").astype(str)
    monthly = sales.groupby("invoice_month", as_index=False).agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        units_sold=("quantity", "sum"),
    )
    monthly.to_csv(OUT / "monthly_sales.csv", index=False)

    products = sales.groupby(["stock_code", "description"], dropna=False, as_index=False).agg(
        revenue=("revenue", "sum"),
        units_sold=("quantity", "sum"),
        orders=("invoice_no", "nunique"),
    ).sort_values("revenue", ascending=False)
    products.to_csv(OUT / "product_performance.csv", index=False)

    countries = sales.groupby("country", as_index=False).agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        customers=("customer_id", "nunique"),
    ).sort_values("revenue", ascending=False)
    countries.to_csv(OUT / "country_performance.csv", index=False)

    customer_sales = sales.dropna(subset=["customer_id"]).groupby("customer_id", as_index=False).agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        first_purchase=("invoice_date", "min"),
        last_purchase=("invoice_date", "max"),
    )
    customer_sales.to_csv(OUT / "customer_performance.csv", index=False)

    # Charts: generated from the cleaned positive-sales fact.
    monthly["revenue"] = monthly["revenue"].round(2)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["invoice_month"], monthly["revenue"], marker="o")
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Invoice month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(REPORTS / "monthly_revenue.png", dpi=160)
    plt.close(fig)

    top10 = products.head(10).sort_values("revenue")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top10["description"].fillna(top10["stock_code"]).astype(str), top10["revenue"])
    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Revenue")
    fig.tight_layout()
    fig.savefig(REPORTS / "top_products.png", dpi=160)
    plt.close(fig)

    summary = {
        "source_rows": initial_rows,
        "clean_sales_rows": len(sales),
        "total_revenue": round(float(sales["revenue"].sum()), 2),
        "distinct_orders": int(sales["invoice_no"].nunique()),
        "known_customers": int(sales["customer_id"].nunique()),
        "countries": int(sales["country"].nunique()),
        "missing_customer_id_sales_rows": int(sales["customer_id"].isna().sum()),
    }
    pd.DataFrame([summary]).to_csv(OUT / "project_kpi_summary.csv", index=False)

    print("Analysis complete.")
    print(pd.Series(summary).to_string())
    print(f"Outputs: {OUT} and {REPORTS}")

if __name__ == "__main__":
    main()
