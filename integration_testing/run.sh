#!/usr/bin/env bash

docker build -t mlops-project-credit-score-prediction:v1 ..

docker-compose up -d

sleep 5

pipenv run python test_docker.py

docker-compose down