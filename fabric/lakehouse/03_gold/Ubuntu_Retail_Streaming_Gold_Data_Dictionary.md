# Streaming Gold Data Dictionary

## Overview

The Streaming Gold layer is the business-oriented analytical layer of the streaming branch of the Ubuntu Retail Group unified retail data platform.

The platform follows a unified **Bronze → Silver → Gold Medallion Architecture** for both batch and streaming workloads. The Gold stage has two different implementations because batch and streaming data have different processing and latency requirements:

- **Batch Gold:** Fabric Warehouse tables created with SQL/T-SQL.
- **Streaming Gold:** Lakehouse Delta tables maintained with PySpark Structured Streaming.

Therefore, the project does **not** contain two separate Medallion Architectures. It contains one logical Medallion Architecture with two Gold outputs/implementations.

The Streaming Gold layer continuously consumes the refined Streaming Silver data and produces business-ready near-real-time metrics for downstream analytics.

---

# 1. Position of Streaming Gold in the Medallion Architecture

The overall platform can be represented as:

```text
                    UNIFIED MEDALLION ARCHITECTURE

                         BRONZE
                            |
                  +---------+---------+
                  |                   |
                  v                   v
             Batch Silver       Streaming Silver
                  |                   |
                  v                   v
        Fabric Warehouse       Streaming Gold
                  |             Lakehouse / Delta
             Batch Gold        PySpark Structured
             SQL / T-SQL          Streaming
                  |                   |
                  +---------+---------+
                            |
                         Power BI
```

The Gold stage therefore has two outputs:

### Batch Gold Output
- Location: Fabric Warehouse
- Storage: Warehouse tables
- Processing: SQL/T-SQL
- Purpose: Business-ready analytics for batch workloads

### Streaming Gold Output
- Location: Fabric Lakehouse
- Storage: Delta tables
- Processing: PySpark Structured Streaming
- Purpose: Business-ready near-real-time analytics

Both outputs represent the **Gold stage** of the same overall Medallion-based platform.

---

# 2. Streaming Data Flow

The streaming branch follows this path:

```text
Python Event Simulator
        |
        v
Azure Event Hubs
        |
        v
Microsoft Fabric Eventstream
        |
        v
Lakehouse Bronze
        |
        v
PySpark Structured Streaming
        |
        v
Streaming Silver
        |
        v
PySpark Structured Streaming
        |
        v
Streaming Gold
        |
        v
Power BI
```

Streaming Gold does not ingest raw events directly. It consumes the already cleaned, validated, deduplicated, and enriched data produced by Streaming Silver.

---

# 3. Purpose of Streaming Gold

The purpose of Streaming Gold is to transform refined streaming events into **business-ready near-real-time metrics**.

Examples include:

- Event activity over time
- Event activity by event type
- Event activity by country
- Product views
- Cart actions
- Checkout starts
- Successful purchases
- Checkout-to-purchase conversion metrics
- Average processing delay

Streaming Gold is the bridge between **technical streaming data processing** and **business-facing analytics**.

---

# 4. Streaming Gold Tables

The Streaming Gold implementation contains three primary Delta tables.

## 4.1 `gold_streaming_event_metrics`

### Purpose

Provides near-real-time event volumes by event type and time window.

| Column | Data Type | Description |
|---|---|---|
| `event_minute` | TIMESTAMP | Start of the one-minute event-time window |
| `event_type` | STRING | Type of retail event |
| `event_count` | BIGINT | Number of events recorded within the window for the event type |

### Supported Event Types

- `product_view`
- `cart_action`
- `checkout_start`
- `purchase_success`
- `inventory_update`

This table can support Power BI visualizations such as events per minute, event volume trends, and event-type distribution.

---

## 4.2 `gold_streaming_country_metrics`

### Purpose

Provides a near-real-time view of streaming event activity by country.

| Column | Data Type | Description |
|---|---|---|
| `country` | STRING | Country associated with the event |
| `event_count` | BIGINT | Number of streaming events associated with the country |

This table can support country-level activity and geographic comparisons in Power BI.

---

## 4.3 `gold_streaming_realtime_kpis`

### Purpose

Provides business-oriented near-real-time KPIs derived from streaming events.

