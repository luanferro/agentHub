from sqlalchemy import String, Integer
from rh.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)

    cargos: Mapped[list["Cargo"]] = relationship("Cargo", back_populates="departamento")
    funcionarios: Mapped[list["Funcionario"]] = relationship(
        "Funcionario", back_populates="departamento"
    )