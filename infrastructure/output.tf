output "mlflow-server-url" {
  value = "https://${aws_apprunner_service.mlflow_server.service_url}"
}

output "mlflow-model-artifact" {
  value = "s3://${var.mlflow_artifact_bucket_name}"
}

outupt "mlflow-db-backstore" {
  value = "${aws_rds_cluster.mlflow_backend_store.endpoint}"
}