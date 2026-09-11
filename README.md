# Ubuntu Unified Retail Data Platform

> **An end-to-end simulated enterprise data engineering platform built with Microsoft Fabric, Python, PySpark and SQL to integrate heterogeneous retail, e-commerce, operational and real-time data sources into a trusted analytics environment.**

---

# 1. Project Overview

The **Ubuntu Unified Retail Data Platform** is a simulated enterprise data engineering project designed to demonstrate how a modern retail organization can integrate data from multiple operational systems, markets, sales channels and ingestion patterns into a centralized analytics platform.

The fictional organization, **Ubuntu Retail Group**, operates across multiple retail and e-commerce environments and has accumulated data from different source systems.

The platform integrates:

* European e-commerce sales transactions
* Brazilian e-commerce data
* Customers
* Orders
* Order Items
* Payments
* Products
* Sellers
* Customer Reviews
* Stores
* Employees
* Inventory
* Suppliers
* Promotions
* Simulated real-time business events

The platform uses **Microsoft Fabric and OneLake as the unified logical data lake and storage foundation**, with a **Fabric Lakehouse implementing the Medallion Architecture**:

**Bronze → Silver → Gold**

The project demonstrates both **batch and real-time data engineering patterns**.

Historical and reference datasets are prepared using Python and then processed within the Fabric Lakehouse.

The Medallion Architecture contains distinct batch and streaming paths:

* **Bronze (Batch):** lightweight PySpark preprocessing is performed where required before batch data is written as Delta tables.
* **Bronze (Streaming):** raw streaming events are written directly to a Bronze Delta table through Fabric Eventstream. No PySpark transformations are performed in this layer.
* **Silver (Batch):** comprehensive cleansing, transformation, standardization and validation are performed using PySpark.
* **Silver (Streaming):** streaming events are cleaned, validated, deduplicated and transformed using **PySpark Structured Streaming**, then written to the Silver streaming table.
* **Streaming Gold:** near-real-time business aggregations are produced using **PySpark Structured Streaming**.
* **Batch Gold:** validated Silver data is modelled using SQL and dimensional modelling principles, with analytical structures persisted in the Fabric Warehouse.

The real-time workload is simulated using existing project data. The `event_simulator.py` script generates events, which are sent through **Azure Event Hubs** and routed using **Microsoft Fabric Eventstream**. Eventstream writes the raw events directly to the Bronze Streaming Delta table and also routes the same events to **Microsoft Fabric Eventhouse** for real-time analytics.

The overall architecture is **Lakehouse-centric for data engineering**, while Eventhouse/KQL provides a complementary, purpose-built path for low-latency real-time analytics.

---

# 2. Business Context

Ubuntu Retail Group is a fictional multi-market retail organization operating across different sales channels and business functions.

As the organization has expanded, its data has become distributed across multiple operational systems.

These systems produce data with different structures, formats, geographic contexts and processing patterns.

The platform therefore simulates a realistic enterprise environment containing multiple data domains.

## European E-Commerce Operations

The **Online Retail II** public dataset represents historical European/UK e-commerce sales activity.

The existing project filename is:

`pos_sales_transactions.csv`

The filename is intentionally retained to maintain consistency with the existing project architecture.

Within the business context, however, the dataset is defined as:

**European E-Commerce Sales Transactions**

The dataset was reduced and prepared using Python before being ingested into Microsoft Fabric.

## Brazilian E-Commerce Operations

The **Olist Brazilian E-Commerce** dataset represents Ubuntu's Brazilian e-commerce operation.

It provides data relating to:

* Customers
* Orders
* Order Items
* Payments
* Products
* Reviews
* Sellers

## Operational Systems

Synthetic datasets generated using Python represent additional operational systems:

* Stores
* Employees
* Inventory
* Suppliers
* Promotions

## Real-Time Operations

The project also includes a simulated real-time streaming workload.

The `event_simulator.py` script generates real-time events from existing project data.

These events are sent to **Azure Event Hubs**, processed and routed through **Microsoft Fabric Eventstream**, and persisted into the **Bronze layer of the Fabric Lakehouse** and additionally in the eventhouse/kql database 

This allows the project to demonstrate how an enterprise platform can handle both historical batch workloads and continuously arriving event data.

---

