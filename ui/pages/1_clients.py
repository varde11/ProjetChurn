import streamlit as st
import pandas as pd
from api_client import get_clients_by_label, get_client_by_id, ApiError

st.title("👥 Clients")

col1, col2 = st.columns([1, 2])

with col1:
    label = st.selectbox("Filtrer par label", ["all", "churn", "no_churn"], index=0)
    st.caption("Basé sur les prédictions enregistrées en base (jointure Client ↔ Prediction).")

with col2:
    st.subheader("Recherche rapide")
    id_search = st.number_input("Rechercher un client par id_client", min_value=1, step=1, value=1)
    if st.button("Chercher"):
        try:
            client = get_client_by_id(int(id_search))
            st.success(f"Client trouvé : id_client={client.get('id_client')}")
            st.json(client)
        except ApiError as e:
            st.error(str(e))

st.divider()

try:
    clients = get_clients_by_label(label)
    if not clients:
        st.info("Aucun client trouvé avec ce filtre.")
    else:
        df = pd.DataFrame(clients)
        st.dataframe(df, width='stretch', hide_index=True)
        st.caption(f"{len(df)} client(s)")
except ApiError as e:
    st.error(str(e))
