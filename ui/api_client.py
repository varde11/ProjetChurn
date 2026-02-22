import os
import requests
from typing import Any, Dict, List

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

class ApiError(RuntimeError):
    pass

def _handle(resp: requests.Response) -> Any:
    try:
        data = resp.json()
    except Exception:
        data = resp.text

    if resp.status_code >= 400:
        raise ApiError(f"API error {resp.status_code}: {data}")
    return data

def get_client_by_id(id_client: int) -> Dict[str, Any]:
    resp = requests.get(f"{API_URL}/GetClientByIdClient", params={"id_client": id_client}, timeout=20)
    return _handle(resp)

def get_clients_by_label(label: str) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_URL}/GetAllClientByLabel", params={"label": label}, timeout=30)
    return _handle(resp)

def get_predictions_by_client(id_client: int) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_URL}/getPredictionByIdClient", params={"id_client": id_client}, timeout=30)
    return _handle(resp)

def decision(
    id_client: int,
    option: str,
    threshold: float,
    churn_cost: float = 500.0,
    retention_cost: float = 50.0,
    success_rate: float = 0.30,
) -> Dict[str, Any]:

    payload = {
        "id_client": id_client,
        "option": option,
        "threshold": threshold,
        "churn_cost": churn_cost,
        "retention_cost": retention_cost,
        "success_rate": success_rate,
    }

    resp = requests.post(f"{API_URL}/Decision", json=payload, timeout=60)
    return _handle(resp)


def add_prediction(id_client: int, option: str, threshold: float) -> Dict[str, Any]:
    resp = requests.post(
        f"{API_URL}/AddPrediction/{id_client}/{option}",
        params={"threshold": threshold},
        timeout=30
    )
    return _handle(resp)


def simulate_roi(payload: Dict[str, Any]) -> Dict[str, Any]:
    resp = requests.post(f"{API_URL}/Simulation", json=payload, timeout=120)
    return _handle(resp)