| Column | Data Type | Description |
|---|---|---|
| `event_minute` | TIMESTAMP | Start of the one-minute event-time window |
| `total_events` | BIGINT | Total number of streaming events in the window |
| `product_views` | BIGINT | Number of product view events |
| `cart_actions` | BIGINT | Number of cart action events |
| `checkout_starts` | BIGINT | Number of checkout start events |
| `purchases` | BIGINT | Number of successful purchase events |
| `checkout_to_purchase_rate` | DOUBLE | Ratio of successful purchases to checkout starts |
| `avg_processing_delay_seconds` | DOUBLE | Average processing delay for events in the window |

### KPI Definition

```text
checkout_to_purchase_rate =
successful purchases / checkout starts
```

When there are no checkout starts in a window, the metric is set to `0.0`.

This should be described as **checkout-to-purchase conversion**, rather than customer conversion, because the Streaming Silver dataset does not necessarily represent unique customers completing the entire funnel.

---

# 5. Streaming Gold Data Limitation

The unified Streaming Silver table does not contain the purchase-specific revenue attributes required to calculate streaming revenue metrics.

Therefore, Streaming Gold will **not invent or derive revenue metrics** from columns that are not present.

The current Streaming Gold implementation focuses only on metrics that can be correctly derived from the available streaming event data.

If streaming revenue analytics are required in the future, a dedicated purchase-specific Streaming Silver dataset containing attributes such as invoice ID, quantity, unit price, and total order value would be required.

---

# 6. Processing Technology

Streaming Gold is implemented using:

- **PySpark Structured Streaming**
- **Delta Lake**
- **Fabric Lakehouse**
- **Event-time windowing**
- **Watermarking**
- **Streaming aggregations**

The Streaming Gold process continuously reads from the Streaming Silver Delta table.

```text
Streaming Silver Delta
        |
        v
PySpark Structured Streaming
        |
        +--> Event Metrics
        |
        +--> Country Metrics
        |
        +--> Real-Time KPIs
        |
        v
Streaming Gold Delta Tables
```

---

# 7. Event-Time Processing

Streaming Gold uses the event timestamp from Streaming Silver for time-based aggregations.

The primary time window is a **one-minute event-time window**.

This allows the platform to calculate metrics such as:

- Events per minute
- Purchases per minute
- Product views per minute
- Checkout starts per minute

Using event time is important because the time an event occurred is different from the time the event was received or processed.

---

# 8. Watermarking

Streaming Gold uses a watermark based on the event timestamp.

The streaming pipeline uses a **10-minute watermark** to allow for late-arriving events while preventing streaming state from growing indefinitely.

---

# 9. Deduplication

Streaming Silver is responsible for event-level deduplication before the data reaches Streaming Gold.

Streaming Gold therefore operates on the refined Streaming Silver dataset rather than independently deduplicating raw events.

```text
Bronze
  |
  | Raw / minimally processed events
  v
Silver
  |
  | Cleaning, validation, enrichment,
  | watermarking and deduplication
  v
Gold
  |
  | Business aggregations and KPIs
  v
Power BI
```

---

# 10. Gold Layer Responsibility

The Streaming Gold layer is responsible primarily for **business aggregation and analytical readiness**, rather than raw data cleaning.

### Bronze
- Ingestion
- Raw event preservation
- Minimal standardization

### Silver
- Cleaning
- Validation
- Standardization
- Deduplication
- Event-time processing
- Enrichment

### Gold
- Business metrics
- Aggregations
- KPIs
- Analytical structures
- Near-real-time reporting

This separation follows the core purpose of the Medallion Architecture.

---

# 11. Batch Gold vs Streaming Gold

The project deliberately uses different technologies for the two Gold outputs.

| Aspect | Batch Gold | Streaming Gold |
|---|---|---|
| Processing type | Batch | Streaming |
| Location | Fabric Warehouse | Fabric Lakehouse |
| Storage | Warehouse tables | Delta tables |
| Processing technology | SQL/T-SQL | PySpark Structured Streaming |
| Update pattern | Batch refresh | Continuous / near-real-time |
| Primary purpose | Historical/business analytics | Near-real-time event analytics |
| Power BI | Batch semantic model | Streaming-focused analytics |

