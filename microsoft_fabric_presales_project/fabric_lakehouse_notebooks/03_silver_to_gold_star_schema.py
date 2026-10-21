# Fabric Notebook: 03_silver_to_gold_star_schema
# Description: Generates dimensional Star Schema (Gold Layer) optimized for Power BI Direct Lake.
#              Enforces Parquet V-Order, builds Dim Date, Dimension tables with surrogate keys,
#              and builds Fact tables with multi-dimensional keys and Z-Order optimization.

# CELL 1: Setup & Direct Lake Optimization Parameters
# MAGIC %md
# MAGIC # 🥇 Notebook 03: Silver to Gold Dimensional Star Schema
# MAGIC **Microsoft Fabric Lakehouse Medallion Architecture**
# MAGIC 
# MAGIC - Builds a Kimball-standard Star Schema ready for **Direct Lake** semantic modeling.
# MAGIC - Enables Microsoft Fabric **Parquet V-Order** for VertiPaq in-memory scanning.
# MAGIC - Generates Role-Playing Date Keys (`YYYYMMDD` integers).
# MAGIC - Optimizes Delta tables via `OPTIMIZE ... ZORDER BY` for lightning-fast Power BI queries.

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

# Fabric Performance Optimization
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.microsoft.delta.autoCompact.enabled", "true")

# CELL 2: Generate Enterprise Calendar Dimension (gold_dim_date)
# MAGIC %md
# MAGIC ### 1. Enterprise Calendar Dimension (`gold_dim_date`)
date_range_df = spark.sql("""
    SELECT explode(sequence(to_date('2023-01-01'), to_date('2027-12-31'), interval 1 day)) as full_date
""")

gold_dim_date = (
    date_range_df
    .withColumn("date_key", F.date_format(F.col("full_date"), "yyyyMMdd").cast("integer"))
    .withColumn("year", F.year(F.col("full_date")))
    .withColumn("quarter_num", F.quarter(F.col("full_date")))
    .withColumn("quarter", F.concat(F.lit("Q"), F.quarter(F.col("full_date"))))
    .withColumn("quarter_name", F.concat(F.year(F.col("full_date")), F.lit("-Q"), F.quarter(F.col("full_date"))))
    .withColumn("month_num", F.month(F.col("full_date")))
    .withColumn("month_name", F.date_format(F.col("full_date"), "MMMM"))
    .withColumn("month_short", F.date_format(F.col("full_date"), "MMM"))
    .withColumn("year_month", F.date_format(F.col("full_date"), "yyyy-MM"))
    .withColumn("week_of_year", F.weekofyear(F.col("full_date")))
    .withColumn("day_of_month", F.dayofmonth(F.col("full_date")))
    .withColumn("day_of_week_num", F.dayofweek(F.col("full_date")))
    .withColumn("day_of_week_name", F.date_format(F.col("full_date"), "EEEE"))
    .withColumn("is_weekend", F.dayofweek(F.col("full_date")).isin(1, 7))
    .withColumn(
        "fiscal_year",
        F.when(F.month(F.col("full_date")) >= 7, F.concat(F.lit("FY"), F.substring(F.year(F.col("full_date")) + 1, 3, 2)))
         .otherwise(F.concat(F.lit("FY"), F.substring(F.year(F.col("full_date")), 3, 2)))
    )
    .withColumn(
        "fiscal_quarter",
        F.when(F.month(F.col("full_date")).isin(7, 8, 9), "FQ1")
         .when(F.month(F.col("full_date")).isin(10, 11, 12), "FQ2")
         .when(F.month(F.col("full_date")).isin(1, 2, 3), "FQ3")
         .otherwise("FQ4")
    )
)

gold_dim_date.write.format("delta").mode("overwrite").saveAsTable("gold_dim_date")
print("✓ gold_dim_date generated successfully.")

# CELL 3: Dimension Account (gold_dim_account)
# MAGIC %md
# MAGIC ### 2. Dimension Account (`gold_dim_account`)
silver_accounts = spark.table("silver_accounts")

gold_dim_account = (
    silver_accounts
    .withColumn("account_sk", F.dense_rank().over(Window.orderBy("account_id")))
    .select(
        F.col("account_sk"),
        F.col("account_id"),
        F.col("account_name"),
        F.col("industry"),
        F.col("account_tier"),
        F.col("annual_revenue_usd"),
        F.col("annual_revenue_bracket"),
        F.col("employee_count"),
        F.col("country_name"),
        F.col("country_code"),
        F.col("region"),
        F.col("account_created_date")
    )
)

