FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["/src/FE_categorical_columns.py", "/src/ordinal_columns_encoding.py", "/src/predict.py", "./"]

RUN mkdir model
COPY ["/model/model.pkl","/model/standard_scaler.pkl", "./model/"]

EXPOSE 9696
CMD ["gunicorn", "--timeout", "1000"] 
ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]