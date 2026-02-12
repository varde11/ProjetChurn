import streamlit as st
import pandas as pd
from api_client import get_client_by_id, get_predictions_by_client, decision, ApiError

st.title("🧾 Détail client & Décision (Prédiction + Actions + ROI)")

left, right = st.columns([1, 1])

with left:
    id_client = st.number_input("id_client", min_value=1, step=1, value=1)

    option = st.selectbox("Modèle", ["precision", "recall"], index=0)

    threshold = st.slider(
        "Seuil de décision (threshold)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
    )

    st.subheader("Hypothèses coût (ROI)")
    churn_cost = st.number_input("Coût churn", min_value=0.0, value=500.0, step=10.0)
    retention_cost = st.number_input("Coût rétention", min_value=0.0, value=50.0, step=5.0)
    success_rate = st.slider("Taux de succès rétention", 0.0, 1.0, 0.30, 0.05)

    run = st.button("Exécuter et enregistrer")

with right:
    try:
        client = get_client_by_id(int(id_client))
        st.subheader("Client")
        st.dataframe(pd.DataFrame([client]), width="stretch", hide_index=True)
    except ApiError as e:
        st.error(str(e))
        st.stop()

if run:
    try:
        res = decision(
            id_client=int(id_client),
            option=option,
            threshold=float(threshold),
            churn_cost=float(churn_cost),
            retention_cost=float(retention_cost),
            success_rate=float(success_rate),
        )

        st.success("Décision enregistrée ✅")

        # res est ton Prediction complet
        st.subheader("Résultat")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Probabilité churn", f"{float(res.get('score', 0.0)):.2f}")
        c2.metric("Label", str(res.get("label", "")))
        c3.metric("Modèle", str(res.get("option_model", "")))
        c4.metric("Seuil", f"{float(res.get('threshold', 0.0)):.2f}")

        st.caption(f"id_prediction: {res.get('id_prediction')} — time_stamp: {res.get('time_stamp')}")

        st.subheader("Recommandations d'action")
        actions = res.get("actions", [])
        if actions:
            for a in actions:
                st.write(f"- {a}")
        else:
            st.info("Aucune recommandation retournée.")

        st.subheader("ROI")
        roi = res.get("roi", {})
        if roi:
            cc1, cc2, cc3, cc4 = st.columns(4)
            cc1.metric("Gain attendu", f"{float(roi.get('expected_saved', 0.0)):.2f}")
            cc2.metric("Coût action", f"{float(roi.get('expected_cost', 0.0)):.2f}")
            cc3.metric("ROI attendu", f"{float(roi.get('expected_roi', 0.0)):.2f}")
            cc4.metric("Treat", "Oui" if roi.get("treat") else "Non")
        else:
            st.info("ROI non retourné.")

        st.divider()
        st.subheader("Historique des prédictions du client")
        hist = get_predictions_by_client(int(id_client))
        if hist:
            st.dataframe(pd.DataFrame(hist), width="stretch", hide_index=True)
        else:
            st.info("Aucune prédiction enregistrée pour ce client.")

    except ApiError as e:
        st.error(str(e))
