from pydantic import BaseModel, ConfigDict

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str


class EmpresaCreate(EmpresaBase):
    razao_social: str | None = None
    ramo: str | None = None
    endereco: str | None = None
    
class EmpresaUpdate(BaseModel):
    nome: str | None = None
    cnpj: str | None = None
    razao_social: str | None = None
    ramo: str | None = None
    endereco: str | None = None

class EmpresaResponse(EmpresaCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)