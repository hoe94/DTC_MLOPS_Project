import pandas as pd
from sklearn.preprocessing import StandardScaler


def process_age_count(df: pd.DataFrame):
    """This is the function process the age column"""
    # std_scaler = StandardScaler()

    df = df[
        (df["Age"] > 0) & (df["Age"] < 100)
    ]  # filter the outlier value less than 100 & more than 0 years old
    # df['Age'] = std_scaler.fit_transform(df[['Age']]).flatten() #normalize the age column value from -1 to 1
    return df


def process_monthly_inhand_salary(df: pd.DataFrame):
    """This is the function process the Annual_Income column
    1. Fill the missing value with mean of Monthly_Inhand_Salary
    2. Normalize the Monthly_Inhand_Salary column value from -1 to 1
    """

    # std_scaler = StandardScaler()

    df["Monthly_Inhand_Salary"] = df["Monthly_Inhand_Salary"].fillna(
        df["Monthly_Inhand_Salary"].mean()
    )
    # df['Monthly_Inhand_Salary'] = std_scaler.fit_transform(df[['Monthly_Inhand_Salary']]).flatten()  #normalize the Monthly_Inhand_Salary column value from -1 to 1
    return df
    # v2: handle the outlier value


def process_num_credit_inquiries(df: pd.DataFrame):
    """This is the function process the Num_Credit_Inquiries column
    1. Fill the missing value with the most value of Num_Credit_Inquiries
    2. Normalize the Monthly_Inhand_Salary column value from -1 to 1
    """
    # std_scaler = StandardScaler()

    df["Num_Credit_Inquiries"] = df["Num_Credit_Inquiries"].fillna(
        df["Num_Credit_Inquiries"].mode()[0]
    )
    # df['Num_Credit_Inquiries'] = std_scaler.fit_transform(df[['Num_Credit_Inquiries']]).flatten()  #normalize the Monthly_Inhand_Salary column value from -1 to 1
    return df


def process_amount_invested_monthly(df: pd.DataFrame):
    """This is the function impute the missing value with mean value of column, Amount_invested_monthly"""

    df["Amount_invested_monthly"] = df["Amount_invested_monthly"].fillna(
        df["Amount_invested_monthly"].mean()
    )
    return df


def process_monthly_balance(df: pd.DataFrame):
    """This is the function process the Monthly_Balance column
    1. Fill the missing value with the most value of Monthly_Balance
    2. Normalize the Monthly_Balance column value from -1 to 1
    """
    # std_scaler = StandardScaler()
    df["Monthly_Balance"] = df["Monthly_Balance"].fillna(df["Monthly_Balance"].mean())
    # df['Monthly_Balance'] = std_scaler.fit_transform(df[['Monthly_Balance']]).flatten()
    return df


def normalization_columns(df: pd.DataFrame, column_list: list):
    """This is the function apply the Normalization on the list of columns"""

    #'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate','Num_of_Loan','Delay_from_due_date','Num_of_Delayed_Payment','Changed_Credit_Limit','Num_Credit_Inquiries','Outstanding_Debt','Credit_Utilization_Ratio','Total_EMI_per_month','Amount_invested_monthly'
    # 'Occupation', 'Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour',	'Credit_Score',	'Month_num'
    # 'Age', 'Monthly_Inhand_Salary', 'Num_Credit_Inquiries', 'Monthly_Balance'
    std_scaler = StandardScaler()

    for feature in column_list:
        # df[feature] = std_scaler.fit_transform(df[[feature]]).flatten()
        std_scaler.fit(df[[feature]])
        df[feature] = std_scaler.transform(df[[feature]]).flatten()

    return df, std_scaler


def FE_numeric_main(df: pd.DataFrame, column_list: list):
    """Consolidated functions to apply the feature engineering technique into numerical columns"""


    df = process_age_count(df)
    df = process_monthly_inhand_salary(df)
    df = process_num_credit_inquiries(df)
    df = process_amount_invested_monthly(df)
    df = process_monthly_balance(df)
    df, std_scaler = normalization_columns(df, column_list)
    return df, std_scaler
