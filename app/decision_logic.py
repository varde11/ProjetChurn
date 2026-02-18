from schema import ClientOut

def recommend_actions(client: ClientOut, label: str) -> list[str]:
    actions = []

    contract = client.contract.lower()
    tenure = float(client.tenure)
    monthly = float(client.monthlycharges)
    techsupport = client.techsupport.lower()
    onlinesecurity = client.onlinesecurity.lower()
    internet = client.internetservice.lower()
    payment = client.paymentmethod.lower()

    if label == "no_churn":
        actions.append("Risque sous le seuil défini : Surveillance mensuelle.")
        return actions

  
    if "month" in contract:
        actions.append("Proposer une migration vers un contrat One year / Two year (réduction ciblée).")
    if tenure < 6:
        actions.append("Appel régulier pour faire le point sur sa satisfaction.")
    if monthly > 80:
        actions.append("Offre promotionnelle courte (2-3 mois) plutôt qu'une remise permanente.")
    if internet == "fiber optic":
        actions.append("Vérifier la qualité de la fibre + support proactif.")
    if techsupport in ["no", "no internet service"]:
        actions.append("Offrir Tech Support 1-2 mois (pack) pour réduire la friction.")
    if onlinesecurity in ["no", "no internet service"]:
        actions.append("Proposer Online Security si pertinent.")
    if "electronic" in payment:
        actions.append("Proposer un paiement plus stable (auto-pay) + petit incentive.")

    if not actions:
        actions.append("Action générique : contact client + offre de rétention ciblée.")
    return actions


def compute_roi(score: float, threshold: float, churn_cost: float, retention_cost: float, success_rate: float) -> dict:
    """
    ROI simple :
    - On traite seulement si score >= threshold
    - Si on traite : coût = retention_cost
    - Gain espéré = score * churn_cost * success_rate
    """
    treat = score >= threshold
    if not treat:
        return {
            "treat": False,
            "expected_saved": 0.0,
            "expected_cost": 0.0,
            "expected_roi": 0.0,
        }

    expected_saved = score * churn_cost * success_rate
    expected_cost = retention_cost
    expected_roi = expected_saved - expected_cost

    return {
        "treat": True,
        "expected_saved": float(expected_saved),
        "expected_cost": float(expected_cost),
        "expected_roi": float(expected_roi),
    }
