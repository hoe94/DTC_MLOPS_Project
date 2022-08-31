data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_db_subnet_group" "rds" {
  name       = "mlflow-rds-subnet-group"
  #subnet_ids = aws_subnet.mlflow_public_subnet.*.id 
  subnet_ids = ["${aws_subnet.mlflow_public_subnet.id}","${aws_subnet.mlflow_public_subnet2.id}"]
}

resource "aws_rds_cluster" "mlflow_backend_store" {
  cluster_identifier        = "mlflow-rds"
  engine                    = "aurora-postgresql"
  engine_mode               = "serverless"
  port                      = 5432
  db_subnet_group_name      = aws_db_subnet_group.rds.name
  vpc_security_group_ids    = [aws_security_group.mlflow_server_sg.id]
  #availability_zones        = slice(data.aws_availability_zones.available.names, 0, 3)
  availability_zones        = slice(data.aws_availability_zones.available.names, 0, 2)
  database_name             = "mlflow"
  master_username           = "mlflow"
  master_password           = "asdf1234"
  backup_retention_period   = 5
  preferred_backup_window   = "04:00-06:00"
  final_snapshot_identifier = "mlflow-db-backup"
  skip_final_snapshot       = true
  deletion_protection       = false
  apply_immediately         = true

  scaling_configuration {
    min_capacity             = 2
    max_capacity             = 32
    auto_pause               = true
    seconds_until_auto_pause = 1800
  }
  
  lifecycle {
    ignore_changes = [
      final_snapshot_identifier,
    ]
}

  tags ={
      Name = "mlflow-rds"
    }
}