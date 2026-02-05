import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app 
from db import get_db
from table_structure import Client, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./dummy.db" 


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Nécessaire pour SQLite
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def setup_database():
    """Cette fonction réinitialise la base et crée un client test"""
   
    Base.metadata.create_all(bind=engine)


    db = TestingSessionLocal()
    fake_client = Client(
        seniorcitizen =  "Yes",
        partner = "Yes",
        dependents = "Yes",
        phoneservice = "Yes",
        paperlessbilling = "Yes",
        multiplelines = "Yes",
        internetservice = "DSL",
        onlinesecurity = "Yes",
        onlinebackup = "Yes",
        deviceprotection = "Yes",
        techsupport = "Yes",
        streamingtv = "Yes",
        streamingmovies = "Yes",
        contract = "Two year",
        paymentmethod = "Credit card (automatic)",

        monthlycharges = 1000,
        tenure = 2,
        totalcharges = 1002
    )
    
    db.add(fake_client)
    db.commit()
    db.close()



def test_get_client():
    setup_database()

    response_get = client.get("/GetClientByIdClient?id_client=1")
    assert response_get.status_code == 200
    assert response_get.json()["id_client"] == 1
    assert response_get.json()["monthlycharges"] == 1000
    assert response_get.json()["tenure"] == 2
    assert response_get.json()["totalcharges"] == 1002


def test_predict():
    

    for option in ["precision", "recall"]:
        reponse_post = client.post(f"/AddPrediction/{option}/1")
        assert reponse_post.status_code ==200

        data=reponse_post.json()
        assert 'label' in data 
        assert 'score' in data
        assert 'time_stamp' in data
        assert 'option_model' in data
        assert data['id_client'] == 1 

        
    for id in range(1,3):
        reponse_get_by_idPred = client.get(f"/getPredictionByIdPrediction?id_prediction={id}")

        assert reponse_get_by_idPred.status_code ==200

        assert reponse_get_by_idPred.json()['id_prediction'] == id
        assert reponse_get_by_idPred.json()['id_client'] == 1 # au début on a fait f"/Prediction/{option}/1 , on a 1 client d'id 1.

    reponse_get_by_idClient = client.get("/getPredictionByIdClient?id_client=1")

    assert reponse_get_by_idClient.status_code == 200
    assert len(reponse_get_by_idClient.json()) == 2 # On est supposé avoir autant de prédiction que d'option, ie:2
    

def test_delete():

    reponse_delete_by_idPred = client.delete("/deletePredictionByIdPrediction?id_prediction=1")

    assert reponse_delete_by_idPred.status_code == 200
    assert reponse_delete_by_idPred.json()['id_prediction'] == 1

    reponse_delete_by_idClient = client.delete("/deletePredictionByIdClient?id_client=1")

    assert reponse_delete_by_idClient.status_code == 200
    assert len(reponse_delete_by_idClient.json()) == 1

    reponse_get_prediction_by_idClient = client.get("/getPredictionByIdClient?id_client=1")
    assert reponse_get_prediction_by_idClient.status_code == 200 #client existe mais n'a fait aucune prédiction

    reponse_get_prediction_by_idprediction = client.get("/getPredictionByIdPrediction?id_prediction=1")
    reponse_get_prediction_by_idprediction.status_code == 404

    reponse_delete_client = client.delete("/DeleteClientByIdClient?id_client=1")
    assert reponse_delete_client.status_code == 200
    
    reponse_get_client_by_idClient = client.get("/GetClientByIdClient?id_client=1")
    assert reponse_get_client_by_idClient.status_code == 404


def test_addclient():

    client_fake = {
        "seniorcitizen" : "Yes",
        "partner" : "Yes",
        "dependents" :"Yes",
        "phoneservice" : "Yes",
        "paperlessbilling" : "Yes",
        "multiplelines" : "Yes",
        "internetservice" : "DSL",
        "onlinesecurity" : "Yes",
        "onlinebackup" : "Yes",
        "deviceprotection" : "Yes",
        "techsupport" : "Yes",
        "streamingtv" : "Yes",
        "streamingmovies" :"Yes",
        "contract" : "Two year",
        "paymentmethod" : "Credit card (automatic)",
        "monthlycharges" : 10000,
        "tenure" : 1,
        "totalcharges" : 1002
    }

    reponse_add = client.post("/AddClient",json=client_fake)
    assert reponse_add.status_code == 200
    
    assert reponse_add.json()["monthlycharges"] == 10000
    assert reponse_add.json()["tenure"] == 1
    assert reponse_add.json()["totalcharges"] == 1002
    option = "precision"
    reponse_post = client.post(f"/AddPrediction/{option}/1")
    assert reponse_post.status_code == 200
    
    assert 'label' in reponse_post.json()
    assert 'score' in reponse_post.json()
    assert 'time_stamp' in reponse_post.json()
    assert 'option_model' in reponse_post.json()
    assert reponse_post.json()['id_client'] == 1
    assert reponse_post.json()['id_prediction'] == 1

    get_client = client.get(f"/GetAllClientByLabel?label={reponse_post.json()['label']}")
    assert get_client.status_code == 200
    assert len(get_client.json()) == 1

    reponse_delete_client = client.delete("/DeleteClientByIdClient?id_client=1")
    assert reponse_delete_client.status_code == 200

    response_get_client = client.get("/GetClientByIdClient/1")
    assert response_get_client.status_code == 404

    reponse_get_by_idPred = client.get("/getPredictionByIdPrediction/1")
    assert reponse_get_by_idPred.status_code == 404









    


    