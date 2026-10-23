# Fabric Lakehouse Notebook: 03_gold_star_schema_modeling
# Description: Kimball Star Schema dimensional modeling, surrogate keys, V-Order optimization, and Z-Order for Power BI Direct Lake.
# Target Lakehouse: lh_sales_analytics
# Layer: Gold (Direct Lake & Semantic Model consumption)

from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, monotonically_increasing_id, date_format, year, month, quarter, dayofweek,
    when, lit, current_timestamp
)

spark = SparkSession.builder \
    .appName("Fabric_Sales_03_Gold_Dimensional_Modeling") \
    .config("spark.sql.parquet.vorder.enabled", "true") \
    .config("spark.microsoft.delta.optimizeWrite.enabled", "true") \
    .config("spark.microsoft.delta.autoCompact.enabled", "true") \
    .getOrCreate()

print(f"[{datetime.now().isoformat()}] Starting Fabric Gold Star Schema Generation...")

# ==============================================================================
# 1. Gold Dimension: gold_dim_customer
# ==============================================================================
df_silver_cust = spark.table("silver_customers")
df_gold_cust = df_silver_cust \
    .withColumn("CustomerKey", monotonically_increasing_id() + 1000) \
    .select(
        "CustomerKey",
        "CustomerID",
        "CustomerName",
        "CustomerSegment",
        "Country",
        "Region",
        "CreditRating",
        "AccountManagerEmail",
        "CustomerJoinDate",
        "IsStrategicAccount"
    )

df_gold_cust.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_dim_customer")
print(f"  [GOLD] Dimension table 'gold_dim_customer' created.")

# ==============================================================================
# 2. Gold Dimension: gold_dim_product
# ==============================================================================
df_silver_prod = spark.table("silver_products")
df_gold_prod = df_silver_prod \
    .withColumn("ProductKey", monotonically_increasing_id() + 2000) \
    .select(
        "ProductKey",
        "ProductID",
        "ProductName",
        "Category",
        "SubCategory",
        "StandardCostUSD",
        "ListPriceUSD",
        "StandardMarginPercent",
        "IsActive"
    )

df_gold_prod.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_dim_product")
print(f"  [GOLD] Dimension table 'gold_dim_product' created.")

# ==============================================================================
# 3. Gold Dimension: gold_dim_store_region
# ==============================================================================
df_silver_store = spark.table("silver_store_regions")
df_gold_store = df_silver_store \
    .withColumn("StoreRegionKey", monotonically_increasing_id() + 3000) \
    .select(
        "StoreRegionKey",
        "ChannelID",
        "ChannelName",
        "RegionCode",
        "RegionName",
        "Country",
        "RegionalVP",
        "SalesDirector",
        "ChannelType",
        "CommissionTier"
    )

df_gold_store.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_dim_store_region")
print(f"  [GOLD] Dimension table 'gold_dim_store_region' created.")

# ==============================================================================
# 4. Gold Dimension: gold_dim_date
# ==============================================================================
df_raw_date = spark.table("bronze_dates")
df_gold_date = df_raw_date.select(
    date_format(col("Date"), "yyyyMMdd").cast("integer").alias("DateKey"),
    col("Date").cast("date").alias("Date"),
    col("Year").cast("integer").alias("Year"),
    col("Quarter").cast("string").alias("Quarter"),
    col("MonthNum").cast("integer").alias("MonthNum"),
    col("MonthName").cast("string").alias("MonthName"),
    col("YearMonth").cast("integer").alias("YearMonth"),
    col("DayOfWeek").cast("integer").alias("DayOfWeek"),
    col("IsWeekend").cast("integer").alias("IsWeekend"),
    col("FiscalYear").cast("string").alias("FiscalYear"),
    col("FiscalQuarter").cast("string").alias("FiscalQuarter")
)

df_gold_date.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_dim_date")
print(f"  [GOLD] Dimension table 'gold_dim_date' created.")

# ==============================================================================
# 5. Gold Fact: gold_fact_sales
# ==============================================================================
df_silver_sales = spark.table("silver_sales")

df_gold_sales = df_silver_sales \
    .join(df_gold_cust.select("CustomerID", "CustomerKey"), on="CustomerID", how="left") \
    .join(df_gold_prod.select("ProductID", "ProductKey"), on="ProductID", how="left") \
    .join(df_gold_store.select("ChannelID", "StoreRegionKey"), on="ChannelID", how="left") \
    .withColumn("OrderDateKey", date_format(col("OrderDate"), "yyyyMMdd").cast("integer")) \
    .withColumn("ShipDateKey", date_format(col("ShipDate"), "yyyyMMdd").cast("integer")) \
    .select(
        "SalesLineID",
        "SalesOrderNumber",
        "OrderLineNumber",
        "OrderDateKey",
        "ShipDateKey",
        "CustomerKey",
        "ProductKey",
        "StoreRegionKey",
        "Quantity",
        "GrossSalesUSD",
        "DiscountAmountUSD",
        "NetSalesUSD",
        "TotalCostUSD",
        "MarginUSD",
        "GrossMarginPct",
        "DiscountPct",
        "FulfillmentDays",
        "OrderStatus"
    )

# Save with V-Order and cluster with Z-Order on key join columns
df_gold_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_fact_sales")

# Optimize Delta table with Z-ORDER for sub-second Direct Lake query speeds
spark.sql("OPTIMIZE gold_fact_sales ZORDER BY (OrderDateKey, CustomerKey, ProductKey)")
print(f"  [GOLD] Fact table 'gold_fact_sales' optimized with V-Order and Z-Order on 3 keys.")

# ==============================================================================
# 6. Gold Fact: gold_fact_budget
# ==============================================================================
df_silver_bud = spark.table("silver_budget")
df_gold_bud = df_silver_bud \
    .join(df_gold_store.select("ChannelID", "StoreRegionKey"), on="ChannelID", how="left") \
    .withColumn("DateKey", date_format(col("PeriodDate"), "yyyyMMdd").cast("integer")) \
    .select(
        "BudgetID",
        "DateKey",
        "YearMonth",
        "StoreRegionKey",
        "Category",
        "BudgetUSD"
    )

df_gold_bud.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_fact_budget")
spark.sql("OPTIMIZE gold_fact_budget ZORDER BY (DateKey, StoreRegionKey)")
print(f"  [GOLD] Fact table 'gold_fact_budget' created and optimized.")

print(f"[{datetime.now().isoformat()}] Fabric Gold Star Schema Ready for Direct Lake Power BI!")
