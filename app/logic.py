import joblib        
import pandas as pd
import numpy as np
from typing import Dict, Any
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PRECISION_PATH = os.path.join(BASE_DIR,"model","best_model_precision.pkl")
MODEL_RECALL_PATH = os.path.join(BASE_DIR,"model","best_model_recall.pkl")
SCALER_PATH = os.path.join(BASE_DIR,"preprocessing","scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR,"preprocessing","encoder.pkl")

_model_precision = None
_model_recall=None
_scaler = None
_encoder = None



def load_artifacts():
  
    global _model_precision,_model_recall, _scaler, _encoder
    if _model_precision is None:
        _model_precision = joblib.load(MODEL_PRECISION_PATH)
    if _model_recall is None:
        _model_recall=joblib.load(MODEL_RECALL_PATH)
    if _scaler is None:
        _scaler = joblib.load(SCALER_PATH)
    if _encoder is None:
        _encoder = joblib.load(ENCODER_PATH)
    
    #print(_model_precision,_model_recall,_scaler,_encoder)



def build_dataframe_from_json(input_user: Dict[str, Any]) -> pd.DataFrame:

    df = pd.DataFrame([input_user])
    return df


def preprocess(df: pd.DataFrame) -> np.ndarray:
    
    
    bin_cols = ["seniorcitizen","partner","dependents","phoneservice","paperlessbilling"]
    for c in bin_cols:
        if c in df.columns:
            df[c] = df[c].map({ "Yes": 1, "No": 0, 1:1, 0:0 }).fillna(df[c])

    
    cat_cols = ['multiplelines', 'internetservice', 'onlinesecurity',
      'onlinebackup', 'deviceprotection', 'techsupport', 
      'streamingtv', 'streamingmovies', 'contract', 'paymentmethod']
    
    cat_part = _encoder.transform(df[cat_cols]) if hasattr(_encoder, "transform") else df[cat_cols].values

    
    num_cols = ["tenure","monthlycharges","totalcharges"]
    num_part = _scaler.transform(df[num_cols])

    # on utilie hstack pour stacker les 3 tableaux de valeurs
    X = np.hstack([df[bin_cols].values,cat_part,num_part]) 
    return X

def predict_churn(df:pd.DataFrame,option: str,threshold: float ) -> Dict[str, Any]:
   
    load_artifacts()
    X = preprocess(df)

    if threshold < 0 or threshold > 1 :
        return {"erreur":" La valeur de threshold n'est pas respectée."}

    if option =='precision':
        probs = _model_precision.predict_proba(X)[:, 1]
    elif option =='recall':
        probs = _model_recall.predict_proba(X)[:, 1]
    else:
        raise ValueError("option must be 'precision' or 'recall'")

    prob = float(probs[0])
    label = "churn" if prob >= threshold else "no_churn"
    return {"churn_probability": prob, "prediction": label}


def predict_proba_batch(df: pd.DataFrame, option: str) -> np.ndarray:
    load_artifacts()
    X = preprocess(df)

    if option == "precision":
        probs = _model_precision.predict_proba(X)[:, 1]
    elif option == "recall":
        probs = _model_recall.predict_proba(X)[:, 1]
    else:
        raise ValueError("option must be 'precision' or 'recall'")

    return probs
