# Fabric Lakehouse Notebook: 02_silver_sales_transformation
# Description: Cleansing, schema casting, business logic enrichment, and Delta MERGE into Silver layer.
# Target Lakehouse: lh_sales_analytics
# Layer: Silver (Cleaned, Conformed, Deduplicated)

from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, to_date, when, round, datediff, row_number, coalesce, lit, current_timestamp
)
from pyspark.sql.window import Window
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("Fabric_Sales_02_Silver_Transformation") \
    .config("spark.sql.parquet.vorder.enabled", "true") \
    .getOrCreate()

print(f"[{datetime.now().isoformat()}] Starting Fabric Silver Transformation Pipeline...")

# ==============================================================================
# 1. Cleanse & Standardize Customers (silver_customers)
# ==============================================================================
df_cust_raw = spark.table("bronze_customers")
w_cust = Window.partitionBy("CustomerID").orderBy(col("_ingestion_timestamp").desc())

df_cust_silver = df_cust_raw \
    .withColumn("rn", row_number().over(w_cust)) \
    .filter(col("rn") == 1) \
    .drop("rn") \
    .select(
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("CustomerName")).alias("CustomerName"),
        trim(col("CustomerSegment")).alias("CustomerSegment"),
        trim(col("Country")).alias("Country"),
        trim(col("Region")).alias("Region"),
        trim(col("CreditRating")).alias("CreditRating"),
        trim(col("AccountManagerEmail")).alias("AccountManagerEmail"),
        to_date(col("CustomerJoinDate"), "yyyy-MM-dd").alias("CustomerJoinDate"),
        col("IsStrategicAccount").cast("integer").alias("IsStrategicAccount"),
        current_timestamp().alias("_silver_processed_timestamp")
    )

df_cust_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_customers")
print(f"  [CLEAN] silver_customers created with {df_cust_silver.count():,} rows.")

# ==============================================================================
# 2. Cleanse & Standardize Products (silver_products)
# ==============================================================================
df_prod_raw = spark.table("bronze_products")
w_prod = Window.partitionBy("ProductID").orderBy(col("_ingestion_timestamp").desc())

df_prod_silver = df_prod_raw \
    .withColumn("rn", row_number().over(w_prod)) \
    .filter(col("rn") == 1) \
    .drop("rn") \
    .select(
        trim(col("ProductID")).alias("ProductID"),
        trim(col("ProductName")).alias("ProductName"),
        trim(col("Category")).alias("Category"),
        trim(col("SubCategory")).alias("SubCategory"),
        col("StandardCost").cast("double").alias("StandardCostUSD"),
        col("ListPrice").cast("double").alias("ListPriceUSD"),
        round(col("StandardMarginPercent").cast("double"), 4).alias("StandardMarginPercent"),
        col("IsActive").cast("integer").alias("IsActive"),
        current_timestamp().alias("_silver_processed_timestamp")
    )

df_prod_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_products")
print(f"  [CLEAN] silver_products created with {df_prod_silver.count():,} rows.")

# ==============================================================================
# 3. Cleanse & Standardize Store Regions & Channels (silver_store_regions)
# ==============================================================================
df_store_raw = spark.table("bronze_store_regions")
df_store_silver = df_store_raw.select(
    trim(col("ChannelID")).alias("ChannelID"),
    trim(col("ChannelName")).alias("ChannelName"),
    trim(col("RegionCode")).alias("RegionCode"),
    trim(col("RegionName")).alias("RegionName"),
    trim(col("Country")).alias("Country"),
    trim(col("RegionalVP")).alias("RegionalVP"),
    trim(col("SalesDirector")).alias("SalesDirector"),
    trim(col("ChannelType")).alias("ChannelType"),
    trim(col("CommissionTier")).alias("CommissionTier"),
    current_timestamp().alias("_silver_processed_timestamp")
)
df_store_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_store_regions")
print(f"  [CLEAN] silver_store_regions created.")

# ==============================================================================
# 4. Cleanse, Deduplicate & Enrich Sales Transactions (silver_sales)
# ==============================================================================
df_sales_raw = spark.table("bronze_sales")
w_sales = Window.partitionBy("SalesLineID").orderBy(col("_ingestion_timestamp").desc())

df_sales_silver = df_sales_raw \
    .withColumn("rn", row_number().over(w_sales)) \
    .filter(col("rn") == 1) \
    .drop("rn") \
    .select(
        col("SalesLineID").cast("long").alias("SalesLineID"),
        trim(col("SalesOrderNumber")).alias("SalesOrderNumber"),
        col("OrderLineNumber").cast("integer").alias("OrderLineNumber"),
        to_date(col("OrderDate"), "yyyy-MM-dd").alias("OrderDate"),
        to_date(col("ShipDate"), "yyyy-MM-dd").alias("ShipDate"),
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("ProductID")).alias("ProductID"),
        trim(col("ChannelID")).alias("ChannelID"),
        trim(col("TransactionCurrency")).alias("TransactionCurrency"),
        col("Quantity").cast("integer").alias("Quantity"),
        round(col("LocalGrossSales").cast("double"), 2).alias("LocalGrossSales"),
        round(col("LocalDiscount").cast("double"), 2).alias("LocalDiscount"),
        round(col("LocalNetSales").cast("double"), 2).alias("LocalNetSales"),
        round(col("GrossSalesUSD").cast("double"), 2).alias("GrossSalesUSD"),
        round(col("DiscountAmountUSD").cast("double"), 2).alias("DiscountAmountUSD"),
        round(col("NetSalesUSD").cast("double"), 2).alias("NetSalesUSD"),
        round(col("TotalCostUSD").cast("double"), 2).alias("TotalCostUSD"),
        round(col("MarginUSD").cast("double"), 2).alias("MarginUSD"),
        trim(col("OrderStatus")).alias("OrderStatus")
    ) \
    .withColumn("FulfillmentDays", datediff(col("ShipDate"), col("OrderDate"))) \
    .withColumn("GrossMarginPct", round(col("MarginUSD") / when(col("NetSalesUSD") != 0, col("NetSalesUSD")).otherwise(1.0), 4)) \
    .withColumn("DiscountPct", round(col("DiscountAmountUSD") / when(col("GrossSalesUSD") != 0, col("GrossSalesUSD")).otherwise(1.0), 4)) \
    .withColumn("_silver_processed_timestamp", current_timestamp())

# Upsert into Silver Delta table
df_sales_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver_sales")

print(f"  [CLEAN] silver_sales created with {df_sales_silver.count():,} transaction lines.")

# ==============================================================================
# 5. Cleanse & Standardize Sales Budgets (silver_budget)
# ==============================================================================
df_bud_raw = spark.table("bronze_budget")
df_bud_silver = df_bud_raw.select(
    trim(col("BudgetID")).alias("BudgetID"),
    to_date(col("PeriodDate"), "yyyy-MM-dd").alias("PeriodDate"),
    col("YearMonth").cast("integer").alias("YearMonth"),
    trim(col("ChannelID")).alias("ChannelID"),
    trim(col("Category")).alias("Category"),
    round(col("BudgetUSD").cast("double"), 2).alias("BudgetUSD"),
    current_timestamp().alias("_silver_processed_timestamp")
)
df_bud_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_budget")
print(f"  [CLEAN] silver_budget created with {df_bud_silver.count():,} rows.")

print(f"[{datetime.now().isoformat()}] Fabric Silver Transformation Completed Successfully.")
