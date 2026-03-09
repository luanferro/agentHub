from sqlalchemy import select
from sqlalchemy.orm import Session
from crm.models.contato import Contato
from crm.services.empresa_service import get_empresa

def get_contatos(db: Session):
    stmt = select(Contato)
    contatos = db.execute(stmt).scalars().all()
    return contatos

def create_contato(db: Session, contato_data: dict):
    empresa = get_empresa(db, contato_data["empresa_id"])
    if not empresa:
        return None
    novo_contato = Contato(**contato_data)
    db.add(novo_contato)
    db.commit()
    db.refresh(novo_contato)
    return novo_contato

def get_contato(db: Session, contato_id: int):
    stmt = select(Contato).where(Contato.id == contato_id)
    contato = db.execute(stmt).scalar_one_or_none()
    return contato

def update_contato(db: Session, contato_id: int, contato_data: dict):
    contato = get_contato(db, contato_id)
    if not contato:
        return None
    for key, value in contato_data.items():
        setattr(contato, key, value)
    db.commit()
    db.refresh(contato)
    return contato

def delete_contato(db: Session, contato_id: int):
    contato = get_contato(db, contato_id)
    if not contato:
        return None
    db.delete(contato)
    db.commit()
    return contato