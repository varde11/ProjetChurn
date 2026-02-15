from logic import load_artifacts,predict_churn,predict_proba_batch
from fastapi import FastAPI,HTTPException,Depends,Query
from db import get_db, sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import asc
from schema import PredictRequest,ClientOut,EnumOption,EnumChurn,ClientIn,DecisionOut,DecisionIn,SimulationIn,SimulationOut
from table_structure import Client,Prediction
from table_structure import Base
from db import engine
from decision_logic import recommend_actions,compute_roi
import pandas as pd
from datetime import datetime
from fill_db import seed_clients_if_empty
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("préparation des ressources!")
    Base.metadata.create_all(bind=engine)
    load_artifacts()

    # Depends() isn't resolved for the lifespan function, create a session explicitly
    db = sessionLocal()
    try:
        seed_clients_if_empty(db)
    finally:
        db.close()

    print("préparation terminée")
    yield
    print("fermeture de l'application, merci de l'avoir essayer, a+")


app = FastAPI(title="Churn Prediction API ",lifespan=lifespan)



@app.get("/Healthycheck")
def get_healthy():
    return {"healthy":"okay"}

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

    
    client_obj = db.query(Client).filter(Client.id_client == id_client).first()
    if not client_obj:
        raise HTTPException(status_code=404, detail=f"Client introuvable pour id_client={id_client}")

    client_schema = ClientOut.model_validate(client_obj)

    
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
    deleted = [DecisionOut.model_validate(pred).model_dump() for pred in predictions]

    db.query(Prediction).filter(Prediction.id_client==id_client).delete(synchronize_session=False)
    db.commit()

    return deleted


@app.delete("/deletePredictionByIdPrediction",response_model=DecisionOut)
def delete_predictions_by_idprediction(id_prediction:int, db:Session=Depends(get_db)):
    
    prediction = db.query(Prediction).filter(Prediction.id_prediction==id_prediction).first()
    if not prediction:
        raise HTTPException(status_code=404, detail=f"Aucune prédiction trouvée avec l'id {id_prediction}")

    deleted = DecisionOut.model_validate(prediction).model_dump()
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





import numpy as np
@app.post("/Simulation", response_model=SimulationOut)
def simulate_roi(payload: SimulationIn, db: Session = Depends(get_db)):
    # 1) charger tous les clients
    clients = db.query(Client).filter(Client.id_client%5==0).order_by(asc(Client.id_client)).all()
    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client en base.")

    client_rows = [ClientOut.model_validate(c).model_dump() for c in clients]
    df = pd.DataFrame(client_rows)

    # 2) prédire proba churn pour tous (vectorisé)
    probs = predict_proba_batch(df, payload.option)

    churn_cost = float(payload.churn_cost)
    retention_cost = float(payload.retention_cost)
    success_rate = float(payload.success_rate)

    # helpers
    def compute_for_threshold(th: float):
        treated_mask = probs >= th
        treated = int(treated_mask.sum())
        n = len(probs)

        expected_saved = float((probs[treated_mask] * churn_cost * success_rate).sum())
        expected_cost = float(retention_cost * treated)
        expected_roi = expected_saved - expected_cost

        return {
            "threshold": float(th),
            "treated_clients": treated,
            "treat_rate": float(treated / n),
            "expected_saved": expected_saved,
            "expected_cost": expected_cost,
            "expected_roi": float(expected_roi),
        }

    n_clients = len(probs)

    
    curve = []
    if payload.strategy == "threshold":
        
        thresholds = payload.thresholds or [0.3, 0.5, 0.7] # si l'utilisateur a la flemme de donner les valeurs
    
        for th in thresholds:
            if th < 0 or th > 1:
                raise HTTPException(status_code=422, detail="Tous les thresholds doivent être entre 0 et 1.")
    
        curve = [compute_for_threshold(float(th)) for th in thresholds]
            
        main = max(curve, key=lambda x: x["expected_roi"])
        print("main:\n",main)

        treated_mask = probs >= float(main["threshold"])
        
           

    else:  
        top_percent = float(payload.top_percent or 0.0)
        if top_percent < 0 or top_percent > 100:
            raise HTTPException(status_code=422, detail="top_percent doit être entre 0 et 100.")

        k = int(round(n_clients * (top_percent / 100.0)))
        k = max(0, min(n_clients, k))

        # indices triés par proba décroissante
        order = probs.argsort()[::-1]
        treated_idx = order[:k]
        treated_mask = np.zeros(n_clients, dtype=bool)
        treated_mask[treated_idx] = True

        expected_saved = float((probs[treated_mask] * churn_cost * success_rate).sum())
        expected_cost = float(retention_cost * k)
        expected_roi = float(expected_saved - expected_cost)

        main = {
            "threshold": -1.0,  # non applicable
            "treated_clients": int(k),
            "treat_rate": float(k / n_clients),
            "expected_saved": expected_saved,
            "expected_cost": expected_cost,
            "expected_roi": expected_roi,
        }

    # 4) top clients (pour la démo)
    # on montre les 10 plus risqués (ou traités si stratégie top%)
    ids = [c.id_client for c in clients]
    order_all = probs.argsort()[::-1]
    topN = 10 if n_clients >= 10 else n_clients
    top_clients = []
    for idx in order_all[:topN]:
        p = float(probs[idx])
        saved = float(p * churn_cost * success_rate)
        cost = float(retention_cost if treated_mask[idx] else 0.0)
        top_clients.append({
            "id_client": int(ids[idx]),
            "churn_probability": p,
            "expected_saved": saved if treated_mask[idx] else 0.0,
            "expected_cost": cost,
            "expected_roi": float((saved if treated_mask[idx] else 0.0) - cost),
        })

    return {
        "option": payload.option,
        "strategy": payload.strategy,
        "n_clients": n_clients,
        "treated_clients": int(main["treated_clients"]),
        "treat_rate": float(main["treat_rate"]),
        "optimal_threshold" : float(main["threshold"]),
        "churn_cost": churn_cost,
        "retention_cost": retention_cost,
        "success_rate": success_rate,
        "expected_saved": float(main["expected_saved"]),
        "expected_cost": float(main["expected_cost"]),
        "expected_roi": float(main["expected_roi"]),
        "curve": curve,
        "top_clients": top_clients
    }










