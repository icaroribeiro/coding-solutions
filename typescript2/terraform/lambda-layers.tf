data "archive_file" "deps_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../dist/layers/deps-layer/"
  output_path = "${path.module}/../dist/deps.zip"
}

data "archive_file" "utils_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../dist/layers/utils-layer/"
  output_path = "${path.module}/../dist/utils.zip"
}

resource "aws_lambda_layer_version" "lambda_deps_layer" {
  layer_name          = "shared_deps"
  filename            = data.archive_file.deps_layer_zip.output_path
  source_code_hash    = data.archive_file.deps_layer_zip.output_base64sha256
  compatible_runtimes = ["nodejs20.x"]
}

resource "aws_lambda_layer_version" "lambda_utils_layer" {
  layer_name          = "shared_utils"
  filename            = data.archive_file.utils_layer_zip.output_path
  source_code_hash    = data.archive_file.utils_layer_zip.output_base64sha256
  compatible_runtimes = ["nodejs20.x"]
}
