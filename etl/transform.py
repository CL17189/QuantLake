# etl/transform.py
from delta_writer import write_to_delta
from pyspark.sql.functions import col, from_unixtime, when, round

def run_etl_pipeline(spark):
    df_raw = spark.read.json("data/raw/*.json")

    df_flat = df_raw.select(
        col("symbol"),
        col("timestamp"),
        from_unixtime(col("quote.t")).alias("market_time"),
        col("quote.c").alias("current_price"),
        col("quote.pc").alias("previous_close"),
        col("quote.o").alias("open_price"),
        col("quote.h").alias("high"),
        col("quote.l").alias("low"),
        col("profile.name").alias("company_name"),
        col("profile.exchange").alias("exchange"),
        col("profile.marketCapitalization").alias("market_cap")
    )

    df_clean = df_flat.filter(
        (col("current_price").isNotNull()) &
        (col("previous_close") > 0) &
        (col("current_price") > 0)
    )

    df_enriched = df_clean.withColumn(
        "price_change_pct",
        round((col("current_price") - col("previous_close")) / col("previous_close") * 100, 2)
    )

    df_enriched.createOrReplaceTempView("stocks")

    top_10 = spark.sql("""
        SELECT symbol, company_name, current_price, price_change_pct, market_cap
        FROM stocks
        ORDER BY market_cap DESC
        LIMIT 10
    """)
    print("📈 Top 10 stock：")
    top_10.show(truncate=False)

    df_enriched.write.mode("overwrite").parquet("data/processed/stocks_cleaned.parquet")
    write_to_delta(df_enriched)
