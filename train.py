# src/train.py
import os
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

os.makedirs("models", exist_ok=True)

df = pd.read_csv("final_data.csv")

X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run():
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")   # ✅ FIX

    mlflow.sklearn.log_model(model, "model")
