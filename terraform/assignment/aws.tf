provider "aws" {
  region = var.region_name
  profile = var.aws_profile
}
data "aws_caller_identity" "current" {}


terraform {
  backend "s3" {
    bucket         = "nmd-training-tf-states-706146613458"
    key            = "assignment/samantha-eidson-nmd-data-engineering.tfstate"
    region         = "us-west-2"
    dynamodb_table = "nmd-training-tf-state-lock-table"    
    encrypt        = true                   # Encrypts the state file at rest
  }
}
