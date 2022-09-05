import requests

test_data = {
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


url = "http://localhost:9696/predict"
response = requests.post(url, json=test_data)
print(response.json())
