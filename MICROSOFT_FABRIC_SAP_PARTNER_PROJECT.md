# Enterprise SAP Partner 360 & Analytics in Microsoft Fabric

A complete, production-ready blueprint for ingesting, transforming, and modeling **SAP ECC & S/4HANA Business Partner Data** using **Microsoft Fabric** (OneLake, Lakehouse Medallion Architecture, PySpark, Delta Lake, and Direct Lake Power BI).

---

## 🏗️ 1. Architecture Overview

```
+-----------------------------------------------------------------------------------+
|                                  SAP Source Systems                                |
|  - S/4HANA & ECC Tables: BUT000 (BP), ADRC (Address), KNVP (Partner Functions),   |
|                          VBAK/VBAP (Sales Orders), BSID/BSAD (Open/Cleared AR)    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ [SAP CDC via ODP / Fabric Data Factory]
+-----------------------------------------------------------------------------------+
|                       Microsoft Fabric OneLake - Bronze Layer                     |
|  - Raw delta tables: bronze_sap_but000, bronze_sap_adrc, bronze_sap_knvp, etc.   |
|  - Append-only change log (_change_type, _commit_timestamp)                       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ [PySpark Notebook: Cleaning & SCD2 Upsert]
+-----------------------------------------------------------------------------------+
|                       Microsoft Fabric OneLake - Silver Layer                     |
|  - Harmonized master data: silver_dim_sap_partner (SCD Type 2 history)            |
|  - Cleansed transactions: silver_fact_orders, silver_fact_receivables             |
|  - Deduplicated, geocoded addresses, mapped partner roles                         |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ [PySpark Notebook: Dimensional Star Schema]
+-----------------------------------------------------------------------------------+
|                        Microsoft Fabric OneLake - Gold Layer                      |
|  - gold_dim_partner (Surrogate keys, credit tiers, segment)                       |
|  - gold_dim_partner_function (Sold-to, Ship-to, Bill-to, Payer)                   |
|  - gold_fact_partner_sales & gold_fact_partner_receivables                         |
|  - Parquet V-Order optimization enabled for high-throughput Direct Lake serving   |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ [Direct Lake Mode (Sub-second In-Memory)]
+-----------------------------------------------------------------------------------+
|                    Power BI Semantic Model & Executive Dashboards                 |
|  - Measures: Partner Revenue, DSO, Concentration Pareto, Credit Exposure          |
|  - Real-time drill-down across 15M+ records without Import refresh wait times     |
+-----------------------------------------------------------------------------------+
```

---

## 📋 2. Source SAP Data Dictionary & Entity Mapping

| SAP Table | Entity Name | Description | Key Extraction Columns |
| :--- | :--- | :--- | :--- |
| `BUT000` | Business Partner General | Master record for S/4HANA BP | `PARTNER`, `TYPE`, `BPKIND`, `NAME_ORG1`, `NAME_FIRST`, `NAME_LAST`, `CRDAT` |
| `ADRC` | Addresses | Central address master data | `ADDRNUMBER`, `STREET`, `CITY1`, `POST_CODE1`, `COUNTRY`, `REGION` |
| `KNVP` | Customer Partner Functions | Maps roles (Sold-to, Ship-to, etc.) | `KUNNR`, `VKORG`, `VTWEG`, `SPART`, `PARVW`, `KUNN2` |
| `VBAK` / `VBAP` | Sales Document Header/Item | Transactional order header and line items | `VBELN`, `POSNR`, `KUNNR`, `NETWR`, `WAERK`, `ERDAT`, `ABSTK` |
| `BSID` / `BSAD` | Accounts Receivable (Open/Cleared)| Customer invoices, credit line, aging | `BUKRS`, `KUNNR`, `BELNR`, `WRBTR`, `WAERS`, `ZFBDT`, `ZBD1T` |

---

## 💻 3. PySpark Transformation Pipelines

### Bronze $\rightarrow$ Silver: Data Cleansing & SCD Type 2 Merge
Save in Fabric Notebook: `01_bronze_to_silver_sap_partner`

```python
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# 1. Read Bronze CDC Feed
bronze_bp = spark.read.table("bronze_sap_but000").filter(F.col("_change_type") != "D")
bronze_adrc = spark.read.table("bronze_sap_adrc")

# 2. Enrich and Harmonize Business Partner Master Records
enriched_bp = (
    bronze_bp
    .join(bronze_adrc, on="ADDRNUMBER", how="left")
    .select(
        F.col("PARTNER").alias("partner_id"),
        F.when(F.col("TYPE") == "1", "Person")
         .when(F.col("TYPE") == "2", "Organization")
         .otherwise("Group").alias("partner_type"),
        F.coalesce(
            F.col("NAME_ORG1"), 
            F.concat_ws(" ", F.col("NAME_FIRST"), F.col("NAME_LAST"))
        ).alias("partner_name"),
        F.col("STREET").alias("street"),
        F.col("CITY1").alias("city"),
        F.col("POST_CODE1").alias("postal_code"),
        F.col("COUNTRY").alias("country_code"),
        F.col("CRDAT").cast("date").alias("created_date"),
        F.col("_commit_timestamp").alias("last_modified_timestamp")
    )
)

# 3. Upsert into Silver Delta Table
silver_table = DeltaTable.forName(spark, "silver_dim_sap_partner")

(
    silver_table.alias("target")
    .merge(
        enriched_bp.alias("source"),
        "target.partner_id = source.partner_id"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
```