# 3. Business Problem

Ubuntu Retail Group's data is fragmented across multiple source systems, markets and sales channels.

This makes it difficult for business users to obtain a consistent and trusted view of:

* Sales performance
* Customers
* Orders
* Products
* Payments
* Inventory
* Stores
* Suppliers
* Promotions
* Customer behaviour
* Real-time business activity

The organization therefore requires a modern data platform capable of integrating heterogeneous data sources, improving data quality, preserving business relationships and producing analytics-ready information.

The platform must support both **historical batch data** and **real-time operational events**.

---

# 4. Business Objectives

The platform aims to:

1. Centralize data from multiple retail and e-commerce source systems.
2. Integrate historical batch data with real-time event data.
3. Improve data quality and consistency.
4. Preserve relationships and referential integrity between business entities.
5. Standardize data types, formats and business rules.
6. Create trusted Silver-layer datasets.
7. Build a business-oriented Gold dimensional model.
8. Enable analysis across markets and sales channels.
9. Support inventory, supplier and promotional analysis.
10. Provide a foundation for Power BI reporting and business intelligence.
11. Demonstrate scalable modern data engineering practices using Microsoft Fabric.
12. Demonstrate practical use of Python, PySpark and SQL across different stages of the data lifecycle.
13. Demonstrate integration of batch and real-time data within a Lakehouse-centric architecture.

---

# 5. Key Business Questions

The platform is designed to help Ubuntu Retail Group answer questions such as:

## Sales

* What are total sales and revenue?
* Which products generate the most revenue?
* How are sales performing over time?
* Which markets and channels generate the most revenue?

## Customers

* Who are the most valuable customers?
* How do customer purchasing patterns differ by market?
* Which customers have the highest order frequency?

## Orders and Payments

* How many orders are processed?
* What are the most common payment methods?
* What is the average order value?
* How does payment behaviour vary across markets?

## Products

* Which products sell the most?
* Which products generate the highest revenue?
* Which products receive the best and worst reviews?

## Inventory and Supply Chain

* Which products require replenishment?
* What is the current inventory position?
* Which suppliers support the most products?
* Are inventory levels aligned with sales activity?

## Promotions

* Which promotions generate the most sales?
* How does promotional activity affect product performance?

## Real-Time Operations

* What business events are occurring in real time?
* How can streaming events be captured and persisted?
* How can real-time events be transformed for downstream analytics?
* How could Ubuntu support near-real-time operational monitoring?

---

# 6. Dataset Overview

The platform uses a combination of **public datasets and synthetically generated reference data**.

The datasets do not originate from one real company. Instead, they represent heterogeneous source systems within the simulated Ubuntu Retail Group environment.

## Public Source Data

### Online Retail II

The Online Retail II public dataset is used to represent Ubuntu's **European e-commerce sales channel**.

Existing project filename:

`pos_sales_transactions.csv`

Business interpretation:

**European E-Commerce Sales Transactions**

The dataset was reduced and prepared using Python before being ingested into Microsoft Fabric.

### Olist Brazilian E-Commerce

The Olist dataset represents Ubuntu's Brazilian e-commerce operation.

The project uses:

* `customers.csv`
* `orders.csv`
* `order_items.csv`
* `payments.csv`
* `products.csv`
* `reviews.csv`
* `sellers.csv`

The datasets were reduced and prepared using Python while preserving relationships between related entities.

## Synthetic Reference Data

Python was used to generate additional datasets required to simulate operational systems:

* `employees.csv`
* `inventory_snapshots.csv`
* `promotions.csv`
* `stores.csv`
* `suppliers.csv`

These datasets are explicitly synthetic.

## Simulated Real-Time Data

The project includes a simulated streaming workload.

The `event_simulator.py` script generates streaming events from existing project datasets.

This provides a controlled and reproducible way to demonstrate real-time ingestion without claiming that the events originate from an external production system.

The resulting events are sent through **Azure Event Hubs**, processed using **Microsoft Fabric Eventstream**, and routed to the **Bronze layer of the Fabric Lakehouse**.

---

# 7. Source Data Preparation

Before ingestion into Microsoft Fabric, the public datasets were prepared using Python.

## Python Preprocessing

Python was used to:

