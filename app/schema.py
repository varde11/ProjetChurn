from pydantic import BaseModel, Field
from typing import Literal, List,Optional
from datetime import datetime
from enum import Enum

class PredictRequest(BaseModel):
    id_prediction: int = Field(ge=1)
    id_client: int = Field(ge=1)
    option_model: Literal["precision", "recall"]
    score: float = Field(ge=0)
    threshold: float = Field(ge=0, le=1)
    label: Literal["churn", "no_churn"]
    time_stamp: datetime
    model_config = {"from_attributes": True}

class ClientOut(BaseModel):
    id_client: int = Field(ge=1)
    seniorcitizen: Literal["Yes", "No", "1", "0"]
    partner: Literal["Yes", "No", "1", "0"]
    dependents: Literal["Yes", "No", "1", "0"]
    phoneservice: Literal["Yes", "No", "1", "0"]
    paperlessbilling: Literal["Yes", "No", "1", "0"]
    multiplelines: Literal["No phone service", "Yes", "No"]
    internetservice: Literal["DSL", "Fiber optic", "No"]
    onlinesecurity: Literal["No internet service", "Yes", "No"]
    onlinebackup: Literal["No internet service", "Yes", "No"]
    deviceprotection: Literal["No internet service", "Yes", "No"]
    techsupport: Literal["No internet service", "Yes", "No"]
    streamingtv: Literal["No internet service", "Yes", "No"]
    streamingmovies: Literal["No internet service", "Yes", "No"]

    contract: Literal["Month-to-month", "One year", "Two year"]
    paymentmethod: Literal["Credit card (automatic)", "Mailed check", "Bank transfer (automatic)", "Electronic check"]

    monthlycharges: float = Field(ge=0)
    tenure: int = Field(ge=0)
    totalcharges: float = Field(ge=0)
    # pour accepter les objets SQLAlchemy
    model_config = {"from_attributes": True}

class ClientIn(BaseModel):
    seniorcitizen: Literal["Yes", "No", "1", "0"]
    partner: Literal["Yes", "No", "1", "0"]
    dependents: Literal["Yes", "No", "1", "0"]
    tenure: int = Field(ge=0)
    phoneservice: Literal["Yes", "No", "1", "0"]
    multiplelines: Literal["No phone service", "Yes", "No"]
    internetservice: Literal["DSL", "Fiber optic", "No"]
    onlinesecurity: Literal["No internet service", "Yes", "No"]
    onlinebackup: Literal["No internet service", "Yes", "No"]
    deviceprotection: Literal["No internet service", "Yes", "No"]
    techsupport: Literal["No internet service", "Yes", "No"]
    streamingtv: Literal["No internet service", "Yes", "No"]
    streamingmovies: Literal["No internet service", "Yes", "No"]
    contract: Literal["Month-to-month", "One year", "Two year"]
    paperlessbilling: Literal["Yes", "No", "1", "0"]
    paymentmethod: Literal["Credit card (automatic)", "Mailed check", "Bank transfer (automatic)", "Electronic check"]
    monthlycharges: float = Field(ge=0)
    totalcharges: float = Field(ge=0)


class EnumOption(str, Enum):
    recall = "recall"
    precision = "precision"

class EnumChurn(str, Enum):
    all = "all"
    churn = "churn"
    no_churn = "no_churn"
    



class RoiOut(BaseModel):
    churn_cost: float = Field(ge=0)
    retention_cost: float = Field(ge=0)
    success_rate: float = Field(ge=0, le=1)
    expected_saved: float
    expected_cost: float
    expected_roi: float
    treat: bool

class DecisionOut(BaseModel):
    id_prediction: int = Field(ge=1)
    id_client: int = Field(ge=1)
    option_model: EnumOption
    score: float = Field(ge=0)
    threshold: float = Field(ge=0, le=1)
    label: Literal["churn", "no_churn"]
    actions: List[str]
    roi: RoiOut
    time_stamp: datetime
    model_config = {"from_attributes": True}

class DecisionIn(BaseModel):
    id_client: int = Field(ge=1)
    option: EnumOption
    threshold: float = Field(ge=0, le=1)
    churn_cost: float = Field(ge=0, default=500.0)
    retention_cost: float = Field(ge=0, default=50.0)
    success_rate: float = Field(ge=0, le=1, default=0.30)




class SimulationIn(BaseModel):
    option: Literal["precision", "recall"]

    strategy: Literal["threshold", "top_percent"] = "threshold"
    threshold: Optional[float] = Field(default=0.5, ge=0, le=1)
    top_percent: Optional[float] = Field(default=10.0, ge=0, le=100)

    churn_cost: float = Field(default=500.0, ge=0)
    retention_cost: float = Field(default=50.0, ge=0)
    success_rate: float = Field(default=0.30, ge=0, le=1)

    # pour comparer plusieurs seuils en une requête
    thresholds: Optional[List[float]] = None

class SimulationPointOut(BaseModel):
    threshold: float
    treated_clients: int
    treat_rate: float
    expected_saved: float
    expected_cost: float
    expected_roi: float

class TopClientOut(BaseModel):
    id_client: int
    churn_probability: float
    expected_saved: float
    expected_cost: float
    expected_roi: float

class SimulationOut(BaseModel):
    option: Literal["precision", "recall"]
    strategy: Literal["threshold", "top_percent"]

    n_clients: int
    treated_clients: int
    treat_rate: float
    optimal_threshold:float=Field(ge=0,le=1)

    churn_cost: float
    retention_cost: float
    success_rate: float

    expected_saved: float
    expected_cost: float
    expected_roi: float

    curve: List[SimulationPointOut] = []
    top_clients: List[TopClientOut] = []
