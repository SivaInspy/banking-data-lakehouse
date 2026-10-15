
resource "aws_glue_workflow" "banking_pipeline" {
  name                = "banking-lakehouse-pipeline"
  max_concurrent_runs = 1
}

import {
  to = aws_glue_workflow.banking_pipeline
  id = "banking-lakehouse-pipeline"
}
