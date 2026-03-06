import os
import runpy
import subprocess
import sys

from streamlit.testing.v1 import AppTest

# --- CONFIGURATION DU PATH (Harmonisée avec l'API) ---
base_dir = os.path.dirname(__file__)
st_dir = os.path.join(base_dir, "..", "app", "streamlit_env")
st_path = os.path.abspath(st_dir)

# On ajoute la racine du projet pour que les imports de modules fonctionnent
root_path = os.path.abspath(os.path.join(base_dir, ".."))

if st_path not in sys.path:
    sys.path.insert(0, st_path)
if root_path not in sys.path:
    sys.path.insert(0, root_path)


# --- MOCK RESPONSE ---
class MockResponse:
    """Simule une réponse de la bibliothèque requests."""

    def __init__(self, json_data, status_code=200):
        """Initialise le mock avec des données et un code statut."""
        self._json_data = json_data
        self._status_code = status_code

    def json(self):
        """Renvoie les données JSON simulées."""
        return self._json_data

    @property
    def status_code(self):
        """Simule l'attribut status_code de requests."""
        return self._status_code


# --- TESTS DU LANCEUR (__main__.py) ---


def test_streamlit_main_run_server(monkeypatch):
    """Couvre le lancement du serveur via subprocess (Lignes 12-14, 58)."""
    captured_commands = []

    def mock_run(args, cwd=None, **kwargs):
        captured_commands.append(args)
        return None

    monkeypatch.setattr(subprocess, "run", mock_run)
    # On supprime les variables de test pour forcer le passage dans run_server
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.delenv("STREAMLIT_SERVER_PORT", raising=False)

    runpy.run_module("app.streamlit_env", run_name="__main__")
    assert any("streamlit" in cmd for cmd in captured_commands[0])


def test_streamlit_main_test_mode(monkeypatch, capsys):
    """Vérifie la branche 'Mode Test détecté'."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "true")
    runpy.run_module("app.streamlit_env", run_name="__main__")
    captured = capsys.readouterr()
    assert "Mode Test détecté" in captured.out


# --- TESTS DES PAGES ---


def test_main_page_rendering(monkeypatch):
    """Vérifie le rendu de la page d'accueil."""
    path = os.path.join(st_path, "__main__.py")
    monkeypatch.setenv("STREAMLIT_SERVER_PORT", "8501")
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    at = AppTest.from_file(path).run(timeout=10)
    assert not at.exception
    assert len(at.title) > 0


# --- PAGE 0_INSERT.PY ---


def test_insert_page_success(monkeypatch):
    """Couvre le chemin de succès de l'insertion."""
    path = os.path.join(st_path, "pages", "0_insert.py")
    at = AppTest.from_file(path)

    mock_res = MockResponse({"resultat": 10.0}, 200)
    monkeypatch.setattr("requests.post", lambda *a, **k: mock_res)
    monkeypatch.setenv("FASTAPI_HOST", "localhost")

    at.run()
    at.button[0].click().run()
    assert any("Résultat" in s.value for s in at.success)


def test_insert_page_api_error(monkeypatch):
    """Couvre l'erreur renvoyée par l'API (ex: 400)."""
    path = os.path.join(st_path, "pages", "0_insert.py")
    at = AppTest.from_file(path)

    mock_err = MockResponse({"detail": "Données invalides"}, 400)
    monkeypatch.setattr("requests.post", lambda *a, **k: mock_err)

    at.run()
    at.button[0].click().run()
    assert len(at.error) > 0


def test_insert_page_exception_coverage(monkeypatch):
    """Couvre le bloc except (Lignes 31-32) via un crash forcé."""
    path = os.path.join(st_path, "pages", "0_insert.py")
    at = AppTest.from_file(path)

    def mock_crash(*a, **k):
        raise Exception("Fatal Crash")

    monkeypatch.setattr("requests.post", mock_crash)

    at.run()
    at.button[0].click().run()

    # Correction E501 : Extraction pour rester sous les 88 caractères
    error_msgs = [e.value.lower() for e in at.error]
    assert any("injoignable" in m or "erreur" in m for m in error_msgs)


# --- PAGE 1_AFFICHAGE.PY ---


def test_affichage_page_success(monkeypatch):
    """Couvre la récupération réussie (Lignes 16-21)."""
    path = os.path.join(st_path, "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    data = [{"id": 1, "valeur": 100}]
    monkeypatch.setattr("requests.get", lambda *a, **k: MockResponse(data, 200))
    monkeypatch.setenv("FASTAPI_HOST", "localhost")

    at.run()
    assert len(at.table) > 0 or len(at.dataframe) > 0


def test_affichage_page_api_error_coverage(monkeypatch):
    """Couvre le bloc else (Ligne 21) quand le status_code n'est pas 200."""
    path = os.path.join(st_path, "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    # On simule une erreur 500 renvoyée par l'API
    monkeypatch.setattr("requests.get", lambda *a, **k: MockResponse({}, 500))

    at.run()
    assert len(at.error) > 0


def test_affichage_page_exception_full_coverage(monkeypatch):
    """Couvre le bloc except sur crash réseau."""
    path = os.path.join(st_path, "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    def mock_crash(*a, **k):
        raise Exception("Network Timeout")

    monkeypatch.setattr("requests.get", mock_crash)

    at.run()
    assert any("inaccessible" in e.value for e in at.error)
