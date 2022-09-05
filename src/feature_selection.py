import pandas as pd
from sklearn.feature_selection import mutual_info_classif

df = pd.read_csv("data/train_processed.csv")


# X = df.drop('Credit_Score', axis = 1)
X = df.drop(
    [
        "Credit_Score",
        "ID",
        "Customer_ID",
        "Month",
        "Name",
        "Credit_History_Age",
        "SSN",
        "Type_of_Loan",
    ],
    axis=1,
)
y = df["Credit_Score"]


mutual_info = mutual_info_classif(X, y)
mutual_data = pd.Series(mutual_info, index=X.columns)
mutual_data.sort_values(ascending=False)
