import json
from datetime import datetime

import pandas as pd


def convert_month_name_to_num(mname: str):
    """This is the function convert the month name into month value"""
    mname = datetime.strptime(mname, "%B").month
    return mname


def process_month(df: pd.DataFrame):
    """Create the new column, month_num by apply the function to convert the month name into month value"""
    df["Month_num"] = df["Month"].apply(lambda x: convert_month_name_to_num(x))
    return df


def process_occupation(df: pd.DataFrame, top_N_num: int):
    """
    This is the function apply the ordinal encoding into the column, occupation

    1. Create the dictionary based on top N distinct values of Occupation column
    2. Map the dictionary key into the column, occupation
    3. Save the dictionary to data path
    """

    top_N_num_occupation_list = []
    occupation_rank_list = []

    for i in range(top_N_num + 1):
        occupation = df["Occupation"].value_counts().index[i]

        if occupation != "_______":
            top_N_num_occupation_list.append(occupation)
            occupation_rank = top_N_num_occupation_list.index(occupation) + 1
            occupation_rank_list.append(occupation_rank)
        else:
            pass

    top_N_num_occupation_dict = dict(
        zip(top_N_num_occupation_list, occupation_rank_list)
    )
    top_N_num_occupation_dict["Others"] = 0
    df["Occupation"] = df["Occupation"].map(top_N_num_occupation_dict)
    df["Occupation"] = df["Occupation"].fillna(0)

    with open(f"data/dictionary/occupation_dict.json", "w") as f:
        json.dump(top_N_num_occupation_dict, f)

    return df


def ordinal_columns_encoding_dict(df: pd.DataFrame, feature: str):
    """This is the function create the dictionary for distinct values based on input feature"""

    feature_value_list = []
    feature_value_rank_list = []

    for i in range(len(df[feature].value_counts())):
        featue_value = df[feature].value_counts().index[i]
        feature_value_list.append(featue_value)

        feature_value_rank = feature_value_list.index(featue_value) + 1
        feature_value_rank_list.append(feature_value_rank)

    feature_value_dict = dict(zip(feature_value_list, feature_value_rank_list))
    return feature_value_dict


def ordinal_columns_encoding(df: pd.DataFrame, column_list: list):
    """1. This is the function perform the ordinal encoding on the list of columns
    2. Save the dictionary to data path
    """
    # Credit_Mix Payment_of_Min_Amount Payment_Behaviour Credit_Score

    for feature in column_list:
        feature_value_dict = ordinal_columns_encoding_dict(df, feature)
        df[feature] = df[feature].map(feature_value_dict)
        with open(f"data/dictionary/{feature}_dict.json", "w") as f:
            json.dump(feature_value_dict, f)
    return df


def FE_categorical_main(df: pd.DataFrame, top_N_num: int, column_list: list):
    df = process_month(df)
    df = process_occupation(df, top_N_num)
    df = ordinal_columns_encoding(df, column_list)
    return df
