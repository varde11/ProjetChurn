from api_client import simulate_roi,ApiError
import streamlit as st
import pandas as pd


st.title("📊 Simulation ROI globale")

left, right = st.columns([1, 1])

with left:
    option = st.selectbox("Modèle", ["precision", "recall"], index=0)

    strategy = st.selectbox("Stratégie", ["threshold", "top_percent"], index=0)

    st.subheader("Coûts / hypothèses")
    churn_cost = st.number_input("Coût churn", min_value=0.0, value=500.0, step=10.0)
    retention_cost = st.number_input("Coût rétention", min_value=0.0, value=50.0, step=5.0)
    success_rate = st.slider("Taux de succès rétention", 0.0, 1.0, 0.30, 0.05)

    st.subheader("Paramètres stratégie")
    threshold = 0.5
    top_percent = 10.0
    thresholds = None

    if strategy == "threshold":
        #threshold = st.slider("Seuil principal", 0.0, 1.0, 0.5, 0.01)
        thresholds_text = st.text_input("Comparer ces seuils (ex: 0.3,0.5,0.7)", value="0.3,0.5,0.7")
        try:
            thresholds = [float(x.strip()) for x in thresholds_text.split(",") if x.strip() != ""]
        except:
            thresholds = None
            st.warning("Format seuils invalide, ex: 0.3,0.5,0.7")
    else:
        top_percent = st.slider("Top % clients traités", 0.0, 100.0, 10.0, 1.0)

    run = st.button("Lancer la simulation")

# with right:
#     st.write(
#         """
# Cette simulation calcule un ROI **attendu** sur tout le portefeuille.

# - **threshold** : on traite tous les clients avec proba ≥ seuil
# - **top_percent** : on traite les X% clients les plus à risque
# """
#     )

if run:
    payload = {
        "option": option,
        "strategy": strategy,
        "threshold": threshold,
        "top_percent": top_percent,
        "churn_cost": churn_cost,
        "retention_cost": retention_cost,
        "success_rate": success_rate,
        "thresholds": thresholds,
    }

    try:
        res = simulate_roi(payload)

        st.subheader(f"Résumé avec seuil optimal sélectionné automatiquement:{res['optimal_threshold']}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Clients", str(res["n_clients"]))
        c2.metric("Traités", str(res["treated_clients"]))
        c3.metric("Taux traitement", f"{res['treat_rate']*100:.1f}%")
        c4.metric("ROI total attendu", f"{res['expected_roi']:.2f}")

        st.write(f"Gain attendu: **{res['expected_saved']:.2f}** — Coût actions: **{res['expected_cost']:.2f}**")

        if res["expected_roi"] > 0:
            st.success("Stratégie rentable (ROI > 0)")
        else:
            st.warning("Stratégie non rentable (ROI ≤ 0)")

        # Courbe si threshold list
        if res.get("curve"):
            st.subheader("Comparaison par seuil")
            df_curve = pd.DataFrame(res["curve"]).sort_values("threshold")
            st.dataframe(df_curve, width="stretch", hide_index=True)
            st.line_chart(df_curve.set_index("threshold")[["expected_roi", "treated_clients"]])

        st.subheader("Top clients (risque décroissant)")
        top_df = pd.DataFrame(res.get("top_clients", []))
        if not top_df.empty:
            st.dataframe(top_df, width="stretch", hide_index=True)

    except ApiError as e:
        st.error(str(e))
