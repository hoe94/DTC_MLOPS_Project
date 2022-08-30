variable "aws_region" {
  description = "Enter your AWS region in default value"
  default     = "us-east-2"
}

variable "mlflow_artifact_bucket_name" {
    description = "Enter your MLflow model artifact bucket name in default value"
    default     = "mlops-project-mlflow-model-artifact"
}

variable "dvc_remote_storage" {
    description = "Enter your MLflow model artifact bucket name in default value"
    default     = "mlops-project-dvc-remote-storage"
}