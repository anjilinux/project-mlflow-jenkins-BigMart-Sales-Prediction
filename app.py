from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "model.pkl"

# Load model ONCE
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

FEATURE_NAMES = [
    "Item_Weight", "Item_Fat_Content", "Item_Visibility",
    "Item_Type", "Item_MRP", "Outlet_Establishment_Year",
    "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = data["features"]

        if len(features) != len(FEATURE_NAMES):
            return jsonify({"error": "Invalid feature length"}), 400

        X = pd.DataFrame([features], columns=FEATURE_NAMES)
        prediction = model.predict(X)

        return jsonify({"prediction": float(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
