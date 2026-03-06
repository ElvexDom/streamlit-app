import os

import requests
import streamlit as st

API_PROTO = os.getenv("FASTAPI_PROTO", "http")
API_HOST = os.getenv("FASTAPI_HOST", "localhost")
API_PORT = os.getenv("FASTAPI_PORT", "8000")
API_URL = f"{API_PROTO}://{API_HOST}:{API_PORT}/data"

st.title("📝 Saisie de Calcul")

with st.form("calcul_form"):
    val_a = st.number_input("Valeur A", value=0.0)
    val_b = st.number_input("Valeur B", value=0.0)
    operation = st.selectbox("Opération", ["add", "sub", "multiply", "divide"])
    submitted = st.form_submit_button("Calculer")

if submitted:
    payload = {"valeur_a": val_a, "valeur_b": val_b, "operation": operation}
    try:
        # Appel à l'API en utilisant l'URL configurée
        response = requests.post(API_URL, json=payload, timeout=5)

        if response.status_code == 200:
            st.success(f"Résultat : {response.json()['resultat']}")
        else:
            error_detail = response.json().get("detail", "Erreur inconnue")
            st.error(f"Erreur : {error_detail}")

    except Exception as e:
        st.error(f"L'API est injoignable sur {API_URL} : {e}")
