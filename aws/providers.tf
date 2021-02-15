terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.25.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "2.0.0"
    }
  }

  backend "s3" {
    bucket         = "mybytesni-terraform-state"
    key            = "etlpipeline"
    region         = "us-east-1"
    dynamodb_table = "mybytesni-terraform-state"
    encrypt        = true
  }
}

provider "aws" {
  region  = "us-east-1"
}

provider "archive" {}
