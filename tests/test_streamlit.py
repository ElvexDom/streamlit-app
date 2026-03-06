import os

from streamlit.testing.v1 import AppTest

# --- CONFIGURATION ---

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- MOCKS ---


class MockResponse:
    """Simule une réponse de la bibliothèque requests."""

    def __init__(self, json_data, status_code=200):
        """Initialise le mock avec des données et un code statut."""
        self._json_data = json_data
        self._status_code = status_code

    def json(self):
        """Renvoie les données JSON simulées de requests."""
        return self._json_data

    @property
    def status_code(self):
        """Simule l'attribut .status_code de requests."""
        return self._status_code


# --- TESTS : PAGE D'ACCUEIL ---


def test_main_page(monkeypatch):
    """Vérifie le point d'entrée Streamlit (__main__.py)."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "__main__.py")

    # On mock Popen au cas où le main() tente de lancer les serveurs
    monkeypatch.setattr("subprocess.Popen", lambda *args, **kwargs: None)

    at = AppTest.from_file(path).run(timeout=10)
    assert not at.exception
    assert any("Bienvenue" in t.value for t in at.title)


# --- TESTS : PAGE INSERTION (0_insert.py) ---


def test_insert_page_success(monkeypatch):
    """Couvre le succès API (200 OK) dans l'insertion."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "0_insert.py")
    at = AppTest.from_file(path)  # Pas de .run() ici

    mock_res = MockResponse({"resultat": 42.0}, 200)
    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_res)

    at.run(timeout=10)
    at.button[0].click().run()
    assert any("Résultat : 42.0" in s.value for s in at.success)


def test_insert_page_api_error(monkeypatch):
    """Couvre l'erreur API (400/500) dans l'insertion."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "0_insert.py")
    at = AppTest.from_file(path)

    mock_err = MockResponse({"detail": "Erreur API"}, 400)
    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_err)

    at.run(timeout=10)
    at.button[0].click().run()
    assert any("Erreur : Erreur API" in e.value for e in at.error)


def test_insert_page_exception(monkeypatch):
    """Couvre le crash réseau (except) dans l'insertion."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "0_insert.py")
    at = AppTest.from_file(path)

    def mock_raise(*args, **kwargs):
        raise Exception("Connexion refusée")

    monkeypatch.setattr("requests.post", mock_raise)

    at.run(timeout=10)
    at.button[0].click().run()
    assert any("L'API est injoignable" in e.value for e in at.error)


# --- TESTS : PAGE AFFICHAGE (1_Affichage.py) ---


def test_read_page_display_success(monkeypatch):
    """Couvre l'affichage réussi (200 OK) dans Affichage.py."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    data = [{"id": 1, "nom": "Test"}]
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse(data, 200))

    at.run(timeout=10)
    assert len(at.dataframe) > 0 or len(at.table) > 0


def test_read_page_error_api(monkeypatch):
    """Couvre l'erreur API (else: status_code != 200)."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse({}, 500))

    at.run(timeout=10)
    assert len(at.error) > 0
    assert any("Erreur lors de la récupération" in e.value for e in at.error)


def test_read_page_exception(monkeypatch):
    """Couvre le bloc except (API inaccessible)."""
    path = os.path.join(BASE_DIR, "app", "streamlit_env", "pages", "1_Affichage.py")
    at = AppTest.from_file(path)

    def mock_crash(*args, **kwargs):
        raise Exception("Host Unreachable")

    monkeypatch.setattr("requests.get", mock_crash)

    at.run(timeout=10)
    assert len(at.error) > 0
    assert any("L'API est inaccessible" in e.value for e in at.error)
