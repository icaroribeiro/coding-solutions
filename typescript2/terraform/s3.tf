resource "aws_s3_bucket" "example" {
  count  = var.branch == "prod" || var.branch == "dev" ? 1 : "0"
  bucket = "tfstate-bucket-${var.branch}"
}
