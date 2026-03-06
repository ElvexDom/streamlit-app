import subprocess
import sys


def main():
    """Lance l'API et Streamlit en utilisant la syntaxe de module Python."""
    print("Lancement des services.")
    # Lance le module FastAPI (Backend)
    subprocess.Popen([sys.executable, "-m", "app.fastapi_env"])

    # Lance le module Streamlit (Frontend)
    subprocess.Popen([sys.executable, "-m", "app.streamlit_env"])


if __name__ == "__main__":
    main()  # pragma: no cover
