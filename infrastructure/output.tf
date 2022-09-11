output "aws-ecr-repository" {
  value = "${aws_ecr_repository.ecr_repo.repository_url}"
}

output "dvc_remote_storage" {
  value = "s3://${var.dvc_remote_storage}"
}

output "mlflow-db-backstore" {
  value = "${aws_rds_cluster.mlflow_backend_store.endpoint}"
}

output "mlflow-model-artifact" {
  value = "s3://${var.mlflow_artifact_bucket_name}"
}

output "mlflow-server-url" {
  value = "https://${aws_apprunner_service.mlflow_server.service_url}"
}







