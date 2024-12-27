resource "aws_api_gateway_rest_api" "prj_api" {
  name = "prj-api-${var.branch}"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_account" "prj_api_account" {
  depends_on          = [aws_iam_role_policy_attachment.prj_api_logging_attachment]
  cloudwatch_role_arn = aws_iam_role.prj_api_logging_role.arn
}

resource "aws_api_gateway_deployment" "prj_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.prj_api.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsondecode([
      aws_api_gateway_resource.users_resource,
      aws_api_gateway_method.users_method,
      aws_api_gateway_integration.users_integration,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_client_certificate" "prj_api_client_certificate" {
  description = "prj-client-certificate"
}

resource "aws_api_gateway_resource" "users_resource" {
  rest_api_id = aws_api_gateway_rest_api.prj_api.id
  parent_id   = aws_api_gateway_rest_api.prj_api.root_resource_id
  path_part   = "users"
}


resource "aws_api_gateway_method" "users_method" {
  resource_id   = aws_api_gateway_resource.users_resource.id
  rest_api_id   = aws_api_gateway_rest_api.prj_api.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.prj_authorizer.id
  authorization_scopes = [
    "${aws_cognito_resource_server.prj_resource_server.identifier}/users"
  ]
}

resource "aws_api_gateway_integration" "users_integration" {
  rest_api_id             = aws_api_gateway_rest_api.prj_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_method.http_method
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_prj.invoke_arn
}

resource "aws_api_gateway_stage" "prj_stage" {
  rest_api_id           = aws_api_gateway_rest_api.prj_api.id
  deployment_id         = aws_api_gateway_deployment.prj_api_deployment.id
  stage_name            = var.stage_name
  client_certificate_id = aws_api_gateway_client_certificate.prj_api_client_certificate.id
  xray_tracing_enabled  = true
  depends_on            = [aws_cloudwatch_log_group.prj_api_access_logs]

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.prj_api_access_logs.arn
    format = jsonencode({
      "requestId" : "$context.requestId"
      "extendedRequestId" : "$context.extendedRequestId"
      "ip" : "$context.identity.sourceIp"
      "caller" : "$context.identity.caller"
      "user" : "$context.identity.user"
      "requestTime" : "$context.requestTime"
      "httpMethod" : "$context.httpMethod"
      "resourcePath" : "$context.resourcePath"
      "status" : "$context.status"
      "protocol" : "$context.protocol"
      "responseLength" : "$context.responseLength"
    })
  }
}

resource "aws_api_gateway_method_settings" "prj_method_settings" {
  rest_api_id = aws_api_gateway_rest_api.prj_api.id
  stage_name  = aws_api_gateway_stage.prj_stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}
