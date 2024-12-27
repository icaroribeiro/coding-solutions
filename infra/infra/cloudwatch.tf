resource "aws_cloudwatch_log_group" "prj_api_access_logs" {
  name = "API-Gateway-Access-Logs_${aws_api_gateway_rest_api.prj_api.id}/${var.stage_name}-${var.branch}"
}
