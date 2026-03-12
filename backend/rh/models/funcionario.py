from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Float, ForeignKey
from rh.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    data_admissao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cargo: Mapped[str] = mapped_column(String(255), nullable=False)
    salario: Mapped[float] = mapped_column(Float, nullable=False)
    departamento_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("departamentos.id"), nullable=True
    )

    departamento: Mapped["Departamento"] = relationship(
        "Departamento", back_populates="funcionarios"
    )