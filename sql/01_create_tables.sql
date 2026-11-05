-- SQLite schema. Import data/processed/clean_sales.csv into this table.
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    invoice_no   TEXT NOT NULL,
    stock_code   TEXT NOT NULL,
    description  TEXT,
    quantity     INTEGER NOT NULL,
    invoice_date TEXT NOT NULL,
    unit_price   REAL NOT NULL,
    customer_id  TEXT,
    country      TEXT,
    revenue      REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sales_invoice_date ON sales(invoice_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer_id ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_stock_code ON sales(stock_code);
CREATE INDEX IF NOT EXISTS idx_sales_country ON sales(country);
