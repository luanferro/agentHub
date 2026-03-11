from sqlalchemy import Float, Integer, ForeignKey
from erp.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pedido_id: Mapped[int] = mapped_column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped["Pedido"] = relationship("Pedido", back_populates="itens")
    produto: Mapped["Produto"] = relationship("Produto", back_populates="itens_pedidos")
