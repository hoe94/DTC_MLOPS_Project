#1. Create the state bucket 

terraform {
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

# 2. s3 bucket: MLFlow model artifact 
resource "aws_s3_bucket" "mlflow_model_artifact" {
    bucket = var.mlflow_artifact_bucket_name
    acl    = "private"
    tags   = {
        Name = "mlflow-model-artifact"
    }
}

# 3. VPC for MLFlow Server
 resource "aws_vpc" "mlflow-vpc" {
   cidr_block = "10.0.0.0/16"
   tags = {
     Name = "mlflow-vpc"
   }
 }

# 3.1 Internet Gateway for MLFlow Server
 resource "aws_internet_gateway" "mlflow-gw" {
   vpc_id = aws_vpc.mlflow-vpc.id
 }

# 3.2 Subnet for MLFlow Server

resource "aws_subnet" "mlflow-subnet" {
  vpc_id            = aws_vpc.mlflow-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone =  "us-east-2a"
  tags = {
    Name = "mlflow-subnet"
  }
}

# 3.3 Security Group to allow port 22,80,443 for MLFlow Server
resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "Allow Web inbound traffic"
  vpc_id      = aws_vpc.mlflow-vpc.id

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mlflow-sg"
  }
}

# 3.4 Network interface with an ip in the subnet that was created in step 3.3

resource "aws_network_interface" "mlflow-web-server" {
  subnet_id       = aws_subnet.mlflow-subnet.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow_web.id]
}

# 3.5 elastic IP to the network interface created in step 3.4 for MLFlow Server

resource "aws_eip" "one" {
  vpc                       = true
  network_interface         = aws_network_interface.mlflow-web-server.id
  associate_with_private_ip = "10.0.1.50"
  depends_on                = [aws_internet_gateway.mlflow-gw]
}

# 3.6 ec2: MLFlow Server
resource "aws_instance" "mlflow_server"{
    ami = "ami-02f3416038bdb17fb"
    instance_type = "t2.micro"
    availability_zone = "us-east-2a"
    tags = {
        Name = "mlflow server"
    }
    network_interface {
        device_index         = 0
        network_interface_id = aws_network_interface.mlflow-web-server.id
    }
    user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install mlflow boto3 psycopg2 binary
                EOF
}

# 4. s3 bucket: DVC
resource "aws_s3_bucket" "dvc_remote_storage" {
    bucket = var.mlflow_artifact_bucket_name
    acl    = "private"
    tags   = {
        Name = "mlflow-model-artifact"
    }
}