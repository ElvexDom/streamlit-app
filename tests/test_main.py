import runpy
import subprocess
import sys


def test_main_full_coverage_with_runpy(monkeypatch):
    """Exécute le main via runpy en simulant Windows et Linux (Full Coverage)."""
    # On définit les collecteurs
    captured_popens = []

    # Mocks globaux
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)
    monkeypatch.setattr(
        subprocess, "Popen", lambda args, **kwargs: captured_popens.append(args)
    )
    # Mock de subprocess.run pour ne rien exécuter réellement
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: None)

    # Configuration des ports
    monkeypatch.setenv("FASTAPI_PORT", "8000")
    monkeypatch.setenv("STREAMLIT_PORT", "8501")

    # --- Couverture de la branche Windows ---
    monkeypatch.setattr(sys, "platform", "win32")
    runpy.run_module("app", run_name="__main__")

    # --- Couverture de la branche Unix (Linux/Mac) ---
    # On vide la liste pour repartir propre
    captured_popens.clear()
    monkeypatch.setattr(sys, "platform", "linux")
    runpy.run_module("app", run_name="__main__")

    # Vérifications finales
    assert len(captured_popens) == 2
    assert [sys.executable, "-m", "app.fastapi_env"] in captured_popens
    assert [sys.executable, "-m", "app.streamlit_env"] in captured_popens
