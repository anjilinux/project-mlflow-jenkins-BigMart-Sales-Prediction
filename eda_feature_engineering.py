# src/eda_feature_engineering.py
import pandas as pd
import numpy as np

def feature_engineering():
    df = pd.read_csv("clean_data.csv")

    df["Item_Visibility"] = df["Item_Visibility"].replace(0, df["Item_Visibility"].mean())
    df["Item_Weight"].fillna(df["Item_Weight"].mean(), inplace=True)
    df["Outlet_Size"].fillna(df["Outlet_Size"].mode()[0], inplace=True)

    df.to_csv("featured_data.csv", index=False)

if __name__ == "__main__":
    feature_engineering()