gold_dim_account.write.format("delta").mode("overwrite").saveAsTable("gold_dim_account")
print("✓ gold_dim_account generated successfully.")

# CELL 4: Dimension Solution Engineer (gold_dim_solution_engineer)
# MAGIC %md
# MAGIC ### 3. Dimension Solution Engineer (`gold_dim_solution_engineer`)
silver_se = spark.table("silver_solution_engineers")

# Add dummy unassigned row for deals/activities without an assigned SE
unassigned_se = spark.createDataFrame([
    (-1, "UNASSIGNED", "Unassigned / Direct", "unassigned@company.com", "Global", "Not Applicable", "General", 0, 0.0, 0.0)
], ["se_sk", "se_id", "se_name", "email", "region", "seniority_level", "specialization", "target_weekly_hours", "target_utilization_pct", "hourly_cost_rate_usd"])

assigned_se = (
    silver_se
    .withColumn("se_sk", F.dense_rank().over(Window.orderBy("se_id")))
    .select(
        "se_sk", "se_id", "se_name", "email", "region", "seniority_level", 
        "specialization", "target_weekly_hours", "target_utilization_pct", "hourly_cost_rate_usd"
    )
)

gold_dim_se = assigned_se.unionByName(unassigned_se)
gold_dim_se.write.format("delta").mode("overwrite").saveAsTable("gold_dim_solution_engineer")
print("✓ gold_dim_solution_engineer generated successfully.")

# CELL 5: Dimension Product (gold_dim_product)
# MAGIC %md
# MAGIC ### 4. Dimension Product (`gold_dim_product`)
silver_prd = spark.table("silver_products")

gold_dim_product = (
    silver_prd
    .withColumn("product_sk", F.dense_rank().over(Window.orderBy("product_id")))
    .select(
        "product_sk", "product_id", "product_name", "product_category",
        "deployment_model", "base_annual_license_usd", "standard_poc_duration_days"
    )
)

gold_dim_product.write.format("delta").mode("overwrite").saveAsTable("gold_dim_product")
print("✓ gold_dim_product generated successfully.")

# CELL 6: Dimension Opportunity (gold_dim_opportunity)
# MAGIC %md
# MAGIC ### 5. Dimension Opportunity (`gold_dim_opportunity`)
silver_opp = spark.table("silver_opportunities")

gold_dim_opportunity = (
    silver_opp
    .withColumn("opportunity_sk", F.dense_rank().over(Window.orderBy("opportunity_id")))
    .select(
        "opportunity_sk", "opportunity_id", "opportunity_name", "ae_owner_name",
        "deal_type", "deal_stage", "deal_status", "deal_size_tier",
        "presales_touch_level", "competitor_name", "win_loss_reason", "is_technical_loss"
    )
)

gold_dim_opportunity.write.format("delta").mode("overwrite").saveAsTable("gold_dim_opportunity")
print("✓ gold_dim_opportunity generated successfully.")

# CELL 7: Dimension Pre-Sales Activity Type (gold_dim_activity_type)
# MAGIC %md
# MAGIC ### 6. Dimension Pre-Sales Activity Type (`gold_dim_activity_type`)
silver_act = spark.table("silver_presales_activities")

gold_dim_act_type = (
    silver_act.select("activity_name", "activity_category").distinct()
    .withColumn("activity_type_sk", F.dense_rank().over(Window.orderBy("activity_name")))
    .withColumn(
        "is_customer_facing",
        ~F.col("activity_category").isin("Internal Prep", "Admin")
    )
    .select("activity_type_sk", "activity_name", "activity_category", "is_customer_facing")
)

gold_dim_act_type.write.format("delta").mode("overwrite").saveAsTable("gold_dim_activity_type")
print("✓ gold_dim_activity_type generated successfully.")

# CELL 8: Fact Pre-Sales Activities (gold_fact_presales_activity)
# MAGIC %md
# MAGIC ### 7. Fact Pre-Sales Activities (`gold_fact_presales_activity`)
gold_dim_acc_ref = spark.table("gold_dim_account").select("account_id", "account_sk")
gold_dim_opp_ref = spark.table("gold_dim_opportunity").select("opportunity_id", "opportunity_sk")
gold_dim_se_ref = spark.table("gold_dim_solution_engineer").select("se_id", "se_sk")
gold_dim_type_ref = spark.table("gold_dim_activity_type").select("activity_name", "activity_type_sk")
gold_dim_prd_ref = spark.table("gold_dim_product").select("product_id", "product_sk")
silver_opp_lookup = spark.table("silver_opportunities").select("opportunity_id", "account_id", "product_id")

