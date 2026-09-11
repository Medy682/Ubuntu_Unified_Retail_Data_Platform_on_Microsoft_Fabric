-- 1. Validate Sales KPI Summary
SELECT *
FROM dbo.vw_sales_kpi_summary;

-- 2. Validate Sales Over Time
SELECT TOP 20 *
FROM dbo.vw_sales_over_time
ORDER BY order_date;

-- 3. Validate Product Performance
SELECT TOP 20 *
FROM dbo.vw_product_performance
ORDER BY revenue_rank;

-- 4. Validate Customer Performance
SELECT TOP 20 *
FROM dbo.vw_customer_performance
ORDER BY total_revenue DESC;

-- 5. Validate Store Overview
SELECT TOP 20 *
FROM dbo.vw_store_overview;

-- 6. Validate Store Status
SELECT *
FROM dbo.vw_store_status;

-- 7. Validate Stores by Region
SELECT *
FROM dbo.vw_stores_by_region
ORDER BY store_count DESC;

-- 8. Validate Stores by Type
SELECT *
FROM dbo.vw_stores_by_type
ORDER BY store_count DESC;