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
        return []

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



@app.get("/getPredictionByIdPrediction",response_model=PredictRequest)
def get_prediction_by_id_prediction(id_prediction:int,db:Session=Depends(get_db)):
    prediction_obj= db.query(Prediction).filter(Prediction.id_prediction==id_prediction).first()
    if not prediction_obj:
        raise HTTPException(status_code=404, detail=f"Aucune prédiction d'identifiant {id_prediction} n'a pu être trouvée")

    return prediction_obj



@app.post("/AddPrediction/{id_client}/{option}",response_model=PredictRequest)
def churn_prediction(id_client:int,option:EnumOption, db:Session=Depends(get_db)):

    client_obj= db.query(Client).filter(Client.id_client==id_client).first()
    if not client_obj:
        raise HTTPException(status_code=404, detail=f"Client d'identifiant {id_client} introuvable")
    
    client_schema=ClientOut.model_validate(client_obj)
    client_dico = client_schema.model_dump()
    client_df = pd.DataFrame([client_dico])

    predict = predict_churn(client_df,option)
    time_stamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prediction =Prediction(
        id_client = id_client,
        option_model = option,
        score = round (predict["churn_probability"],2),
        label = predict["prediction"],
        time_stamp = datetime.now().strptime(time_stamp_str,"%Y-%m-%d %H:%M:%S")
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction

@app.post("/AddClient",response_model=ClientOut)
def add_client(client:ClientIn,db:Session=Depends(get_db)):
    new_client = Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@app.delete("/deletePredictionByIdClient",response_model=list[PredictRequest])
def delete_predictions_by_idclient(id_client:int, db:Session=Depends(get_db)):
    client = db.query(Client).filter(Client.id_client==id_client).first()
    if not client :
        raise HTTPException(status_code=404,detail=f"Le client d'identifiant {id_client} n'existe pas.")
    
    predictions = db.query(Prediction).filter(Prediction.id_client==id_client).all()
    deleted = [PredictRequest.model_validate(pred).model_dump() for pred in predictions]

    db.query(Prediction).filter(Prediction.id_client==id_client).delete(synchronize_session=False)
    db.commit()

    return deleted


@app.delete("/deletePredictionByIdPrediction",response_model=PredictRequest)
def delete_predictions_by_idprediction(id_prediction:int, db:Session=Depends(get_db)):
    
    prediction = db.query(Prediction).filter(Prediction.id_prediction==id_prediction).first()
    if not prediction:
        raise HTTPException(status_code=404, detail=f"Aucune prédiction trouvée avec l'id {id_prediction}")

    deleted = PredictRequest.model_validate(prediction).model_dump()
    db.query(Prediction).filter(Prediction.id_prediction==id_prediction).delete(synchronize_session=False)
    db.commit()

    return deleted


@app.delete("/DeleteClientByIdClient",response_model=ClientOut,
            description="Supprimer un client entrainera la suppression de toutes ses prédictions,veuillez les sauvegarder avant.")
def delete_client_by_idclient(id_client:int,db:Session=Depends(get_db)):

    delete_predictions_by_idclient(id_client=id_client,db=db)

    client = db.query(Client).filter(Client.id_client == id_client).first()

    deleted = ClientOut.model_validate(client).model_dump()
    db.query(Client).filter(Client.id_client == id_client).delete(synchronize_session=False)
    db.commit()

    return deleted