gold_fact_act = (
    silver_act
    .join(silver_opp_lookup, on="opportunity_id", how="left")
    .join(gold_dim_acc_ref, on="account_id", how="left")
    .join(gold_dim_opp_ref, on="opportunity_id", how="left")
    .join(gold_dim_se_ref, on="se_id", how="left")
    .join(gold_dim_prd_ref, on="product_id", how="left")
    .join(gold_dim_type_ref, on="activity_name", how="left")
    .withColumn("activity_date_key", F.date_format("activity_date", "yyyyMMdd").cast("integer"))
    .withColumn("activity_sk", F.monotonically_increasing_id() + 1)
    .select(
        F.col("activity_sk"),
        F.col("activity_id"),
        F.col("activity_date_key"),
        F.coalesce(F.col("account_sk"), F.lit(-1)).alias("account_sk"),
        F.coalesce(F.col("opportunity_sk"), F.lit(-1)).alias("opportunity_sk"),
        F.coalesce(F.col("se_sk"), F.lit(-1)).alias("se_sk"),
        F.coalesce(F.col("product_sk"), F.lit(-1)).alias("product_sk"),
        F.coalesce(F.col("activity_type_sk"), F.lit(-1)).alias("activity_type_sk"),
        F.col("duration_hours"),
        F.col("prep_hours"),
        F.col("total_effort_hours"),
        F.col("activity_cost_usd"),
        F.col("customer_attendees_count"),
        F.col("customer_sentiment"),
        F.col("technical_objection"),
        F.col("follow_up_required")
    )
)

gold_fact_act.write.format("delta").mode("overwrite").saveAsTable("gold_fact_presales_activity")
spark.sql("OPTIMIZE gold_fact_presales_activity ZORDER BY (activity_date_key, se_sk)")
print("✓ gold_fact_presales_activity generated & Z-Ordered.")

# CELL 9: Fact Proof of Concept (gold_fact_poc)
# MAGIC %md
# MAGIC ### 8. Fact Proof of Concept (`gold_fact_poc`)
silver_poc = spark.table("silver_poc_projects")

gold_fact_poc = (
    silver_poc
    .join(silver_opp_lookup, on="opportunity_id", how="left")
    .join(gold_dim_acc_ref, on="account_id", how="left")
    .join(gold_dim_opp_ref, on="opportunity_id", how="left")
    .join(gold_dim_prd_ref, on="product_id", how="left")
    .join(gold_dim_se_ref.withColumnRenamed("se_id", "lead_se_id").withColumnRenamed("se_sk", "lead_se_sk"), on="lead_se_id", how="left")
    .withColumn("start_date_key", F.date_format("start_date", "yyyyMMdd").cast("integer"))
    .withColumn("end_date_key", F.date_format("end_date", "yyyyMMdd").cast("integer"))
    .withColumn("poc_sk", F.monotonically_increasing_id() + 1)
    .select(
        F.col("poc_sk"),
        F.col("poc_id"),
        F.col("start_date_key"),
        F.col("end_date_key"),
        F.coalesce(F.col("opportunity_sk"), F.lit(-1)).alias("opportunity_sk"),
        F.coalesce(F.col("account_sk"), F.lit(-1)).alias("account_sk"),
        F.coalesce(F.col("lead_se_sk"), F.lit(-1)).alias("lead_se_sk"),
        F.coalesce(F.col("product_sk"), F.lit(-1)).alias("product_sk"),
        F.col("duration_calendar_days"),
        F.col("poc_status"),
        F.col("complexity_level"),
        F.col("technical_criteria_total"),
        F.col("technical_criteria_met"),
        F.col("criteria_success_rate_pct"),
        F.col("is_technical_win"),
        F.col("total_se_hours_spent"),
        F.col("cloud_lab_infra_cost_usd"),
        F.col("total_poc_investment_usd"),
        F.col("technical_blocker_summary")
    )
)

