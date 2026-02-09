from logic import load_artifacts,predict_churn
from fastapi import FastAPI,HTTPException,Depends,Query
from db import get_db
from sqlalchemy.orm import Session
from schema import PredictRequest,ClientOut,EnumOption,EnumChurn,ClientIn,DecisionOut,DecisionIn
from table_structure import Client,Prediction
from table_structure import Base
from db import engine
from decision_logic import recommend_actions,compute_roi
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


@app.get("/getPredictionByIdClient",response_model=list[DecisionOut])
def get_prediction_by_id_client(id_client:int,db:Session=Depends(get_db)):

    client = db.query(Client).filter(Client.id_client == id_client).first()
    if not client:
        raise HTTPException(status_code=404,detail=f"Le client d'identifiant {id_client} n'existe pas")

    prediction_obj= db.query(Prediction).filter(Prediction.id_client==id_client).all()
    if not prediction_obj:
        return []

    return prediction_obj



@app.get("/getPredictionByIdPrediction",response_model=DecisionOut)
def get_prediction_by_id_prediction(id_prediction:int,db:Session=Depends(get_db)):
    prediction_obj= db.query(Prediction).filter(Prediction.id_prediction==id_prediction).first()
    if not prediction_obj:
        raise HTTPException(status_code=404, detail=f"Aucune prédiction d'identifiant {id_prediction} n'a pu être trouvée")

    return prediction_obj



@app.post("/AddPrediction/{id_client}/{option}")
def churn_prediction(id_client:int,option:EnumOption,threshold:float, db:Session=Depends(get_db)):

    client_obj= db.query(Client).filter(Client.id_client==id_client).first()
    if not client_obj:
        raise HTTPException(status_code=404, detail=f"Client d'identifiant {id_client} introuvable")
    
    if threshold < 0 or threshold > 1:
        raise HTTPException(status_code=422,detail="Le seuil de décision (threshold) doit être compris entre 0 et 1.")
    
    client_schema=ClientOut.model_validate(client_obj)
    client_dico = client_schema.model_dump()
    client_df = pd.DataFrame([client_dico])

    predict = predict_churn(client_df,option,threshold)
    time_stamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    prediction = {
        "id_client":id_client,
        "option_model":option,
        "score":round (predict["churn_probability"],2),
        "threshold":threshold,
        "label":predict["prediction"],
        "time_stamp":datetime.now().strptime(time_stamp_str,"%Y-%m-%d %H:%M:%S")
    }

    # db.add(prediction)
    # db.commit()
    # db.refresh(prediction)

    return prediction



@app.post("/Decision", response_model=DecisionOut)
def decision_by_id_prediction(
    payload: DecisionIn,
    db: Session = Depends(get_db)
):
    """Centralise les petits paramètres dans `DecisionIn` (payload).

    Workflow :
    - appelle `churn_prediction` pour obtenir la prédiction
    - calcule les actions recommandées
    - calcule le ROI
    - stocke et retourne la prédiction
    """

    id_client = payload.id_client
    option = payload.option
    threshold = payload.threshold
    churn_cost = payload.churn_cost
    retention_cost = payload.retention_cost
    success_rate = payload.success_rate

    # Faire la prédiction
    churn_obj = churn_prediction(id_client=id_client, option=option, threshold=threshold, db=db)
    if not churn_obj:
        raise HTTPException(status_code=500, detail="La prédiction n'a pas pu être faite.")

    # Vérifier que le client existe
    client_obj = db.query(Client).filter(Client.id_client == id_client).first()
    if not client_obj:
        raise HTTPException(status_code=404, detail=f"Client introuvable pour id_client={id_client}")

    client_schema = ClientOut.model_validate(client_obj)

    # Recommander les actions et calculer le ROI
    actions = recommend_actions(client_schema, churn_obj["label"])
    roi_calc = compute_roi(
        score=float(churn_obj["score"]),
        threshold=float(churn_obj["threshold"]),
        churn_cost=float(churn_cost),
        retention_cost=float(retention_cost),
        success_rate=float(success_rate),
    )

    roi = {
        "churn_cost": float(churn_cost),
        "retention_cost": float(retention_cost),
        "success_rate": float(success_rate),
        **roi_calc,
    }

    prediction = Prediction(
        id_client=id_client,
        option_model=option,
        score=churn_obj["score"],
        threshold=threshold,
        label=churn_obj["label"],
        actions=actions,
        roi=roi,
        time_stamp=churn_obj["time_stamp"],
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


@app.delete("/deletePredictionByIdClient",response_model=list[DecisionOut])
def delete_predictions_by_idclient(id_client:int, db:Session=Depends(get_db)):
    client = db.query(Client).filter(Client.id_client==id_client).first()
    if not client :
        raise HTTPException(status_code=404,detail=f"Le client d'identifiant {id_client} n'existe pas.")
    
    predictions = db.query(Prediction).filter(Prediction.id_client==id_client).all()
    deleted = [PredictRequest.model_validate(pred).model_dump() for pred in predictions]

    db.query(Prediction).filter(Prediction.id_client==id_client).delete(synchronize_session=False)
    db.commit()

    return deleted


@app.delete("/deletePredictionByIdPrediction",response_model=DecisionOut)
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














