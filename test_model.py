# tests/test_model.py
import joblib
import numpy as np

def test_model_prediction():
    model = joblib.load("model.pkl")
    sample = np.random.rand(1, model.n_features_in_)
    pred = model.predict(sample)
    assert pred.shape == (1,)