* Reduce the size of the public datasets.
* Select relevant data for the project.
* Prepare CSV files for ingestion.
* Preserve relationships between related datasets.
* Maintain key values required for referential integrity.
* Generate synthetic operational datasets.
* Generate simulated real-time events from existing project data.

The main preparation scripts are:

```text
scripts/
├── generate_sample_datasets.py
├── generate_reference_data.py
└── event_simulator.py
```

### `generate_sample_datasets.py`

Responsible for:

* Reducing the Online Retail II dataset.
* Reducing the Olist datasets.
* Preparing project-specific sample datasets.
* Preserving relationships and referential integrity between related tables.

### `generate_reference_data.py`

Generates synthetic operational reference data such as:

* Stores
* Employees
* Inventory
* Suppliers
* Promotions

### `event_simulator.py`

Generates simulated real-time events from existing project data for use by the streaming pipeline.

This demonstrates a real-time ingestion pattern while keeping the project reproducible and self-contained.

## Dataset Reduction

The original public datasets were larger than necessary for the scope of the portfolio project.

Python was therefore used to create project-specific subsets while retaining representative business activity.

## Referential Integrity

When reducing related Olist datasets, care was taken to preserve relationships between entities.

For example:

**Customer → Order → Order Item → Product**

These relationships are subsequently validated during Silver-layer processing.

---

# 8. Data Architecture

The platform is built using **Microsoft Fabric**, with **OneLake as the central data storage foundation**.

The Fabric Lakehouse provides the primary data-engineering environment.

The Lakehouse implements the logical Medallion Architecture:

**Bronze → Silver → Gold**

```text
                         MICROSOFT FABRIC
                                │
                              OneLake
                                │
                       Fabric Lakehouse
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
     BRONZE                  SILVER                   GOLD
        │                       │                       │
   ┌────┴────┐             ┌────┴────┐             ┌────┴────┐
   │         │             │         │             │         │
  Batch   Streaming       Batch   Streaming       Batch   Streaming
  Ingest   Ingest         ELT      Processing     ELT      Processing
   │         │             │         │             │         │
   │         │             │    PySpark            │    PySpark
   │         │             │    Structured         │    Structured
   │         │             │    Streaming          │    Streaming
   │         │             │         │             │         │
   └────┬────┘             └────┬────┘             └────┬────┘
        │                       │                       │
        ▼                       ▼                       ▼
   Bronze tables          Silver tables           Gold tables
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                         Semantic Models
                                │
                                ▼
                             Power BI

```

## OneLake

**OneLake** provides the unified logical data lake and storage foundation for the Microsoft Fabric environment.

It acts as the unified storage layer for the platform's data assets.

## Fabric Lakehouse

The **Fabric Lakehouse** provides the primary data-engineering environment.

The Lakehouse implements the logical Medallion Architecture with separate batch and streaming paths:

**Batch:** Bronze (Batch) → Silver (Batch) → Batch Gold / Fabric Warehouse

**Streaming:** Bronze (Streaming) → Silver (Streaming) → Streaming Gold

## Bronze Layer

The Bronze layer preserves source data close to its incoming form.

### Bronze (Batch)

Batch data may receive lightweight PySpark preprocessing where required before being written to Bronze Delta tables.

### Bronze (Streaming)

Streaming Bronze is a raw landing layer. **No PySpark transformations are performed here.**

The flow is:

**Azure Event Hubs → Fabric Eventstream → Bronze Streaming Delta table**

Bronze Streaming contains:

* Raw streaming events
* Eventstream → Lakehouse routing
* Write to Bronze streaming table

## Silver Layer

The Silver layer contains cleaned, standardized, validated and business-rule-compliant data.

### Silver (Batch)

PySpark performs the primary batch transformation and data-quality processing, including:

* Data profiling
* Cleaning
* Type conversion
* Deduplication
* Standardization
* Foreign-key validation
* Data-quality validation
* Business-rule validation

### Silver (Streaming)

Streaming Silver uses **PySpark Structured Streaming** for continuous transformation and validation.

Processing includes:

* Cleaned, validated and deduplicated data
* Business rules applied
* Extensive streaming transformations
* Write to Silver streaming table

## Gold Layer

The Gold layer contains business-ready analytical outputs.

### Batch Gold

Batch Gold uses SQL and dimensional modelling for:

