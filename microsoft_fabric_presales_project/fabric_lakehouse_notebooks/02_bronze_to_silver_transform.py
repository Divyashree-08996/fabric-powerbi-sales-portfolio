# Fabric Notebook: 02_bronze_to_silver_transform
# Description: Cleanses, enriches, deduplicates, and validates Bronze Pre-Sales data.
#              Writes harmonized, conformed Delta tables in the Silver Lakehouse layer.

# CELL 1: Setup & Delta Imports
# MAGIC %md
# MAGIC # 🥈 Notebook 02: Bronze to Silver Harmonization & Enrichment
# MAGIC **Microsoft Fabric Lakehouse Medallion Architecture**
# MAGIC 
# MAGIC - Deduplication via Window functions on natural keys.
# MAGIC - Schema normalization and casting strings to strict Dates, Decimals, and Booleans.
# MAGIC - Enriching deals with Pre-Sales cost of sale, deal velocity, and technical win flags.
# MAGIC - Upserting via Delta Lake `MERGE` to support incremental batch processing.

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

spark.conf.set("spark.sql.parquet.vorder.enabled", "true")

# CELL 2: Silver Accounts Harmonization
# MAGIC %md
# MAGIC ### 1. Silver Accounts Processing
raw_acc_df = spark.table("bronze_crm_accounts")

