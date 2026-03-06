from pydantic import BaseModel


# Modèle pour la réception des données via POST /data
class DataInput(BaseModel):
    """Modèle pour la réception des données via POST /data."""

    valeur_a: float
    valeur_b: float
    operation: str  # "add", "sub", "square"


# Modèle pour la réponse (ce que l'API renvoie)
class DataResponse(BaseModel):
    """Modèle pour la réponse (ce que l'API renvoie)."""

    id: int
    valeur_a: float
    valeur_b: float
    operation: str
    resultat: float

    class Config:
        """Configuration pour permettre la compatibilité avec SQLAlchemy."""

        from_attributes = True  # Indispensable pour lire les objets SQLAlchemy
