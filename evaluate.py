# src/evaluate.py
import joblib
import pandas as pd
import mlflow
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

model = joblib.load("model.pkl")

df = pd.read_csv("final_data.csv")

X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]

preds = model.predict(X)

rmse = np.sqrt(mean_squared_error(y, preds))
r2 = r2_score(y, preds)

mlflow.log_metric("RMSE", rmse)
mlflow.log_metric("R2", r2)

print("RMSE:", rmse)
print("R2:", r2)
