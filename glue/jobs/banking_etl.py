import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.window import Window


args = getResolvedOptions(sys.argv, ["JOB_NAME"])

SOURCE_DATABASE = "banking_lakehouse"
SOURCE_TABLE = "transactions_csv"

SILVER_PATH = "s3://banking-data-lakehouse/silver/transactions/"
QUARANTINE_PATH = "s3://banking-data-lakehouse/quarantine/transactions/"

REQUIRED_IDS = [
    "transaction_id",
    "account_id",
    "customer_id",
    "merchant_id",
]

ALLOWED_STATUSES = ["SUCCESS", "FAILED", "PENDING"]
ALLOWED_CHANNELS = ["UPI", "CARD", "NET_BANKING", "ATM", "MOBILE_APP"]

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

source = glue_context.create_dynamic_frame.from_catalog(
    database=SOURCE_DATABASE,
    table_name=SOURCE_TABLE,
    transformation_ctx="source_transactions",
)

df = source.toDF()

# Trim string fields before validating them.
for column_name, data_type in df.dtypes:
    if data_type == "string":
        df = df.withColumn(column_name, F.trim(F.col(column_name)))

# Normalize the fields used by the rules.
df = (
    df.withColumn("amount", F.col("amount").cast("double"))
    .withColumn("currency", F.upper(F.col("currency")))
    .withColumn("transaction_status", F.upper(F.col("transaction_status")))
    .withColumn("payment_channel", F.upper(F.col("payment_channel")))
)

validation_errors = []

for column_name in REQUIRED_IDS:
    validation_errors.append(
        F.when(
            F.col(column_name).isNull() | (F.col(column_name) == ""),
            F.lit(f"missing_{column_name}"),
            )
    )

validation_errors.extend(
    [
        F.when(
            F.col("amount").isNull() | (F.col("amount") <= 0),
            F.lit("amount_must_be_greater_than_zero"),
            ),
        F.when(
            F.col("currency").isNull() | (F.col("currency") != "INR"),
            F.lit("currency_must_be_INR"),
            ),
        F.when(
            F.col("transaction_status").isNull()
            | (~F.col("transaction_status").isin(ALLOWED_STATUSES)),
            F.lit("invalid_transaction_status"),
            ),
        F.when(
            F.col("payment_channel").isNull()
            | (~F.col("payment_channel").isin(ALLOWED_CHANNELS)),
            F.lit("invalid_payment_channel"),
            ),
    ]
)

df = df.withColumn(
    "quarantine_reason",
    F.concat_ws("|", *validation_errors),
)

invalid = df.filter(F.col("quarantine_reason") != "")
valid = df.filter(F.col("quarantine_reason") == "").drop("quarantine_reason")

# Keep one deterministic row per transaction_id. Quarantine additional
# valid rows that share the same transaction_id.
tie_break_columns = sorted(
    column_name
    for column_name in valid.columns
    if column_name != "transaction_id"
)

duplicate_order = Window.partitionBy("transaction_id").orderBy(
    *[
        F.col(column_name).asc_nulls_first()
        for column_name in tie_break_columns
    ]
)

ranked = valid.withColumn(
    "_duplicate_rank",
    F.row_number().over(duplicate_order),
)

silver = (
    ranked.filter(F.col("_duplicate_rank") == 1)
    .drop("_duplicate_rank")
)

duplicate_quarantine = (
    ranked.filter(F.col("_duplicate_rank") > 1)
    .drop("_duplicate_rank")
    .withColumn("quarantine_reason", F.lit("duplicate_transaction_id"))
)

quarantine = invalid.unionByName(duplicate_quarantine)

raw_count = df.count()
silver_count = silver.count()
quarantine_count = quarantine.count()

print(
    f"ETL counts: raw={raw_count}, "
    f"silver={silver_count}, quarantine={quarantine_count}"
)

silver.write.mode("overwrite").parquet(SILVER_PATH)
quarantine.write.mode("overwrite").parquet(QUARANTINE_PATH)

job.commit()