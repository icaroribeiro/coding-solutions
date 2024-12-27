resource "aws_cognito_user_pool" "prj_user_pool" {
  name = "prj-user-pool-${var.branch}"
}

resource "aws_cognito_user_pool_domain" "prj_user_pool_domain" {
  domain       = local.cognito_domain
  user_pool_id = aws_cognito_user_pool.prj_user_pool.id
}

resource "aws_cognito_resource_server" "prj_resource_server" {
  name         = "prj-resource-server-${var.branch}"
  identifier   = "https://${local.cognito_domain}.com"
  user_pool_id = aws_cognito_user_pool.prj_user_pool.id

  scope {
    scope_name        = "users"
    scope_description = "Allow access to users API Gateway endpoint"
  }
}

resource "aws_cognito_user_pool_client" "x_user_pool_client" {
  name                                 = "x-user-pool-client-${var.branch}"
  user_pool_id                         = aws_cognito_user_pool.prj_user_pool.id
  generate_secret                      = true
  allowed_oauth_flows                  = ["client_credentials"]
  supported_identity_providers         = ["COGNITO"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["${aws_cognito_resource_server.prj_resource_server.identifier}/users"]
  depends_on                           = [aws_cognito_user_pool.prj_user_pool, aws_cognito_resource_server.prj_resource_server]
  # ISSUE
  # https://github.com/hashicorp/terraform-provider-aws/issues/32504
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "minutes"
  }
  refresh_token_validity = 120
  id_token_validity      = 60
  access_token_validity  = 60
}
