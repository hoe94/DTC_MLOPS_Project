#!/usr/bin/env bash

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

docker build -t mlops-project-credit-score-prediction:v1 ..

docker run -it --rm -p 9696:9696 -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" -e MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" --name mlops-project mlops-project-credit-score-prediction:v1
#docker-compose up -d
sleep 5

pipenv run python test_docker.py

docker-compose down