import pytest
from fastapi.testclient import TestClient

from app.fastapi_env.main import (  # On importe 'storage' pour pouvoir le manipuler
    app,
    storage,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    """Cette fixture vide la liste storage pour garantir l'isolation des tests."""
    storage.clear()
    yield  # Le test s'exécute ici
    # Optionnel : on pourrait rajouter du code de nettoyage après le test ici


def test_get_data_empty():
    """Vérifie que la liste est bien vide au démarrage grâce à la fixture."""
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() == {"data": []}


def test_post_and_get_data():
    """Vérifie l'enchaînement complet : POST puis GET."""
    # 1. POST
    payload = {"key": "temp", "value": "25"}
    client.post("/data", json=payload)

    # 2. GET
    response = client.get("/data")
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["key"] == "temp"


def test_post_invalid_data():
    """Vérifie que FastAPI rejette les données mal formées (Mock de validation)."""
    # On envoie 'val' au lieu de 'value' (le modèle attend 'value')
    payload = {"key": "erreur", "val": "10"}
    response = client.post("/data", json=payload)
    assert response.status_code == 422
