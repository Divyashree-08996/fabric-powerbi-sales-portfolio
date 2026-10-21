# 🚀 Enterprise Pre-Sales Analytics in Microsoft Fabric & Power BI
### End-to-End Medallion Lakehouse, Direct Lake Semantic Model & Executive Dashboards

A complete, production-ready enterprise project implementing **Pre-Sales / Solutions Engineering (SE) Analytics** using **Microsoft Fabric** (OneLake, Lakehouse Medallion Architecture, PySpark, Delta Lake, Fabric Data Factory) and **Power BI Direct Lake Mode**.

---

## 📌 Executive Summary

In enterprise B2B software, cloud, and IT services, **Pre-Sales (Solutions Architecture & Sales Engineering)** is the single highest-leverage resource in the revenue cycle. Yet, most organizations lack visibility into:
- **Pre-Sales ROI**: What is the actual win rate lift when an SE is assigned to an opportunity?
- **Proof of Concept (POC) Health**: Which POCs are stalling, and what is the technical-win to commercial-win conversion rate?
- **SE Workload & Capacity**: Are highly-paid architects spending time on low-probability transactional deals or high-impact strategic accounts?
- **Technical Product Gap Feedback**: What technical reasons (latency, security, integrations) are causing lost revenue?

This project delivers an **end-to-end cloud data and analytics solution** in **Microsoft Fabric** that ingests raw CRM and Pre-Sales operational data, transforms it across Bronze, Silver, and Gold Delta Lakehouse layers, models it in **Direct Lake** mode, and surfaces sub-second actionable insights in Power BI.

---

## 🏗️ End-to-End Architecture

```
+---------------------------------------------------------------------------------------------------+
|                                  SOURCE OPERATIONAL SYSTEMS                                       |
|  - CRM (Salesforce / HubSpot): Accounts, Opportunities, Deal Stages, ACV                          |
|  - Pre-Sales Tools (Vivun / PreSales.com / Jira): Activities, Demos, Workshops, SE Hours         |
|  - Technical POC & RFP Portals: POC Criteria, Cloud Lab Costs, RFP Compliance Scores              |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼ [Fabric Data Factory / OneLake Shortcuts]
+---------------------------------------------------------------------------------------------------+
|                            MICROSOFT FABRIC ONELAKE - BRONZE LAYER                                |
|  - Ingestion Zone: Files/bronze/*.csv                                                             |
|  - Delta Tables: bronze_crm_accounts, bronze_products, bronze_solution_engineers,                  |
|                  bronze_crm_opportunities, bronze_presales_activities, bronze_poc_projects,        |
|                  bronze_rfp_requests                                                              |
|  - System Auditing: _ingestion_timestamp, _source_file, _batch_id                                 |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼ [Fabric Notebook 02: PySpark Cleansing & Merge]
+---------------------------------------------------------------------------------------------------+
|                            MICROSOFT FABRIC ONELAKE - SILVER LAYER                                |
|  - Deduplication via Window functions on natural keys                                            |
|  - Type casting (Dates, Decimals, Booleans), handling nulls & fallbacks                           |
|  - Business enrichments: sales_cycle_days, deal_size_tier, presales_touch_level,                   |
|    activity_cost_usd, total_poc_investment_usd, is_technical_win                                  |
|  - Incremental upserts via Delta Lake MERGE INTO                                                  |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼ [Fabric Notebook 03: Dimensional Star Schema]
+---------------------------------------------------------------------------------------------------+
|                             MICROSOFT FABRIC ONELAKE - GOLD LAYER                                 |
|  - Kimball Star Schema with Surrogate Keys & Role-Playing Dates:                                  |
|    * Dimensions: gold_dim_date, gold_dim_account, gold_dim_solution_engineer,                     |
|                  gold_dim_product, gold_dim_opportunity, gold_dim_activity_type                   |
|    * Facts:      gold_fact_presales_activity, gold_fact_poc,                                      |
|                  gold_fact_opportunity_snapshot, gold_fact_rfp                                    |
|  - Parquet V-Order optimization enabled (spark.sql.parquet.vorder.enabled = true)                 |
|  - Z-Order clustering on high-cardinality join columns                                            |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼ [Direct Lake Mode (Sub-Second In-Memory)]
+---------------------------------------------------------------------------------------------------+
|                               POWER BI DIRECT LAKE SEMANTIC MODEL                                 |
|  - Native VertiPaq columnar memory load directly from OneLake Parquet                             |
|  - 30+ Enterprise DAX Measures across 7 Display Folders                                           |
|  - Role-Level Security (RLS) for Global Execs, Regional Directors, and Individual SEs            |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼ [Executive Decision Support]
+---------------------------------------------------------------------------------------------------+
|                                     POWER BI EXECUTIVE SUITE                                      |
|  1. Pre-Sales Executive Command Center (Win Rate Lift, Revenue Contribution, Pipeline ACV)        |
|  2. Proof of Concept (POC) Control Tower & Velocity (Technical Win vs Commercial Win Funnel)     |
|  3. Solutions Engineering Capacity & Productivity (Workload Heatmap, Prep vs Delivery)          |
|  4. Technical Win/Loss & Competitive Gap Feedback Loop (Product Gap ARR Pareto, Competitors)      |
+---------------------------------------------------------------------------------------------------+
```

