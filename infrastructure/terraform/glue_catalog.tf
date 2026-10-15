resource "aws_glue_catalog_database" "banking" {
  name        = "banking_lakehouse"
  description = "AWS Glue Data Catalog database for the Cloud Banking Data Lakehouse."
}

import {
  to = aws_glue_catalog_database.banking
  id = "762250434485:banking_lakehouse"
}
