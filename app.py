# app/app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = np.array(request.json["features"]).reshape(1, -1)
    prediction = model.predict(data)
    return jsonify({"sales_prediction": prediction[0]})

if __name__ == "__main__":
    app.run(port=5001)
