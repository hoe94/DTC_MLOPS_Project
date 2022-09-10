import json
import os
import pickle
import warnings

import requests
from pymongo import MongoClient
from flask import Flask, jsonify, request
from sklearn.preprocessing import StandardScaler

from FE_categorical_columns import convert_month_name_to_num
from ordinal_columns_encoding import (Credit_Mix_dict_mapping,
                                      Occupation_dict_mapping,
                                      Payment_Behaviour_dict_mapping,
                                      Payment_of_Min_Amount_dict_mapping)


warnings.filterwarnings("ignore")
app = Flask("credit_score_classifier")

MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")

EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE', 'http://127.0.0.1:5000')


with open('model.pkl', 'rb')as f:
   """1. Load the model from the folder"""
   model = pickle.load(f)

with open("standard_scaler.pkl", "rb") as f:
    """2. Load the scaler from the folder"""
    scaler = pickle.load(f)


def process_request(data_request):
    """3. Process the incoming request data"""
    fe_numerical_columns_list = [
        "Annual_Income",
        "Num_Bank_Accounts",
        "Num_Credit_Card",
        "Interest_Rate",
        "Num_of_Loan",
        "Delay_from_due_date",
        "Num_of_Delayed_Payment",
        "Changed_Credit_Limit",
        "Num_Credit_Inquiries",
        "Outstanding_Debt",
        "Credit_Utilization_Ratio",
        "Total_EMI_per_month",
        "Amount_invested_monthly",
        "Occupation",
        "Credit_Mix",
        "Payment_of_Min_Amount",
        "Payment_Behaviour",
        "Month_num",
        "Age",
        "Monthly_Inhand_Salary",
        "Num_Credit_Inquiries",
        "Monthly_Balance",
    ]
    fe_categorical_columns_list = [
        "Credit_Mix",
        "Occupation",
        "Payment_Behaviour",
        "Payment_of_Min_Amount",
    ]

    data_processed_request_dict = {}
    for key, value in data_request.items():
        if (key in fe_categorical_columns_list):  # if the request key is categorical columns
            if key == "Credit_Mix":
                columns_dict = Credit_Mix_dict_mapping(key, value)
                data_processed_request_dict.update(columns_dict)

            elif key == "Occupation":
                columns_dict = Occupation_dict_mapping(key, value)
                data_processed_request_dict.update(columns_dict)

            elif key == "Payment_Behaviour":
                columns_dict = Payment_Behaviour_dict_mapping(key, value)
                data_processed_request_dict.update(columns_dict)

            elif key == "Payment_of_Min_Amount":
                columns_dict = Payment_of_Min_Amount_dict_mapping(key, value)
                data_processed_request_dict.update(columns_dict)

        elif (
            key in fe_numerical_columns_list
        ):  # if the request key is numerical columns
            transformed_value = scaler.transform([[value]])
            extract_value = transformed_value[0]
            data_processed_request_dict[key] = extract_value[0]

        elif key == "Month":
            month_num = convert_month_name_to_num(value)
            data_processed_request_dict["Month_num"] = month_num

        else:
            pass

    return data_processed_request_dict

def save_prediction_data_to_mongodb(request, prediction):
    """4. Insert the request & prediction result into mongodb"""
    req = request.copy()
    req['prediction'] = prediction
    collection.insert_one(req)

def send_to_evidently_service(request, prediction):
    """5. Send the data into evidently AI"""
    rec = request.copy()
    rec['prediction'] = prediction
    requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/credit_score", json=[rec])


@app.route("/predict", methods=["POST"])
def main():

    #drop_column_list = [
    #        "ID",
    #        "Customer_ID",
    #        "Month",
    #        "Name",
    #        "SSN",
    #        "Type_of_Loan",
    #        "Credit_History_Age",
    #        "Credit_Score",
    #    ],
    data_request = request.get_json()
    #data_request = [data_request.pop(column, None) for column in drop_column_list if column in data_request]

    #features = process_request(data_request)
    #feature_values = list(features.values())
    feature_values = list(data_request.values())
    preds = model.predict([feature_values])

    save_prediction_data_to_mongodb(data_request, int(preds[0]))
    send_to_evidently_service(data_request, int(preds[0]))

    result = {"credit_score": int(preds[0])}
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
