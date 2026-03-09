from sqlalchemy import String, Integer, ForeignKey
from crm.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Contato(Base):
    __tablename__ = "contatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(20), nullable=True)
    empresa_id: Mapped[int] = mapped_column(Integer, ForeignKey("empresas.id"), nullable=False)

    oportunidades: Mapped[list["Oportunidade"]] = relationship("Oportunidade", back_populates="contato")
    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="contatos")
