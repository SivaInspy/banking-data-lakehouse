import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


args = getResolvedOptions(sys.argv, ["JOB_NAME"])

SILVER_PATH = "s3://banking-data-lakehouse/silver/transactions/"
GOLD_PATH = "s3://banking-data-lakehouse/gold/daily_transaction_summary/"

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

silver = spark.read.parquet(SILVER_PATH)

# Convert values such as "2026-07-27 09:20:40" to the calendar date.
silver = silver.withColumn(
    "transaction_date",
    F.to_date(F.col("transaction_date"), "yyyy-MM-dd HH:mm:ss"),
).withColumn(
    "amount",
    F.col("amount").cast("decimal(18,2)"),
)

unparsed_date_count = silver.filter(
    F.col("transaction_date").isNull()
).count()

if unparsed_date_count > 0:
    raise ValueError(
        f"Found {unparsed_date_count} Silver rows with an invalid transaction_date"
    )

gold = (
    silver
    .groupBy(
        "transaction_date",
        "payment_channel",
        "transaction_status",
    )
    .agg(
        F.countDistinct("transaction_id").alias("transaction_count"),
        F.sum("amount").alias("transaction_amount_inr"),
        F.sum(
            F.when(
                F.col("transaction_status") == "SUCCESS",
                F.col("amount"),
                ).otherwise(F.lit(0).cast("decimal(18,2)"))
        ).alias("successful_amount_inr"),
    )
    .withColumn("currency", F.lit("INR"))
    .select(
        "transaction_date",
        "payment_channel",
        "transaction_status",
        "currency",
        "transaction_count",
        "transaction_amount_inr",
        "successful_amount_inr",
    )
)

silver_count = silver.count()
gold_count = gold.count()

print(
    f"Gold ETL counts: silver_input={silver_count}, "
    f"daily_summary_rows={gold_count}, "
    f"unparsed_dates={unparsed_date_count}"
)

# Overwrite replaces the previous Gold output when this job is rerun.
gold.write.mode("overwrite").parquet(GOLD_PATH)

job.commit()