gold_fact_poc.write.format("delta").mode("overwrite").saveAsTable("gold_fact_poc")
spark.sql("OPTIMIZE gold_fact_poc ZORDER BY (start_date_key, lead_se_sk)")
print("✓ gold_fact_poc generated & Z-Ordered.")

# CELL 10: Fact Opportunity Pipeline & Win/Loss (gold_fact_opportunity_snapshot)
# MAGIC %md
# MAGIC ### 9. Fact Opportunity Pipeline (`gold_fact_opportunity_snapshot`)
gold_fact_opp = (
    silver_opp
    .join(gold_dim_acc_ref, on="account_id", how="left")
    .join(gold_dim_opp_ref, on="opportunity_id", how="left")
    .join(gold_dim_prd_ref, on="product_id", how="left")
    .join(gold_dim_se_ref.withColumnRenamed("se_id", "se_assigned_id").withColumnRenamed("se_sk", "assigned_se_sk"), on="se_assigned_id", how="left")
    .withColumn("created_date_key", F.date_format("created_date", "yyyyMMdd").cast("integer"))
    .withColumn("target_close_date_key", F.date_format("target_close_date", "yyyyMMdd").cast("integer"))
    .withColumn("actual_close_date_key", F.when(F.col("actual_close_date").isNotNull(), F.date_format("actual_close_date", "yyyyMMdd").cast("integer")).otherwise(F.lit(None)))
    .select(
        F.col("opportunity_sk"),
        F.coalesce(F.col("account_sk"), F.lit(-1)).alias("account_sk"),
        F.coalesce(F.col("product_sk"), F.lit(-1)).alias("product_sk"),
        F.coalesce(F.col("assigned_se_sk"), F.lit(-1)).alias("assigned_se_sk"),
        F.col("created_date_key"),
        F.col("target_close_date_key"),
        F.col("actual_close_date_key"),
        F.col("annual_contract_value_usd"),
        F.col("total_contract_value_usd"),
        F.col("is_presales_engaged"),
        F.col("poc_conducted"),
        F.col("is_closed"),
        F.col("is_won"),
        F.col("is_lost"),
        F.col("is_technical_loss"),
        F.col("sales_cycle_days")
    )
)

gold_fact_opp.write.format("delta").mode("overwrite").saveAsTable("gold_fact_opportunity_snapshot")
spark.sql("OPTIMIZE gold_fact_opportunity_snapshot ZORDER BY (created_date_key, account_sk)")
print("✓ gold_fact_opportunity_snapshot generated & Z-Ordered.")

# CELL 11: Fact RFP Requests (gold_fact_rfp)
# MAGIC %md
# MAGIC ### 10. Fact RFP Requests (`gold_fact_rfp`)
silver_rfp = spark.table("silver_rfp_requests")

gold_fact_rfp = (
    silver_rfp
    .join(gold_dim_opp_ref, on="opportunity_id", how="left")
    .join(gold_dim_se_ref.withColumnRenamed("se_id", "assigned_se_id").withColumnRenamed("se_sk", "assigned_se_sk"), on="assigned_se_id", how="left")
    .withColumn("request_date_key", F.date_format("request_date", "yyyyMMdd").cast("integer"))
    .withColumn("submission_date_key", F.date_format("submission_date", "yyyyMMdd").cast("integer"))
    .withColumn("rfp_sk", F.monotonically_increasing_id() + 1)
    .select(
        F.col("rfp_sk"),
        F.col("rfp_id"),
        F.col("request_date_key"),
        F.col("submission_date_key"),
        F.coalesce(F.col("opportunity_sk"), F.lit(-1)).alias("opportunity_sk"),
        F.coalesce(F.col("assigned_se_sk"), F.lit(-1)).alias("assigned_se_sk"),
        F.col("turnaround_days"),
        F.col("questions_count"),
        F.col("compliance_score_pct"),
        F.col("rfp_status"),
        F.col("se_effort_hours"),
        F.col("hours_per_question")
    )
)

gold_fact_rfp.write.format("delta").mode("overwrite").saveAsTable("gold_fact_rfp")
spark.sql("OPTIMIZE gold_fact_rfp ZORDER BY (request_date_key, assigned_se_sk)")
print("✓ gold_fact_rfp generated & Z-Ordered.")
print("======================================================================")
print("✓ GOLD STAR SCHEMA COMPLETE! Ready for Power BI Direct Lake modeling.")
print("======================================================================")
