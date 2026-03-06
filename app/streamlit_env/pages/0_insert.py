import requests
import streamlit as st

st.title("📝 Saisie de Calcul")

with st.form("calcul_form"):
    val_a = st.number_input("Valeur A", value=0.0)
    val_b = st.number_input("Valeur B", value=0.0)
    operation = st.selectbox("Opération", ["add", "sub", "multiply", "divide"])
    submitted = st.form_submit_button("Calculer")

if submitted:
    payload = {"valeur_a": val_a, "valeur_b": val_b, "operation": operation}
    try:
        # On utilise localhost pour le moment (sera 'api' via Docker)
        response = requests.post("http://localhost:8000/data", json=payload, timeout=5)
        if response.status_code == 200:
            st.success(f"Résultat : {response.json()['resultat']}")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")
    except Exception as e:
        st.error(f"L'API est injoignable : {e}")
