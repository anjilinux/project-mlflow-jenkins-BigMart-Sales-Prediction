# predict.py

import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load("model.pkl")

# 🔑 Get exact training feature order
FEATURE_NAMES = list(model.feature_names_in_)

print("Model expects features in this order:")
print(FEATURE_NAMES)

# Example input (values MUST match encoding used in training)
feature_values = {
    "Item_Identifier": 1023,
    "Item_Weight": 9.3,
    "Item_Fat_Content": 0,
    "Item_Visibility": 0.05,
    "Item_Type": 3,
    "Item_MRP": 249.8,
    "Outlet_Identifier": 17,
    "Outlet_Establishment_Year": 2005,
    "Outlet_Size": 1,
    "Outlet_Location_Type": 2,
    "Outlet_Type": 1
}

# Build DataFrame in EXACT order
X = pd.DataFrame([[feature_values[col] for col in FEATURE_NAMES]],
                 columns=FEATURE_NAMES)

prediction = model.predict(X)
print("✅ Prediction successful:", prediction)
