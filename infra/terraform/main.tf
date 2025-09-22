terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "project" {
  type    = string
  default = "mini-telecom-etl"
}

resource "aws_s3_bucket" "landing" {
  bucket = "${var.project}-landing"
}

output "landing_bucket" {
  value = aws_s3_bucket.landing.bucket
}
