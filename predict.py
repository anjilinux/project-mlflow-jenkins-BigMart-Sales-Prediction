# src/predict.py
import joblib
import numpy as np

model = joblib.load("model.pkl")

sample = np.random.rand(1, model.n_features_in_)
prediction = model.predict(sample)

print("Prediction successful:", prediction)
