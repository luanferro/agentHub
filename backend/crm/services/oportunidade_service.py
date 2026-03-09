from sqlalchemy import select
from sqlalchemy.orm import Session
from crm.models.oportunidade import Oportunidade
from crm.services.empresa_service import get_empresa
from crm.services.contato_service import get_contato

def get_oportunidades(db: Session):
    stmt = select(Oportunidade)
    oportunidades = db.execute(stmt).scalars().all()
    return oportunidades

def create_oportunidade(db: Session, oportunidade_data: dict):
    empresa = get_empresa(db, oportunidade_data["empresa_id"])
    contato = get_contato(db, oportunidade_data["contato_id"])
    if not empresa or not contato:
        return None
    nova_oportunidade = Oportunidade(**oportunidade_data)
    db.add(nova_oportunidade)
    db.commit()
    db.refresh(nova_oportunidade)
    return nova_oportunidade

def get_oportunidade(db: Session, oportunidade_id: int):
    stmt = select(Oportunidade).where(Oportunidade.id == oportunidade_id)
    oportunidade = db.execute(stmt).scalar_one_or_none()
    return oportunidade

def update_oportunidade(db: Session, oportunidade_id: int, oportunidade_data: dict):
    oportunidade = get_oportunidade(db, oportunidade_id)
    if not oportunidade:
        return None
    for key, value in oportunidade_data.items():
        setattr(oportunidade, key, value)
    db.commit()
    db.refresh(oportunidade)
    return oportunidade 

def delete_oportunidade(db: Session, oportunidade_id: int):
    oportunidade = get_oportunidade(db, oportunidade_id)
    if not oportunidade:
        return None
    db.delete(oportunidade)
    db.commit()
    return oportunidade