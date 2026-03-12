from sqlalchemy import select
from sqlalchemy.orm import Session
from erp.models.produto import Produto

def get_all_produtos(db: Session):
    stmt = select(Produto)
    produtos = db.execute(stmt).scalars().all()
    return produtos

def get_produto(db: Session, produto_id: int):
    stmt = select(Produto).where(Produto.id == produto_id)
    produto = db.execute(stmt).scalar_one_or_none()
    return produto

def create_produto(db: Session, produto_data: dict):
    novo_produto = Produto(**produto_data)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def update_produto(db: Session, produto_id: int, produto_data: dict):
    produto = get_produto(db, produto_id)
    if not produto:
        return None
    for key, value in produto_data.items():
        setattr(produto, key, value)
    db.commit()
    db.refresh(produto)
    return produto

def delete_produto(db: Session, produto_id: int):
    produto = get_produto(db, produto_id)
    if not produto:
        return None
    db.delete(produto)
    db.commit()
    return produto
    