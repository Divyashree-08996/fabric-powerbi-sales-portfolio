# Fabric Notebook: 01_ingest_bronze_lakehouse
# Description: Ingests raw pre-sales CSV/JSON/Parquet files from OneLake Landing Zone (Files/bronze/)
#              into Delta Lake Bronze tables with ingestion metadata auditing.

# CELL 1: Setup & Configuration
# MAGIC %md
# MAGIC # 📥 Notebook 01: Raw Ingestion to Bronze Lakehouse Layer
# MAGIC **Microsoft Fabric End-to-End Pre-Sales Analytics**
# MAGIC 
# MAGIC This notebook scans the OneLake landing zone (`Files/bronze/` or Shortcuts to ADLS Gen2/S3/Salesforce/Vivun),
# MAGIC enforces bronze schemas, attaches system audit metadata (`_ingestion_timestamp`, `_source_file`, `_batch_id`),
# MAGIC and writes the data to raw Delta tables in append-mode.

import uuid
from datetime import datetime
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, 
    BooleanType, TimestampType, DateType
)

# Generate a unique batch ID for this ingestion run
BATCH_ID = str(uuid.uuid4())
INGESTION_TIMESTAMP = datetime.utcnow()

print(f"Starting Bronze Ingestion. Batch ID: {BATCH_ID}")
print(f"Timestamp: {INGESTION_TIMESTAMP.isoformat()}")

# Enable V-Order for high performance read in Fabric
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")

# CELL 2: Helper Function to Append Ingestion Metadata
def append_metadata(df, source_file_name: str, batch_id: str):
    """Adds audit metadata columns to raw bronze streams/files."""
    return (
        df.withColumn("_ingestion_timestamp", F.current_timestamp())
          .withColumn("_source_file", F.lit(source_file_name))
          .withColumn("_batch_id", F.lit(batch_id))
    )

# CELL 3: Ingest Raw CRM Accounts
# MAGIC %md
# MAGIC ### 1. Bronze CRM Accounts Ingestion
accounts_schema = StructType([
    StructField("account_id", StringType(), False),
    StructField("account_name", StringType(), True),
    StructField("industry", StringType(), True),
    StructField("account_tier", StringType(), True),
    StructField("annual_revenue_usd", DoubleType(), True),
    StructField("employee_count", IntegerType(), True),
    StructField("country_name", StringType(), True),
    StructField("country_code", StringType(), True),
    StructField("region", StringType(), True),
    StructField("created_date", StringType(), True)
])

raw_accounts_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(accounts_schema)
    .load("Files/bronze/crm_accounts.csv")
)

bronze_accounts = append_metadata(raw_accounts_df, "crm_accounts.csv", BATCH_ID)

bronze_accounts.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_crm_accounts")

print(f"✓ bronze_crm_accounts ingested: {bronze_accounts.count()} rows")

# CELL 4: Ingest Products Catalog
# MAGIC %md
# MAGIC ### 2. Bronze Products Ingestion
products_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), True),
    StructField("product_category", StringType(), True),
    StructField("deployment_model", StringType(), True),
    StructField("base_annual_license_usd", DoubleType(), True),
    StructField("standard_poc_duration_days", IntegerType(), True)
])

raw_products_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(products_schema)
    .load("Files/bronze/products.csv")
)

bronze_products = append_metadata(raw_products_df, "products.csv", BATCH_ID)

bronze_products.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_products")

print(f"✓ bronze_products ingested: {bronze_products.count()} rows")

# CELL 5: Ingest Solution Engineers Master
# MAGIC %md
# MAGIC ### 3. Bronze Solution Engineers Ingestion
se_schema = StructType([
    StructField("se_id", StringType(), False),
    StructField("se_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("region", StringType(), True),
    StructField("seniority_level", StringType(), True),
    StructField("specialization", StringType(), True),
    StructField("target_weekly_hours", IntegerType(), True),
    StructField("target_utilization_pct", DoubleType(), True),
    StructField("hourly_cost_rate_usd", DoubleType(), True)
])

raw_se_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(se_schema)
    .load("Files/bronze/solution_engineers.csv")
)

bronze_se = append_metadata(raw_se_df, "solution_engineers.csv", BATCH_ID)

bronze_se.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_solution_engineers")

print(f"✓ bronze_solution_engineers ingested: {bronze_se.count()} rows")

