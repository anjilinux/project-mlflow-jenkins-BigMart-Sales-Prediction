# src/data_ingestion.py
import pandas as pd

def load_data():
    df = pd.read_csv("BigMart.csv")
    df.to_csv("clean_data.csv", index=False)

if __name__ == "__main__":
    load_data()