This is an intentional architectural choice rather than a duplication of the Gold layer.

---

# 12. Eventhouse / KQL Relationship to Streaming Gold

The platform also contains a separate **Eventhouse/KQL Real-Time Intelligence branch**.

This branch does **not** form another Bronze → Silver → Gold Medallion Architecture.

Instead, Eventstream routes the same incoming streaming events to Eventhouse as an additional destination.

```text
                         Fabric Eventstream
                                |
                   +------------+------------+
                   |                         |
                   v                         v
              Lakehouse                 Eventhouse
                   |                         |
                Bronze                       |
                   |                         |
                Silver                       |
                   |                         |
             Streaming Gold                 KQL
                   |                         |
                   |                  Real-Time Analytics
                   |                         |
                   +------------+------------+
                                |
                             Power BI
```

The Eventhouse branch is therefore a **complementary Real-Time Intelligence architecture**.

Its purpose is to demonstrate how Microsoft Fabric can ingest, store, query, and analyse streaming events using Eventhouse and KQL without forcing those events through the traditional Medallion layers.

---

# 13. Power BI Consumption

The project will use **one Power BI report** for the streaming analytics.

The report will contain two main streaming-focused pages.

## Page 1 — Streaming Gold

This page will consume the Streaming Gold Delta tables from the Lakehouse.

It will demonstrate business-oriented analytics produced by PySpark Structured Streaming.

Potential visuals include:

- Total events
- Events per minute
- Events by event type
- Events by country
- Product views
- Cart actions
- Checkout starts
- Purchases
- Checkout-to-purchase conversion
- Average processing delay

## Page 2 — Eventhouse / Real-Time Intelligence

This page will use the Eventhouse/KQL branch.

It will demonstrate real-time event analytics using queries such as:

- Events per minute
- Events by event type
- Events by country
- Purchases per minute
- Recent streaming events
- Average processing delay

The two pages demonstrate two different approaches to analysing streaming data within Microsoft Fabric.

---

# 14. Complete Streaming Architecture

```text
                    Python Event Simulator
                              |
                              v
                       Azure Event Hubs
                              |
                              v
                     Microsoft Eventstream
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          Lakehouse Bronze             Eventhouse
                 |                         |
                 v                         v
       PySpark Structured                KQL
          Streaming                    Queries
                 |
                 v
        Streaming Silver
                 |
                 v
       PySpark Structured
          Streaming
                 |
                 v
        Streaming Gold
         Delta Tables
                 |
                 v
              Power BI
```

The Eventhouse path operates in parallel with the Lakehouse streaming path.

---

# 15. Final Architecture Summary

The Ubuntu Retail Group platform uses **one unified Medallion Architecture** across its batch and streaming data-engineering workloads.

The architecture consists of:

### Batch

```text
Source CSV
   ↓
Lakehouse Bronze
   ↓
Lakehouse Silver
   ↓
Fabric Warehouse
   ↓
Batch Gold
   ↓
Power BI
```

### Streaming

```text
Event Simulator
   ↓
Azure Event Hubs
   ↓
Fabric Eventstream
   ↓
Lakehouse Bronze
   ↓
Streaming Silver
   ↓
Streaming Gold
   ↓
Power BI
```

### Real-Time Intelligence

```text
Event Simulator
   ↓
Azure Event Hubs
   ↓
Fabric Eventstream
   ↓
Eventhouse
   ↓
KQL
   ↓
Power BI
```

The key architectural principle is:

> **There is one logical Bronze → Silver → Gold Medallion Architecture, with separate batch and streaming implementations at the Gold stage.**

Batch Gold is implemented using **Fabric Warehouse and SQL/T-SQL**, while Streaming Gold is implemented using **Lakehouse Delta tables and PySpark Structured Streaming**.

Eventhouse/KQL is a **parallel complementary Real-Time Intelligence branch**, not another Medallion layer.

This design allows the platform to demonstrate batch data engineering, streaming data engineering, Delta Lake, PySpark, PySpark Structured Streaming, Fabric Warehouse, SQL/T-SQL, Event Hubs, Fabric Eventstream, Eventhouse, KQL, Power BI, near-real-time analytics, and Real-Time Intelligence within one unified platform.
