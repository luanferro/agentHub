from sqlalchemy import String, Integer
from crm.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=True)
    ramo: Mapped[str] = mapped_column(String(255), nullable=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)

    contatos: Mapped[list["Contato"]] = relationship("Contato", back_populates="empresa")
    oportunidades: Mapped[list["Oportunidade"]] = relationship("Oportunidade", back_populates="empresa")