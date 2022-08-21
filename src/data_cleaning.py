import pandas as pd
from DC_columns import clean_integer_columns, clean_float_columns
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    df = pd.read_csv("data/train.csv")
    df = clean_integer_columns(df)
    df = clean_float_columns(df)
    df.to_csv("data/train_clean.csv", index = False)
    