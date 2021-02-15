locals {
  covid_etl_function_name =  "covid_etl"
  pandas_layer_arn = "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-pandas:27"
}

resource "aws_lambda_function" "covid-etl" {
  function_name = local.covid_etl_function_name
  description   = "Extract, Transform and Load reported Covid19 data into Dynamodb"
  handler       = "handlers.run"
  layers = [
    local.pandas_layer_arn
  ]
  role             = aws_iam_role.covid-etl-lambda-execution-role.arn
  runtime          = "python3.8"
  filename         = data.archive_file.source.output_path
  source_code_hash = data.archive_file.source.output_base64sha256
  memory_size = 256
  timeout = 60
}

resource "aws_lambda_permission" "covid-etl" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.covid-etl.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.covid-etl.arn
}