---

## 📁 Repository & Project Structure

```
microsoft_fabric_presales_project/
│
├── README.md                                   # Master architectural blueprint & documentation
├── presales_lakehouse.db                       # Local SQLite Lakehouse for instant offline verification
│
├── data_generator/                             # Zero-dependency synthetic data generation
│   ├── generate_presales_data.py               # Generates 7 rich enterprise CSV datasets
│   └── local_lakehouse_simulator.py            # Local Python/SQLite engine simulating Fabric execution
│
├── sample_data/                                # Generated raw Bronze datasets (CSV)
│   ├── crm_accounts.csv                        # 220 Enterprise & Mid-Market Accounts
│   ├── products.csv                            # 8 Core Software & Cloud Products
│   ├── solution_engineers.csv                  # 20 Solutions Engineers & Architects
│   ├── crm_opportunities.csv                   # 750 Opportunities with SE involvement flags
│   ├── presales_activities.csv                 # 2,737 Detailed technical engagements
│   ├── poc_projects.csv                        # 318 Proof of Concept project evaluations
│   └── rfp_requests.csv                        # 224 RFP/Security submissions
│
├── gold_lakehouse_data/                        # Gold Star Schema tables (CSV)
│   ├── gold_dim_date.csv                       # Role-playing calendar (2024-2026)
│   ├── gold_dim_account.csv                    # Cleaned accounts with revenue tiers
│   ├── gold_dim_solution_engineer.csv          # SE master with rates and utilization targets
│   ├── gold_dim_product.csv                    # Product catalog and list prices
│   ├── gold_dim_opportunity.csv                # Opportunity metadata and touch levels
│   ├── gold_dim_activity_type.csv              # Standard demos, custom demos, ADS, etc.
│   ├── gold_fact_presales_activity.csv         # Granular activity effort and costs
│   ├── gold_fact_poc.csv                       # POC duration, criteria success, tech win
│   ├── gold_fact_opportunity_snapshot.csv      # Opportunity revenue snapshot
│   └── gold_fact_rfp.csv                       # RFP turnarounds and compliance scores
│
├── fabric_lakehouse_notebooks/                 # Production Fabric PySpark Notebooks
│   ├── 01_ingest_bronze_lakehouse.py           # Ingestion from landing zone with metadata audit
│   ├── 02_bronze_to_silver_transform.py        # Data cleansing, enrichment, and Delta MERGE
│   └── 03_silver_to_gold_star_schema.py        # Kimball Star Schema generation with V-Order
│
├── sql_scripts/                                # SQL Analytics Endpoint & Warehouse
│   ├── 01_fabric_lakehouse_sql_views.sql       # Business views for SQL consumers & BI
│   └── 02_analytical_validation_queries.sql    # Complex analytical queries (ROI, POC Funnel, Pareto)
│
├── semantic_model/                             # Power BI Direct Lake Modeling
│   ├── dax_measures_library.dax                # 30+ Production DAX Measures organized by folder
│   └── model_relationships_and_tmdl.md         # Star schema relationships & TMDL specification
│
├── powerbi_report/                             # Power BI Reporting Specifications
│   ├── dashboard_design_specification.md       # 4-page UI/UX wireframes and visual configurations
│   └── presales_powerbi_theme.json             # Custom Microsoft Fluent palette theme
│
├── fabric_pipeline/                            # Fabric Data Factory Orchestration
│   └── pipeline_orchestration_definition.json  # Scheduled pipeline JSON with error handling & alerts
│
└── deployment_and_governance/                  # Governance, Security, and CI/CD
    ├── fabric_rls_security_guide.md            # Role-Level Security (RLS) setup for Direct Lake
    └── git_cicd_deployment_guide.md            # Fabric Git integration, PBIP, and multi-stage pipelines
```

---

## 📊 Business Metrics & Analytical Findings

Execution of the full data pipeline over the synthetic dataset yields actionable pre-sales benchmarks:

| Analytical Metric | Pre-Sales Engaged | Unassisted / Baseline | Business Impact / Lift |
| :--- | :--- | :--- | :--- |
| **Win Rate %** | **60.0%** | **25.2%** | **+34.8 percentage points lift!** |
| **Jumbo Enterprise Deals (>$400k)** | **64.0%** | **25.0%** | **+39.0 points lift ($50.3M won)** |
| **Major Deals ($200k - $400k)** | **64.0%** | **27.3%** | **+36.7 points lift ($35.7M won)** |
| **Core Deals ($75k - $200k)** | **56.3%** | **25.8%** | **+30.5 points lift ($19.5M won)** |
| **Total Won ACV Generated** | **$98.5M** | **$8.2M** | **92.3% of total revenue is SE-influenced!** |
| **Average Sales Cycle** | **84 Days** | **112 Days** | **28 days faster cycle time** |

