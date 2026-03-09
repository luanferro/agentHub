from sqlalchemy import select
from sqlalchemy.orm import Session
from crm.models.empresa import Empresa


def get_empresas(db: Session):
    stmt = select(Empresa)
    empresas = db.execute(stmt).scalars().all()
    return empresas

def create_empresa(db: Session, empresa_data: dict):
    nova_empresa = Empresa(**empresa_data)
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa

def get_empresa(db: Session, empresa_id: int):
    stmt = select(Empresa).where(Empresa.id == empresa_id)
    empresa = db.execute(stmt).scalar_one_or_none()
    return empresa

def update_empresa(db: Session, empresa_id: int, empresa_data: dict):
    empresa = get_empresa(db, empresa_id)
    if not empresa:
        return None
    for key, value in empresa_data.items():
        setattr(empresa, key, value)
    db.commit()
    db.refresh(empresa)
    return empresa

def delete_empresa(db: Session, empresa_id: int):
    empresa = get_empresa(db, empresa_id)
    if not empresa:
        return None
    db.delete(empresa)
    db.commit()
    return empresa