from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FuncionarioBase(BaseModel):
    nome: str
    email: str
    cpf: str
    data_admissao: datetime
    cargo: str
    salario: float

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUpdate(FuncionarioBase):
    departamento_id: int | None = None

class FuncionarioResponse(FuncionarioCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)