* Fact tables
* Dimension tables
* Business-oriented views
* Analytical queries
* Aggregations
* Curated reporting structures

Batch Gold is also represented in the **Microsoft Fabric Warehouse**.

### Streaming Gold

Streaming Gold is maintained in the Lakehouse and uses **PySpark Structured Streaming** to create:

* Near-real-time aggregations
* Business-ready streaming data
* Real-time KPI outputs
* Event-oriented analytical metrics

# 9. CRISP-DM Methodology

The project follows the **CRISP-DM methodology**.

## 1. Business Understanding

Define Ubuntu Retail Group's business context, business problems, objectives and analytical requirements.

## 2. Data Understanding

Explore and profile the available datasets.

This includes understanding:

* Data structures
* Data types
* Relationships
* Missing values
* Duplicates
* Invalid values
* Geographic context
* Business meaning
* Data-quality issues

## 3. Data Preparation

Prepare source data using Python and perform further processing within the Fabric Lakehouse using PySpark.

## 4. Modelling

Use SQL and dimensional modelling principles to transform validated Silver data into business-ready Gold structures.

## 5. Evaluation

Evaluate:

* Data quality
* Referential integrity
* Business rules
* Transformation accuracy
* KPI correctness
* Model integrity
* Analytical usefulness

## 6. Deployment

Deploy the solution using Microsoft Fabric pipelines, Lakehouse structures, semantic models, Power BI and supporting engineering practices.

---

# 10. Microsoft Fabric Architecture

Microsoft Fabric is the primary platform used to implement the solution.

Key components include:

* Microsoft Fabric
* OneLake
* Fabric Lakehouse
* Fabric Notebooks
* PySpark
* SQL
* Data Pipelines
* Azure Event Hubs
* Fabric Eventstream
* Semantic Models
* Power BI

The architecture supports both batch and real-time workloads.

## Batch Architecture

```text
CSV Sources
    ↓
Python Preparation
    ↓
Batch Ingestion
    ↓
Fabric Lakehouse
    ↓
Bronze Layer
    ↓
PySpark Minimal Processing
    ↓
Bronze Delta Tables
    ↓
PySpark Transformations & Validation
    ↓
Silver Delta Tables
    ↓
SQL Dimensional Modelling
    ↓
Gold
```

The distinction between Bronze and Silver processing is intentional:

### Bronze

**Minimal PySpark processing**

* Lightweight preprocessing
* Required standardization
* Preparation for Delta-table creation
* Writing batch data into Bronze Delta tables

### Silver

**Comprehensive PySpark processing**

* Cleansing
* Transformation
* Standardization
* Deduplication
* Validation
* Business rules
* Referential integrity

## Real-Time Architecture

```text
Existing Project Data
        ↓
event_simulator.py
        ↓
Simulated Real-Time Events
        ↓
Azure Event Hubs
        ↓
Fabric Eventstream
        ├──────────────→ Bronze (Streaming)
        │                    ↓
        │             PySpark Structured Streaming
        │                    ↓
        │             Silver (Streaming)
        │                    ↓
        │             PySpark Structured Streaming
        │                    ↓
        │             Streaming Gold
        │
        └──────────────→ Fabric Eventhouse / KQL
                             ↓
                    Real-Time Analytics
```

### Real-Time Data Processing Strategy

Real-time events are ingested through **Azure Event Hubs** and routed using **Microsoft Fabric Eventstream**.

The raw events are written directly to the **Bronze Streaming Delta table**. No transformation is performed in the Bronze Streaming layer.

Downstream, **PySpark Structured Streaming** processes the Bronze Streaming data into the Silver Streaming layer, where cleansing, validation, deduplication and business transformations are applied. The same streaming processing pattern is then used to produce the Streaming Gold analytical outputs.

In parallel, the event stream is routed to **Microsoft Fabric Eventhouse**, where KQL provides a purpose-built environment for interactive real-time analytics.

This creates the following division:

**Event Hubs + Eventstream → Streaming ingestion and routing**

**PySpark Structured Streaming → Streaming transformation and analytical engineering**

**Eventhouse + KQL → Low-latency real-time analytics**

**SQL → Batch Gold dimensional modelling and analytical querying**

**Power BI → Business consumption and visualization**

