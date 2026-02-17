import streamlit as st
import pandas as pd
from api_client import get_clients_by_label, get_client_by_id, ApiError

st.title("👥 Clients")


st.subheader("Filtrer par label")

label = st.selectbox("Label", ["all", "churn", "no_churn"], index=0)
run_filter = st.button("Appliquer le filtre")

if run_filter:
    try:
        clients = get_clients_by_label(label)
        if not clients:
            st.info("Aucun client trouvé avec ce filtre.")
        else:
            df = pd.DataFrame(clients)
            st.dataframe(df, width="stretch", hide_index=True)
            st.caption(f"{len(df)} client(s) — filtre: {label}")
    except ApiError as e:
        st.error(str(e))

st.divider()


st.subheader("Recherche rapide")

id_search = st.number_input("Rechercher un client par id_client", min_value=1, step=1, value=1)
run_search = st.button("Chercher par id_client")

if run_search:
    try:
        client = get_client_by_id(int(id_search))
        st.success(f"Client trouvé : id_client={client.get('id_client')}")
        st.dataframe(pd.DataFrame([client]), width="stretch", hide_index=True)
    except ApiError as e:
        st.error(str(e))
