from logic import load_artifacts,predict_churn
from fastapi import FastAPI,HTTPException,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import PredictRequest,ClientOut,EnumOption,EnumChurn,ClientIn
from table_structure import Client,Prediction
from table_structure import Base
from db import engine
import pandas as pd
from datetime import datetime

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("préparation des ressources!")
    Base.metadata.create_all(bind=engine)
    load_artifacts()
    print("préparation terminée")
    yield
    print("fermeture de l'application, merci de l'avoir essayer, a+")


app = FastAPI(title="Churn Prediction API ",lifespan=lifespan)


@app.get("/GetClientByIdClient",response_model=ClientOut)
def get_client_by_id(id_client:int, db:Session=Depends(get_db)):
    client_obj= db.query(Client).filter(Client.id_client==id_client).first()
    if not client_obj:
        raise HTTPException(status_code=404, detail=f"Client  d'identifiant {id_client} introuvable")

    return client_obj

@app.get("/GetAllClientByLabel",response_model=list[ClientOut])
def get_all_client(label:EnumChurn,db:Session=Depends(get_db)):

    if label == "all":
        clients = db.query(Client).join(Prediction,Prediction.id_client == Client.id_client).distinct().all()
    else :
        clients = db.query(Client).join(Prediction,Prediction.id_client == Client.id_client).filter(Prediction.label == label).distinct().all()
    
    if not clients :
        []

    return clients


@app.get("/getPredictionByIdClient",response_model=list[PredictRequest])
def get_prediction_by_id_client(id_client:int,db:Session=Depends(get_db)):

    client = db.query(Client).filter(Client.id_client == id_client).first()
    if not client:
        raise HTTPException(status_code=404,detail=f"Le client d'identifiant {id_client} n'existe pas")

    prediction_obj= db.query(Prediction).filter(Prediction.id_client==id_client).all()
    if not prediction_obj:
        return []

    return prediction_obj

#####













