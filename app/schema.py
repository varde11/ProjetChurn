from pydantic import BaseModel,Field
from typing import Literal,Optional
from datetime import datetime
from enum import Enum

class PredictRequest(BaseModel):
    id_prediction : int =Field(ge=1)
    id_client : int = Field (ge=1)
    option_model : Literal["precision","recall"]
    score : float = Field (ge=0)
    label : Literal ["churn","no_churn"]
    time_stamp : datetime 
    model_config = {"from_attributes": True}

class ClientOut(BaseModel):
    id_client : int = Field(ge=1)
    seniorcitizen: Literal["Yes","No","1","0"]
    partner: Literal["Yes","No","1","0"]
    dependents: Literal["Yes","No","1","0"]
    phoneservice: Literal["Yes","No","1","0"]
    paperlessbilling: Literal["Yes","No","1","0"]
    multiplelines: Literal["No phone service","Yes","No"]
    internetservice: Literal["DSL","Fiber optic","No"]
    onlinesecurity: Literal["No internet service","Yes","No"]
    onlinebackup: Literal["No internet service","Yes","No"]
    deviceprotection: Literal["No internet service","Yes","No"]
    techsupport: Literal["No internet service","Yes","No"]
    streamingtv: Literal["No internet service","Yes","No"]
    streamingmovies: Literal["No internet service","Yes","No"]

    contract: Literal["Month-to-month","One year","Two year"]
    paymentmethod : Literal ["Credit card (automatic)","Mailed check","Bank transfer (automatic)","Electronic check"]

    monthlycharges: float =Field(ge=0)
    tenure: int = Field(ge=0)
    totalcharges: float =Field(ge=0)
    #  pour accepter les objets SQLAlchemy
    model_config = {"from_attributes": True}

class ClientIn(BaseModel):
    seniorcitizen: Literal["Yes","No","1","0"]
    partner: Literal["Yes","No","1","0"]
    dependents: Literal["Yes","No","1","0"]
    tenure: int = Field(ge=0)
    phoneservice: Literal["Yes","No","1","0"]
    multiplelines: Literal["No phone service","Yes","No"]
    internetservice: Literal["DSL","Fiber optic","No"]
    onlinesecurity: Literal["No internet service","Yes","No"]
    onlinebackup: Literal["No internet service","Yes","No"]
    deviceprotection: Literal["No internet service","Yes","No"]
    techsupport: Literal["No internet service","Yes","No"]
    streamingtv: Literal["No internet service","Yes","No"]
    streamingmovies: Literal["No internet service","Yes","No"]
    contract: Literal["Month-to-month","One year","Two year"]
    paperlessbilling: Literal["Yes","No","1","0"]
    paymentmethod : Literal ["Credit card (automatic)","Mailed check","Bank transfer (automatic)","Electronic check"]
    monthlycharges: float =Field(ge=0)
    totalcharges: float =Field(ge=0)


class EnumOption(str,Enum):
    recall = "recall"
    precision = "precision"

class EnumChurn(str,Enum):
    all = "all"
    churn = "churn"
    no_churn = "no_churn"
    
