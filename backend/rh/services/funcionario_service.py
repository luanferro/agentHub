from sqlalchemy import select
from sqlalchemy.orm import Session
from rh.models.funcionario import Funcionario

def get_funcionarios(db: Session):
    stmt = select(Funcionario)
    funcionarios = db.execute(stmt).scalars().all()
    return funcionarios

def get_funcionario(db: Session, funcionario_id: int):
    stmt = select(Funcionario).where(Funcionario.id == funcionario_id)
    funcionario = db.execute(stmt).scalar_one_or_none()
    return funcionario

def create_funcionario(db: Session, funcionario_data: dict):
    funcionario = Funcionario(**funcionario_data)
    db.add(funcionario)
    db.commit()
    db.refresh(funcionario)
    return funcionario

def update_funcionario(db: Session, funcionario_id: int, funcionario_data: dict):
    funcionario = get_funcionario(db, funcionario_id)
    if not funcionario:
        return None
    for key, value in funcionario_data.items():
        setattr(funcionario, key, value)
    db.commit()
    db.refresh(funcionario)
    return funcionario

def delete_funcionario(db: Session, funcionario_id: int):
    funcionario = get_funcionario(db, funcionario_id)
    if not funcionario:
        return None
    db.delete(funcionario)
    db.commit()
    return funcionario