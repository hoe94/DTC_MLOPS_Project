FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["../src/FE_categorical_columns.py", "../src/ordinal_columns_encoding.py", "../src/predict.py", "./"]

WORKDIR /model

COPY ["../model/standard_scaler.pkl", "./model"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]