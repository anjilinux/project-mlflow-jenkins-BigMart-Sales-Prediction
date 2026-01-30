# src/evaluate.py
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import pandas as pd
import mlflow

model = joblib.load("model.pkl")

df = pd.read_csv("data/processed/final_data.csv")
X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]

preds = model.predict(X)

mlflow.log_metric("RMSE", mean_squared_error(y, preds, squared=False))
mlflow.log_metric("R2", r2_score(y, preds))
