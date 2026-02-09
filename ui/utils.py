from typing import Dict, Any

def recommend_actions(client: Dict[str, Any], churn_prob: float, threshold: float) -> list[str]:
    """
    Règles simples (explicables) : le but c'est 'passer à l'action'.
    Tu pourras les raffiner plus tard (ou baser sur SHAP).
    """
    actions = []
    will_churn = churn_prob >= threshold

    contract = str(client.get("contract", "")).lower()
    tenure = float(client.get("tenure", 0) or 0)
    monthly = float(client.get("monthlycharges", 0) or 0)
    techsupport = str(client.get("techsupport", "")).lower()
    onlinesecurity = str(client.get("onlinesecurity", "")).lower()
    internet = str(client.get("internetservice", "")).lower()
    payment = str(client.get("paymentmethod", "")).lower()

    if not will_churn:
        actions.append("✅ Risque sous le seuil : conserver le client sans incentive coûteux, surveiller mensuellement.")
        return actions

    # Actions "très business", faciles à justifier
    if "month" in contract:
        actions.append("📌 Proposer une migration vers un contrat 1 an / 2 ans (réduction ou bonus) : faible coût, gros impact.")
    if tenure < 6:
        actions.append("📞 Appel onboarding / satisfaction (nouveaux clients) + check qualité du service.")
    if monthly > 80:
        actions.append("💸 Proposer un bundle / remise ciblée sur 2-3 mois plutôt qu’une remise permanente.")
    if internet == "fiber optic":
        actions.append("🛠️ Vérifier incidents/qualité fibre (zone) + proposer support proactif.")
    if techsupport in ["no", "no internet service"]:
        actions.append("🎁 Offrir Tech Support pendant 1-2 mois (ou pack) pour réduire la friction.")
    if onlinesecurity in ["no", "no internet service"]:
        actions.append("🔐 Proposer Online Security (pack) si pertinent, souvent corrélé à meilleure rétention.")
    if "electronic" in payment:
        actions.append("💳 Proposer un moyen de paiement plus stable (auto-pay) si possible + petit incentive.")

    if not actions:
        actions.append("📌 Action générique : contact client + offre de rétention ciblée.")
    return actions

def simple_roi(
    churn_prob: float,
    threshold: float,
    churn_cost: float,
    retention_cost: float,
    retention_success_rate: float,
) -> dict:
    """
    Mini modèle ROI :
    - On traite (on fait une action de rétention) seulement si prob >= threshold.
    - Si on traite : on paye retention_cost.
    - La rétention 'réussit' avec un taux retention_success_rate, ce qui évite churn_cost * churn_prob.
    """
    will_treat = churn_prob >= threshold

    if not will_treat:
        return {
            "will_treat": False,
            "expected_roi": 0.0,
            "expected_saved": 0.0,
            "expected_cost": 0.0,
        }

    expected_saved = churn_prob * churn_cost * retention_success_rate
    expected_cost = retention_cost
    expected_roi = expected_saved - expected_cost

    return {
        "will_treat": True,
        "expected_roi": float(expected_roi),
        "expected_saved": float(expected_saved),
        "expected_cost": float(expected_cost),
    }
