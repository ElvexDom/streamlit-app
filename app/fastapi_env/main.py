from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.fastapi_env.maths import mon_module
from app.fastapi_env.models.models import DataInput, DataResponse
from app.fastapi_env.modules import crud
from app.fastapi_env.modules.connect import SessionLocal, init_db

# Initialise la DB (utile pour SQLite local)
init_db()

app = FastAPI(title="Toolbox API")


# Dépendance pour obtenir la session DB
def get_db():
    """Générateur de session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data", response_model=list[DataResponse])
def get_data(db: Session = Depends(get_db)):
    """Récupérer la liste de tous les calculs enregistrés."""
    return crud.get_all_results(db)


@app.post("/data", response_model=DataResponse)
def post_data(payload: DataInput, db: Session = Depends(get_db)):
    """Effectuer un calcul et enregistrer le résultat."""
    try:
        if payload.operation == "add":
            res = mon_module.add(payload.valeur_a, payload.valeur_b)
        elif payload.operation == "sub":
            res = mon_module.sub(payload.valeur_a, payload.valeur_b)
        elif payload.operation == "multiply":
            res = mon_module.multiply(payload.valeur_a, payload.valeur_b)
        elif payload.operation == "divide":
            res = mon_module.divide(payload.valeur_a, payload.valeur_b)
        else:
            # Gestion d'une opération inconnue
            from fastapi import HTTPException

            raise HTTPException(status_code=400, detail="Opération non supportée")

        return crud.create_operation_result(db, payload, res)

    except ValueError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=str(e))
