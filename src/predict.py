import flask
import pickle
import mlflow
from mlflow.tracking import MlflowClient

'''Load the best model from mlflow based on the accuracy score'''
mlflow.set_tracking_uri('http://localhost:5000')
client = MlflowClient()
best_performance_model = client.search_runs(
    experiment_ids = 1,
    filter_string = "metrics.accuracy > 0.70",
    order_by = ['metrics.accuracy DESC']
)[0]

model_artifact_uri = best_performance_model.info.artifact_uri
model_uri = f"{model_artifact_uri}/artifact_folder"
model = mlflow.pyfunc.load_model(model_uri)