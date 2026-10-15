
resource "aws_glue_crawler" "raw" {
  name          = "banking-raw-crawler"
  database_name = aws_glue_catalog_database.banking.name
  role          = "service-role/AWSGlueServiceRole-BankingCrawler"
  description   = "Crawls raw banking CSV files from Amazon S3 and populates the AWS Glue Data Catalog."

  s3_target {
    path = "s3://banking-data-lakehouse/raw/"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }

  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}

resource "aws_glue_crawler" "gold" {
  name          = "banking-gold-crawler"
  database_name = aws_glue_catalog_database.banking.name
  role          = "service-role/AWSGlueServiceRole-BankingCrawler"
  table_prefix  = "gold_"

  s3_target {
    path = "s3://banking-data-lakehouse/gold/daily_transaction_summary/"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }

  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}

import {
  to = aws_glue_crawler.raw
  id = "banking-raw-crawler"
}

import {
  to = aws_glue_crawler.gold
  id = "banking-gold-crawler"
}
