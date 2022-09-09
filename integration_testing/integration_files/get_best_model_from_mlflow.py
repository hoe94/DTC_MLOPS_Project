import mlflow
import os
import pickle
from mlflow.tracking import MlflowClient

"""1. Load the best model from mlflow based on the accuracy score"""
# mlflow.set_tracking_uri('http://127.0.0.1:5000')
os.environ["MLFLOW_TRACKING_USERNAME"] = "mlflow"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "asdf1234"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

client = MlflowClient()
best_performance_model = client.search_runs(
    experiment_ids=1,
    filter_string="metrics.accuracy > 0.70",
    order_by=["metrics.accuracy DESC"],
)[0]

model_artifact_uri = best_performance_model.info.artifact_uri
model_uri = f"{model_artifact_uri}/artifact_folder"
model = mlflow.pyfunc.load_model(model_uri)

with open('./model.pkl', 'wb')as f:
     pickle.dump(model, f)