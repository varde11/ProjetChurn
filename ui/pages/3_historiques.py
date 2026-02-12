import streamlit as st
import pandas as pd
from api_client import get_client_by_id, get_predictions_by_client, ApiError

st.title("📚 Historique & Décisions")

# ======================
# Sélection du client
# ======================
id_client = st.number_input("id_client", min_value=1, step=1, value=1)

try:
    client = get_client_by_id(int(id_client))
except ApiError as e:
    st.error(str(e))
    st.stop()

st.subheader("Client")
st.dataframe(pd.DataFrame([client]), width="stretch", hide_index=True)

# ======================
# Historique
# ======================
try:
    preds = get_predictions_by_client(int(id_client))
except ApiError as e:
    st.error(str(e))
    st.stop()

st.subheader("Historique des prédictions")

if not preds:
    st.info("Aucune prédiction enregistrée pour ce client.")
    st.stop()

df = pd.DataFrame(preds)

# Colonnes utiles pour lecture rapide
display_cols = [
    "id_prediction",
    "option_model",
    "score",
    "threshold",
    "label",
    "time_stamp",
]

st.dataframe(df[display_cols], width="stretch", hide_index=True)

# ======================
# Sélection d'une prédiction
# ======================
st.divider()
st.subheader("Détail d'une décision")

id_prediction = st.selectbox(
    "Choisir une id_prediction",
    options=df["id_prediction"].tolist(),
)

pred = df[df["id_prediction"] == id_prediction].iloc[0].to_dict()

# ======================
# Résumé décision
# ======================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Score churn", f"{float(pred['score']):.2f}")
c2.metric("Threshold", f"{float(pred['threshold']):.2f}")
c3.metric("Label", pred["label"])
c4.metric("Modèle", pred["option_model"])

st.caption(f"Timestamp : {pred['time_stamp']}")

# ======================
# Actions
# ======================
st.subheader("Recommandations d'action")

actions = pred.get("actions", [])
if actions:
    for a in actions:
        st.write(f"- {a}")
else:
    st.info("Aucune action enregistrée.")

# ======================
# ROI
# ======================
st.subheader("Analyse ROI")

roi = pred.get("roi", {})

if roi :
    cc1, cc2, cc3, cc4 = st.columns(4)
    cc1.metric("Gain attendu", f"{roi.get('expected_saved', 0):.2f}")
    cc2.metric("Coût action", f"{roi.get('expected_cost', 0):.2f}")
    cc3.metric("ROI attendu", f"{roi.get('expected_roi', 0):.2f}")
    cc4.metric("Treat", "Oui" if roi.get("treat") else "Non")

    st.divider()

    if roi.get("expected_roi", 0) > 0:
        st.success("Décision rentable — action recommandée")
    if roi["treat"] and roi.get("expected_roi")<=0:
        st.warning("Décision non rentable — action à reconsidérer")
else:
    st.info("ROI non disponible pour cette prédiction.")
