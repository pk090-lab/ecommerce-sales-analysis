-- 1. Overall KPI snapshot
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_id) AS known_customers,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT invoice_no), 0), 2) AS average_order_value,
    SUM(quantity) AS units_sold
FROM sales;

-- 2. Monthly revenue and order trend
SELECT
    strftime('%Y-%m', invoice_date) AS sales_month,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY strftime('%Y-%m', invoice_date)
ORDER BY sales_month;

-- 3. Top 10 products by revenue
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders
FROM sales
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 10;

-- 4. Revenue by country
SELECT
    country,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM sales
GROUP BY country
ORDER BY revenue DESC;

-- 5. Repeat customer analysis (known customer IDs only)
WITH customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT invoice_no) AS order_count,
           SUM(revenue) AS customer_revenue
    FROM sales
    WHERE customer_id IS NOT NULL AND TRIM(customer_id) <> ''
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2)
        AS repeat_customer_pct,
    ROUND(AVG(customer_revenue), 2) AS avg_revenue_per_customer
FROM customer_orders;

-- 6. Average order value by month
WITH invoice_totals AS (
    SELECT invoice_no, strftime('%Y-%m', invoice_date) AS sales_month,
           SUM(revenue) AS invoice_revenue
    FROM sales
    GROUP BY invoice_no, strftime('%Y-%m', invoice_date)
)
SELECT sales_month,
       ROUND(AVG(invoice_revenue), 2) AS average_order_value,
       COUNT(*) AS orders
FROM invoice_totals
GROUP BY sales_month
ORDER BY sales_month;

-- 7. Weekday performance
SELECT
    CASE CAST(strftime('%w', invoice_date) AS INTEGER)
        WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday' ELSE 'Saturday'
    END AS weekday,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders
FROM sales
GROUP BY strftime('%w', invoice_date)
ORDER BY CAST(strftime('%w', invoice_date) AS INTEGER);

-- 8. Top customers by revenue
SELECT customer_id,
       COUNT(DISTINCT invoice_no) AS orders,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE customer_id IS NOT NULL AND TRIM(customer_id) <> ''
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;

-- 9. Product revenue contribution
WITH product_revenue AS (
    SELECT stock_code, description, SUM(revenue) AS revenue
    FROM sales
    GROUP BY stock_code, description
)
SELECT stock_code, description, ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * revenue / NULLIF((SELECT SUM(revenue) FROM product_revenue), 0), 2)
           AS revenue_share_pct
FROM product_revenue
ORDER BY revenue DESC
LIMIT 20;
