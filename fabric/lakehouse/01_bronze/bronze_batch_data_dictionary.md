# Bronze Data Dictionary

## Overview

The Bronze layer contains the ingested source datasets stored as Delta tables in the Microsoft Fabric Lakehouse.

The Bronze layer preserves the source structure while adding ingestion metadata for data lineage and traceability.

The Bronze layer currently contains **13 Delta tables**:

* **8 batch datasets**
* **5 reference datasets**

All Bronze tables include the following ingestion metadata:

* `_source_file`
* `_ingestion_timestamp`
* `_ingestion_date`

---

# Batch Data

## 1. Customers

**Bronze table:** `bronze.bronze_customers`

**Source:** `Files/batch/customers.csv`

**Purpose:** Contains customer identification and geographic information.

| Column                     | Data Type | Description                                                              | Key / Role            |
| -------------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `customer_id`              | string    | Unique identifier for a customer record.                                 | Primary key candidate |
| `customer_unique_id`       | string    | Identifier representing the unique customer across records.              | Business identifier   |
| `customer_zip_code_prefix` | integer   | Postal code prefix associated with the customer.                         | Attribute             |
| `customer_city`            | string    | City associated with the customer.                                       | Attribute             |
| `customer_state`           | string    | State associated with the customer.                                      | Attribute             |
| `_source_file`             | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp`     | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`          | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

## 2. Order Items

**Bronze table:** `bronze.bronze_order_items`

**Source:** `Files/batch/order_items.csv`

**Purpose:** Contains individual products and sellers associated with customer orders.

| Column                 | Data Type | Description                                                              | Key / Role              |
| ---------------------- | --------- | ------------------------------------------------------------------------ | ----------------------- |
| `order_id`             | string    | Identifier of the associated order.                                      | Foreign key candidate   |
| `order_item_id`        | integer   | Sequential identifier for an item within an order.                       | Composite key candidate |
| `product_id`           | string    | Identifier of the purchased product.                                     | Foreign key candidate   |
| `seller_id`            | string    | Identifier of the seller fulfilling the item.                            | Foreign key candidate   |
| `shipping_limit_date`  | timestamp | Deadline by which the seller should ship the item.                       | Date/time attribute     |
| `price`                | double    | Price of the purchased item.                                             | Measure                 |
| `freight_value`        | double    | Freight or shipping cost associated with the item.                       | Measure                 |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage            |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata          |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata          |

**Key consideration:** `order_id` + `order_item_id` can be treated as a composite key candidate.

---

## 3. Orders

**Bronze table:** `bronze.bronze_orders`

**Source:** `Files/batch/orders.csv`

**Purpose:** Contains order-level transaction and fulfillment information.

| Column                          | Data Type | Description                                                              | Key / Role            |
| ------------------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `order_id`                      | string    | Unique identifier for an order.                                          | Primary key candidate |
| `customer_id`                   | string    | Identifier of the customer who placed the order.                         | Foreign key candidate |
| `order_status`                  | string    | Current status of the order.                                             | Business attribute    |
| `order_purchase_timestamp`      | timestamp | Date and time when the order was placed.                                 | Date/time attribute   |
| `order_approved_at`             | timestamp | Date and time when the order payment was approved.                       | Date/time attribute   |
| `order_delivered_carrier_date`  | timestamp | Date when the order was handed to the carrier.                           | Date/time attribute   |
| `order_delivered_customer_date` | timestamp | Date when the order was delivered to the customer.                       | Date/time attribute   |
| `order_estimated_delivery_date` | timestamp | Estimated delivery date for the order.                                   | Date/time attribute   |
| `_source_file`                  | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp`          | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`               | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

## 4. Payments

**Bronze table:** `bronze.bronze_payments`

**Source:** `Files/batch/payments.csv`

**Purpose:** Contains payment information associated with customer orders.

| Column                 | Data Type | Description                                                              | Key / Role              |
| ---------------------- | --------- | ------------------------------------------------------------------------ | ----------------------- |
| `order_id`             | string    | Identifier of the associated order.                                      | Foreign key candidate   |
| `payment_sequential`   | integer   | Sequence number of a payment associated with an order.                   | Composite key candidate |
| `payment_type`         | string    | Payment method used for the order.                                       | Business attribute      |
| `payment_installments` | integer   | Number of installments used for the payment.                             | Measure                 |
| `payment_value`        | double    | Monetary value of the payment.                                           | Measure                 |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage            |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata          |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata          |

**Key consideration:** `order_id` + `payment_sequential` can be treated as a composite key candidate.

---

## 5. POS Sales Transactions

**Bronze table:** `bronze.bronze_pos_sales_transactions`

**Source:** `Files/batch/pos_sales_transactions.csv`

**Purpose:** Contains point-of-sale transaction information.

