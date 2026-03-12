from sqlalchemy import String, Integer, ForeignKey, Float
from rh.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Cargo(Base):
    __tablename__ = "cargos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    salario_base: Mapped[float] = mapped_column(Float, nullable=False)
    departamento_id: Mapped[int] = mapped_column(Integer, ForeignKey("departamentos.id"), nullable=True)