# CELL 6: Ingest CRM Opportunities
# MAGIC %md
# MAGIC ### 4. Bronze CRM Opportunities Ingestion
opp_schema = StructType([
    StructField("opportunity_id", StringType(), False),
    StructField("account_id", StringType(), True),
    StructField("opportunity_name", StringType(), True),
    StructField("ae_owner_name", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("deal_type", StringType(), True),
    StructField("created_date", StringType(), True),
    StructField("target_close_date", StringType(), True),
    StructField("actual_close_date", StringType(), True),
    StructField("deal_stage", StringType(), True),
    StructField("deal_status", StringType(), True),
    StructField("annual_contract_value_usd", DoubleType(), True),
    StructField("total_contract_value_usd", DoubleType(), True),
    StructField("se_assigned_id", StringType(), True),
    StructField("is_presales_engaged", BooleanType(), True),
    StructField("poc_conducted", BooleanType(), True),
    StructField("competitor_name", StringType(), True),
    StructField("win_loss_reason", StringType(), True),
    StructField("is_technical_loss", BooleanType(), True)
])

raw_opp_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(opp_schema)
    .load("Files/bronze/crm_opportunities.csv")
)

bronze_opp = append_metadata(raw_opp_df, "crm_opportunities.csv", BATCH_ID)

bronze_opp.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_crm_opportunities")

print(f"✓ bronze_crm_opportunities ingested: {bronze_opp.count()} rows")

# CELL 7: Ingest Pre-Sales Activities
# MAGIC %md
# MAGIC ### 5. Bronze Pre-Sales Activities Ingestion
act_schema = StructType([
    StructField("activity_id", StringType(), False),
    StructField("opportunity_id", StringType(), True),
    StructField("se_id", StringType(), True),
    StructField("activity_name", StringType(), True),
    StructField("activity_category", StringType(), True),
    StructField("activity_date", StringType(), True),
    StructField("duration_hours", DoubleType(), True),
    StructField("prep_hours", DoubleType(), True),
    StructField("total_effort_hours", DoubleType(), True),
    StructField("customer_attendees_count", IntegerType(), True),
    StructField("customer_sentiment", StringType(), True),
    StructField("technical_objection", StringType(), True),
    StructField("follow_up_required", BooleanType(), True)
])

raw_act_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(act_schema)
    .load("Files/bronze/presales_activities.csv")
)

bronze_act = append_metadata(raw_act_df, "presales_activities.csv", BATCH_ID)

bronze_act.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_presales_activities")

print(f"✓ bronze_presales_activities ingested: {bronze_act.count()} rows")

# CELL 8: Ingest Proof of Concepts (POCs)
# MAGIC %md
# MAGIC ### 6. Bronze Proof of Concept (POC) Ingestion
poc_schema = StructType([
    StructField("poc_id", StringType(), False),
    StructField("opportunity_id", StringType(), True),
    StructField("lead_se_id", StringType(), True),
    StructField("poc_name", StringType(), True),
    StructField("start_date", StringType(), True),
    StructField("end_date", StringType(), True),
    StructField("duration_calendar_days", IntegerType(), True),
    StructField("poc_status", StringType(), True),
    StructField("complexity_level", StringType(), True),
    StructField("technical_criteria_total", IntegerType(), True),
    StructField("technical_criteria_met", IntegerType(), True),
    StructField("criteria_success_rate_pct", DoubleType(), True),
    StructField("is_technical_win", BooleanType(), True),
    StructField("total_se_hours_spent", DoubleType(), True),
    StructField("cloud_lab_infra_cost_usd", DoubleType(), True),
    StructField("technical_blocker_summary", StringType(), True)
])

raw_poc_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(poc_schema)
    .load("Files/bronze/poc_projects.csv")
)

bronze_poc = append_metadata(raw_poc_df, "poc_projects.csv", BATCH_ID)

bronze_poc.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_poc_projects")

print(f"✓ bronze_poc_projects ingested: {bronze_poc.count()} rows")

# CELL 9: Ingest RFP Requests
# MAGIC %md
# MAGIC ### 7. Bronze RFP Requests Ingestion
rfp_schema = StructType([
    StructField("rfp_id", StringType(), False),
    StructField("opportunity_id", StringType(), True),
    StructField("assigned_se_id", StringType(), True),
    StructField("rfp_title", StringType(), True),
    StructField("request_date", StringType(), True),
    StructField("due_date", StringType(), True),
    StructField("submission_date", StringType(), True),
    StructField("turnaround_days", IntegerType(), True),
    StructField("questions_count", IntegerType(), True),
    StructField("compliance_score_pct", DoubleType(), True),
    StructField("rfp_status", StringType(), True),
    StructField("se_effort_hours", DoubleType(), True)
])

raw_rfp_df = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(rfp_schema)
    .load("Files/bronze/rfp_requests.csv")
)

bronze_rfp = append_metadata(raw_rfp_df, "rfp_requests.csv", BATCH_ID)

bronze_rfp.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze_rfp_requests")

print(f"✓ bronze_rfp_requests ingested: {bronze_rfp.count()} rows")
print(f"✓ Ingestion to Bronze Lakehouse completed for batch {BATCH_ID}")
