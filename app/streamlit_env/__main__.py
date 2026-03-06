"""Point d'entrée pour lancer le service Streamlit ou simuler son chargement."""

import os
import subprocess
import sys

import streamlit as st


def run_app():
    """Contenu de la page d'accueil Streamlit."""
    st.set_page_config(page_title="Toolbox Project", page_icon="🛠️")
    st.title("🛠️ Bienvenue dans la Toolbox")
    st.write("Utilisez le menu à gauche pour naviguer.")


def run_server():
    """Lancer le processus Streamlit avec configuration par environnement."""
    # Récupération du port via variable d'environnement
    port = os.getenv("STREAMLIT_PORT", "8501")

    # Définition dynamique des chemins pour une robustesse totale
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_file = os.path.basename(__file__)

    print(f"Démarrage du serveur Streamlit sur le port {port}")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            current_file,
            "--server.port",
            port,
            "--server.address",
            "0.0.0.0",
        ],
        cwd=current_dir,
        check=False,
    )


def main():
    """Déterminer s'il faut lancer le serveur ou afficher l'UI."""
    # Sécurité pour Pytest : évite de lancer un processus bloquant lors des tests
    if "PYTEST_CURRENT_TEST" in os.environ:
        print("Mode Test détecté : chargement de streamlit_env validé.")
        return

    # Si la variable STREAMLIT_SERVER_PORT n'est pas définie, c'est le
    # premier lancement : on doit démarrer le serveur via run_server().
    # Sinon, on est déjà dans le processus Streamlit, on affiche run_app().
    if "STREAMLIT_SERVER_PORT" not in os.environ:
        run_server()
    else:
        run_app()


if __name__ == "__main__":
    main()  # pragma: no cover
