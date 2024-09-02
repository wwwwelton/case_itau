provider "aws" {
  region = "sa-east-1"
}

resource "aws_lambda_function" "books_lambda" {
  function_name = "BooksLambdaFunction"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "run.lambda_handler"
  runtime       = "python3.10"
  timeout       = 300

  filename = "${path.module}/../function.zip"

  source_code_hash = filebase64sha256("${path.module}/../function.zip")

  environment {
    variables = {
      PYTHONPATH     = "/var/task/dependencies"
      GOOGLE_API     = var.GOOGLE_API
      OPENAI_API_KEY = var.OPENAI_API_KEY
      STAGE_NAME     = var.STAGE_NAME
    }
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  inline_policy {
    name = "lambda-logs-policy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_api_gateway_rest_api" "books_lambda" {
  name        = "booksApi"
  description = "API Gateway for Books Lambda Function"
}

resource "aws_api_gateway_resource" "apidocs_resource" {
  rest_api_id = aws_api_gateway_rest_api.books_lambda.id
  parent_id   = aws_api_gateway_rest_api.books_lambda.root_resource_id
  path_part   = "apidocs"
}

resource "aws_api_gateway_resource" "apispec_json_resource" {
  rest_api_id = aws_api_gateway_rest_api.books_lambda.id
  parent_id   = aws_api_gateway_rest_api.books_lambda.root_resource_id
  path_part   = "apispec"
}

resource "aws_api_gateway_resource" "apispec_1_json_resource" {
  rest_api_id = aws_api_gateway_rest_api.books_lambda.id
  parent_id   = aws_api_gateway_resource.apispec_json_resource.id
  path_part   = "apispec_1.json"
}

resource "aws_api_gateway_method" "get_method_root" {
  rest_api_id   = aws_api_gateway_rest_api.books_lambda.id
  resource_id   = aws_api_gateway_rest_api.books_lambda.root_resource_id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_method_apidocs" {
  rest_api_id   = aws_api_gateway_rest_api.books_lambda.id
  resource_id   = aws_api_gateway_resource.apidocs_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_method_apispec_json" {
  rest_api_id   = aws_api_gateway_rest_api.books_lambda.id
  resource_id   = aws_api_gateway_resource.apispec_1_json_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration_root" {
  rest_api_id             = aws_api_gateway_rest_api.books_lambda.id
  resource_id             = aws_api_gateway_rest_api.books_lambda.root_resource_id
  http_method             = aws_api_gateway_method.get_method_root.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.books_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "lambda_integration_apidocs" {
  rest_api_id             = aws_api_gateway_rest_api.books_lambda.id
  resource_id             = aws_api_gateway_resource.apidocs_resource.id
  http_method             = aws_api_gateway_method.get_method_apidocs.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.books_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "lambda_integration_apispec_json" {
  rest_api_id             = aws_api_gateway_rest_api.books_lambda.id
  resource_id             = aws_api_gateway_resource.apispec_1_json_resource.id
  http_method             = aws_api_gateway_method.get_method_apispec_json.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.books_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.books_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.books_lambda.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "books_lambda_deployment" {
  depends_on  = [aws_api_gateway_integration.lambda_integration_root, aws_api_gateway_integration.lambda_integration_apidocs, aws_api_gateway_integration.lambda_integration_apispec_json]
  rest_api_id = aws_api_gateway_rest_api.books_lambda.id
  stage_name  = var.STAGE_NAME
}

output "api_gateway_url" {
  value       = aws_api_gateway_deployment.books_lambda_deployment.invoke_url
  description = "The URL of the Books API"
}