| Column                 | Data Type | Description                                                              | Key / Role             |
| ---------------------- | --------- | ------------------------------------------------------------------------ | ---------------------- |
| `Invoice`              | string    | Invoice or transaction identifier.                                       | Transaction identifier |
| `StockCode`            | string    | Product or stock identifier associated with the transaction.             | Product identifier     |
| `Description`          | string    | Description of the product.                                              | Attribute              |
| `Quantity`             | integer   | Number of units involved in the transaction.                             | Measure                |
| `InvoiceDate`          | timestamp | Date and time of the transaction.                                        | Date/time attribute    |
| `Price`                | double    | Unit price of the product.                                               | Measure                |
| `Customer ID`          | double    | Customer identifier associated with the transaction.                     | Foreign key candidate  |
| `Country`              | string    | Country associated with the transaction or customer.                     | Attribute              |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage           |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata         |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata         |

**Data quality consideration:** `Customer ID` contains a space and is stored as `double`. The column name and data type should be standardized during Silver transformation.

---

## 6. Products

**Bronze table:** `bronze.bronze_products`

**Source:** `Files/batch/products.csv`

**Purpose:** Contains product attributes and physical characteristics.

| Column                       | Data Type | Description                                                              | Key / Role            |
| ---------------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `product_id`                 | string    | Unique identifier for a product.                                         | Primary key candidate |
| `product_category_name`      | string    | Category assigned to the product.                                        | Business attribute    |
| `product_name_lenght`        | double    | Length of the product name.                                              | Measure               |
| `product_description_lenght` | double    | Length of the product description.                                       | Measure               |
| `product_photos_qty`         | double    | Number of photographs associated with the product.                       | Measure               |
| `product_weight_g`           | double    | Product weight in grams.                                                 | Measure               |
| `product_length_cm`          | double    | Product length in centimeters.                                           | Measure               |
| `product_height_cm`          | double    | Product height in centimeters.                                           | Measure               |
| `product_width_cm`           | double    | Product width in centimeters.                                            | Measure               |
| `_source_file`               | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp`       | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`            | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

**Data quality consideration:** `product_name_lenght` and `product_description_lenght` contain the source spelling `lenght`. These can be standardized to `product_name_length` and `product_description_length` in Silver.

---

## 7. Reviews

**Bronze table:** `bronze.bronze_reviews`

**Source:** `Files/batch/reviews.csv`

**Purpose:** Contains customer reviews and review-related information.

| Column                    | Data Type | Description                                                              | Key / Role            |
| ------------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `review_id`               | string    | Identifier for the review.                                               | Primary key candidate |
| `order_id`                | string    | Identifier of the order associated with the review.                      | Foreign key candidate |
| `review_score`            | string    | Customer rating or score associated with the review.                     | Business attribute    |
| `review_comment_title`    | string    | Title of the customer's review comment.                                  | Text attribute        |
| `review_comment_message`  | string    | Main text of the customer's review.                                      | Text attribute        |
| `review_creation_date`    | string    | Date associated with creation of the review.                             | Date attribute        |
| `review_answer_timestamp` | timestamp | Date and time when the review was answered.                              | Date/time attribute   |
| `_source_file`            | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp`    | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`         | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

**Data quality considerations:**

* `review_score` is currently stored as `string` and requires type standardization.
* `review_creation_date` is currently stored as `string` and requires date conversion.
* The source CSV contained blank and malformed records that require further Silver-layer investigation and validation.

---

## 8. Sellers

**Bronze table:** `bronze.bronze_sellers`

**Source:** `Files/batch/sellers.csv`

**Purpose:** Contains seller identification and geographic information.

| Column                   | Data Type | Description                                                              | Key / Role            |
| ------------------------ | --------- | ------------------------------------------------------------------------ | --------------------- |
| `seller_id`              | string    | Unique identifier for a seller.                                          | Primary key candidate |
| `seller_zip_code_prefix` | integer   | Postal code prefix associated with the seller.                           | Attribute             |
| `seller_city`            | string    | City associated with the seller.                                         | Attribute             |
| `seller_state`           | string    | State associated with the seller.                                        | Attribute             |
| `_source_file`           | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp`   | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`        | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

# Reference Data

## 9. Employees

**Bronze table:** `bronze.bronze_employees`

**Source:** `Files/reference/employees.csv`

**Purpose:** Contains employee and organizational reference information.

| Column                 | Data Type | Description                                                              | Key / Role            |
| ---------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `employee_id`          | string    | Unique identifier for an employee.                                       | Primary key candidate |
| `first_name`           | string    | Employee's first name.                                                   | Attribute             |
| `last_name`            | string    | Employee's last name.                                                    | Attribute             |
| `department`           | string    | Department in which the employee works.                                  | Business attribute    |
| `job_title`            | string    | Employee's job title.                                                    | Business attribute    |
| `store_id`             | string    | Store associated with the employee.                                      | Foreign key candidate |
| `hire_date`            | date      | Date the employee was hired.                                             | Date attribute        |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

## 10. Inventory Snapshots

**Bronze table:** `bronze.bronze_inventory_snapshots`

**Source:** `Files/reference/inventory_snapshots.csv`

**Purpose:** Contains periodic inventory levels for products at stores.