# Window to deduplicate latest record per account_id
acc_window = Window.partitionBy("account_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_accounts_df = (
    raw_acc_df.withColumn("row_num", F.row_number().over(acc_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("account_id")).alias("account_id"),
        F.trim(F.col("account_name")).alias("account_name"),
        F.coalesce(F.trim(F.col("industry")), F.lit("Other")).alias("industry"),
        F.coalesce(F.trim(F.col("account_tier")), F.lit("Standard")).alias("account_tier"),
        F.col("annual_revenue_usd").cast("double").alias("annual_revenue_usd"),
        F.when(F.col("annual_revenue_usd") >= 1000000000, "Enterprise Tier 1 (>$1B)")
         .when(F.col("annual_revenue_usd") >= 250000000, "Enterprise Tier 2 ($250M-$1B)")
         .otherwise("Mid-Market (<$250M)").alias("annual_revenue_bracket"),
        F.col("employee_count").cast("integer").alias("employee_count"),
        F.trim(F.col("country_name")).alias("country_name"),
        F.upper(F.trim(F.col("country_code"))).alias("country_code"),
        F.trim(F.col("region")).alias("region"),
        F.col("created_date").cast("date").alias("account_created_date"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

# Merge into silver_accounts
if not spark.catalog.tableExists("silver_accounts"):
    silver_accounts_df.write.format("delta").mode("overwrite").saveAsTable("silver_accounts")
else:
    target_table = DeltaTable.forName(spark, "silver_accounts")
    (
        target_table.alias("target")
        .merge(
            silver_accounts_df.alias("source"),
            "target.account_id = source.account_id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

print("✓ silver_accounts upsert complete.")

# CELL 3: Silver Products Processing
# MAGIC %md
# MAGIC ### 2. Silver Products Processing
raw_prd_df = spark.table("bronze_products")
prd_window = Window.partitionBy("product_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_products_df = (
    raw_prd_df.withColumn("row_num", F.row_number().over(prd_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("product_id")).alias("product_id"),
        F.trim(F.col("product_name")).alias("product_name"),
        F.trim(F.col("product_category")).alias("product_category"),
        F.trim(F.col("deployment_model")).alias("deployment_model"),
        F.col("base_annual_license_usd").cast("double").alias("base_annual_license_usd"),
        F.col("standard_poc_duration_days").cast("integer").alias("standard_poc_duration_days"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_products"):
    silver_products_df.write.format("delta").mode("overwrite").saveAsTable("silver_products")
else:
    target_prd = DeltaTable.forName(spark, "silver_products")
    target_prd.alias("tgt").merge(
        silver_products_df.alias("src"),
        "tgt.product_id = src.product_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_products upsert complete.")

# CELL 4: Silver Solution Engineers Processing
# MAGIC %md
# MAGIC ### 3. Silver Solution Engineers Processing
raw_se_df = spark.table("bronze_solution_engineers")
se_window = Window.partitionBy("se_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_se_df = (
    raw_se_df.withColumn("row_num", F.row_number().over(se_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("se_id")).alias("se_id"),
        F.trim(F.col("se_name")).alias("se_name"),
        F.lower(F.trim(F.col("email"))).alias("email"),
        F.trim(F.col("region")).alias("region"),
        F.trim(F.col("seniority_level")).alias("seniority_level"),
        F.trim(F.col("specialization")).alias("specialization"),
        F.col("target_weekly_hours").cast("integer").alias("target_weekly_hours"),
        F.col("target_utilization_pct").cast("double").alias("target_utilization_pct"),
        F.col("hourly_cost_rate_usd").cast("double").alias("hourly_cost_rate_usd"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_solution_engineers"):
    silver_se_df.write.format("delta").mode("overwrite").saveAsTable("silver_solution_engineers")
else:
    target_se = DeltaTable.forName(spark, "silver_solution_engineers")
    target_se.alias("tgt").merge(
        silver_se_df.alias("src"),
        "tgt.se_id = src.se_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_solution_engineers upsert complete.")

# CELL 5: Silver CRM Opportunities Enrichment
# MAGIC %md
# MAGIC ### 4. Silver CRM Opportunities Enrichment & Metrics
raw_opp_df = spark.table("bronze_crm_opportunities")
opp_window = Window.partitionBy("opportunity_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_opp_df = (
    raw_opp_df.withColumn("row_num", F.row_number().over(opp_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .withColumn("created_date_dt", F.col("created_date").cast("date"))
    .withColumn("actual_close_date_dt", F.col("actual_close_date").cast("date"))
    .withColumn("target_close_date_dt", F.col("target_close_date").cast("date"))
    .withColumn(
        "sales_cycle_days",
        F.when(F.col("actual_close_date_dt").isNotNull(),
               F.datediff(F.col("actual_close_date_dt"), F.col("created_date_dt")))
         .otherwise(F.datediff(F.current_date(), F.col("created_date_dt")))
    )
    .withColumn("is_closed", F.col("deal_status").isin("Closed Won", "Closed Lost"))
    .withColumn("is_won", F.col("deal_status") == "Closed Won")
    .withColumn("is_lost", F.col("deal_status") == "Closed Lost")
    .withColumn(
        "deal_size_tier",
        F.when(F.col("annual_contract_value_usd") >= 400000, "Jumbo Enterprise (>$400k)")
         .when(F.col("annual_contract_value_usd") >= 200000, "Major ($200k-$400k)")
         .when(F.col("annual_contract_value_usd") >= 75000, "Core ($75k-$200k)")
         .otherwise("Velocity / Emerging (<$75k)")
    )
    .withColumn(
        "presales_touch_level",
        F.when(F.col("poc_conducted") == True, "High Touch (POC Completed)")
         .when(F.col("is_presales_engaged") == True, "Medium Touch (SE Engaged)")
         .otherwise("Low / Unassisted (Self-Serve / Rep Only)")
    )
    .select(
        F.trim(F.col("opportunity_id")).alias("opportunity_id"),
        F.trim(F.col("account_id")).alias("account_id"),
        F.trim(F.col("opportunity_name")).alias("opportunity_name"),
        F.trim(F.col("ae_owner_name")).alias("ae_owner_name"),
        F.trim(F.col("product_id")).alias("product_id"),
        F.trim(F.col("deal_type")).alias("deal_type"),
        F.col("created_date_dt").alias("created_date"),
        F.col("target_close_date_dt").alias("target_close_date"),
        F.col("actual_close_date_dt").alias("actual_close_date"),
        F.trim(F.col("deal_stage")).alias("deal_stage"),
        F.trim(F.col("deal_status")).alias("deal_status"),
        F.col("annual_contract_value_usd").cast("double").alias("annual_contract_value_usd"),
        F.col("total_contract_value_usd").cast("double").alias("total_contract_value_usd"),
        F.coalesce(F.trim(F.col("se_assigned_id")), F.lit("UNASSIGNED")).alias("se_assigned_id"),
        F.col("is_presales_engaged").cast("boolean").alias("is_presales_engaged"),
        F.col("poc_conducted").cast("boolean").alias("poc_conducted"),
        F.coalesce(F.trim(F.col("competitor_name")), F.lit("None")).alias("competitor_name"),
        F.coalesce(F.trim(F.col("win_loss_reason")), F.lit("N/A - In Flight")).alias("win_loss_reason"),
        F.col("is_technical_loss").cast("boolean").alias("is_technical_loss"),
        F.col("sales_cycle_days").cast("integer").alias("sales_cycle_days"),
        F.col("is_closed").cast("boolean").alias("is_closed"),
        F.col("is_won").cast("boolean").alias("is_won"),
        F.col("is_lost").cast("boolean").alias("is_lost"),
        F.col("deal_size_tier").alias("deal_size_tier"),
        F.col("presales_touch_level").alias("presales_touch_level"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_opportunities"):
    silver_opp_df.write.format("delta").mode("overwrite").saveAsTable("silver_opportunities")
else:
    target_opp = DeltaTable.forName(spark, "silver_opportunities")
    target_opp.alias("tgt").merge(
        silver_opp_df.alias("src"),
        "tgt.opportunity_id = src.opportunity_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_opportunities upsert complete.")

# CELL 6: Silver Pre-Sales Activities Processing
# MAGIC %md
# MAGIC ### 5. Silver Pre-Sales Activities & Effort Costing
raw_act_df = spark.table("bronze_presales_activities")
act_window = Window.partitionBy("activity_id").orderBy(F.col("_ingestion_timestamp").desc())

# Join with SE hourly cost to enrich effort cost
silver_act_df = (
    raw_act_df.withColumn("row_num", F.row_number().over(act_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .join(silver_se_df.select("se_id", "hourly_cost_rate_usd"), on="se_id", how="left")
    .withColumn("hourly_rate", F.coalesce(F.col("hourly_cost_rate_usd"), F.lit(125.0)))
    .withColumn("duration_hours", F.col("duration_hours").cast("double"))
    .withColumn("prep_hours", F.col("prep_hours").cast("double"))
    .withColumn("total_effort_hours", F.col("duration_hours") + F.col("prep_hours"))
    .withColumn("activity_cost_usd", F.round(F.col("total_effort_hours") * F.col("hourly_rate"), 2))
    .select(
        F.trim(F.col("activity_id")).alias("activity_id"),
        F.trim(F.col("opportunity_id")).alias("opportunity_id"),
        F.trim(F.col("se_id")).alias("se_id"),
        F.trim(F.col("activity_name")).alias("activity_name"),
        F.trim(F.col("activity_category")).alias("activity_category"),
        F.col("activity_date").cast("date").alias("activity_date"),
        F.col("duration_hours").alias("duration_hours"),
        F.col("prep_hours").alias("prep_hours"),
        F.col("total_effort_hours").alias("total_effort_hours"),
        F.col("activity_cost_usd").alias("activity_cost_usd"),
        F.col("customer_attendees_count").cast("integer").alias("customer_attendees_count"),
        F.trim(F.col("customer_sentiment")).alias("customer_sentiment"),
        F.trim(F.col("technical_objection")).alias("technical_objection"),
        F.col("follow_up_required").cast("boolean").alias("follow_up_required"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_presales_activities"):
    silver_act_df.write.format("delta").mode("overwrite").saveAsTable("silver_presales_activities")
else:
    target_act = DeltaTable.forName(spark, "silver_presales_activities")
    target_act.alias("tgt").merge(
        silver_act_df.alias("src"),
        "tgt.activity_id = src.activity_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_presales_activities upsert complete.")

# CELL 7: Silver Proof of Concepts (POC) Processing
# MAGIC %md
# MAGIC ### 6. Silver POC Processing & Technical ROI
raw_poc_df = spark.table("bronze_poc_projects")
poc_window = Window.partitionBy("poc_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_poc_df = (
    raw_poc_df.withColumn("row_num", F.row_number().over(poc_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .join(silver_se_df.select(F.col("se_id").alias("lead_se_id"), "hourly_cost_rate_usd"), on="lead_se_id", how="left")
    .withColumn("hourly_rate", F.coalesce(F.col("hourly_cost_rate_usd"), F.lit(130.0)))
    .withColumn("se_labor_cost_usd", F.round(F.col("total_se_hours_spent") * F.col("hourly_rate"), 2))
    .withColumn("cloud_infra_cost", F.coalesce(F.col("cloud_lab_infra_cost_usd").cast("double"), F.lit(0.0)))
    .withColumn("total_poc_investment_usd", F.round(F.col("se_labor_cost_usd") + F.col("cloud_infra_cost"), 2))
    .select(
        F.trim(F.col("poc_id")).alias("poc_id"),
        F.trim(F.col("opportunity_id")).alias("opportunity_id"),
        F.trim(F.col("lead_se_id")).alias("lead_se_id"),
        F.trim(F.col("poc_name")).alias("poc_name"),
        F.col("start_date").cast("date").alias("start_date"),
        F.col("end_date").cast("date").alias("end_date"),
        F.col("duration_calendar_days").cast("integer").alias("duration_calendar_days"),
        F.trim(F.col("poc_status")).alias("poc_status"),
        F.trim(F.col("complexity_level")).alias("complexity_level"),
        F.col("technical_criteria_total").cast("integer").alias("technical_criteria_total"),
        F.col("technical_criteria_met").cast("integer").alias("technical_criteria_met"),
        F.col("criteria_success_rate_pct").cast("double").alias("criteria_success_rate_pct"),
        F.col("is_technical_win").cast("boolean").alias("is_technical_win"),
        F.col("total_se_hours_spent").cast("double").alias("total_se_hours_spent"),
        F.col("cloud_infra_cost").alias("cloud_lab_infra_cost_usd"),
        F.col("total_poc_investment_usd").alias("total_poc_investment_usd"),
        F.trim(F.col("technical_blocker_summary")).alias("technical_blocker_summary"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_poc_projects"):
    silver_poc_df.write.format("delta").mode("overwrite").saveAsTable("silver_poc_projects")
else:
    target_poc = DeltaTable.forName(spark, "silver_poc_projects")
    target_poc.alias("tgt").merge(
        silver_poc_df.alias("src"),
        "tgt.poc_id = src.poc_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_poc_projects upsert complete.")

# CELL 8: Silver RFP Requests Processing
# MAGIC %md
# MAGIC ### 7. Silver RFP Requests Processing
raw_rfp_df = spark.table("bronze_rfp_requests")
rfp_window = Window.partitionBy("rfp_id").orderBy(F.col("_ingestion_timestamp").desc())

silver_rfp_df = (
    raw_rfp_df.withColumn("row_num", F.row_number().over(rfp_window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .withColumn("hours_per_question", F.round(F.col("se_effort_hours") / F.col("questions_count"), 2))
    .select(
        F.trim(F.col("rfp_id")).alias("rfp_id"),
        F.trim(F.col("opportunity_id")).alias("opportunity_id"),
        F.trim(F.col("assigned_se_id")).alias("assigned_se_id"),
        F.trim(F.col("rfp_title")).alias("rfp_title"),
        F.col("request_date").cast("date").alias("request_date"),
        F.col("due_date").cast("date").alias("due_date"),
        F.col("submission_date").cast("date").alias("submission_date"),
        F.col("turnaround_days").cast("integer").alias("turnaround_days"),
        F.col("questions_count").cast("integer").alias("questions_count"),
        F.col("compliance_score_pct").cast("double").alias("compliance_score_pct"),
        F.trim(F.col("rfp_status")).alias("rfp_status"),
        F.col("se_effort_hours").cast("double").alias("se_effort_hours"),
        F.col("hours_per_question").alias("hours_per_question"),
        F.current_timestamp().alias("_silver_processed_timestamp")
    )
)

if not spark.catalog.tableExists("silver_rfp_requests"):
    silver_rfp_df.write.format("delta").mode("overwrite").saveAsTable("silver_rfp_requests")
else:
    target_rfp = DeltaTable.forName(spark, "silver_rfp_requests")
    target_rfp.alias("tgt").merge(
        silver_rfp_df.alias("src"),
        "tgt.rfp_id = src.rfp_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("✓ silver_rfp_requests upsert complete.")
print("✓ Silver Lakehouse Transformation pipeline completed successfully!")
