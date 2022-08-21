import pandas as pd

'''1. Integer columns'''

def clean_age_column(df: pd.DataFrame):
    df['Age'] = df['Age'].apply(lambda x:x.rstrip('_'))
    df['Age'] = df['Age'].astype('int')
    return df

def clean_num_of_loan_column(df: pd.DataFrame):
    df['Num_of_Loan'] = df['Num_of_Loan'].apply(lambda x:x.rstrip('_'))
    df['Num_of_Loan'] = df['Num_of_Loan'].astype('int')
    return df

def clean_num_of_delayed_payment(df: pd.DataFrame):
    impute_missing_value = df['Num_of_Delayed_Payment'].mode()[0]
    df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].fillna(impute_missing_value)

    df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].apply(lambda x:x.rstrip('_'))
    df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].astype('int')
    return df

def clean_integer_columns(df: pd.DataFrame):
    df = clean_age_column(df)
    df = clean_num_of_loan_column(df)
    df = clean_num_of_delayed_payment(df)
    return df

'''2. Float type columns'''

def clean_annual_income(df: pd.DataFrame):
    df['Annual_Income'] = df['Annual_Income'].apply(lambda x:x.rstrip('_'))
    df['Annual_Income'] = df['Annual_Income'].astype("float")
    return df

def clean_changed_credit_limit(df: pd.DataFrame):
    df['Changed_Credit_Limit'] = df['Changed_Credit_Limit'].replace('_', 0)
    df['Changed_Credit_Limit'] = df['Changed_Credit_Limit'].astype('float')
    return df

def clean_outstanding_debt(df: pd.DataFrame):
    df['Outstanding_Debt'] = df['Outstanding_Debt'].apply(lambda x:x.rstrip('_'))
    df['Outstanding_Debt'] = df['Outstanding_Debt'].astype("float")
    return df

def clean_amount_invested_monthly(df: pd.DataFrame):
    df["Amount_invested_monthly"] = df["Amount_invested_monthly"].replace("__10000__", "10000")
    df["Amount_invested_monthly"] = df["Amount_invested_monthly"].astype("float")
    return df

def clean_monthly_balance(df: pd.DataFrame):
    df = df[df['Monthly_Balance'] != '__-333333333333333333333333333__']
    df['Monthly_Balance'] = df['Monthly_Balance'].astype("float")
    return df

def clean_float_columns(df: pd.DataFrame):
    df = clean_annual_income(df)
    df = clean_changed_credit_limit(df)
    df = clean_outstanding_debt(df)
    df = clean_amount_invested_monthly(df)
    df = clean_monthly_balance(df)
    return df
    
