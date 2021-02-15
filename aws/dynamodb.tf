locals {
  table_counter = "CovidETLCounter"
  table_data = "CovidData"
}

resource "aws_dynamodb_table" "covid-etl-counter" {
  hash_key = "ID"
  name     = local.table_counter

  attribute {
    name = "ID"
    type = "N"
  }

  write_capacity = 1
  read_capacity  = 1
}

resource "aws_dynamodb_table" "covid-data" {
  hash_key = "Date"
  name     = local.table_data

  attribute {
    name = "Date"
    type = "S"
  }

  write_capacity = 10
  read_capacity  = 1
}
