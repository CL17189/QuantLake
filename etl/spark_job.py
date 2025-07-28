# etl/spark_job.py

import os
from pyspark.sql import SparkSession
from transform import run_etl_pipeline  # Assuming this is the correct import for your ETL logic
from delta import configure_spark_with_delta_pip


def create_spark_session(app_name="QuantLakeETL"):  
    builder = SparkSession.builder.appName(app_name) 
    builder = builder.config("spark.master", "local[*]") 
    # Delta Lake extensions
    builder = builder.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") 
    builder = builder.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 
    # Performance tuning
    builder = builder.config("spark.sql.shuffle.partitions", "200")  # Adjust based on your data size
    builder = builder.config("spark.sql.adaptive.enabled", "true")  # self-adaptive execution
    builder = builder.config("spark.sql.adaptive.coalescePartitions.enabled", "true")  # coalesce partitions
    builder = builder.config("spark.sql.adaptive.skewJoin.enabled", "true")  # skew join optimization
    return configure_spark_with_delta_pip(builder).getOrCreate()




def main():
    spark = create_spark_session()
    print("Starting ETL Job...")
    run_etl_pipeline(spark)  # Assuming this function runs your ETL logic
    spark.stop()
    print("ETL Job Completed.")

if __name__ == "__main__":
    main()
