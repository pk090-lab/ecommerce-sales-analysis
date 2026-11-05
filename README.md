# E-Commerce Sales Analysis

An end-to-end data analytics portfolio project using **SQL, Python, and Power BI**. The project analyzes the UCI Online Retail transactional dataset to identify revenue trends, product performance, customer behavior, and geographic sales patterns.

## Business problem

A UK-based online retailer wants to understand:
- How revenue changes over time.
- Which products and countries contribute most to revenue.
- How many customers make repeat purchases.
- Which months and days have the strongest sales.
- How returns and cancelled invoices affect reported performance.

## Tools

- **Python:** pandas, NumPy, matplotlib, openpyxl
- **SQL:** SQLite (portable; works locally without a database server)
- **BI:** Microsoft Power BI Desktop
- **Dataset:** UCI Machine Learning Repository — Online Retail

## Dataset

Download the original `Online Retail.xlsx` file from the [UCI Online Retail dataset page](https://archive.ics.uci.edu/dataset/352/online+retail).

You can also run the included downloader:

```bash
python -m pip install -r requirements.txt
python src/download_data.py
```

The downloader retrieves the UCI dataset ZIP and extracts the workbook into `data/raw/`. If the UCI download URL changes, use the official dataset page and place `Online Retail.xlsx` in `data/raw/`.

**Dataset notes:** The dataset contains transactions from 2010-12-01 through 2011-12-09. It includes invoice number, product, quantity, invoice date, unit price, customer ID, and country. Review the UCI page for citation and license details before redistributing the raw file. This repository intentionally does not commit the raw workbook.

## Repository structure

```text
ecommerce-sales-analysis/
├── data/
│   ├── raw/                  # Original workbook (not committed)
│   └── processed/            # Generated CSVs (not committed by default)
├── powerbi/
│   ├── dax_measures.md
│   └── dashboard_guide.md
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_analysis_queries.sql
│   └── 03_data_quality_checks.sql
├── src/
│   ├── download_data.py
│   └── analysis.py
├── reports/                  # Generated charts and summary tables
├── .gitignore
├── requirements.txt
└── README.md
```

## Run the project

### 1. Create an environment and install dependencies

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

### 2. Download the data

```bash
python src/download_data.py
```

Or manually download the workbook from UCI and save it as:

```text
data/raw/Online Retail.xlsx
```

### 3. Clean and analyze with Python

```bash
python src/analysis.py
```

The script:
- Loads the Excel workbook.
- Standardizes column names and types.
- Flags cancelled invoices (invoice numbers beginning with `C`).
- Separates positive sales from returns/cancellations.
- Excludes invalid non-positive quantities and prices from the sales fact table.
- Preserves missing customer IDs as unknown rather than inventing IDs.
- Creates a clean transaction CSV, a customer summary, a product summary, and chart images.

Generated files appear in `data/processed/` and `reports/`.

### 4. Load data into SQLite and run SQL

From the project root:

```bash
sqlite3 ecommerce.db < sql/01_create_tables.sql
```

Then import the generated `clean_sales.csv` into the `sales` table. One simple Python option is:

```bash
python -c "import pandas as pd, sqlite3; df=pd.read_csv('data/processed/clean_sales.csv'); con=sqlite3.connect('ecommerce.db'); df.to_sql('sales', con, if_exists='replace', index=False); con.close()"
```

Run the analysis queries:

```bash
sqlite3 ecommerce.db < sql/02_analysis_queries.sql
```

Or open `ecommerce.db` with DB Browser for SQLite and execute the SQL files.

### 5. Build the Power BI dashboard

1. Open Power BI Desktop.
2. Select **Get Data → Text/CSV** and load `data/processed/clean_sales.csv`.
3. Set `InvoiceDate` to Date/Time and numeric columns to appropriate numeric types.
4. Create the measures in `powerbi/dax_measures.md`.
5. Follow the report layout and visual instructions in `powerbi/dashboard_guide.md`.
6. Save the report as `powerbi/Ecommerce_Sales_Analysis.pbix`.

Power BI Desktop is available from [Microsoft](https://powerbi.microsoft.com/desktop/).

## Business questions and analysis

1. What is total net sales revenue from valid positive sales lines?
2. Which months have the highest revenue?
3. Which products generate the most revenue?
4. Which countries contribute the most revenue?
5. How many unique customers purchased?
6. What is average revenue per invoice?
7. What share of customers made more than one purchase?
8. How do order volume and average order value change over time?

**Metric definitions**
- Revenue: sum of `Quantity × UnitPrice` for valid positive sales lines.
- Orders: distinct invoice numbers in the cleaned sales table.
- Customers: distinct non-null customer IDs.
- Average order value (AOV): revenue divided by distinct invoices.
- Repeat customer: a known customer ID associated with more than one distinct invoice.
- Returns/cancellations: excluded from the positive-sales fact table and summarized separately by the Python script where possible.

## Data-quality decisions and limitations

- Invoice numbers beginning with `C` indicate cancellations/credit notes in this dataset; they are not counted as positive sales.
- Positive sales rows require `Quantity > 0` and `UnitPrice > 0`.
- Rows with missing `CustomerID` remain in sales totals but are excluded from customer-level metrics.
- Revenue is a sales-line value, not accounting profit: product cost, shipping, tax, and payment fees are not supplied.
- The dataset is historical and limited to one retailer. Findings should not be generalized to all e-commerce businesses.
- The Python script creates an auditable row-level exclusion summary. Review it before publishing conclusions.

## Suggested GitHub project description

> End-to-end e-commerce analytics project using Python, SQL, and Power BI to clean transactional data, analyze sales and customer behavior, and build an interactive business performance dashboard.

## Suggested resume bullet (replace placeholders with your actual results)

> Analyzed **[N]+** e-commerce transaction records using Python, SQL, and Power BI; cleaned and validated sales data, developed KPI measures, and built an interactive dashboard highlighting revenue trends, top products, customer segments, and geographic performance.

## Dataset citation

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

## License and attribution

The dataset is provided by the UCI Machine Learning Repository. Check the dataset page for the current license/terms and cite UCI when using it. The code in this portfolio repository is provided under the MIT License unless you choose another license; this does not change the dataset's terms.
