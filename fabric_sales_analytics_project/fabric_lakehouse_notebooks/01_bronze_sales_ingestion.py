# Fabric Lakehouse Notebook: 01_bronze_sales_ingestion
# Description: Automated Raw Ingestion of Sales Operational CSV/Parquet into Delta Lake Bronze tables in OneLake.
# Target Lakehouse: lh_sales_analytics
# Layer: Bronze (Raw zone, append-only, lineage auditing)

import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit, expr

# Initialize Spark session (automatic in Microsoft Fabric)
spark = SparkSession.builder \
    .appName("Fabric_Sales_01_Bronze_Ingestion") \
    .config("spark.sql.parquet.vorder.enabled", "true") \
    .getOrCreate()

print(f"[{datetime.now().isoformat()}] Starting Fabric Bronze Sales Ingestion Pipeline...")

# Define OneLake Landing Zone Paths
LANDING_ZONE_PATH = "Files/landing_sales/"
BRONZE_DELTA_TABLES = {
    "bronze_sales": f"{LANDING_ZONE_PATH}Fact_Sales.csv",
    "bronze_budget": f"{LANDING_ZONE_PATH}Fact_Budget.csv",
    "bronze_customers": f"{LANDING_ZONE_PATH}Dim_Customer.csv",
    "bronze_products": f"{LANDING_ZONE_PATH}Dim_Product.csv",
    "bronze_store_regions": f"{LANDING_ZONE_PATH}Dim_Store_Region.csv",
    "bronze_sales_reps": f"{LANDING_ZONE_PATH}Dim_SalesRep.csv",
    "bronze_dates": f"{LANDING_ZONE_PATH}Dim_Date.csv"
}

batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")

for table_name, file_path in BRONZE_DELTA_TABLES.items():
    print(f"--> Ingesting raw source: {file_path} into Delta table: {table_name}")
    try:
        # Read raw CSV with header and inferred schema
        df_raw = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(file_path)
        
        # Add system audit and lineage tracking columns
        df_bronze = df_raw \
            .withColumn("_ingestion_timestamp", current_timestamp()) \
            .withColumn("_source_file", input_file_name()) \
            .withColumn("_batch_id", lit(batch_id))
        
        # Save as Bronze Delta Table with V-Order optimization enabled
        df_bronze.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .saveAsTable(table_name)
        
        count = spark.table(table_name).count()
        print(f"    [SUCCESS] Ingested {count:,} rows into Bronze table '{table_name}'.")
        
    except Exception as e:
        print(f"    [WARNING] Could not ingest {file_path}: {str(e)}")

print(f"[{datetime.now().isoformat()}] Fabric Bronze Ingestion Finished Successfully.")
