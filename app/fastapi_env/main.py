import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Charge les variables du fichier .env dans l'environnement système
load_dotenv()

app = FastAPI()

# Récupération avec os.getenv (plus propre) et typage
API_PORT = int(os.getenv("API_PORT", 8000))


@app.get("/")
def health_check():
    """Vérifie l'état de santé de l'API et retourne le port utilisé."""
    return {"status": "healthy"}


# Modèle de données pour la route POST
class DataPayload(BaseModel):
    """Représente la structure des données envoyées via la route POST."""

    key: str
    value: str


# Base de données temporaire en mémoire
storage = []


@app.get("/data")
def get_data():
    """Récupère toutes les données sauvegardées."""
    return {"data": storage}


@app.post("/data")
def post_data(payload: DataPayload):
    """Sauvegarde une nouvelle donnée."""
    storage.append(payload.model_dump())
    return {"message": "Donnée sauvegardée avec succès", "added": payload}