# 11. Real-Time Architecture Decision

The project uses **Azure Event Hubs** and **Microsoft Fabric Eventstream** as the streaming ingestion and routing layer.

The streaming workflow is:

**Python Event Simulator → Azure Event Hubs → Fabric Eventstream**

From Eventstream, the same events are routed to two complementary destinations:

**Eventstream → Bronze Streaming Delta table**

**Eventstream → Fabric Eventhouse / KQL**

The **Lakehouse path** is used for streaming data engineering. Raw events land directly in Bronze Streaming, then **PySpark Structured Streaming** performs the Silver and Gold transformations.

The **Eventhouse path** is used for specialized real-time analytics. Eventhouse/KQL provides a purpose-built environment for interactive analysis of continuously arriving event data and complements the Lakehouse medallion pipeline.

This results in a deliberate hybrid architecture:

**OneLake → Fabric Lakehouse → Bronze → Silver → Streaming Gold**

for governed streaming data engineering, alongside:

**Eventstream → Eventhouse / KQL**

for real-time analytics.

# 12. Data Quality Framework

The Silver layer contains a reusable data-quality and validation framework.

Checks include, where applicable:

* Null values
* Blank values
* Duplicate records
* Data types
* Invalid values
* Value ranges
* Date validity
* Primary-key integrity
* Foreign-key integrity
* Business rules

The objective is to prevent invalid or unreliable data from propagating into the Gold analytical layer.

---

# 13. Silver Layer Transformations

The Silver layer is implemented primarily using PySpark.

Each dataset follows a repeatable workflow:

### 1. Profile

Understand the incoming Bronze DataFrame.

### 2. Define Rules

Identify data-quality requirements and business rules.

### 3. Transform

Clean, standardize and transform the data.

### 4. Validate

Execute data-quality and business-rule checks.

### 5. Write

Persist the validated DataFrame as a Silver Delta table.

### 6. Verify

Confirm that the Silver table was successfully written and contains the expected data.

Current Silver-layer workflow:

* Customers — Completed
* Order Items — Completed
* Orders — Completed
* Payments — Completed
* Products — Completed
* Reviews — Completed
* Sellers — Completed
* E-Commerce Sales Transactions — Completed
* Stores — Completed
* Employees — Completed
* Inventory — Completed
* Promotions — Completed
* Suppliers — Completed

---

# 14. Gold Layer & Dimensional Data Modelling

The Gold layer transforms validated Silver datasets into business-oriented analytical structures.

**SQL is the primary modelling language for the Gold layer.**

Dimensional modelling principles are used to create appropriate fact and dimension structures.

Potential dimensions include:

* `dim_customer`
* `dim_product`
* `dim_date`
* `dim_store`
* `dim_employee`
* `dim_supplier`
* `dim_promotion`
* `dim_seller`
* `dim_market`
* `dim_channel`

Potential facts include:

* `fact_sales`
* `fact_orders`
* `fact_payments`
* `fact_inventory`
* `fact_reviews`
* `fact_promotions`

The final Gold model will be determined by the business requirements and relationships established during the Data Understanding and Data Preparation stages.

The Gold layer will provide the foundation for the semantic model and Power BI analytics.

---

# 15. Orchestration

The platform uses Microsoft Fabric Data Factory Pipelines to orchestrate the batch ELT workflow, coordinating the execution and dependencies across the platform.

The orchestration process coordinates:

1.Source ingestion
2.Bronze loading
3.Silver transformations and data-quality validation
4.Gold transformations and data-quality validation
5.Downstream analytical processing

Data-quality checks are embedded within the relevant PySpark notebooks and SQL processing, allowing data to be validated as it moves through the transformation layers rather than relying solely on a separate validation step.

For streaming, PySpark Structured Streaming continuously processes incoming events, so the streaming processing loop does not need to be repeatedly triggered by the batch orchestration pipeline.

The platform also includes a separate low-latency Real-Time Intelligence path using Eventhouse and KQL Database, which provides near-real-time event analytics without requiring Fabric Data Factory to orchestrate each incoming event.

Note: Streaming workloads can still have operational orchestration for activities such as deployment, lifecycle management, and recovery. However, this platform does not use Fabric Data Factory to repeatedly trigger the continuous streaming processing loop or individual incoming events.

