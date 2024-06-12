locals {
    bucket_name = "illo-laz-iceberg-data"
}

resource "aws_s3_bucket" "data_bucket" {
    bucket = local.bucket_name
}

resource "aws_glue_catalog_database" "glue_database" {
    name = "iceberg_catalog"
    description = "Contains all tables manged my iceberg"
}

resource "aws_athena_workgroup" "athena_workgroup" {
    name = "athena_workgroup"
    state = "ENABLED"

    configuration {
        result_configuration {
        output_location = "s3://${aws_s3_bucket.data_bucket.id}/athena_results"
        }
    }

    depends_on = [aws_glue_catalog_database.glue_database, aws_s3_bucket.data_bucket]
}

output "data_bucket" {
    value = aws_s3_bucket.data_bucket.id
}

resource "local_file" "output_variables" {
    filename = "${path.module}/../terraform.env"
    content  = <<-EOF
        DATA_BUCKET=${aws_s3_bucket.data_bucket.id}
    EOF
}
