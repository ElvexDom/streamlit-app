import runpy
import sys


def test_app_main_with_monkeypatch(monkeypatch):
    """Teste le lancement du module app en capturant les commandes sans MagicMock."""
    # 1. On crée une liste pour stocker les commandes interceptées
    captured_commands = []

    # 2. On définit une fonction factice qui remplace subprocess.Popen
    def mock_popen(args, **kwargs):
        captured_commands.append(args)
        return None  # On simule que le processus est lancé

    # 3. On applique le remplacement
    monkeypatch.setattr("subprocess.Popen", mock_popen)

    # 4. On exécute le module app (__main__.py)
    runpy.run_module("app", run_name="__main__")

    # 5. Vérifications
    assert len(captured_commands) == 2
    assert [sys.executable, "-m", "app.fastapi_env"] in captured_commands
    assert [sys.executable, "-m", "app.streamlit_env"] in captured_commands
