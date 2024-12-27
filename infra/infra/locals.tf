locals {
  cognito_domain = var.branch == "main" ? var.project : "${var.project}-${var.branch}"
}
