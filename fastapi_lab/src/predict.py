import joblib
from functools import lru_cache
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "iris_model.pkl"

@lru_cache(maxsize=1)
def get_model():
    # Loads once, then cached forever
    return joblib.load(MODEL_PATH)

def predict_data(X):
    model = get_model()
    return model.predict(X)

def predict_proba(X):
    model = get_model()
    return model.predict_proba(X)