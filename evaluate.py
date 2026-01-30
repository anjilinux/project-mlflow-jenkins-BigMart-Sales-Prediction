# src/evaluate.py
import joblib
import pandas as pd
import mlflow
from sklearn.metrics import r2_score, mean_squared_error

model = joblib.load("model.pkl")   # ✅ FIX

df = pd.read_csv("final_data.csv")

X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]

preds = model.predict(X)

mlflow.log_metric("RMSE", mean_squared_error(y, preds, squared=False))
mlflow.log_metric("R2", r2_score(y, preds))
