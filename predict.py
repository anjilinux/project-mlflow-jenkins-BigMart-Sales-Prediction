# predict.py

import joblib
import pandas as pd

model = joblib.load("model.pkl")

FEATURE_NAMES = [
    "Item_Identifier",
    "Outlet_Identifier",
    "Item_Weight",
    "Item_Fat_Content",
    "Item_Visibility",
    "Item_Type",
    "Item_MRP",
    "Outlet_Establishment_Year",
    "Outlet_Size",
    "Outlet_Location_Type",
    "Outlet_Type"
]

# Dummy test input (MUST match training encoding)
features = [
    1023,   # Item_Identifier (encoded)
    17,     # Outlet_Identifier (encoded)
    9.3,
    0,
    0.05,
    3,
    249.8,
    2005,
    1,
    2,
    1
]

X = pd.DataFrame([features], columns=FEATURE_NAMES)

prediction = model.predict(X)
print("Prediction successful:", prediction)
