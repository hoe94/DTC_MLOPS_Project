resource "aws_apprunner_service" "mlflow_server" {
  service_name = "mlflow-server"

  source_configuration {
    auto_deployments_enabled = false

    image_repository {
      image_identifier      = "public.ecr.aws/t9j8s4z8/mlflow:main"
      image_repository_type = "ECR_PUBLIC"

      image_configuration {
        port = 5000
        runtime_environment_variables = {
          "MLFLOW_ARTIFACT_URI" = "s3://${var.mlflow_artifact_bucket_name}"
          "MLFLOW_DB_DIALECT" = "postgresql"
          "MLFLOW_DB_USERNAME" = "${aws_rds_cluster.mlflow_backend_store.master_username}"
          "MLFLOW_DB_PASSWORD" = "${aws_rds_cluster.mlflow_backend_store.master_password}"
          "MLFLOW_DB_HOST" = "${aws_rds_cluster.mlflow_backend_store.endpoint}"
          "MLFLOW_DB_PORT" = "${aws_rds_cluster.mlflow_backend_store.port}"
          "MLFLOW_DB_DATABASE" = "${aws_rds_cluster.mlflow_backend_store.database_name}"
          "MLFLOW_TRACKING_USERNAME" = "mlflow"
          "MLFLOW_TRACKING_PASSWORD" = "asdf1234"
          "MLFLOW_SQLALCHEMYSTORE_POOL_CLASS" = "NullPool"
          }
        }    
      }
  }

  instance_configuration {
    cpu = 1024
    memory = 2048
    instance_role_arn = aws_iam_role.mlflow_iam_role.arn
  }

  network_configuration {
    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.connector.arn
    }
  }

  health_check_configuration {
    healthy_threshold   = 1
    unhealthy_threshold = 5
    interval            = 20
    timeout             = 20
    path                = "/health"
    protocol            = "HTTP"
  }

  tags = {
        Name = "mlflow-server"
    }
}

resource "aws_apprunner_vpc_connector" "connector" {
  vpc_connector_name = "mlflow-connector"
  subnets            = ["${aws_subnet.mlflow_public_subnet.id}","${aws_subnet.mlflow_public_subnet2.id}"]
  security_groups    = ["${aws_security_group.mlflow_server_sg.id}"]
}