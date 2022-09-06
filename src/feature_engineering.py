import pickle
import warnings

import pandas as pd
from sklearn.preprocessing import StandardScaler

from FE_categorical_columns import FE_categorical_main
from FE_numeric_columns import FE_numeric_main, normalization_columns

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    df = pd.read_csv("data/test_clean.csv")
    fe_categorical_columns_list = [
        "Credit_Mix",
        "Payment_of_Min_Amount",
        "Payment_Behaviour",
        "Credit_Score",
    ]
    # fe_numerical_columns_list = ['Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate','Num_of_Loan','Delay_from_due_date','Num_of_Delayed_Payment','Changed_Credit_Limit','Num_Credit_Inquiries','Outstanding_Debt','Credit_Utilization_Ratio','Total_EMI_per_month','Amount_invested_monthly']
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

    # normalization_columns_list = ['Occupation', 'Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour',	'Month_num', 'Age', 'Monthly_Inhand_Salary', 'Num_Credit_Inquiries', 'Monthly_Balance']
    top_N_num = 5

    df = FE_categorical_main(df, top_N_num, fe_categorical_columns_list)
    df, std_scaler = FE_numeric_main(df, fe_numerical_columns_list)
    # df = normalization_columns(df, normalization_columns_list)
    df.to_csv("data/train_processed.csv", index=False)
    # df.head(1000).to_csv(
    #    "monitoring_service/evidently_service/datasets/test_processed.csv", index=False
    # )

    with open("model/standard_scaler.pkl", "wb") as f:
        pickle.dump(std_scaler, f)
