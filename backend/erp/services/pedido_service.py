from sqlalchemy import select
from sqlalchemy.orm import Session
from erp.models.pedido import Pedido

def get_all_pedidos(db: Session):
    stmt = select(Pedido)
    pedidos = db.execute(stmt).scalars().all()
    return pedidos

def get_pedido(db: Session, pedido_id: int):
    stmt = select(Pedido).where(Pedido.id == pedido_id)
    pedido = db.execute(stmt).scalar_one_or_none()
    return pedido

def create_pedido(db: Session, pedido_data: dict):
    novo_pedido = Pedido(**pedido_data)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

def update_pedido(db: Session, pedido_id: int, pedido_data: dict):
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    for key, value in pedido_data.items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return pedido

def delete_pedido(db: Session, pedido_id: int):
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    db.delete(pedido)
    db.commit()
    return pedido