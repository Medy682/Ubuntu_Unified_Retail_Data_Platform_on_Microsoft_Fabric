-- ============================================================
-- GOLD ANALYTICAL VIEWS
-- Ubuntu Unified Retail Data Platform
-- Microsoft Fabric Warehouse
-- ============================================================

-- ============================================================
-- 1. SALES — KPI SUMMARY
-- Business questions:
--   - Total Revenue
--   - Total Orders
--   - Average Order Value
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_sales_kpi_summary
AS
SELECT
    SUM(price) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) / NULLIF(COUNT(DISTINCT order_id), 0)
        AS average_order_value,
    SUM(freight_value) AS total_freight
FROM dbo.fact_sales;


-- ============================================================
-- 2. SALES — OVER TIME
-- Business questions:
--   - Sales over Time
--   - Revenue over Time
--   - Orders over Time
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_sales_over_time
AS
SELECT
    order_date,
    SUM(price) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) / NULLIF(COUNT(DISTINCT order_id), 0)
        AS average_order_value
FROM dbo.fact_sales
GROUP BY
    order_date;

-- ============================================================
-- 3. PRODUCT — PERFORMANCE
-- Business questions:
--   - Best-selling Products
--   - Highest-revenue Products
--   - Average Product Price
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_product_performance
AS
WITH product_sales AS
(
    SELECT
        p.product_id,
        p.product_category_name,
        p.product_category_name_en,
        COUNT(f.order_item_id) AS order_item_count,
        SUM(f.price) AS total_revenue,
        AVG(f.price) AS average_item_price
    FROM dbo.fact_sales AS f
    INNER JOIN dbo.dim_product AS p
        ON f.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.product_category_name,
        p.product_category_name_en
)
SELECT
    product_id,
    product_category_name,
    product_category_name_en,
    order_item_count,
    total_revenue,
    average_item_price,

    RANK() OVER (
        ORDER BY order_item_count DESC
    ) AS order_item_rank,

    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank

FROM product_sales;

-- ============================================================
-- 4. CUSTOMER — PERFORMANCE
-- Business questions:
--   - Most Valuable Customers
--   - Customer Order Frequency
--   - Customer Purchasing Behaviour
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_customer_performance
AS
WITH customer_sales AS
(
    SELECT
        c.customer_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        SUM(f.price) AS total_revenue,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.price) / NULLIF(COUNT(DISTINCT f.order_id), 0)
            AS average_order_value
    FROM dbo.fact_sales AS f
    INNER JOIN dbo.dim_customer AS c
        ON f.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state
)
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    total_revenue,
    total_orders,
    average_order_value,

    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS customer_revenue_rank

FROM customer_sales;

-- ============================================================
-- 5. STORE — OVERVIEW
-- Business questions:
--   - Store Overview
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_store_overview
AS
SELECT
    store_id,
    store_name,
    store_type,
    city,
    region,
    is_active
FROM dbo.dim_store;

-- ============================================================
-- 6. STORE — ACTIVE VS INACTIVE
-- Business questions:
--   - Active vs Inactive Stores
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_store_status
AS
SELECT
    is_active,
    COUNT(*) AS store_count
FROM dbo.dim_store
GROUP BY
    is_active;


-- ============================================================
-- 7. STORE — BY REGION
-- Business questions:
--   - Stores by Region
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_stores_by_region
AS
SELECT
    region,
    COUNT(*) AS store_count
FROM dbo.dim_store
GROUP BY
    region;


-- ============================================================
-- 8. STORE — BY TYPE
-- Business questions:
--   - Stores by Type
-- ============================================================

CREATE OR ALTER VIEW dbo.vw_stores_by_type
AS
SELECT
    store_type,
    COUNT(*) AS store_count
FROM dbo.dim_store
GROUP BY
    store_type;