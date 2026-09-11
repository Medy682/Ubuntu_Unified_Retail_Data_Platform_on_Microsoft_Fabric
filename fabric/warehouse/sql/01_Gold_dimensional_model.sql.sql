-- Gold — Create fact_sales

DROP TABLE IF EXISTS dbo.fact_sales;
CREATE TABLE dbo.fact_sales
AS
SELECT
    o.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    CAST(o.order_purchase_timestamp AS DATE) AS order_date,
    o.order_status,
    oi.price,
    oi.freight_value
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_orders AS o
INNER JOIN Retail_Data_Platform_Lakehouse.[2_silver].silver_order_items AS oi
    ON o.order_id = oi.order_id;

-- Gold — Validate fact_sales

SELECT COUNT(*) AS fact_sales_rows
FROM dbo.fact_sales;

-- Gold — Validate fact_sales grain

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(DISTINCT product_id) AS distinct_products
FROM dbo.fact_sales;

-- Gold — Inspect fact_sales

SELECT TOP 20 *
FROM dbo.fact_sales
ORDER BY order_date, order_id, order_item_id;

-- Gold — Validate customer dimension

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS distinct_customer_id,
    COUNT(DISTINCT customer_unique_id) AS distinct_customer_unique_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN customer_unique_id IS NULL THEN 1 ELSE 0 END) AS null_customer_unique_id
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_customers;

-- Gold — Validate customer uniqueness

SELECT
    customer_unique_id,
    COUNT(*) AS customer_record_count
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_customers
GROUP BY customer_unique_id
HAVING COUNT(*) > 1
ORDER BY customer_record_count DESC;


-- Gold — Create dim_customer

DROP TABLE IF EXISTS dbo.dim_customer;
CREATE TABLE dbo.dim_customer
AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_customers;

-- Gold — Validate dim_customer

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS distinct_customer_id,
    COUNT(DISTINCT customer_unique_id) AS distinct_customer_unique_id
FROM dbo.dim_customer;

-- Gold — Validate products

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS distinct_product_id,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id,
    SUM(CASE WHEN product_category_name_en IS NULL THEN 1 ELSE 0 END) AS null_category
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_products;

-- Gold — Create dim_product

DROP TABLE IF EXISTS dbo.dim_product;
CREATE TABLE dbo.dim_product
AS
SELECT
    product_id,
    product_category_name,
    product_category_name_en,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_products;

-- Gold — Validate dim_product

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS distinct_product_id,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id
FROM dbo.dim_product;

-- Gold — Validate stores

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT store_id) AS distinct_store_id,
    SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) AS null_store_id,
    SUM(CASE WHEN store_name IS NULL THEN 1 ELSE 0 END) AS null_store_name,
    SUM(CASE WHEN store_type IS NULL THEN 1 ELSE 0 END) AS null_store_type,
    SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END) AS null_city,
    SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS null_region
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_stores;

-- Gold — Create dim_store

DROP TABLE IF EXISTS dbo.dim_store;
CREATE TABLE dbo.dim_store
AS
SELECT
    store_id,
    store_name,
    store_type,
    city,
    region,
    is_active
FROM Retail_Data_Platform_Lakehouse.[2_silver].silver_stores;


-- Gold — Validate dim_store

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT store_id) AS distinct_store_id,
    SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) AS null_store_id
FROM dbo.dim_store;


-- Gold — Validate sales date range

SELECT
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date,
    COUNT(DISTINCT order_date) AS distinct_sales_dates
FROM dbo.fact_sales;


-- Gold — Create dim_date

DROP TABLE IF EXISTS dbo.dim_date;
CREATE TABLE dbo.dim_date
AS
SELECT
    CAST(DATEADD(DAY, value, '2016-10-04') AS DATE) AS date_key,
    YEAR(DATEADD(DAY, value, '2016-10-04')) AS year,
    DATEPART(QUARTER, DATEADD(DAY, value, '2016-10-04')) AS quarter,
    MONTH(DATEADD(DAY, value, '2016-10-04')) AS month,
    CAST(DATENAME(MONTH, DATEADD(DAY, value, '2016-10-04')) AS VARCHAR(20)) AS month_name,
    DATEPART(WEEK, DATEADD(DAY, value, '2016-10-04')) AS week_of_year,
    DAY(DATEADD(DAY, value, '2016-10-04')) AS day_of_month,
    CAST(DATENAME(WEEKDAY, DATEADD(DAY, value, '2016-10-04')) AS VARCHAR(20)) AS day_name,
    CASE
        WHEN DATEDIFF(DAY, '1900-01-01',
             DATEADD(DAY, value, '2016-10-04')) % 7 IN (5, 6)
        THEN 0
        ELSE 1
    END AS is_weekday
FROM GENERATE_SERIES(0, 694);


-- Gold — Validate dim_date

SELECT
    COUNT(*) AS total_dates,
    MIN(date_key) AS min_date,
    MAX(date_key) AS max_date
FROM dbo.dim_date;
