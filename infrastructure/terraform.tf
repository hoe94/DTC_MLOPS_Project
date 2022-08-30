#State bucket for Terraform
terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "4.28.0"
        }

    }
    required_version = ">= 1.0"
    backend "s3" {
      bucket  = "mlops-project-terraform-statebucket"
      key     = "mlops-zoomcamp.tfstate"
      region  = "us-east-2"
      encrypt = true
    }
}

provider "aws" {
    region = var.aws_region
}