
resource "aws_glue_trigger" "raw_crawler" {
  name          = "banking-raw-crawler"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.banking_pipeline.name
  enabled       = true

  actions {
    job_name = aws_glue_job.transactions_etl.name
  }

  predicate {
    logical = "ANY"

    conditions {
      crawler_name = "banking-raw-crawler"
      crawl_state  = "SUCCEEDED"
    }
  }
}

resource "aws_glue_trigger" "transactions_gold" {
  name          = "banking-transactions-gold"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.banking_pipeline.name
  enabled       = true

  actions {
    job_name = aws_glue_job.transactions_gold.name
  }

  predicate {
    logical = "ANY"

    conditions {
      job_name = aws_glue_job.transactions_etl.name
      state    = "SUCCEEDED"
    }
  }
}

resource "aws_glue_trigger" "gold_crawler" {
  name          = "banking-gold-crawler"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.banking_pipeline.name
  enabled       = true

  actions {
    crawler_name = "banking-gold-crawler"
  }

  predicate {
    logical = "ANY"

    conditions {
      job_name = aws_glue_job.transactions_gold.name
      state    = "SUCCEEDED"
    }
  }
}

import {
  to = aws_glue_trigger.raw_crawler
  id = "banking-raw-crawler"
}

import {
  to = aws_glue_trigger.transactions_gold
  id = "banking-transactions-gold"
}

import {
  to = aws_glue_trigger.gold_crawler
  id = "banking-gold-crawler"
}
