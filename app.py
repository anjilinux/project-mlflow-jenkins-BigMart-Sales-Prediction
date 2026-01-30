# app/app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = "model.pkl"

# Load model safely
try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except Exception as e:
    model = None
    model_loaded = False
    load_error = str(e)


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for Jenkins / Kubernetes / Load Balancers
    """
    status = {
        "status": "UP" if model_loaded else "DOWN",
        "model_loaded": model_loaded,
        "model_path": MODEL_PATH
    }

    if not model_loaded:
        status["error"] = load_error

    return jsonify(status), 200 if model_loaded else 500


@app.route("/predict", methods=["POST"])
def predict():
    if not model_loaded:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.json.get("features")

    if data is None:
        return jsonify({"error": "Missing 'features' in request"}), 400

    data = np.array(data).reshape(1, -1)
    prediction = model.predict(data)

    return jsonify({
        "sales_prediction": float(prediction[0])
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
