# 1. s3 bucket: MLFlow model artifact 
resource "aws_s3_bucket" "mlflow_model_artifact" {
    bucket = var.mlflow_artifact_bucket_name
    acl    = "private"
    tags   = {
        Name = "mlflow-model-artifact"
    }
}

# 2. s3 bucket: DVC
resource "aws_s3_bucket" "dvc_remote_storage" {
    bucket = var.dvc_remote_storage
    acl    = "private"
    tags   = {
        Name = "dvc-remote-storage"
    }
}