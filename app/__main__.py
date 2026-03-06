import os
import subprocess
import sys

from dotenv import load_dotenv


def kill_process_on_port(port):
    """Arrêter tout processus utilisant le port spécifié (Multi-plateforme)."""
    if sys.platform == "win32":
        cmd = (
            f"Stop-Process -Id (Get-NetTCPConnection "
            f"-LocalPort {port}).OwningProcess -Force"
        )
        subprocess.run(
            ["powershell", "-Command", cmd], capture_output=True, check=False
        )
    else:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, check=False)


def main():
    """Nettoyer les ports, charger l'environnement et lancer les services."""
    load_dotenv()

    # Récupération des ports (par défaut 8000 et 8501)
    api_port = os.getenv("FASTAPI_PORT", "8000")
    st_port = os.getenv("STREAMLIT_PORT", "8501")

    print(f"Lancement des services (API:{api_port}, UI:{st_port}).")

    # On tue les anciens processus pour éviter l'erreur 10048
    kill_process_on_port(api_port)
    kill_process_on_port(st_port)

    # Lance le module FastAPI (Backend)
    subprocess.Popen([sys.executable, "-m", "app.fastapi_env"])

    # Lance le module Streamlit (Frontend)
    subprocess.Popen([sys.executable, "-m", "app.streamlit_env"])


if __name__ == "__main__":
    main()  # pragma: no cover
