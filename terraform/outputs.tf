output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.users.name
}

output "iam_role_arn" {
  value = aws_iam_role.eks_role.arn
}