The overall platform combines:

**Scheduled Batch Processing + Continuous Streaming**

---

---

# 16. Monitoring

Monitoring focuses on pipeline reliability, data quality and processing health.

Key monitoring areas include:

* Pipeline success/failure
* Data ingestion status
* Transformation failures
* Record counts
* Data-quality failures
* Streaming activity
* Processing latency
* Missing data
* Unexpected data volumes

The objective is to make pipeline and data-quality issues visible and actionable.

---

# 17. Security

Security considerations include:

* Workspace permissions
* Access control
* Data access
* Credential management
* Secure connection handling
* Separation of development and production environments

Sensitive credentials should not be stored directly in notebooks, source code or version-controlled files.

---

# 18. CI/CD

The project incorporates source control and deployment practices where applicable.

The repository includes GitHub Actions workflows for:

* Continuous Integration
* Continuous Deployment
* Security scanning

The objective is to demonstrate:

* Version control
* Automated validation
* Data testing
* Security checks
* Reproducible transformations
* Controlled deployment

---

# 19. Power BI / Analytics

The Gold layer provides the foundation for Power BI analytics.

Potential dashboards include:

## Sales Performance

* Revenue
* Orders
* Average Order Value
* Sales trends
* Product performance

## Customer Analytics

* Customer distribution
* Customer purchasing behaviour
* Customer value
* Customer segmentation

## Product Analytics

* Product revenue
* Product quantity

## Operations

* Inventory
* Stores
* Suppliers
* Promotions

## Real-Time Analytics

The project includes a **Retail Streaming Analytics** Power BI experience over the Streaming Gold outputs, exposing real-time-oriented KPIs and event activity.

The project also uses **Fabric Eventhouse / KQL** as a complementary path for interactive real-time event analytics.

---

# 20. Key Insights

This section will document the business insights discovered after completion of the Gold layer and analytical model.

Potential insights include:

* Highest-performing products
* Highest-value customers
* Revenue by market
* customer_average_order_value
* orders status and orders by country
* Real-time operational activity

This section will be completed after the analytical layer has been developed.

---

# 21. Technologies Used

## Data Platform

* Microsoft Fabric
* OneLake
* Fabric Lakehouse
* Delta Lake

## Data Engineering

* Python
* pandas
* PySpark
* SQL

## Data Modelling

* SQL
* Dimensional Modelling
* Star Schema
* Fact Tables
* Dimension Tables

## Real-Time Data

* Python Event Simulation
* Azure Event Hubs
* Microsoft Fabric Eventstream
* Fabric Lakehouse
* Real-Time Event Processing

## Analytics

* Power BI
* Semantic Models

## Engineering & DevOps

* Git
* GitHub Actions
* CI/CD
* Automated Testing
* Security Scanning
* Docker

## Methodologies

* CRISP-DM
* Medallion Architecture
* Data Quality Framework

---

# 22. Project Repository Structure

```text
Ubuntu-Unified-Retail-Data-Platform/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       ├── dbt_tests.yml
│       └── security_scan.yml
│
├── architecture/
│   └──images/ 
│        └──Ubuntu_Unified_Retail_Project_Architecture.md
│   
├── config/
│   ├── config.yml
│   ├── logging.yml
│   └── settings.py
│
├── data/
│   ├── original/
│   ├── batch/
│   ├── reference/
│   └── streaming/
│   
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── entrypoint.sh
│
├── docs/
│     └── gold_layer
│          └── batch_gold_data_dictionary.md
│      
├── fabric/
│   ├── data_factory/
│   │   └── pipelines/
│   │
│   ├── lakehouse/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   │
│   ├── notebooks/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   │
│   ├── warehouse/
│   ├── power_bi/
│   └── monitoring/
│
├── ingestion/
│   ├── connectors/
│   ├── loaders/
│   └── config/
│
├── scripts/
│   ├── bootstrap_project.py
│   ├── generate_sample_datasets.py
│   ├── generate_reference_data.py
│   ├── event_simulator.py
│   └── utilities.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── data_quality/
│   └── performance/
│
├── logs/
│   ├── generate_sample_datasets.log
│   ├── generate_reference_data.log
│   └── event_simulator.log
│
├── .gitignore
├── Makefile
├── README.md
├── requirements.txt
└── LICENSE
```

