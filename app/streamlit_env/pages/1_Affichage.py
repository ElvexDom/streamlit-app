import os

import requests
import streamlit as st

API_PORT = os.getenv("FASTAPI_PORT", "8000")
BACKEND_URL = os.getenv("BACKEND_URL", f"http://localhost:{API_PORT}")
API_URL = f"{BACKEND_URL}/data"

st.title("Affichage des données")

try:
    response = requests.get(API_URL, timeout=5)

    if response.status_code == 200:
        data = response.json()
        st.table(data)
    else:
        # Affiche le code d'erreur spécifique renvoyé par le serveur
        st.error(f"Erreur lors de la récupération : {response.status_code}")

except Exception as e:
    # Gère les problèmes de DNS, de timeout ou de protocole (ex: HTTPS mal configuré)
    st.error(f"L'API est inaccessible sur {API_URL} : {e}")
