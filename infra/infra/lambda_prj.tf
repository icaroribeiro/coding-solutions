data "archive_file" "lambda_prj_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../lambdas/lambda_prj/dist"
  output_path = local.lambda_prj_output_path
}

resource "aws_lambda_function" "lambda_prj" {
  function_name    = "lambda-prj-${local.pipeline_id}"
  source_code_hash = data.archive_file.lambda_prj_zip.output_base64sha256
  handler          = "index.lambda_handler"
  runtime          = "python3.12"

  environment {
    variables = {
      REGION = var.region
    }
  }

  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "INFO"
  }
}