### Repository Structure Rationale

The repository separates the project into clear engineering concerns:

* `.github/` — CI/CD and automated engineering workflows.
* `architecture/` — Architecture diagrams and visual documentation.
* `config/` — Central configuration and logging settings.
* `data/` — Original, prepared, reference, streaming and output data.
* `docker/` — Containerization configuration.
* `docs/` — Supporting project documentation and runbooks.
* `fabric/` — Microsoft Fabric implementation artifacts.
* `ingestion/` — Reusable ingestion components and connectors.
* `sql/` — Gold-layer SQL modelling and analytical queries.
* `scripts/` — Dataset preparation, synthetic-data generation and event simulation.
* `tests/` — Unit, integration, data-quality and performance tests.
* `logs/` — Runtime and pipeline logs.

The structure is intentionally modular and reflects the separation of source preparation, ingestion, transformation, modelling, testing, orchestration and deployment concerns in an enterprise-style data engineering project.

---

# 23. Lessons Learned

This project is designed to demonstrate practical lessons in modern data engineering, including:

* Working with heterogeneous data sources.
* Preparing public datasets for engineering workloads.
* Reducing datasets while preserving referential integrity.
* Designing Bronze, Silver and Gold layers.
* Using PySpark for Bronze and Silver for batch path and pyspark structured streaming for silver and gold for stream path data engineering.
* Using SQL for dimensional modelling.
* Integrating batch and streaming data.
* Simulating real-time events from existing datasets.
* Using Azure Event Hubs and Fabric Eventstream.
* Designing a Lakehouse-centric streaming architecture.
* Evaluating and using Eventhouse as a complementary real-time analytics destination.
* Designing business-oriented data models.
* Building reliable data pipelines.
* Applying data-quality frameworks.
* Connecting technical implementation to business requirements.
* Applying CI/CD and automated testing practices.
* Designing a data platform around a realistic enterprise scenario.

---

# 24. Future Improvements

Potential future enhancements include:

* More advanced incremental processing.
* Additional real-time event sources.
* Automated data-quality testing.
* More comprehensive monitoring.
* Enhanced CI/CD automation.
* Data lineage improvements.
* Advanced security and governance.
* Slowly Changing Dimensions.
* Additional Gold-layer business models.
* Advanced Power BI analytics.
* Performance optimization.
* Partitioning strategies.
* Production-style deployment patterns.
* Further optimization of Eventhouse/KQL for workloads requiring specialized low-latency real-time analytics.

---

# Project Methodology & Architecture Summary

The project combines **CRISP-DM**, **Microsoft Fabric Medallion Architecture**, batch processing, real-time streaming and multiple data-engineering technologies.

```text
                                                       CRISP-DM
                                    │
                                    ▼
                        Business Understanding
                                    │
                                    ▼
                          Data Understanding
                                    │
                                    ▼
                           Data Preparation
                                    │
                                    ▼
                        Python Source Scripts
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
             Dataset Preparation  Reference Data  Event Simulation
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                                    ▼
                           Microsoft Fabric
                                    │
                                  OneLake
                                    │
                                    ▼
                            Fabric Lakehouse
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                   BATCH                       STREAMING
                     │                             │
                     ▼                             ▼
                  BRONZE                         BRONZE
                     │                             │
            Minimal Processing             Event Data Landing
                     │                             │
                     ▼                             ▼
                  PySpark                 PySpark Structured
                     │                        Streaming
                     │                             │
          Clean / Transform /             Clean / Transform /
          Validate / Standardize          Validate / Standardize /
                                         Deduplicate
                     │                             │
                     ▼                             ▼
                  SILVER                         SILVER
                     │                             │
                     │                             ▼
                     │                    PySpark Structured
                     │                        Streaming
                     │                             │
                     │                    Gold Transformations /
                     │                    Aggregations /
                     │                    Business Logic
                     │                             │
                     ▼                             ▼
              GOLD / WAREHOUSE                STREAMING GOLD
                     │                             │
                SQL / Fabric                        │
                 Warehouse                           │
                     │                               │
             ┌───────┼────────┐                      │
             │       │        │                      │
           Facts  Dimensions  Views                   │
             │       │        │                      │
             └───────┼────────┘                      │
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                          DIRECT LAKE SEMANTIC
                                MODELS
                                     │
                                     ▼
                                  POWER BI
```

