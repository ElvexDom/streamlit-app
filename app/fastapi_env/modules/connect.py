import os

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL dynamique : SQLite par défaut, remplacée par DATABASE_URL dans Docker
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# SQLite nécessite un argument spécifique pour le multithreading
is_sqlite = SQLALCHEMY_DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modèle de table SQLAlchemy
class OperationResult(Base):
    """Modèle de table SQLAlchemy pour stocker les résultats des opérations."""

    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    valeur_a = Column(Float)
    valeur_b = Column(Float)
    operation = Column(String)
    resultat = Column(Float)


# Création des tables (utile pour SQLite en local)
def init_db():
    """Créer les tables de la base de données."""
    Base.metadata.create_all(bind=engine)
