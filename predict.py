# src/predict.py

import joblib
import pandas as pd

MODEL_PATH = "model.pkl"

FEATURE_NAMES = [
    "Item_Weight", "Item_Fat_Content", "Item_Visibility",
    "Item_Type", "Item_MRP", "Outlet_Establishment_Year",
    "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
]

# Load model
model = joblib.load(MODEL_PATH)

# Example test input (MUST match training features)
features = [1, 0, 0.05, 3, 249.8, 2005, 1, 2, 1]

# Convert to DataFrame (IMPORTANT)
X = pd.DataFrame([features], columns=FEATURE_NAMES)

# Predict
prediction = model.predict(X)

print("Prediction successful:", prediction)
