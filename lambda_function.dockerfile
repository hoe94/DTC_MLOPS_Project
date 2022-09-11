FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["/src/FE_categorical_columns.py", "/src/ordinal_columns_encoding.py", "/src/lambda_function.py", "./"]

RUN mkdir model
COPY ["/model/model.pkl","/model/standard_scaler.pkl", "./model/"]

CMD [ "lambda_function.lambda_handler" ]