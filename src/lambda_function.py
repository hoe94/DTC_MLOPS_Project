import pickle
from sklearn.preprocessing import StandardScaler

from FE_categorical_columns import convert_month_name_to_num
from ordinal_columns_encoding import (Credit_Mix_dict_mapping,
                                      Occupation_dict_mapping,
                                      Payment_Behaviour_dict_mapping,
                                      Payment_of_Min_Amount_dict_mapping)

with open('model/model.pkl', 'rb')as f:
    """1. Load the scaler from model path"""
    model = pickle.load(f)


with open("model/standard_scaler.pkl", "rb") as f:
    """2. Load the scaler from model path"""
    scaler = pickle.load(f)


def process_request(data_request):
    """Process the incoming request data"""
    # X_original = {"ID":"0x1602","Customer_ID":"CUS_0xd40","Month":"January","Name":"Aaron Maashoh","Age":23,"SSN":"821-00-0265","Occupation":"Scientist","Annual_Income":19114.12,"Monthly_Inhand_Salary":1824.8433333333,"Num_Bank_Accounts":3,"Num_Credit_Card":4,"Interest_Rate":3,"Num_of_Loan":4,"Type_of_Loan":"Auto Loan, Credit-Builder Loan, Personal Loan, and Home Equity Loan","Delay_from_due_date":3,"Num_of_Delayed_Payment":7,"Changed_Credit_Limit":11.27,"Num_Credit_Inquiries":4.0,"Credit_Mix":"_","Outstanding_Debt":809.98,"Credit_Utilization_Ratio":26.8226196237,"Credit_History_Age":"22 Years and 1 Months","Payment_of_Min_Amount":"No","Total_EMI_per_month":49.5749492149,"Amount_invested_monthly":80.415295439,"Payment_Behaviour":"High_spent_Small_value_payments","Monthly_Balance":312.4940886794,"Credit_Score":"Good"}
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
        if (
            key in fe_categorical_columns_list
        ):  # if the request key is categorical columns
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


def predict(event):
    data_request = event

    features = process_request(data_request)
    feature_values = list(features.values())

    preds = model.predict([feature_values])

    result = {"credit_score": int(preds[0])}

    return result


def lambda_handler(event, context):
    result = predict(event)
    return result