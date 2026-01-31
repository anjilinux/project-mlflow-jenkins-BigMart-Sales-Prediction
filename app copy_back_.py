from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "model.pkl"

# Load model ONCE at startup
model = joblib.load(MODEL_PATH)

# MUST match training schema EXACTLY
FEATURE_NAMES = [
    "Item_Identifier",
    "Item_Weight",
    "Item_Fat_Content",
    "Item_Visibility",
    "Item_Type",
    "Item_MRP",
    "Outlet_Identifier",
    "Outlet_Establishment_Year",
    "Outlet_Size",
    "Outlet_Location_Type",
    "Outlet_Type"
]

print("✅ Model loaded successfully")
print("Model expects features:", FEATURE_NAMES)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if "features" not in data:
            return jsonify({"error": "Missing 'features' key"}), 400

        features = data["features"]

        if len(features) != len(FEATURE_NAMES):
            return jsonify({
                "error": f"Expected {len(FEATURE_NAMES)} features, got {len(features)}"
            }), 400

        X = pd.DataFrame([features], columns=FEATURE_NAMES)
        prediction = model.predict(X)

        return jsonify({"prediction": float(prediction[0])}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
