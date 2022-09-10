import os
import pickle

import mlflow
import numpy as np
import pandas as pd
# from omegaconf import DictConfig
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from mlflow.tracking import MlflowClient
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split

# import hydra


# MLFLOW_TRACKING_USERNAME = os.getenv('MLFLOW_TRACKING_USERNAME')
# MLFLOW_TRACKING_PASSWORD = os.getenv('MLFLOW_TRACKING_PASSWORD')
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# mlflow.set_tracking_uri('http://localhost:5000')
os.environ["MLFLOW_TRACKING_USERNAME"] = "mlflow"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "asdf1234"
# mlflow.set_tracking_uri('https://zmqztduci9.us-east-2.awsapprunner.com')
mlflow.set_experiment("Random_Forest")


@task(name="load_data")
def load_data():
    df = pd.read_csv("data/train_processed.csv")
    X = df.drop(
        [
            "ID",
            "Customer_ID",
            "Month",
            "Name",
            "SSN",
            "Type_of_Loan",
            "Credit_History_Age",
            "Credit_Score",
        ],
        axis=1,
    )
    y = df["Credit_Score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


@task(name="random_forest")
def random_forest(run_name, X_train, X_test, y_train, y_test):
    """This is the function train the model by using Random Forest algorithm
    and perform the hyperparameter tuning on hyperopt
    """

    def rf_function(params):
        with mlflow.start_run(run_name=run_name):
            mlflow.set_tag("ml_algorithm", "random_forest")
            rf_model = RandomForestClassifier(**params)
            mlflow.log_params(params)
            rf_model.fit(X_train, y_train)

            y_pred = rf_model.predict(X_test)
            accuracy = accuracy_score(y_pred, y_test)
            mlflow.log_metric("accuracy", accuracy)

            loss_score = cross_val_score(
                rf_model, X_train, y_train, scoring="accuracy"
            ).mean()

            with open('./model/rf_model.pkl', 'wb')as file:
                pickle.dump(rf_model, file)

            mlflow.sklearn.log_model(rf_model, artifact_path="artifact_folder")

        return {"loss": loss_score, "status": STATUS_OK}

    parameters = {
        "max_depth": scope.int(hp.quniform("max_depth", 1, 20, 1)),
        "n_estimators": scope.int(hp.quniform("n_estimators", 10, 100, 1)),
        "min_samples_split": scope.int(hp.quniform("min_samples_split", 2, 10, 1)),
        "min_samples_leaf": scope.int(hp.quniform("min_samples_leaf", 1, 4, 1)),
        "random_state": 42,
    }

    rstate_ = np.random.default_rng(42)  # for reproducible results
    fmin(
        fn=rf_function,
        space=parameters,
        algo=tpe.suggest,
        max_evals=5,
        trials=Trials(),
        rstate=rstate_,
    )


@task(name="register_best_model")
def register_best_model(experiment_id, run_name):
    """This is the function register the best model based on the accuracy score greater than 70%"""
    client = MlflowClient()
    best_performace_runs = client.search_runs(
        experiment_ids=experiment_id,
        filter_string="metrics.accuracy > 0.70",
        order_by=["metrics.accuracy DESC"],
    )[0]

    best_performace_runs_name = best_performace_runs.data.tags[
        "mlflow.runName"
    ]  # Get the run name from the best performance runs

    if (
        best_performace_runs_name != run_name
    ):  # If the best performance runs is not from the current run
        pass
    else:
        model_uri = best_performace_runs.info.run_id
        mlflow.register_model(
            model_uri=f"runs:/{model_uri}/artifact_folder", name="Credit_Score_Model"
        )


@task(name="transition_model_stage")
def transition_model_stage():
    """This is the function get the model latest version and transitioned to staging env/ production env"""
    client = MlflowClient()
    all_transitions = client.get_latest_versions(name="Credit_Score_Model")

    latest_transitions_version = len(all_transitions) - 1
    # latest_transitions_current_stage = all_transitions[latest_transitions_version].current_stage

    if latest_transitions_version == 0:
        client.transition_model_version_stage(
            name="Credit_Score_Model",
            version=latest_transitions_version + 1,
            stage="Production",
            archive_existing_versions=False,
        )
    else:
        client.transition_model_version_stage(
            name="Credit_Score_Model",
            version=latest_transitions_version + 1,
            stage="Staging",
            archive_existing_versions=False,
        )


# @hydra.main(version_base = None, config_path = '../', config_name = 'config')
# def model_training(config: DictConfig):
#    if config.algorithm == 'LogisticRegression':
#        logistic_regression('08162022_Logistic_Regression')
#
#    elif config.algorithm == 'RandomForest':
#        random_forest('08172022_Random_Forest')
#
#    else:
#        pass
#


@flow(name="mlops_project", task_runner=SequentialTaskRunner())
def main(run_name):
    """This is the flow function contains all the task function"""
    X_train, X_test, y_train, y_test = load_data()
    random_forest(run_name, X_train, X_test, y_train, y_test)
    register_best_model("1", run_name)
    transition_model_stage()


if __name__ == "__main__":
    run_name = "09102022_1_Random_Forest"
    main(run_name)

    # Deploy the prefect workflow
    deployment = Deployment.build_from_flow(
        flow=main,
        name="01_Deployment",
        version=1,
        schedule=CronSchedule(
            cron="0 9 1 * *",  # Run the prefect flow at 09:00 (GMT-4), 21:00 (GMT+8) on every 1st day of month
            timezone="America/New_York",
        ),
    )
    deployment.apply()