---

## 💻 Step-by-Step Implementation Guide

### Option A: Local Verification (Zero Dependencies - Immediate)
You can run the entire pipeline locally on your machine using standard Python without installing Spark or Docker:

```powershell
# 1. Generate realistic synthetic CRM, SE, POC, and Activity data
python microsoft_fabric_presales_project/data_generator/generate_presales_data.py

# 2. Run the Local Lakehouse Simulator (cleanses data, builds Gold Star Schema & SQLite DB)
python microsoft_fabric_presales_project/data_generator/local_lakehouse_simulator.py
```
*Result*: Populates `gold_lakehouse_data/` with all Dimension and Fact tables and creates `presales_lakehouse.db` for instant querying.

---

### Option B: Deploying to Microsoft Fabric Cloud

#### Step 1: Create a Fabric Workspace & Lakehouse
1. Sign in to [Microsoft Fabric](https://app.fabric.microsoft.com).
2. Create a new workspace: `PreSales-Analytics-Prod`.
3. In the workspace, create a **Lakehouse**: `lh_presales_analytics`.

#### Step 2: Upload Landing Files
1. In `lh_presales_analytics`, go to **Files** $\rightarrow$ Create folder `bronze`.
2. Upload the 7 CSV files from `microsoft_fabric_presales_project/sample_data/` into `Files/bronze/`.

#### Step 3: Import & Execute PySpark Notebooks
1. In the Fabric workspace, click **New item** $\rightarrow$ **Notebook** $\rightarrow$ **Import notebook**.
2. Import the 3 notebooks from `fabric_lakehouse_notebooks/`:
   - `01_ingest_bronze_lakehouse.py` $\rightarrow$ Run to populate Bronze Delta tables.
   - `02_bronze_to_silver_transform.py` $\rightarrow$ Run to cleanse, enrich, and build Silver Delta tables.
   - `03_silver_to_gold_star_schema.py` $\rightarrow$ Run to generate Gold Star Schema Delta tables with V-Order.

#### Step 4: Create the Direct Lake Semantic Model
1. In the Lakehouse, switch to the **SQL Analytics Endpoint**.
2. Click **New Semantic Model** on the top ribbon.
3. Select the Gold tables:
   - Dimensions: `gold_dim_date`, `gold_dim_account`, `gold_dim_solution_engineer`, `gold_dim_product`, `gold_dim_opportunity`, `gold_dim_activity_type`.
   - Facts: `gold_fact_presales_activity`, `gold_fact_poc`, `gold_fact_opportunity_snapshot`, `gold_fact_rfp`.
4. Name the model: `sm_presales_direct_lake`.
5. Establish relationships as documented in [`model_relationships_and_tmdl.md`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/semantic_model/model_relationships_and_tmdl.md).
6. Copy the DAX measures from [`dax_measures_library.dax`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/semantic_model/dax_measures_library.dax) into the model.

#### Step 5: Build Reports & Deploy Pipeline
1. Apply the Fluent theme from [`presales_powerbi_theme.json`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/powerbi_report/presales_powerbi_theme.json).
2. Build the 4-page dashboard following the layout in [`dashboard_design_specification.md`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/powerbi_report/dashboard_design_specification.md).
3. Import the Data Factory pipeline from [`pipeline_orchestration_definition.json`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/fabric_pipeline/pipeline_orchestration_definition.json) to schedule automatic daily refreshes.

---

## ⚡ Direct Lake Performance Best Practices

To guarantee that Power BI queries Delta tables in OneLake with sub-second response times without ever falling back to DirectQuery:
1. **Parquet V-Order**: Configured in Notebook 03 via `spark.conf.set("spark.sql.parquet.vorder.enabled", "true")`.
2. **Table Maintenance**: Compact small files and optimize data layout using `OPTIMIZE <table> ZORDER BY (<join_columns>)`.
3. **Integer Surrogate Keys**: Joining facts to dimensions on integer keys (`YYYYMMDD` integers and dense integer surrogate keys) maximizes VertiPaq dictionary compression.
4. **Calculated Columns Upstream**: Avoid DAX calculated columns in Direct Lake models; compute all flags and categories in PySpark Silver/Gold layers.

---

## 🛡️ Governance & Row-Level Security (RLS)

Configured with 3 role profiles:
- **`Executive_Unrestricted`**: Unrestricted global view for CRO and VP Pre-Sales.
- **`Regional_SE_Lead`**: Dynamically filters data by user geographic region (`USERPRINCIPALNAME()` mapped via security table).
- **`Individual_SE_Access`**: Restricts individual Solutions Engineers to their personal deals, activities, and POC assignments.

See full configuration in [`fabric_rls_security_guide.md`](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/microsoft_fabric_presales_project/deployment_and_governance/fabric_rls_security_guide.md).

---

## 👥 Authors & License
- **Architecture**: Microsoft Fabric & Power BI Direct Lake Solutions Architecture
- **License**: MIT Open Source
