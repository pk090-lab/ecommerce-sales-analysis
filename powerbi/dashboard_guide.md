# Power BI Dashboard Build Guide

## Data import and preparation

1. Run `python src/analysis.py`.
2. In Power BI Desktop, import `data/processed/clean_sales.csv`.
3. Rename the table to `Sales`.
4. Set data types:
   - `invoice_no`, `stock_code`, `description`, `customer_id`, `country`: Text
   - `quantity`: Whole number
   - `unit_price`, `revenue`: Decimal number
   - `invoice_date`: Date/Time
5. Create `InvoiceDate_Date` as described in `dax_measures.md`.
6. Create a Date table and relationship if using time-intelligence measures.

## Page 1 — Executive Overview

KPI cards:
- Total Revenue
- Total Orders
- Known Customers
- Average Order Value
- Units Sold

Visuals:
- Line chart: Revenue by month
- Bar chart: Top 10 products by revenue
- Filled map or bar chart: Revenue by country
- Slicers: Date, Country, Product

## Page 2 — Product Performance

Visuals:
- Top 10 products by revenue
- Top 10 products by units sold
- Revenue by product
- Product-level order count
- Slicers: Country and date

Business questions:
- Which products contribute most to revenue?
- Are the most frequently purchased products also the highest-revenue products?
- Is revenue concentrated in a small number of products?

## Page 3 — Customer Analysis

Visuals:
- Known customer count
- Repeat customer rate
- Revenue per known customer
- Top 10 customers by revenue
- Customer order frequency distribution

Business questions:
- What proportion of identified customers purchase more than once?
- Which customers contribute the most revenue?
- How does customer value vary?

## Page 4 — Geographic & Time Trends

Visuals:
- Revenue by country
- Monthly revenue trend
- Orders by weekday
- Revenue by weekday
- Country and date slicers

## Design recommendations

- Use a consistent, restrained color palette.
- Put high-level KPIs at the top.
- Use descriptive titles and currency formatting.
- Add tooltip details where useful.
- Avoid clutter and unnecessary 3D charts.
- Include a small note: "Revenue reflects positive sales lines; cancelled invoices and non-positive quantity/price rows are excluded."

## Validation

Compare Power BI totals against:
- `project_kpi_summary.csv`
- SQL overall KPI query in `sql/02_analysis_queries.sql`

Investigate any mismatch before publishing screenshots or claims.
