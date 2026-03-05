import os
import subprocess
import sys

from app.main import main


# Test de la fonction main directement
def test_front_main_output(capsys):
    """Vérifie que la fonction main affiche le bon message dans la console."""
    main()
    captured = capsys.readouterr()
    assert "Hello from streamlit-app!" in captured.out


# Test de l'exécution en mode script (le bloc if __name__ == "__main__")
def test_front_script_execution():
    """Vérifie le comportement du script lorsqu'il est appelé directement via Python."""
    path_to_script = os.path.join("app", "main.py")
    result = subprocess.run(
        [sys.executable, path_to_script], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Hello from streamlit-app!" in result.stdout
