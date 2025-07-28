# etl/spark_job.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_unixtime, to_date, arrays_zip, explode, 
    lag, avg, stddev, abs as _abs, when, sum as _sum, round
)
from pyspark.sql.window import Window
from delta import configure_spark_with_delta_pip
from delta_writer import write_table



def run_etl_pipeline(spark: SparkSession):
    # 1. read raw data
    df_raw = spark.read.option("multiline", "true").json("../data/raw/*.json").cache()

    # 2. construct K-line table by exploding historical candle data and caching it
    df_candle = (
        df_raw
        .select(
            col("symbol"),
            explode(
                arrays_zip(
                    col("candles.t"), col("candles.c"), col("candles.h"),
                    col("candles.l"), col("candles.o"), col("candles.v")
                )
            ).alias("c")
        )
        .select(
            col("symbol"),
            to_date(from_unixtime(col("c.t"))).alias("trade_date"),
            col("c.c").alias("close"),
            col("c.h").alias("high"),
            col("c.l").alias("low"),
            col("c.o").alias("open"),
            col("c.v").alias("volume"),
            col("quote.pc").alias("prev_close")
        )
        .cache()
    )

    # window specifications for various calculations
    win7 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-6, 0)
    win5 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-4, 0)
    win20 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-19, 0)
    win30 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-29, 0)

    # 3. calculate various factors and write to Delta Lake
    def write_table(df, name, part_cols, zorder_cols=None):
        path = f"data/lake/{name}"
        df.repartition(*part_cols)
        df.write.format("delta").mode("overwrite").partitionBy(*part_cols).save(path)
        # combine small files and do re-partitioning
        if zorder_cols:
            spark.sql(f"OPTIMIZE delta.`{path}` ZORDER BY ({', '.join(zorder_cols)})")
        else:
            spark.sql(f"OPTIMIZE delta.`{path}`")

    # PriceFactors
    df_price = (
        df_candle
        .withColumn("price_change_pct", round((col("close") - col("prev_close")) / col("prev_close") * 100, 2))
        .withColumn("ma_5", round(avg("close").over(win5), 2))
        .withColumn("ma_20", round(avg("close").over(win20), 2))
        .select("symbol", "trade_date", "close", "prev_close", "price_change_pct", "ma_5", "ma_20")
    )
    write_table(df_price, "PriceFactors", ["symbol", "trade_date"], ["symbol"])

    # VolumeFactors
    df_volume = (
        df_candle
        .withColumn("avg_volume_7d", round(avg("volume").over(win7), 2))
        .withColumn("volume_spike_ratio", round(col("volume") / col("avg_volume_7d"), 2))
        .select("symbol", "trade_date", "volume", "avg_volume_7d", "volume_spike_ratio")
    )
    write_table(df_volume, "VolumeFactors", ["symbol", "trade_date"], ["symbol"])

    # ImpactFactors
    df_impact = (
        df_candle
        .withColumn("price_impact_factor", round((col("high") - col("low")) / (col("volume") + 1), 6))
        .withColumn("abs_return", _abs((col("close") - col("prev_close")) / col("prev_close")))
        .withColumn("jump_risk_flag", when(col("abs_return") > 0.05, 1).otherwise(0))
        .withColumn("jump_risk_index", _sum("jump_risk_flag").over(win7))
        .withColumn(
            "abnormal_volume_index",
            round(
                (col("volume") - avg("volume").over(win30)) /
                (stddev("volume").over(win30) + 1), 4
            )
        )
        .select("symbol", "trade_date", "high", "low", "price_impact_factor", "jump_risk_index", "abnormal_volume_index")
    )
    write_table(df_impact, "ImpactFactors", ["symbol", "trade_date"], ["symbol"])

    # Fundamentals
    df_fund = (
        df_raw
        .select(
            col("symbol"),
            to_date(col("timestamp")).alias("report_date"),
            col("metrics.metric.peTTM").alias("pe_ratio"),
            col("metrics.metric.epsAnnual").alias("eps"),
            col("metrics.metric.revenuePerShareTTM").alias("revenue_per_share"),
            col("profile.marketCapitalization").alias("market_cap")
        )
    )
    write_table(df_fund, "Fundamentals", ["symbol", "report_date"], ["symbol"])

    # Clear cache
    spark.catalog.clearCache()
    spark.stop()

if __name__ == "__main__":
    spark = create_spark_session()
    run_etl_pipeline(spark)


