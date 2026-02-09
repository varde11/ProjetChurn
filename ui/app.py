import streamlit as st

st.set_page_config(
    page_title="Churn Decision App",
    page_icon="📉",
    layout="wide",
)

st.title("📉 Churn Decision App")
st.write(
    """
Cette application consomme l'API FastAPI de prédiction de churn.

Utilise le menu à gauche pour naviguer :
- **Clients**
- **Détail client**
- **Historique & Stratégie**
"""
)
