resource "aws_iam_role" "prj_api_logging_role" {
  name = "${var.iam_role_prefix}-prj-api-logging-role-${var.branch}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = {
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "apigateway.amazonaws.com"
      }
    }
  })
}


resource "aws_iam_role_policy_attachment" "prj_api_logging_attachment" {
  policy_arn = "arn:aws:iam:aws:policy/service-role/AmazonAPIGatewayPushToClouldWatchLogs"
  role       = aws_iam_role.prj_api_logging_role.name
}
