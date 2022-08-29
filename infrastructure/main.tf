#1. Create the state bucket 

terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket  = "stg-mlops-project-tf-statebucket"
    key     = "mlops-zoomcamp-stg.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}

provider "aws" {
    region = "us-east-2"
}

# 2. s3 bucket
resource "aws_s3_bucket" "mlflow_model_artifact" {
    bucket = "stg-mlops-project-bucket"
    acl    = "private"
    tags   = {
        Name = "mlflow_model_artifact"
    }
}

# 3. Mlflow Server
resource "aws_instance" "mlflow_server"{
    ami = "ami-02f3416038bdb17fb"
    instance_type = "t2.micro"
    tags = {
        Name = mlflow server"
    }
}