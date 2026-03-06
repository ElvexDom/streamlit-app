import requests
import streamlit as st

st.title("Affichage des données")

try:
    response = requests.get("http://localhost:8000/data")  # ou ton URL
    if response.status_code == 200:
        data = response.json()
        st.table(data)
    else:
        # C'est cette ligne qui fera passer le test !
        st.error(f"Erreur lors de la récupération : {response.status_code}")
except Exception as e:
    # Et celle-ci pour les crashs réseaux
    st.error(f"L'API est inaccessible : {e}")
