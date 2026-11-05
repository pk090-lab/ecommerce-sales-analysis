-- Check for null or blank required identifiers
SELECT
    SUM(CASE WHEN invoice_no IS NULL OR TRIM(invoice_no) = '' THEN 1 ELSE 0 END) AS missing_invoice,
    SUM(CASE WHEN stock_code IS NULL OR TRIM(stock_code) = '' THEN 1 ELSE 0 END) AS missing_stock_code,
    SUM(CASE WHEN invoice_date IS NULL OR TRIM(invoice_date) = '' THEN 1 ELSE 0 END) AS missing_invoice_date
FROM sales;

-- Confirm the cleaned sales table contains only positive sales values
SELECT COUNT(*) AS invalid_sales_rows
FROM sales
WHERE quantity <= 0 OR unit_price <= 0 OR revenue <= 0;

-- Duplicate-looking invoice/product/date combinations (review, do not blindly delete)
SELECT invoice_no, stock_code, invoice_date, COUNT(*) AS row_count
FROM sales
GROUP BY invoice_no, stock_code, invoice_date
HAVING COUNT(*) > 1
ORDER BY row_count DESC
LIMIT 50;

-- Missing customer IDs are allowed in the sales fact, but must be excluded
-- from customer-level distinct counts and retention calculations.
SELECT COUNT(*) AS rows_without_customer_id
FROM sales
WHERE customer_id IS NULL OR TRIM(customer_id) = '';