## Final Project Objective

The **Ubuntu Unified Retail Data Platform** demonstrates the design and implementation of a modern enterprise-style data platform capable of integrating heterogeneous **batch and simulated real-time data sources**, applying systematic data-quality and transformation processes, modelling trusted business data using **SQL and dimensional modelling**, and delivering analytics-ready information using **Microsoft Fabric**.

The project uses:

**Python → Source Data Preparation, Dataset Generation & Event Simulation**

**OneLake → Central Data Storage Foundation**

**Fabric Lakehouse → Unifed logical data lake and storage foundation**

**PySpark → Batch Bronze Processing + Batch  Silver Transformation & Validation**

**PySpark Structured Streaming → Streaming Silver & Streaming Gold Processing**

**Azure Event Hubs → Real-Time Event Ingestion**

**Fabric Eventstream → Real-Time Event Routing**

**Fabric Eventhouse / KQL → Purpose-Built Real-Time Analytics**

**SQL → Batch Gold Dimensional Modelling & Analytical Queries**

**Power BI → Analytics & Business Intelligence**

The architecture intentionally follows a **Lakehouse-centric data-engineering design** for batch and streaming workloads, while Eventhouse provides a complementary real-time analytics path.

The streaming architecture is:

**Event Simulator → Event Hubs → Eventstream → Bronze Streaming → PySpark Structured Streaming → Silver Streaming → Streaming Gold**

with the same event stream also routed to:

**Eventstream → Eventhouse / KQL**

This project therefore demonstrates not only individual technology skills, but the ability to design an integrated, business-driven and enterprise-style data engineering platform using both batch and streaming patterns.



                    STREAMING BRONZE
                           │
                           ▼
              bronze_streaming_events
                           │
                           ▼
              PySpark Structured Streaming
                           │
             Clean / Validate / Standardize /
                    Deduplicate
                           │
                           ▼
                  STREAMING SILVER
                           │
                           ▼
              silver_streaming_events
                           │
                           ▼
              PySpark Structured Streaming
                           │
            Gold Transformations /
             Aggregations / Metrics
                           │
                           ▼
                  STREAMING GOLD
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Event Metrics  Country Metrics  Real-Time KPIs
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
              STREAMING GOLD SEMANTIC
                       MODEL
                           │
                           ▼
                        POWER BI



## NB. 🧪 Testing and Data Quality

The platform's transformation notebooks were developed, executed, and validated in Microsoft Fabric using PySpark. Data-quality validation is embedded directly within the transformation workflows to ensure data integrity throughout the pipeline.

Validation includes:

- Null and missing value checks
- Duplicate record detection
- Data-type validation
- Referential integrity and foreign-key validation
- Business-rule validation
- Row-count and record-level consistency checks
- Post-write validation of transformed Silver data

Automated **unit and integration testing frameworks** were considered as an additional software-engineering practice. However, given the extensive validation already implemented and executed within the Fabric PySpark transformation workflows, a separate automated testing framework was not included in the current implementation.

This keeps the testing approach proportional to the project's architecture while ensuring that the data transformations and resulting datasets are thoroughly validated.

## NB. 🔄 Reproducible Data Generation with Docker

Docker is used to make the project's Python data-generation environment reproducible and portable. The generated batch and reference datasets are intentionally excluded from version control; instead, the repository contains the original source data, Python generation scripts, Docker configuration, and dependencies required to recreate them.

An engineer can clone the repository, build the Docker environment using Docker Compose, and execute the same generation scripts to reproduce the datasets locally


# Build the Docker environment
docker compose -f docker/docker-compose.yml build

# Generate batch datasets
docker compose -f docker/docker-compose.yml run --rm retail-platform python scripts/generate_sample_datasets.py

# Generate reference datasets
docker compose -f docker/docker-compose.yml run --rm retail-platform python scripts/generate_reference_data.py


The resulting 8 batch CSV files and 5 reference CSV files can then be ingested and used on the engineer's platform of choice, including Microsoft Fabric, Snowflake, Databricks, or another data platform.

Reproducibility principle: The repository provides the code and environment required to regenerate the data rather than relying on pre-generated datasets.