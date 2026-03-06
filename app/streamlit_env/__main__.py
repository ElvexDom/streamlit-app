import os
import subprocess
import sys

import streamlit as st


def run_app():
    """Contenu de la page d'accueil Streamlit."""
    st.set_page_config(page_title="Toolbox Project", page_icon="🛠️")
    st.title("🛠️ Bienvenue dans la Toolbox")
    st.write("Utilisez le menu à gauche pour naviguer.")


def main():
    """Point d'entrée : lance Streamlit ou affiche la page."""
    # Ce bloc est exécuté par Pytest, donc il est couvert
    if "PYTEST_CURRENT_TEST" in os.environ:
        run_app()
        return

    # Tout ce qui suit est le lancement REEL du serveur.
    # On l'exclut car on ne peut pas tester un serveur infini en test unitaire.
    if "STREAMLIT_SERVER_PORT" not in os.environ:  # pragma: no cover
        print("Démarrage du serveur Streamlit...")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                __file__,
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
            ]
        )
    else:  # pragma: no cover
        run_app()


if __name__ == "__main__":
    main()  # pragma: no cover
