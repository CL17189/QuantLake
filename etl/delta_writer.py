# etl/delta_writer.py

import os
from pyspark.sql import DataFrame

def write_to_delta(df: DataFrame, output_path="data/lake/stocks_delta"):
    """
    write DataFrame to local Delta Lake format, partitioned by symbol and date.
    """
    print(f"📝 Writing to Delta Lake: {output_path}")
    df.write.format("delta") \
        .mode("overwrite") \
        .partitionBy("symbol") \
        .save(output_path)
    print("✅ Delta write completed.")


def write_to_delta_S3(df: DataFrame):
    
    bucket = "datalake"
    path = f"s3a://{bucket}/stocks_delta"

    spark = df.sparkSession

    # set S3 access keys and endpoint
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"])
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"])
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.environ["MINIO_ENDPOINT"])
    spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    print(f"📝 Writing to MinIO Delta Lake at {path}")
    df.write.format("delta") \
        .mode("overwrite") \
        .partitionBy("symbol") \
        .save(path)

    print("✅ Delta write to MinIO completed.")