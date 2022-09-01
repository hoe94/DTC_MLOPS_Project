output "mlflow-server-url" {
  value = "https://${aws_apprunner_service.mlflow_server.service_url}"
}

output "mlflow-model-artifact" {
  value = "s3://${var.mlflow_artifact_bucket_name}"
}

output "mlflow-db-backstore" {
  value = "${aws_rds_cluster.mlflow_backend_store.endpoint}"
}

output "aws-ecr-repository" {
  value = "${aws_ecr_repository.ecr_repo.repository_url}"
}