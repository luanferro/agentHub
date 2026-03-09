from pydantic import BaseModel, ConfigDict

class ContatoBase(BaseModel):
    nome: str
    email: str

class ContatoCreate(ContatoBase):
    telefone: str | None = None
    empresa_id: int

class ContatoUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None

class ContatoResponse(ContatoCreate):
    id: int
    empresa_id: int

    model_config = ConfigDict(from_attributes=True)