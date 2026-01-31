from flask import Flask, request, jsonify
import pandas as pd
import time
import os
import joblib

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# =========================
# Prometheus Metrics
# =========================
REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total number of prediction requests"
)

PREDICTION_TIME = Histogram(
    "prediction_latency_seconds",
    "Time spent processing prediction"
)

# =========================
# Load Model ONCE (joblib)
# =========================
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ model.pkl not found. Train model before starting API")

model = joblib.load(MODEL_PATH)

FEATURE_NAMES = [
    "Item_Identifier", "Item_Weight", "Item_Fat_Content",
    "Item_Visibility", "Item_Type", "Item_MRP",
    "Outlet_Identifier", "Outlet_Establishment_Year",
    "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
]

# =========================
# Health Check
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

# =========================
# Prediction Endpoint
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    REQUEST_COUNT.inc()
    start_time = time.time()

    try:
        data = request.get_json()
        features = data["features"]

        if len(features) != len(FEATURE_NAMES):
            return jsonify({
                "error": f"Expected {len(FEATURE_NAMES)} features, got {len(features)}"
            }), 400

        X = pd.DataFrame([features], columns=FEATURE_NAMES)
        prediction = model.predict(X)

        return jsonify({"prediction": float(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        PREDICTION_TIME.observe(time.time() - start_time)

# =========================
# Prometheus Metrics
# =========================
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
