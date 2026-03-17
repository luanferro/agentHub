from pydantic import BaseModel, ConfigDict

class DepartamentoBase(BaseModel):
    nome: str

class DepartamentoCreate(DepartamentoBase):
    descricao: str | None = None

class DepartamentoUpdate(DepartamentoBase):
    nome: str | None = None
    descricao: str | None = None

class DepartamentoResponse(DepartamentoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)