import os
import runpy
import subprocess
import sys

from fastapi.testclient import TestClient

# --- CONFIGURATION DU PATH ---
base_dir = os.path.dirname(__file__)
api_dir = os.path.join(base_dir, "..", "app", "fastapi_env")
api_path = os.path.abspath(api_dir)

if api_path not in sys.path:
    sys.path.insert(0, api_path)

# --- IMPORTS ---
from app.fastapi_env.api import app  # noqa: E402

client = TestClient(app)

# --- TESTS DU LANCEUR (__main__.py) ---


def test_fastapi_main_full_coverage(monkeypatch, capsys):
    """Force le passage dans run_server() hors mode test."""
    # 1. Mock de subprocess pour éviter de lancer uvicorn
    captured_commands = []

    def mock_run(args, cwd=None, **kwargs):
        captured_commands.append(args)
        return None

    monkeypatch.setattr(subprocess, "run", mock_run)

    # 2. On supprime temporairement la variable d'env
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    # 3. Exécution avec run_name="__main__" pour entrer dans le bloc if final
    runpy.run_module("app.fastapi_env", run_name="__main__")

    assert len(captured_commands) > 0
    assert "uvicorn" in captured_commands[0]


def test_fastapi_main_test_mode(monkeypatch, capsys):
    """Vérifie la branche 'Mode Test détecté'."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "true")
    runpy.run_module("app.fastapi_env", run_name="__main__")

    captured = capsys.readouterr()
    assert "Mode Test détecté" in captured.out


def test_run_server_logic(monkeypatch):
    """Vérifie la construction de la commande uvicorn."""
    captured_data = []

    def mock_run(args, cwd=None, **kwargs):
        captured_data.append({"args": args, "cwd": cwd})
        return None

    monkeypatch.setattr(subprocess, "run", mock_run)

    from app.fastapi_env.__main__ import run_server

    run_server()

    cmd = captured_data[0]["args"]
    assert "uvicorn" in cmd
    assert "api:app" in cmd
    assert captured_data[0]["cwd"].endswith("fastapi_env")


# --- TESTS DES ROUTES API ---


def test_get_data_structure():
    """Vérifie que la route GET renvoie bien une liste."""
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_operations_success():
    """Vérifie le succès des opérations mathématiques."""
    operations = [
        ("add", 10, 20, 30.0),
        ("sub", 10, 5, 5.0),
        ("multiply", 3, 4, 12.0),
        ("divide", 10, 2, 5.0),
    ]
    for op, a, b, expected in operations:
        payload = {"valeur_a": a, "valeur_b": b, "operation": op}
        res = client.post("/data", json=payload)
        assert res.status_code == 200
        assert res.json()["resultat"] == expected


def test_post_invalid_operation():
    """Vérifie l'erreur 400 pour opération inconnue."""
    payload = {"valeur_a": 10, "valeur_b": 5, "operation": "modulo"}
    response = client.post("/data", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Opération non supportée"


def test_post_division_by_zero():
    """Vérifie l'erreur 400 en cas de division par zéro."""
    payload = {"valeur_a": 10, "valeur_b": 0, "operation": "divide"}
    response = client.post("/data", json=payload)
    assert response.status_code == 400
    assert "Division par zéro" in response.json()["detail"]


def test_post_bad_schema():
    """Vérifie l'erreur 422 pour schéma JSON invalide."""
    response = client.post("/data", json={"valeur_a": 10})
    assert response.status_code == 422
