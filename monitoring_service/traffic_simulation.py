import json
import uuid
from datetime import datetime
from time import sleep

import pyarrow as pa
import pandas as pd
import requests

df = pd.read_csv("test_processed.csv")
#df = df.drop(["ID","Customer_ID","Month","Name","SSN","Type_of_Loan","Credit_History_Age"],axis=1)
table = pa.Table.from_pandas(df)
data = table.to_pylist()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


for row in data:
    resp = requests.post("http://127.0.0.1:9696/predict",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(row, cls=DateTimeEncoder)).json()
    print(f"prediction: {resp['credit_score']}")
    sleep(1)