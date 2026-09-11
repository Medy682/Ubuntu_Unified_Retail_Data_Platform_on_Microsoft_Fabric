# Gold Data Dictionary
## Ubuntu Unified Retail Data Platform
### Microsoft Fabric

---

## 1. Gold Layer Overview

The Gold layer is implemented in a **Microsoft Fabric Warehouse** and provides the curated analytical layer of the Ubuntu Unified Retail Data Platform.

The Gold layer contains:

- Dimensional tables for analytical modelling
- Business-oriented analytical views
- Validated relationships and data quality checks

The main Brazilian retail model follows a dimensional structure:

```text
                 dim_customer
                      │
                      │
dim_product ───── fact_sales ───── dim_date


                 dim_store
              (independent)
```

`dim_store` is intentionally independent from `fact_sales` because the available store data does not contain a relationship to the sales fact.

---

# 2. Gold Dimensional Model

## 2.1 fact_sales

### Purpose

The central fact table containing sales transaction-line information.

### Source

Built from:

- `silver_orders`
- `silver_order_items`

The two Silver tables are joined using `order_id`.

### Grain

**One row represents one order item within an order.**

### Columns

| Column | Description |
|---|---|
| `order_id` | Unique identifier of the customer order |
| `order_item_id` | Identifier of the individual order item |
| `customer_id` | Identifier of the customer associated with the order |
| `product_id` | Identifier of the product purchased |
| `seller_id` | Identifier of the seller associated with the order item |
| `order_date` | Order purchase date derived from `order_purchase_timestamp` |
| `order_status` | Current status of the order |
| `price` | Price of the individual order item |
| `freight_value` | Freight/shipping value associated with the order item |

### Analytical Role

`fact_sales` provides the measures used for:

- Revenue
- Orders
- Average Order Value
- Sales over time
- Product performance
- Customer performance

---

# 2.2 dim_customer

### Purpose

Provides customer attributes for analysing sales by customer and location.

### Source

`silver_customers`

### Grain

**One row represents one customer record identified by `customer_id`.**

### Columns

| Column | Description |
|---|---|
| `customer_id` | Customer identifier used to relate customers to sales |
| `customer_unique_id` | Unique identifier representing the customer |
| `customer_zip_code_prefix` | Customer postal-code prefix |
| `customer_city` | Customer city |
| `customer_state` | Customer state |

### Analytical Role

Used to analyse:

- Most Valuable Customers
- Customer Order Frequency
- Customer Purchasing Behaviour
- Customer sales by city and state

---

# 2.3 dim_product

### Purpose

Provides product attributes for product-level sales analysis.

### Source

`silver_products`

### Grain

**One row represents one product identified by `product_id`.**

### Columns

| Column | Description |
|---|---|
| `product_id` | Product identifier |
| `product_category_name` | Original product category |
| `product_category_name_en` | English product category |
| `product_name_length` | Length of the product name |
| `product_description_length` | Length of the product description |
| `product_photos_qty` | Number of product photos |
| `product_weight_g` | Product weight in grams |
| `product_length_cm` | Product length in centimetres |
| `product_height_cm` | Product height in centimetres |
| `product_width_cm` | Product width in centimetres |

### Analytical Role

Used for:

- Best-selling Products
- Highest-revenue Products
- Product performance
- Product category analysis
- Average Product Price

---

# 2.4 dim_date

### Purpose

Provides calendar attributes for time-based analysis.

### Source

Generated in the Gold Warehouse using a date range beginning on `2016-10-04`.

### Grain

**One row represents one calendar date.**

### Columns

| Column | Description |
|---|---|
| `date_key` | Calendar date |
| `year` | Calendar year |
| `quarter` | Calendar quarter |
| `month` | Numeric month |
| `month_name` | Month name |
| `week_of_year` | Week number within the year |
| `day_of_month` | Day of the month |
| `day_name` | Day name |
| `is_weekday` | Indicates whether the date is a weekday |

### Analytical Role

Supports:

- Sales over time
- Revenue trends
- Order trends
- Year/month/week/day analysis

---

# 2.5 dim_store

### Purpose

Provides information about retail stores.

### Source

`silver_stores`

### Grain

**One row represents one store identified by `store_id`.**

### Columns

| Column | Description |
|---|---|
| `store_id` | Store identifier |
| `store_name` | Store name |
| `store_type` | Type of store |
| `city` | Store city |
| `region` | Geographic region |
| `is_active` | Indicates whether the store is active |

### Analytical Role

Used for:

- Store Overview
- Active vs Inactive Stores
- Stores by Region
- Stores by Type

### Relationship Note

`dim_store` is intentionally independent from `fact_sales` because no store relationship is available in the Brazilian sales fact data.

---

# 3. Gold Analytical Views

The Gold Warehouse contains business-oriented SQL views built on top of the dimensional model.

---

## 3.1 vw_sales_kpi_summary

### Purpose

Provides a high-level sales KPI summary.

### Business Questions

- What is the Total Revenue?
- How many Total Orders are there?
- What is the Average Order Value?

### Key Outputs

| Column | Description |
|---|---|
| `total_revenue` | Total sales revenue |
| `total_orders` | Number of distinct orders |
| `average_order_value` | Total revenue divided by distinct orders |
| `total_freight` | Total freight value |

---

## 3.2 vw_sales_over_time

### Purpose

Provides daily sales performance.

### Business Questions

- How are Sales changing over Time?
- How is Revenue changing over Time?
- How are Orders changing over Time?

### Key Outputs

