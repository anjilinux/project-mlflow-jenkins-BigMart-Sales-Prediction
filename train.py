# src/train.py
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("BigMart-Sales")

df = pd.read_csv("final_data.csv")

X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with mlflow.start_run():
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    mlflow.log_param("n_estimators", 200)
    mlflow.sklearn.log_model(model, "model")
