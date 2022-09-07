import json
import os
from datetime import datetime

import pandas as pd


def test_clean_age_column():
    """1. row-level unit tests: Test the clean_age_column function from src.DC_columns"""

    test_input = "24_"
    actual_output = 24

    test_input = test_input.rstrip("_")
    expected_output = int(test_input)

    assert expected_output == actual_output


def convert_month_name_to_num(mname: str):
    """This is the function convert the month name into month value"""
    mname = datetime.strptime(mname, "%B").month
    return mname


def test_process_month():
    """2. column-level unit tests: Test the process_month function from src.FE_categorical_columns"""

    """ Create the new column, month_num by apply the function to convert the month name into month value"""

    test_input = pd.Series(["April", "June", "January", "November"], name="Month")
    test_df = test_input.to_frame()
    expected_output = pd.Series([4, 6, 1, 11], name="month_num")

    test_df["month_num"] = test_df["Month"].apply(
        lambda x: convert_month_name_to_num(x)
    )
    # assert test_df['month_num'] == expected_output
    pd.testing.assert_series_equal(expected_output, test_df["month_num"])


def test_requests_columns():
    """3. table-level unit tests: Test the number of columns from request is matched with expected_columns"""
    expected_columns = [
        "ID",
        "Customer_ID",
        "Month",
        "Name",
        "Age",
        "SSN",
        "Occupation",
        "Annual_Income",
        "Monthly_Inhand_Salary",
        "Num_Bank_Accounts",
        "Num_Credit_Card",
        "Interest_Rate",
        "Num_of_Loan",
        "Type_of_Loan",
        "Delay_from_due_date",
        "Num_of_Delayed_Payment",
        "Changed_Credit_Limit",
        "Num_Credit_Inquiries",
        "Credit_Mix",
        "Outstanding_Debt",
        "Credit_Utilization_Ratio",
        "Credit_History_Age",
        "Payment_of_Min_Amount",
        "Total_EMI_per_month",
        "Amount_invested_monthly",
        "Payment_Behaviour",
        "Monthly_Balance",
        "Credit_Score",
    ]

    actual_columns = {
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

    actual_columns = list(actual_columns.keys())
    assert actual_columns == expected_columns
