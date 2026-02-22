import streamlit as st

st.set_page_config(
    page_title="Churn Decision App",
    page_icon="📉",
    layout="wide",
)

st.title("📉 Churn Decision App")
st.write(
    """
Utilise le menu à gauche pour naviguer :
- **Clients** (voir les informations des clients)
- **Predictions** (faire une prédiction sur un client)
- **Historiques** (Visionner l'historique des prédictions)
- **Simulation ROI** (faire des simulations sur l'ensemble des clients)
"""
)
