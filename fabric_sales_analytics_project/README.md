# 🚀 End-to-End Microsoft Fabric & Power BI Enterprise Sales Dashboard
### Production-Grade Medallion Lakehouse, Direct Lake Semantic Model & Interactive Power BI Analytics

[![Power BI](https://img.shields.io/badge/Power_BI-Direct_Lake-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Microsoft Fabric](https://img.shields.io/badge/Microsoft_Fabric-OneLake-0078D4?logo=microsoft)](https://azure.microsoft.com/products/microsoft-fabric)
[![Delta Lake](https://img.shields.io/badge/Delta_Lake-V--Order-107C41)](https://delta.io/)
[![DAX](https://img.shields.io/badge/DAX-Intermediate_to_Advanced-118DFF)](https://dax.guide/)

---

## 📑 Table of Contents
1. [Executive Summary & Business Context](#-1-executive-summary--business-context)
2. [End-to-End Fabric Architecture (Medallion OneLake)](#-2-end-to-end-fabric-architecture)
3. [Kimball Star Schema Data Model](#-3-kimball-star-schema-data-model)
4. [Fabric Lakehouse PySpark Notebooks](#-4-fabric-lakehouse-pyspark-notebooks)
5. [Fabric Data Factory Pipeline Orchestration](#-5-fabric-data-factory-pipeline-orchestration)
6. [SQL Analytics Endpoint & Dynamic Row-Level Security](#-6-sql-analytics-endpoint--dynamic-rls)
7. [Direct Lake Semantic Model & Intermediate DAX Library](#-7-direct-lake-semantic-model--dax-library)
8. [Interactive Power BI Dashboard Simulator](#-8-interactive-power-bi-dashboard-simulator)
9. [Step-by-Step Deployment Guide](#-9-step-by-step-deployment-guide)

---

## 🎯 1. Executive Summary & Business Context

A multinational enterprise operates across **North America (NA)**, **Europe, Middle East, Africa (EMEA)**, and **Asia Pacific (APAC)** selling Hardware, Software Licenses, Cloud Compute, and Professional Services through direct sales, strategic reseller partners, and digital marketplaces.

### Key Business Challenges Solved:
- **Lagging Visibility**: Legacy reporting relied on nightly SQL batch imports, causing 24-hour data latency.
- **Direct Lake Performance**: Microsoft Fabric **Direct Lake Mode** loads 35,500+ Delta Lake parquet records directly into memory without data movement or scheduled dataset refreshes.
- **Budget vs. Actual Tracking**: Real-time comparison of sales against channel targets with variance percentages and status indicators.
- **Margin Sensitivity & Scenario Simulation**: Interactive What-If sliders allowing sales directors to test price adjustments and supplier cost inflation before finalizing quarterly quotas.

---

## 🏗️ 2. End-to-End Fabric Architecture

```
+-----------------------------------------------------------------------------------------+
|                                OPERATIONAL DATA SOURCES                                 |
|               - ERP & POS Systems (Sales Invoices, Line Items, Orders)                  |
|               - CRM (Customer Accounts, Regional VPs, Sales Reps)                       |
|               - FP&A Budgets & Targets (CSV / Parquet Drops)                            |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼ [Fabric Data Factory / Ingestion Pipeline]
+-----------------------------------------------------------------------------------------+
|                              FABRIC ONELAKE: BRONZE LAYER                               |
|   - Files/landing_sales/ -> Immutable Delta Tables                                      |
|   - bronze_sales, bronze_budget, bronze_customers, bronze_products, bronze_store_regions|
|   - Audit Columns: _ingestion_timestamp, _source_file, _batch_id                        |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼ [Fabric PySpark Notebook 02: Cleansing & Merge]
+-----------------------------------------------------------------------------------------+
|                              FABRIC ONELAKE: SILVER LAYER                               |
|   - Deduplication via Window Partitions on natural keys                                 |
|   - Type casting, date standardization, null handling                                   |
|   - Enrichments: FulfillmentDays, GrossMarginPct, DiscountPct                           |
|   - Tables: silver_sales, silver_customers, silver_products, silver_store_regions       |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼ [Fabric PySpark Notebook 03: Star Schema & V-Order]
+-----------------------------------------------------------------------------------------+
|                               FABRIC ONELAKE: GOLD LAYER                                |
|   - Kimball Star Schema with Surrogate Keys                                             |
|   - Dimensions: gold_dim_date, gold_dim_customer, gold_dim_product, gold_dim_store_region|
|   - Facts: gold_fact_sales (35.5k rows), gold_fact_budget                               |
|   - Engine Optimizations: Parquet V-Order + Z-ORDER BY (OrderDateKey, CustomerKey)     |
+-----------------------------------------------------------------------------------------+
                                             │
                        ┌────────────────────┴────────────────────┐
                        ▼                                         ▼
+---------------------------------------+ +-----------------------------------------------+
|      SQL ANALYTICS ENDPOINT           | |          DIRECT LAKE SEMANTIC MODEL           |
|  - T-SQL Views (v_fact_sales, etc.)   | |  - Sub-second In-Memory VertiPaq Queries     |
|  - Dynamic Row-Level Security (RLS)   | |  - Production DAX Measures (YoY, AOV, Margin)|
|  - Ad-hoc Reporting & Excel Queries   | |  - Power BI Desktop PBIP Report Native       |
+---------------------------------------+ +-----------------------------------------------+
```

---

## 📐 3. Kimball Star Schema Data Model

The Gold Layer enforces a strict **Star Schema (1-to-many, single-directional filtering)**:

| Table Name | Type | Key Column | Description |
| :--- | :--- | :--- | :--- |
| `gold_dim_date` | Dimension | `DateKey` (PK) | 400-day calendar with Fiscal Quarters and YearMonth |
| `gold_dim_customer` | Dimension | `CustomerKey` (PK) | Customer accounts, credit tiers, segment, geography |
| `gold_dim_product` | Dimension | `ProductKey` (PK) | Catalog items, category, sub-category, standard costs |
| `gold_dim_store_region`| Dimension | `StoreRegionKey` (PK)| Sales channels, territories (NA, EMEA, APAC), Regional VPs |
| `gold_fact_sales` | Fact | `SalesLineID` (PK) | 35,502 order lines: Quantity, NetSalesUSD, MarginUSD |
| `gold_fact_budget` | Fact | `BudgetID` (PK) | Monthly channel and category targets in USD |

---

## ⚡ 4. Fabric Lakehouse PySpark Notebooks

Located in [`fabric_lakehouse_notebooks/`](./fabric_lakehouse_notebooks/):
1. [`01_bronze_sales_ingestion.py`](./fabric_lakehouse_notebooks/01_bronze_sales_ingestion.py): Ingests raw landing files into Delta tables with audit lineage.
2. [`02_silver_sales_transformation.py`](./fabric_lakehouse_notebooks/02_silver_sales_transformation.py): Schema enforcement, deduplication with `row_number()`, line-item margin calculations, and Delta upserts.
3. [`03_gold_star_schema_modeling.py`](./fabric_lakehouse_notebooks/03_gold_star_schema_modeling.py): Joins dimensions, generates integer surrogate keys, formats date keys, and runs `OPTIMIZE ... ZORDER BY`.

---

## 📊 5. Direct Lake Semantic Model & DAX Library

Located in [`semantic_model/DAX_Measures_Library.dax`](./semantic_model/DAX_Measures_Library.dax).

### Core Sales Measures:
- **Total Net Sales**: `SUM(gold_fact_sales[NetSalesUSD])`
- **Gross Profit**: `[Total Sales] - [Total Cost]`
- **Gross Margin %**: `DIVIDE([Gross Profit], [Total Sales], 0)`
- **Average Order Value (AOV)**: `DIVIDE([Total Sales], [Total Orders], 0)`

### Intermediate Time Intelligence & Variance Measures:
- **Sales Prior Year (PY)**: `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(gold_dim_date[Date]))`
- **Sales YoY Growth %**: `DIVIDE([Total Sales] - [Sales Prior Year (PY)], [Sales Prior Year (PY)], 0)`
- **Budget Achievement %**: `DIVIDE([Total Sales], [Total Budget], 0)`
- **Budget Status**:
```dax
[Budget Status Indicator] = 
SWITCH(
    TRUE(),
    ISBLANK([Total Budget]), "⚪ No Target",
    [Budget Achievement %] >= 1.0, "🟢 Exceeded Target",
    [Budget Achievement %] >= 0.9, "🟡 On Track (>=90%)",
    "🔴 Behind Target (<90%)"
)
```

---

## 🖥️ 6. Interactive Power BI Dashboard Simulator

A complete standalone and interactive Power BI Dashboard experience is provided in:
- [`interactive_dashboard/index.html`](./interactive_dashboard/index.html)
- Standalone zero-setup browser preview: [`sales_dashboard_preview.html`](../sales_dashboard_preview.html)

### Features:
- **Live Reactive Slicers**: Fiscal Year (2023, 2024, 2025), Sales Region (NA, EMEA, APAC), Product Category.
- **Dynamic KPI Callouts**: Net Sales, Gross Profit, Gross Margin %, Orders, AOV, and Target Attainment with YoY pills.
- **Interactive Visuals**:
  - Monthly Sales Trend vs Target combo chart.
  - Regional Sales Mix doughnut chart.
  - Category Revenue Contribution bar chart.
  - Top 10 Enterprise Customer accounts table with in-cell margin progress bars.
- **What-If Scenario Simulation**: Real-time margin sensitivity sliders for price elasticity and supplier inflation.
- **Theme Switcher**: Power BI Light Modern vs Power BI Dark Executive.
- **Export to CSV**: Instant export of filtered data to Excel/CSV.

---

## 🛠️ 7. Step-by-Step Deployment Guide

### Deploying to Microsoft Fabric:
1. Open [Microsoft Fabric](https://app.fabric.microsoft.com/).
2. Create a new workspace: `Sales_Analytics_Prod`.
3. Create a Lakehouse: `lh_sales_analytics`.
4. Upload files from [`data/`](./data/) into `Files/landing_sales/`.
5. Import and run notebooks `01`, `02`, and `03` from [`fabric_lakehouse_notebooks/`](./fabric_lakehouse_notebooks/).
6. Create a **New Semantic Model** using **Direct Lake** mode selecting the Gold tables.
7. Add the DAX measures from [`semantic_model/DAX_Measures_Library.dax`](./semantic_model/DAX_Measures_Library.dax).

### Opening in Power BI Desktop (PBIP):
1. In Power BI Desktop, enable **Power BI Project (.pbip) save option** under Preview Features.
2. Open [`powerbi_pbip/Sales_Analytics.Report/`](./powerbi_pbip/Sales_Analytics.Report/).
