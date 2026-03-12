from sqlalchemy import String, Integer, Float
from erp.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=True)

    item_pedidos: Mapped[list["ItemPedido"]] = relationship(back_populates="produto")