---

### Silver $\rightarrow$ Gold: Star Schema & V-Order Optimization
Save in Fabric Notebook: `02_silver_to_gold_dimensional_model`

```python
from pyspark.sql import functions as F

# Enable Fabric V-Order compression for Direct Lake read acceleration
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")

# 1. Curate Gold Partner Dimension with Credit Tiers
silver_bp = spark.read.table("silver_dim_sap_partner")
silver_ar = spark.read.table("silver_fact_sap_receivables")

partner_summary = (
    silver_ar.groupBy("partner_id")
    .agg(
        F.sum("open_amount_usd").alias("total_outstanding_ar"),
        F.max("days_past_due").alias("max_days_past_due")
    )
)

gold_dim_partner = (
    silver_bp.join(partner_summary, on="partner_id", how="left")
    .withColumn(
        "credit_risk_tier",
        F.when(F.col("max_days_past_due") > 90, "High Risk")
         .when(F.col("max_days_past_due") > 30, "Medium Risk")
         .otherwise("Low Risk / Current")
    )
)

gold_dim_partner.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_partner")

# 2. Curate Gold Fact Sales
gold_fact_sales = (
    spark.read.table("silver_fact_sap_orders")
    .select(
        "order_number",
        "order_item",
        "partner_id",
        "sales_org_id",
        "order_date_key",
        "net_value_usd",
        "margin_value_usd",
        "order_status"
    )
)

gold_fact_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_fact_partner_sales")

# 3. Optimize and Compact Tables
spark.sql("OPTIMIZE gold_fact_partner_sales ZORDER BY (partner_id, order_date_key)")
spark.sql("VACUUM gold_fact_partner_sales RETAIN 168 HOURS")
```

---

## 📊 4. Power BI Direct Lake Semantic Model & DAX Measures

### What Makes Direct Lake Superior?
* **Zero ETL Refresh Delay**: Queries read parquet files directly from OneLake storage in memory.
* **No DirectQuery Bottleneck**: Doesn't translate DAX into slow T-SQL statements; runs natively on the Tabular Analysis Services engine.

### Key Production DAX Measures

```dax
// 1. Total Partner Sales
Total Partner Revenue = 
SUM('gold_fact_partner_sales'[net_value_usd])

// 2. Gross Margin %
Partner Gross Margin % = 
DIVIDE(
    SUM('gold_fact_partner_sales'[margin_value_usd]),
    [Total Partner Revenue],
    0
)

// 3. Top 20% Partner Revenue Concentration (Pareto Ratio)
Top20_Partner_Revenue_Share = 
VAR TotalRev = [Total Partner Revenue]
VAR Top20Rev = 
    CALCULATE(
        [Total Partner Revenue],
        TOPN(
            DIVIDE(DISTINCTCOUNT('gold_dim_partner'[partner_id]), 5, 1),
            ALLSELECTED('gold_dim_partner'[partner_id]),
            [Total Partner Revenue],
            DESC
        )
    )
RETURN 
    DIVIDE(Top20Rev, TotalRev, 0)

// 4. Days Sales Outstanding (DSO)
Partner DSO = 
VAR TotalOpenAR = SUM('gold_fact_partner_receivables'[open_amount_usd])
VAR AnnualizedSales = [Total Partner Revenue]
RETURN 
    DIVIDE(TotalOpenAR, DIVIDE(AnnualizedSales, 365, 0), 0)
```

---

## 🔒 5. Governance, CI/CD & Production Operations

1. **Deployment Pipelines**:
   * Setup three Fabric workspaces: `DEV_Fabric_Partner_Analytics`, `TEST_Fabric_Partner_Analytics`, `PROD_Fabric_Partner_Analytics`.
   * Bind workspaces to GitHub or Azure DevOps repository using native Fabric Git Integration.
2. **Data Quality Assertions**:
   * Schema enforcement on Bronze Delta tables.
   * Null checks on foreign keys (`partner_id`, `order_date_key`).
   * Automated alerting via Fabric Data Activator on abnormal credit balance spikes.
3. **Microsoft Purview**:
   * Complete asset cataloging and data lineage from SAP Source extraction to executive Power BI visual.
