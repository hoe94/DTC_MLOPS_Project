#!/usr/bin/env bash

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

docker build -t mlops-project-credit-score-prediction:v1 ..

docker-compose up -d

sleep 5

pipenv run python test_docker.py

docker-compose down