from sqlalchemy.orm import Session

from app.fastapi_env.models.models import DataInput

from .connect import OperationResult


def create_operation_result(db: Session, data: DataInput, result: float):
    """Créer un nouvel enregistrement de résultat dans la base de données."""
    db_obj = OperationResult(
        valeur_a=data.valeur_a,
        valeur_b=data.valeur_b,
        operation=data.operation,
        resultat=result,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_all_results(db: Session):
    """Récupérer tous les résultats enregistrés depuis la base de données."""
    return db.query(OperationResult).all()