| Column                 | Data Type | Description                                                              | Key / Role              |
| ---------------------- | --------- | ------------------------------------------------------------------------ | ----------------------- |
| `snapshot_date`        | date      | Date on which the inventory snapshot was recorded.                       | Composite key candidate |
| `store_id`             | string    | Identifier of the store.                                                 | Foreign key candidate   |
| `product_id`           | string    | Identifier of the product.                                               | Foreign key candidate   |
| `stock_on_hand`        | integer   | Quantity of product currently available.                                 | Measure                 |
| `safety_stock_level`   | integer   | Minimum inventory level maintained as a safety buffer.                   | Measure                 |
| `stock_status`         | string    | Status describing the current inventory condition.                       | Business attribute      |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage            |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata          |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata          |

**Key consideration:** `snapshot_date` + `store_id` + `product_id` can be treated as a composite key candidate.

---

## 11. Promotions

**Bronze table:** `bronze.bronze_promotions`

**Source:** `Files/reference/promotions.csv`

**Purpose:** Contains promotional campaign and discount information.

| Column                 | Data Type | Description                                                              | Key / Role              |
| ---------------------- | --------- | ------------------------------------------------------------------------ | ----------------------- |
| `promotion_id`         | string    | Unique identifier for a promotion.                                       | Primary key candidate   |
| `campaign_name`        | string    | Name of the promotional campaign.                                        | Business attribute      |
| `discount_percentage`  | double    | Percentage discount associated with the promotion.                       | Measure                 |
| `marketing_channel`    | string    | Marketing channel through which the promotion is delivered.              | Business attribute      |
| `is_stackable`         | boolean   | Indicates whether the promotion can be combined with other promotions.   | Business rule attribute |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage            |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata          |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata          |

---

## 12. Stores

**Bronze table:** `bronze.bronze_stores`

**Source:** `Files/reference/stores.csv`

**Purpose:** Contains store identification, classification, location, and operational status.

| Column                 | Data Type | Description                                                              | Key / Role            |
| ---------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `store_id`             | string    | Unique identifier for a store.                                           | Primary key candidate |
| `store_name`           | string    | Name of the store.                                                       | Attribute             |
| `store_type`           | string    | Type or classification of the store.                                     | Business attribute    |
| `city`                 | string    | City where the store is located.                                         | Attribute             |
| `region`               | string    | Region associated with the store.                                        | Attribute             |
| `is_active`            | boolean   | Indicates whether the store is currently active.                         | Business attribute    |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

## 13. Suppliers

**Bronze table:** `bronze.bronze_suppliers`

**Source:** `Files/reference/suppliers.csv`

**Purpose:** Contains supplier identification and classification information.

| Column                 | Data Type | Description                                                              | Key / Role            |
| ---------------------- | --------- | ------------------------------------------------------------------------ | --------------------- |
| `supplier_id`          | string    | Unique identifier for a supplier.                                        | Primary key candidate |
| `supplier_name`        | string    | Name of the supplier.                                                    | Attribute             |
| `primary_category`     | string    | Main product category supplied by the supplier.                          | Business attribute    |
| `supplier_tier`        | string    | Classification or tier assigned to the supplier.                         | Business attribute    |
| `country`              | string    | Country associated with the supplier.                                    | Attribute             |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested.         | Data lineage          |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. | Audit metadata        |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer.             | Audit metadata        |

---

# Ingestion Metadata Reference

These technical metadata columns are added to every Bronze table during the ingestion process.

| Column                 | Data Type | Description                                                                                                                  |
| ---------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `_source_file`         | string    | Name/path of the source file from which the record was ingested. Used for data lineage and source traceability.              |
| `_ingestion_timestamp` | timestamp | Timestamp indicating when the record was ingested into the Bronze layer. Used for auditability and ingestion tracking.       |
| `_ingestion_date`      | date      | Date on which the record was ingested into the Bronze layer. Useful for partitioning, filtering, and operational monitoring. |

---

# Bronze Layer Summary

| #  | Dataset                | Type      | Bronze Table                           |
| -- | ---------------------- | --------- | -------------------------------------- |
| 1  | Customers              | Batch     | `bronze.bronze_customers`              |
| 2  | Order Items            | Batch     | `bronze.bronze_order_items`            |
| 3  | Orders                 | Batch     | `bronze.bronze_orders`                 |
| 4  | Payments               | Batch     | `bronze.bronze_payments`               |
| 5  | POS Sales Transactions | Batch     | `bronze.bronze_pos_sales_transactions` |
| 6  | Products               | Batch     | `bronze.bronze_products`               |
| 7  | Reviews                | Batch     | `bronze.bronze_reviews`                |
| 8  | Sellers                | Batch     | `bronze.bronze_sellers`                |
| 9  | Employees              | Reference | `bronze.bronze_employees`              |
| 10 | Inventory Snapshots    | Reference | `bronze.bronze_inventory_snapshots`    |
| 11 | Promotions             | Reference | `bronze.bronze_promotions`             |
| 12 | Stores                 | Reference | `bronze.bronze_stores`                 |
| 13 | Suppliers              | Reference | `bronze.bronze_suppliers`              |

**Bronze Layer Status: COMPLETE**

All 13 Bronze Delta tables have been successfully ingested and validated. Source/DataFrame row counts were compared against Bronze table row counts, ingestion metadata was verified, and table naming was confirmed.