| Column | Description |
|---|---|
| `order_date` | Sales date |
| `total_revenue` | Revenue generated on the date |
| `total_orders` | Distinct orders on the date |
| `average_order_value` | Average revenue per order |

---

## 3.3 vw_product_performance

### Purpose

Provides aggregated product-level sales performance and rankings.

### Business Questions

- Which are the Best-selling Products?
- Which Products generate the Highest Revenue?
- What is the Average Product Price?

### Key Outputs

| Column | Description |
|---|---|
| `product_id` | Product identifier |
| `product_category_name` | Original product category |
| `product_category_name_en` | English product category |
| `order_item_count` | Number of order-item records for the product |
| `total_revenue` | Total revenue generated by the product |
| `average_item_price` | Average price of the product across order items |
| `order_item_rank` | Product ranking by order-item count |
| `revenue_rank` | Product ranking by total revenue |

### Ranking Note

`order_item_rank` identifies products with the highest number of order-item records.

`revenue_rank` identifies products with the highest total revenue.

Because the fact table is at **order-item grain** and does not contain a quantity field, `order_item_count` is used to identify the most frequently ordered products.

---

# 3.4 vw_customer_performance

### Purpose

Provides aggregated customer-level sales performance and revenue ranking.

### Business Questions

- Who are the Most Valuable Customers?
- How frequently do customers place orders?
- What is Customer Purchasing Behaviour?

### Key Outputs

| Column | Description |
|---|---|
| `customer_id` | Customer identifier |
| `customer_unique_id` | Unique customer identifier |
| `customer_city` | Customer city |
| `customer_state` | Customer state |
| `total_revenue` | Total revenue generated by the customer |
| `total_orders` | Number of distinct orders placed by the customer |
| `average_order_value` | Average revenue per order |
| `customer_revenue_rank` | Customer ranking by total revenue |

### Ranking Note

`customer_revenue_rank` identifies customers generating the highest total revenue.

---

# 3.5 vw_store_overview

### Purpose

Provides a complete overview of stores.

### Business Question

- What stores exist and what are their characteristics?

### Key Outputs

| Column | Description |
|---|---|
| `store_id` | Store identifier |
| `store_name` | Store name |
| `store_type` | Store type |
| `city` | Store city |
| `region` | Geographic region |
| `is_active` | Store active status |

---

# 3.6 vw_store_status

### Purpose

Aggregates stores by active status.

### Business Question

- How many stores are Active vs Inactive?

### Key Outputs

| Column | Description |
|---|---|
| `is_active` | Store status |
| `store_count` | Number of stores with that status |

---

# 3.7 vw_stores_by_region

### Purpose

Aggregates stores by geographic region.

### Business Question

- How many stores operate in each Region?

### Key Outputs

| Column | Description |
|---|---|
| `region` | Geographic region |
| `store_count` | Number of stores in the region |

---

# 3.8 vw_stores_by_type

### Purpose

Aggregates stores by store type.

### Business Question

- How many stores exist for each Store Type?

### Key Outputs

| Column | Description |
|---|---|
| `store_type` | Type of store |
| `store_count` | Number of stores of that type |

---

# 4. Business Questions Supported

## Sales

| Business Question | Gold Object |
|---|---|
| Total Revenue | `vw_sales_kpi_summary` |
| Total Orders | `vw_sales_kpi_summary` |
| Average Order Value | `vw_sales_kpi_summary` |
| Sales over Time | `vw_sales_over_time` |
| Revenue over Time | `vw_sales_over_time` |
| Orders over Time | `vw_sales_over_time` |

## Products

| Business Question | Gold Object |
|---|---|
| Best-selling Products | `vw_product_performance` |
| Highest-revenue Products | `vw_product_performance` |
| Average Product Price | `vw_product_performance` |

## Customers

| Business Question | Gold Object |
|---|---|
| Most Valuable Customers | `vw_customer_performance` |
| Customer Order Frequency | `vw_customer_performance` |
| Customer Purchasing Behaviour | `vw_customer_performance` |

## Stores

| Business Question | Gold Object |
|---|---|
| Store Overview | `vw_store_overview` |
| Active vs Inactive Stores | `vw_store_status` |
| Stores by Region | `vw_stores_by_region` |
| Stores by Type | `vw_stores_by_type` |

---

# 5. Gold Layer Validation

The Gold layer was validated using dedicated SQL validation scripts.

Validation includes:

- Fact table row counts
- Fact table grain
- Distinct orders and order items
- Customer uniqueness
- Product uniqueness
- Null-value checks
- Store uniqueness and null checks
- Sales date-range validation
- Dimension-to-fact relationship validation
- Analytical view output validation

The dimensional relationship validation confirms matching customer, product, and sales-date keys between the fact table and their corresponding dimensions.

---

# 6. Architectural Notes

- The Gold dimensional model is implemented in a **Microsoft Fabric Warehouse**.
- The core Brazilian retail model uses a dimensional structure consisting of a sales fact table and customer, product, and date dimensions.
- `dim_store` is maintained as an independent dimension because no relationship to `fact_sales` exists in the available dataset.
- Gold analytical views provide business-oriented aggregations and rankings on top of the dimensional model.
- Product and customer performance views use SQL window functions to provide explicit revenue/order rankings.
- The European POS dataset is independent of the Brazilian retail model and is not included in the Gold dimensional model.
- The European POS dataset can be consumed directly from its cleaned Silver-layer table for separate Power BI analysis without creating an unnecessary Gold Warehouse table.
