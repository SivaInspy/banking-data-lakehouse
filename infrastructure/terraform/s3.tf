resource "aws_s3_bucket" "lakehouse" {
  bucket = "banking-data-lakehouse"
}

import {
  to = aws_s3_bucket.lakehouse
  id = "banking-data-lakehouse"
}