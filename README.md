# 💎 Ubuntu Unified Retail Data Platform on Microsoft Fabric

[![Ubuntu Unified Data Platform CI](https://github.com/Medy682/Ubuntu_Unified_Retail_Data_Platform_on_Microsoft_Fabric/actions/workflows/platform-ci.yml/badge.svg)](https://github.com/Medy682/Ubuntu_Unified_Retail_Data_Platform_on_Microsoft_Fabric/actions/workflows/platform-ci.yml)

> An end-to-end simulated enterprise data engineering platform built with Microsoft Fabric, Python, PySpark and SQL for integrating batch, streaming and real-time retail data into an analytics-ready environment.


---

👤 Author: Kidima Medy Masuka 

Date: 2026

---


# 📌 1. Project Overview

The **Ubuntu Unified Retail Data Platform** demonstrates how heterogeneous retail and e-commerce data can be prepared, ingested, transformed, validated, modelled and consumed through Microsoft Fabric.

The platform combines:

- **Batch ELT** — manually uploaded source files → Bronze → Silver → Gold / Warehouse
- **Streaming data engineering** — Event Hubs → Eventstream → Bronze → Silver → Streaming Gold using PySpark Structured Streaming
- **Real-time analytics** — streaming events were alternatively also routed from Eventstream to Eventhouse / KQL for low-latency real-time analytics
- **Analytics and BI** using Power BI and Direct Lake
- **Reproducible development** using Docker
- **Automated repository validation** using GitHub Actions CI

The architecture follows a **Medallion Architecture: Bronze → Silver → Gold**.

---

# 🏗️ 2. Platform Architecture

```text
                         MICROSOFT FABRIC
                                │
                              OneLake
                                │
                       Fabric Lakehouse
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
       BRONZE                SILVER                 GOLD
          │                     │                     │
     ┌────┴────┐           ┌────┴────┐          ┌────┴────┐
     │         │           │         │          │         │
   Batch   Streaming     Batch   Streaming    Batch   Streaming
     │         │           │         │          │         │
     │         │         PySpark   PySpark      SQL     PySpark
     │         │         Transform Structured  Model   Structured
     │         │         & Validate Streaming          Streaming
     │         │           │         │          │         │
     └────┬────┘           └────┬────┘          └────┬────┘
          │                     │                     │
          ▼                     ▼                     ▼
     Bronze tables         Silver tables        Gold outputs
                                                      │
                                      ┌───────────────┴───────────────┐
                                      │                               │
                                Fabric Warehouse               Streaming Gold
                                      │                               │
                                      └───────────────┬───────────────┘
                                                      │
                                             Semantic Models
                                                      │
                                                      ▼
                                                   Power BI
```

### 👉 Fabric components

**OneLake** — unified logical data lake and storage foundation.

**Lakehouse** — primary data-engineering environment using Delta tables and Bronze, Silver and Gold layers.

**Fabric Warehouse** — SQL-based analytical layer supporting dimensional modelling and BI workloads.

**Eventhouse** — purpose-built environment for low-latency real-time event analytics using KQL.

**Power BI** — analytical and reporting layer using semantic models and Direct Lake.

---

# 🗃️ 3. Data Sources & Preparation

The project combines public retail/e-commerce datasets, synthetic operational data and simulated real-time events.

### 👉 Public datasets

- Online Retail II
- Olist Brazilian E-Commerce

### 👉 Synthetic operational data

Python scripts generate supporting datasets such as:

- Stores
- Employees
- Inventory snapshots
- Suppliers
- Promotions

### 👉 Event simulation

```text
Existing Project Data
        ↓
event_simulator.py
        ↓
Simulated Events
        ↓
Azure Event Hubs
        ↓
Microsoft Fabric Eventstream
```

The repository contains the source data and Python scripts required to reproduce the prepared datasets.

---

# ⚙️ 4. Batch Data Engineering

The batch workflow follows an **ELT-oriented** pattern:

```text
Source Files
    ↓
Manual Upload to Lakehouse Files
    ↓
Bronze
    ↓
PySpark Transformation & Validation
    ↓
Silver
    ↓
SQL Dimensional Modelling
    ↓
Gold / Fabric Warehouse
```

### 👉 Bronze

Source data is ingested into the Bronze layer with lightweight preparation where required.

### 👉 Silver

PySpark performs cleansing, standardisation, deduplication, transformation and validation.

### 👉 Gold

SQL is used for analytical modelling and business-oriented structures. Gold outputs are consumed through the analytical layer and Power BI.

---

# 🔥 5. Real-Time & Streaming Architecture

The streaming architecture uses Azure Event Hubs and Fabric Eventstream for ingestion and routing.

```text
                         Python Event Simulator
                                  ↓
                            Azure Event Hubs
                                  ↓
                         Fabric Eventstream
                           /                                        /                                         ▼                  ▼
              Bronze Streaming       Eventhouse / KQL
                         │                  │
                         ▼                  ▼
              PySpark Structured       Real-Time
                  Streaming            Analytics
                         │
                         ▼
               Silver Streaming
                         │
                         ▼
              PySpark Structured
                  Streaming
                         │
                         ▼
                 Streaming Gold
                         │
                         ▼
                 Power BI Analytics
```

The architecture deliberately provides two complementary paths:

```text
Fabric Eventstream
       │
       ├──────────────► Lakehouse Streaming
       │                    │
       │                    ▼
       │              Bronze → Silver → Streaming Gold
       │                    │
       │                    ▼
       │                 Power BI
       │
       └──────────────► Eventhouse / KQL
                            │
                            ▼
                     Real-Time Analytics
```

**Lakehouse streaming** is the primary streaming data-engineering path.

**Eventhouse/KQL** provides a complementary low-latency environment for interactive real-time analytics.

---

# ✨ 6. Data Quality

Data-quality validation is embedded within the transformation workflows.

Validation includes:

- Null and missing-value checks
- Duplicate detection
- Data-type validation
- Primary-key integrity
- Foreign-key and referential-integrity validation
- Business-rule validation
- Invalid-value and range checks
- Row-count and record-level consistency checks
- Post-write verification

The transformation notebooks were developed, executed and validated in Microsoft Fabric using PySpark.

A separate automated unit/integration testing framework is **not currently implemented**; validation is performed within the Fabric transformation workflows.

---

# 🚀 7. Orchestration

Microsoft Fabric Data Factory Pipelines orchestrate the scheduled batch ELT workflow:

```text
              Fabric Data Factory Pipeline
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Bronze         Silver           Gold
      Processing     Processing       Processing
                         │
                   Data Quality
                    Validation
```

For streaming, **PySpark Structured Streaming continuously processes incoming events** rather than being repeatedly triggered by the batch orchestration pipeline.

Eventhouse/KQL provides an additional real-time analytics path without requiring the batch orchestration pipeline to trigger individual incoming events.

---

# 📈 8. Analytics & Power BI

The platform uses Power BI for analytical consumption.

- **Batch analytics** — Power BI reports consume curated analytical data from the Gold / Fabric Warehouse layer.
- **Streaming analytics** — Power BI can consume the Streaming Gold analytical layer for streaming-oriented KPIs.
- **Direct Lake** — semantic models use Direct Lake to work with supported Lakehouse and Fabric Warehouse data without requiring a traditional full import.
- **Real-time analytics** — Eventhouse / KQL provides a separate low-latency analytical experience for incoming streaming events.

```text
Batch Gold ───────────────────────┐
                                  │
Streaming Gold ──────────────────┼──► Power BI Semantic Model
                                  │
                                  └──► Power BI Analytics

Eventhouse / KQL ─────────────────────► Real-Time Analytics
```

---

# 🐳 9. Docker & Reproducibility

Docker provides a reproducible environment for the project's Python data-generation and supporting scripts.

Build the environment:

```powershell
docker compose -f docker/docker-compose.yml build
```

Generate batch datasets:

```powershell
docker compose -f docker/docker-compose.yml run --rm retail-platform python scripts/generate_sample_datasets.py
```

Generate reference datasets:

```powershell
docker compose -f docker/docker-compose.yml run --rm retail-platform python scripts/generate_reference_data.py
```

Generated batch and reference datasets are intentionally excluded from version control. The repository provides the source data, generation scripts, Docker configuration and dependencies required to reproduce them.

---

# 🔐 10. CI & Security

The repository uses Git and GitHub Actions for automated validation.

The current CI workflow performs:

- Python validation
- Dependency validation
- Dependency vulnerability scanning
- Secret detection

The workflow runs on pushes and pull requests targeting `main` and can also be triggered manually.

### 👉 Continuous Deployment

**Continuous Deployment (CD) is not currently implemented.**

Fabric notebooks, pipelines and other platform artefacts are maintained as part of the project repository, but the repository does not currently automate their deployment or promotion to a target Fabric workspace.

---

# 🎯 11. Technology Stack

| Area | Technologies |
|---|---|
| Data Platform | Microsoft Fabric, OneLake |
| Data Engineering | Fabric Lakehouse, PySpark, Python, pandas |
| Batch Processing | PySpark, SQL, Fabric Data Factory Pipelines |
| Streaming | Azure Event Hubs, Fabric Eventstream, PySpark Structured Streaming |
| Real-Time Analytics | Fabric Eventhouse, KQL |
| Data Modelling | SQL, Dimensional Modelling, Star Schema |
| Analytics | Power BI, Semantic Models, Direct Lake |
| Engineering | Docker, Git, GitHub Actions |
| Storage Format | Delta Lake |
| Methodology | Medallion Architecture, CRISP-DM |

---

# 📂 12. Repository Structure

```text
UBUNTU_UNIFIED_RETAIL_DATA_PLATFORM_ON_MICROSOFT_FABRIC/
│
├── .github/
│   └── workflows/
│       └── platform-ci.yml
│
├── config/
│
├── data/
│   └── Original_data/
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── entrypoint.sh
│
├── docs/
│
├── fabric/
│   ├── data_factory/
│   ├── lakehouse/
│   ├── notebooks/
│   └── warehouse/
│
├── scripts/
│   ├── event_simulator.py
│   ├── generate_sample_datasets.py
│   ├── generate_reference_data.py
│   └── utilities.py
│
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

> Local-only directories and ignored files such as generated data, logs, environment files and historical material are intentionally excluded from the public repository structure.

---

# 🔴 13. Key Engineering Lessons

This project demonstrates practical experience with:

- Lakehouse and Medallion Architecture
- Batch ELT
- PySpark data transformation
- PySpark Structured Streaming
- Delta Lake
- SQL dimensional modelling
- Fabric Data Factory orchestration
- Azure Event Hubs and Fabric Eventstream
- Eventhouse/KQL real-time analytics
- Data-quality and referential-integrity validation
- Power BI and Direct Lake
- Docker-based reproducibility
- GitHub Actions CI and security automation

---

# 💥 14. Future Improvements

Potential future enhancements include:

- Automated deployment of Fabric artefacts through CD
- Expanded monitoring and observability
- More advanced incremental processing
- Additional streaming sources
- Slowly Changing Dimensions
- Further Gold-layer analytical models
- Performance and partitioning optimisation
- Additional Eventhouse/KQL optimisation

---

## ✅ Project Summary

```text
Python
  ↓
Source Preparation / Data Generation / Event Simulation
  ↓
Microsoft Fabric
  │
  ├── Batch
  │    └── Bronze → Silver → Gold / Fabric Warehouse
  │                         ↓
  │                    Power BI Analytics
  │
  └── Streaming Events
       ↓
   Azure Event Hubs
       ↓
   Fabric Eventstream
       │
       ├── Lakehouse Streaming Path
       │       ↓
       │    Bronze → Silver → Streaming Gold
       │                         ↓
       │                    Power BI Analytics
       │
       └── Real-Time Analytics Path
               ↓
          Eventhouse / KQL
               ↓
       Low-Latency Real-Time Analytics
```

The **Ubuntu Unified Retail Data Platform** brings together batch ELT, continuous streaming, real-time analytics, data quality, orchestration, dimensional modelling, Docker reproducibility and CI automation in a single Microsoft Fabric data-engineering project.

---

# 👤 Author

**Kidima Medy Masuka**

Junior Data Engineer

Focused on:
- Data Engineering
- Data Analytics
- Machine Learning
- Data-Driven Decision Making

---

# 📌 Portfolio Note

This project was built for educational and portfolio purposes to demonstrate practical cloud data engineering skills using modern data platform technologies.

If reused or adapted, appropriate credit must be given to the author.

📰 This project is part of my personal data science and analytics portfolio ✅