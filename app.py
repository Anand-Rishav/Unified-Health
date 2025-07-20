from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd, joblib
from pathlib import Path

# Auto-load latest model
MODEL = joblib.load(sorted(Path('models').glob('best_pipe_*.joblib'))[-1])
app = FastAPI(title='Blood Recommendation API')

# Corrected the input features to match the training data
class InputFeatures(BaseModel):
    Recency: int
    Frequency: int
    Monetary: int
    Time: int

@app.post('/predict')
def predict(p:InputFeatures):
    df  = pd.DataFrame([p.dict()])
    prob = MODEL.predict_proba(df)[0,1]
    pred = MODEL.predict(df)[0]
    return {'prediction': int(pred), 'probability': float(prob)}
