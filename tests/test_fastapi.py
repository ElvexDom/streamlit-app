from fastapi.testclient import TestClient

from app.fastapi_env.main import app

client = TestClient(app)


def test_get_data_structure():
    """Vérifie que la route GET renvoie bien une liste (même vide)."""
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_operations_success():
    """Vérifie que le POST traite correctement toutes les opérations supportées."""
    # Test ADD (Ligne 36)
    payload_add = {"valeur_a": 10, "valeur_b": 20, "operation": "add"}
    res_add = client.post("/data", json=payload_add)
    assert res_add.status_code == 200
    assert res_add.json()["resultat"] == 30.0

    # Test SUB (Ligne 38)
    payload_sub = {"valeur_a": 10, "valeur_b": 5, "operation": "sub"}
    res_sub = client.post("/data", json=payload_sub)
    assert res_sub.json()["resultat"] == 5.0

    # Test MULTIPLY (Ligne 40)
    payload_mul = {"valeur_a": 3, "valeur_b": 4, "operation": "multiply"}
    res_mul = client.post("/data", json=payload_mul)
    assert res_mul.json()["resultat"] == 12.0

    # Test DIVIDE (Ligne 42)
    payload_div = {"valeur_a": 10, "valeur_b": 2, "operation": "divide"}
    res_div = client.post("/data", json=payload_div)
    assert res_div.json()["resultat"] == 5.0


def test_post_invalid_operation():
    """Vérifie la gestion d'une opération non supportée (Erreur 400, Lignes 52-54)."""
    payload = {"valeur_a": 10, "valeur_b": 5, "operation": "modulo"}
    response = client.post("/data", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Opération non supportée"


def test_post_division_by_zero():
    """Vérifie la capture de ValueError via l'exception HTTP."""
    payload = {"valeur_a": 10, "valeur_b": 0, "operation": "divide"}
    response = client.post("/data", json=payload)
    assert response.status_code == 400
    # On vérifie que le message d'erreur vient bien de ton module mathématique
    assert "Division par zéro" in response.json()["detail"]


def test_post_bad_schema():
    """Vérifie que FastAPI rejette un JSON incomplet (Erreur 422)."""
    payload = {"valeur_a": 10}
    response = client.post("/data", json=payload)
    assert response.status_code == 422
