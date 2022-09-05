import json
import pickle
import warnings

from sklearn.preprocessing import StandardScaler

from FE_categorical_columns import convert_month_name_to_num
from ordinal_columns_encoding import (Credit_Mix_dict_mapping,
                                      Occupation_dict_mapping,
                                      Payment_Behaviour_dict_mapping,
                                      Payment_of_Min_Amount_dict_mapping)

warnings.filterwarnings("ignore")
with open("model/standard_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# X_original =  {'Credit_Mix': 'Bad', 'Occupation': 'Engineer', 'Num_Bank_Accounts': 3}
X_original = {
    "ID": "0x1602",
    "Customer_ID": "CUS_0xd40",
    "Month": "January",
    "Name": "Aaron Maashoh",
    "Age": 23,
    "SSN": "821-00-0265",
    "Occupation": "Scientist",
    "Annual_Income": 19114.12,
    "Monthly_Inhand_Salary": 1824.8433333333,
    "Num_Bank_Accounts": 3,
    "Num_Credit_Card": 4,
    "Interest_Rate": 3,
    "Num_of_Loan": 4,
    "Type_of_Loan": "Auto Loan, Credit-Builder Loan, Personal Loan, and Home Equity Loan",
    "Delay_from_due_date": 3,
    "Num_of_Delayed_Payment": 7,
    "Changed_Credit_Limit": 11.27,
    "Num_Credit_Inquiries": 4.0,
    "Credit_Mix": "_",
    "Outstanding_Debt": 809.98,
    "Credit_Utilization_Ratio": 26.8226196237,
    "Credit_History_Age": "22 Years and 1 Months",
    "Payment_of_Min_Amount": "No",
    "Total_EMI_per_month": 49.5749492149,
    "Amount_invested_monthly": 80.415295439,
    "Payment_Behaviour": "High_spent_Small_value_payments",
    "Monthly_Balance": 312.4940886794,
    "Credit_Score": "Good",
}


fe_numerical_columns_list = [
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


updated_dict = {}
for key, value in X_original.items():
    if key in fe_categorical_columns_list:  # if the request key is categorical columns
        if key == "Credit_Mix":
            columns_dict = Credit_Mix_dict_mapping(key, value)
            updated_dict.update(columns_dict)

        elif key == "Occupation":
            columns_dict = Occupation_dict_mapping(key, value)
            updated_dict.update(columns_dict)

        elif key == "Payment_Behaviour":
            columns_dict = Payment_Behaviour_dict_mapping(key, value)
            updated_dict.update(columns_dict)

        elif key == "Payment_of_Min_Amount":
            columns_dict = Payment_of_Min_Amount_dict_mapping(key, value)
            updated_dict.update(columns_dict)

    elif key in fe_numerical_columns_list:  # if the request key is numerical columns
        transformed_value = scaler.transform([[value]])
        extract_value = transformed_value[0]
        updated_dict[key] = extract_value[0]

    elif key == "Month":
        month_num = convert_month_name_to_num(value)
        updated_dict["Month_num"] = month_num

    else:
        pass

# input = {"Month_num": 1, "Age": -1.7849873970750565, "Occupation": 4, "Annual_Income": 88.02363516054615, "Monthly_Inhand_Salary": 6.691260608872023, "Num_Bank_Accounts": -1.8790715813006242, "Num_Credit_Card": -1.874367372089346, "Interest_Rate": -1.8790715813006242, "Num_of_Loan": -1.874367372089346, "Delay_from_due_date": -1.8790715813006242, "Num_of_Delayed_Payment": -1.8602547444555109, "Changed_Credit_Limit": -1.8401677711233522, "Num_Credit_Inquiries": -1.874367372089346, "Credit_Mix": 3, "Outstanding_Debt": 1.9171311680168157, "Credit_Utilization_Ratio": -1.7670049946300332, "Payment_of_Min_Amount": 2, "Total_EMI_per_month": -1.6599732761890682, "Amount_invested_monthly": -1.5148938354026422, "Payment_Behaviour": 5, "Monthly_Balance": -0.4231466384987781}

list_ = [
    "Age",
    "Occupation",
    "Annual_Income",
    "Monthly_Inhand_Salary",
    "Num_Bank_Accounts",
    "Num_Credit_Card",
    "Interest_Rate",
    "Num_of_Loan",
    "Delay_from_due_date",
    "Num_of_Delayed_Payment",
    "Changed_Credit_Limit",
    "Num_Credit_Inquiries",
    "Credit_Mix",
    "Outstanding_Debt",
    "Credit_Utilization_Ratio",
    "Payment_of_Min_Amount",
    "Total_EMI_per_month",
    "Amount_invested_monthly",
    "Payment_Behaviour",
    "Monthly_Balance",
    "Month_num",
]

ordered_dict = {}
for item in list_:
    ordered_dict[item] = updated_dict[item]
print(ordered_dict)

with open(f"data/input.json", "w") as f:
    json.dump(ordered_dict, f)
