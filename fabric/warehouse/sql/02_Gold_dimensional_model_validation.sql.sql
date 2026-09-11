-- Gold — Validate dimension relationships

SELECT
    COUNT(*) AS total_fact_rows,

    COUNT(DISTINCT fs.customer_id) AS distinct_customers,
    COUNT(DISTINCT dc.customer_id) AS matched_customers,

    COUNT(DISTINCT fs.product_id) AS distinct_products,
    COUNT(DISTINCT dp.product_id) AS matched_products,

    COUNT(DISTINCT fs.order_date) AS distinct_sales_dates,
    COUNT(DISTINCT dd.date_key) AS matched_dates

FROM dbo.fact_sales fs

LEFT JOIN dbo.dim_customer dc
    ON fs.customer_id = dc.customer_id

LEFT JOIN dbo.dim_product dp
    ON fs.product_id = dp.product_id

LEFT JOIN dbo.dim_date dd
    ON fs.order_date = dd.date_key;



-- Gold — Validate fact_sales grain

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(DISTINCT CONCAT(order_id, '-', order_item_id)) AS distinct_order_items
FROM dbo.fact_sales;