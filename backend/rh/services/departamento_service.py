from sqlalchemy import select
from sqlalchemy.orm import Session
from rh.models.departamento import Departamento

def get_departamentos(db: Session):
    stmt = select(Departamento)
    departamentos = db.execute(stmt).scalars().all()
    return departamentos

def get_departamento(db: Session, departamento_id: int):
    stmt = select(Departamento).where(Departamento.id == departamento_id)
    departamento = db.execute(stmt).scalar_one_or_none()
    return departamento

def create_departamento(db: Session, departamento_data: dict):
    departamento = Departamento(**departamento_data)
    db.add(departamento)
    db.commit()
    db.refresh(departamento)
    return departamento

def update_departamento(db: Session, departamento_id: int, departamento_data: dict):
    departamento = get_departamento(db, departamento_id)
    if not departamento:
        return None
    for key, value in departamento_data.items():
        setattr(departamento, key, value)
    db.commit()
    db.refresh(departamento)
    return departamento

def delete_departamento(db: Session, departamento_id: int):
    departamento = get_departamento(db, departamento_id)
    if not departamento:
        return None
    db.delete(departamento)
    db.commit()
    return departamento