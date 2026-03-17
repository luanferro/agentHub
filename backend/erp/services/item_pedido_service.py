from sqlalchemy import select
from sqlalchemy.orm import Session
from erp.services.pedido_service import get_pedido
from erp.services.produto_service import get_produto
from erp.models.item_pedido import ItemPedido

def get_all_itens_pedidos(db: Session):
    stmt = select(ItemPedido)
    itensPedidos = db.execute(stmt).scalars().all()
    return itensPedidos

def get_item_pedido(db: Session, item_pedido_id: int):
    stmt = select(ItemPedido).where(ItemPedido.id == item_pedido_id)
    item_pedido = db.execute(stmt).scalar_one_or_none()
    return item_pedido

def create_item_pedido(db: Session, item_pedido_data: dict):
    produto = get_produto(db, item_pedido_data["produto_id"])
    pedido = get_pedido(db, item_pedido_data["pedido_id"])
    if not produto or not pedido:
        return None
    novo_item_pedido = ItemPedido(**item_pedido_data)
    db.add(novo_item_pedido)
    db.commit()
    db.refresh(novo_item_pedido)
    return novo_item_pedido

def update_item_pedido(db: Session, item_pedido_id: int, item_pedido_data: dict):
    item_pedido = get_item_pedido(db, item_pedido_id)
    if not item_pedido:
        return None
    for key, value in item_pedido_data.items():
        setattr(item_pedido, key, value)
    db.commit()
    db.refresh(item_pedido)
    return item_pedido

def delete_item_pedido(db: Session, item_pedido_id: int):
    item_pedido = get_item_pedido(db, item_pedido_id)
    if not item_pedido:
        return None
    db.delete(item_pedido)
    db.commit()
    return item_pedido