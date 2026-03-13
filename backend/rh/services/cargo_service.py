from sqlalchemy import select
from sqlalchemy.orm import Session
from rh.models.cargo import Cargo

def get_cargos(db: Session):
    stmt = select(Cargo)
    cargos = db.execute(stmt).scalars().all()
    return cargos

def get_cargo(db: Session, cargo_id: int):
    stmt = select(Cargo).where(Cargo.id == cargo_id)
    cargo = db.execute(stmt).scalar_one_or_none()
    return cargo

def create_cargo(db: Session, cargo_data: dict):
    cargo = Cargo(**cargo_data)
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo

def update_cargo(db: Session, cargo_id: int, cargo_data: dict):
    cargo = get_cargo(db, cargo_id)
    if not cargo:
        return None
    for key, value in cargo_data.items():
        setattr(cargo, key, value)
    db.commit()
    db.refresh(cargo)
    return cargo

def delete_cargo(db: Session, cargo_id: int):
    cargo = get_cargo(db, cargo_id)
    if not cargo:
        return None
    db.delete(cargo)
    db.commit()
    return cargo
