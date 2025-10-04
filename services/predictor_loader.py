import os
import joblib

BASE_PATH = "ml_models"

def load_model(stage: int):
    path = os.path.join(BASE_PATH, f"prediction{stage}", "model.pkl")
    return joblib.load(path)

def load_columns(stage: int):
    path = os.path.join(BASE_PATH, f"prediction{stage}", "columns.pkl")
    return joblib.load(path)

def load_encoder(stage: int):
    path = os.path.join(BASE_PATH, f"prediction{stage}", "encoder.pkl")
    return joblib.load(path)

