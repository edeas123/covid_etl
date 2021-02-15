locals {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {
}

data "aws_iam_policy_document" "covid-etl-lambda-execution-role" {
  statement {
    sid = "CreateLogGroup"
    actions = [
      "logs:CreateLogGroup"
    ]
    resources = [
      "arn:aws:logs:${local.region}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {
    sid = "WriteLogs"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${local.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.covid_etl_function_name}:*"
    ]
  }

  statement {
    sid = "DynamodbPermissions"
    actions = [
      "dynamodb:*"
    ]
    resources = [
      "arn:aws:dynamodb:${local.region}:${data.aws_caller_identity.current.account_id}:table/${local.table_counter}",
      "arn:aws:dynamodb:${local.region}:${data.aws_caller_identity.current.account_id}:table/${local.table_data}"
    ]
  }
}

resource "aws_iam_role" "covid-etl-lambda-execution-role" {
  name               = "covid-etl-lambda-execution-role"
  path               = "/service-role/"
  assume_role_policy = file("templates/lambda-assume-role.json")
}

resource "aws_iam_role_policy" "covid-etl-lambda-execution-role" {
  role   = aws_iam_role.covid-etl-lambda-execution-role.id
  name   = "covid-etl-AWSLambdaBasicExecutionRole"
  policy = data.aws_iam_policy_document.covid-etl-lambda-execution-role.json
}
