
resource "aws_glue_job" "transactions_etl" {
  name     = "banking-transactions-etl"
  role_arn = "arn:aws:iam::762250434485:role/AWSGlueServiceRole-BankingETL"

  command {
    name            = "glueetl"
    script_location = "s3://aws-glue-assets-762250434485-ap-southeast-2/scripts/banking-transactions-etl.py"
    python_version  = "3"
  }

  execution_property {
    max_concurrent_runs = 1
  }

  glue_version      = "5.1"
  execution_class   = "STANDARD"
  worker_type       = "G.1X"
  number_of_workers = 2
  timeout           = 30
  max_retries       = 0

  default_arguments = {
    "--enable-metrics"                   = ""
    "--enable-spark-ui"                  = "true"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-762250434485-ap-southeast-2/sparkHistoryLogs/"
    "--enable-job-insights"              = "true"
    "--enable-observability-metrics"     = "true"
    "--conf"                             = "spark.eventLog.rolling.enabled=true --conf spark.sql.catalog.glue_catalog.glue.skip-name-validation=true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--TempDir"                          = "s3://aws-glue-assets-762250434485-ap-southeast-2/temporary/"
  }
}

resource "aws_glue_job" "transactions_gold" {
  name     = "banking-transactions-gold"
  role_arn = "arn:aws:iam::762250434485:role/AWSGlueServiceRole-BankingETL"

  command {
    name            = "glueetl"
    script_location = "s3://aws-glue-assets-762250434485-ap-southeast-2/scripts/banking-transactions-gold.py"
    python_version  = "3"
  }

  execution_property {
    max_concurrent_runs = 1
  }

  glue_version      = "5.1"
  execution_class   = "STANDARD"
  worker_type       = "G.1X"
  number_of_workers = 2
  timeout           = 30
  max_retries       = 0

  default_arguments = {
    "--enable-metrics"                   = ""
    "--enable-spark-ui"                  = "true"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-762250434485-ap-southeast-2/sparkHistoryLogs/"
    "--enable-job-insights"              = "true"
    "--enable-observability-metrics"     = "true"
    "--conf"                             = "spark.eventLog.rolling.enabled=true --conf spark.sql.catalog.glue_catalog.glue.skip-name-validation=true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--TempDir"                          = "s3://aws-glue-assets-762250434485-ap-southeast-2/temporary/"
  }
}

import {
  to = aws_glue_job.transactions_etl
  id = "banking-transactions-etl"
}

import {
  to = aws_glue_job.transactions_gold
  id = "banking-transactions-gold"
}
