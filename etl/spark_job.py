# etl/spark_job.py

import os
from pyspark.sql import SparkSession
from transform import run_etl_pipeline  # Assuming this is the correct import for your ETL logic


def create_spark_session(app_name="FinanceETLJob"):
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()


def main():
    spark = create_spark_session()
    print("🚀 Starting ETL Job...")
    run_etl_pipeline(spark)  # Assuming this function runs your ETL logic
    spark.stop()
    print("✅ ETL Job Completed.")

if __name__ == "__main__":
    main()
