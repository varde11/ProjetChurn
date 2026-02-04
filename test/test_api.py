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
