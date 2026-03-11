from sqlalchemy import String, Integer, Float, DateTime, Boolean
from erp.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
    client_nome: Mapped[str] = mapped_column(String, nullable=False)

    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido")


