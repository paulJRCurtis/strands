terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "security-analysis-vpc"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "security-analysis-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# S3 Bucket for architecture files
resource "aws_s3_bucket" "architecture_files" {
  bucket = "security-analysis-architectures-${random_id.bucket_suffix.hex}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

# DynamoDB table for job tracking
resource "aws_dynamodb_table" "jobs" {
  name           = "security-analysis-jobs"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "job_id"

  attribute {
    name = "job_id"
    type = "S"
  }

  tags = {
    Name = "SecurityAnalysisJobs"
  }
}