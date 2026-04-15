# -------------------
# S3 BUCKET
# -------------------
resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  tags = {
    Name = "SRE Challenge Bucket"
  }
}

# Enable public access block OFF (for simple demo use)
resource "aws_s3_bucket_public_access_block" "bucket_access" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# -------------------
# DYNAMODB TABLE
# -------------------
resource "aws_dynamodb_table" "users" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name = "SRE Users Table"
  }
}
