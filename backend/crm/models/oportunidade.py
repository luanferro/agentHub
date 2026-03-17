from sqlalchemy import String, Integer, ForeignKey, Float, DateTime
from crm.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Oportunidade(Base):

    __tablename__ = "oportunidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_negocio: Mapped[str] = mapped_column(String(255), nullable=False)
    custo: Mapped[float] = mapped_column(Float, nullable=True)
    lucro: Mapped[float] = mapped_column(Float, nullable=True)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    responsavel: Mapped[str] = mapped_column(String(255), nullable=False)
    empresa_id: Mapped[int] = mapped_column(Integer, ForeignKey("empresas.id"), nullable=False)
    contato_id: Mapped[int] = mapped_column(Integer, ForeignKey("contatos.id"), nullable=False)


    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="oportunidades")
    contato: Mapped["Contato"] = relationship("Contato", back_populates="oportunidades")