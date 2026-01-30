# src/preprocessing.py
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def preprocess():
    df = pd.read_csv("featured_data.csv")

    cat_cols = df.select_dtypes(include="object").columns
    le = LabelEncoder()

    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    df.to_csv("final_data.csv", index=False)

if __name__ == "__main__":
    preprocess()
