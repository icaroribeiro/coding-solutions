data "archive_file" "hello_world_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../dist/handlers/hello-world-lambda/"
  output_path = "${path.module}/../dist/hello-world-lambda.zip"
}

resource "aws_lambda_function" "hello_world_lambda" {
  function_name    = "hello-world-lambda"
  runtime          = "nodejs20.x"
  handler          = "index.handler"
  role             = aws_iam_role.lambda_role.arn
  filename         = data.archive_file.hello_world_lambda_zip.output_path
  source_code_hash = data.archive_file.hello_world_lambda_zip.output_base64sha256
  timeout          = var.lambda_function_timeout
  layers = [
    aws_lambda_layer_version.lambda_deps_layer.arn,
    aws_lambda_layer_version.lambda_utils_layer.arn
  ]
}
