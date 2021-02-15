resource "aws_cloudwatch_event_rule" "covid-etl" {
  name                = "covid_etl"
  description         = "At midnight everyday"
  schedule_expression = "cron(0 0 * * ? *)"
  is_enabled          = true
}

resource "aws_cloudwatch_event_target" "covid-etl" {
  arn       = aws_lambda_function.covid-etl.arn
  target_id = "covid-etl-lambda"
  rule      = aws_cloudwatch_event_rule.covid-etl.name
}
