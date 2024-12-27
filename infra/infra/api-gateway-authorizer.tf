resource "aws_api_gateway_authorizer" "prj_authorizer" {
  name          = "prj-authorizer-${var.branch}"
  type          = "COGNITO_USER_POOLS"
  rest_api_id   = aws_api_gateway_rest_api.prj_api.id
  provider_arns = [aws_cognito_user_pool.prj_user_pool.arn]
}
