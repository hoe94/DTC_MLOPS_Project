#Network Configuration (VPC, Internet Gateway, Subnet, Route Table) for MLFlow Server

# 1. Create vpc
resource "aws_vpc" "mlflow_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mlflow-vpc"
  }
}

# 2. Create Internet Gateway
resource "aws_internet_gateway" "mlflow_gateway" {
  vpc_id = aws_vpc.mlflow_vpc.id

  tags = {
    Name = "mlflow-gw"
  }
}

# 3. Create a Subnet 
resource "aws_subnet" "mlflow_public_subnet" {
  vpc_id                  = aws_vpc.mlflow_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-2b"

  tags = {
    Name = "mlflow-public-subnet"
  }
}

# 4. Create Custom Route Table
resource "aws_route_table" "mlflow_route_table" {
  vpc_id = aws_vpc.mlflow_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mlflow_gateway.id
  }

  tags = {
    Name = "mlflow-route-table"
  }
}

# 5. Associate subnet with Route Table
resource "aws_route_table_association" "mlflow_crt_association" {
  subnet_id      = aws_subnet.mlflow_public_subnet.id
  route_table_id = aws_route_table.mlflow_route_table.id
}


# 6. Create VPC Endpoint
resource "aws_vpc_endpoint" "mlflow_endpoint" {
  vpc_id = aws_vpc.mlflow_vpc.id

  service_name = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.mlflow_route_table.id]

  tags = {
    Name = "mlflow-endpoint"
  }
}