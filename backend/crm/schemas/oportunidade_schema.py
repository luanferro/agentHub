from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OportunidadeBase(BaseModel):
    tipo_negocio: str

class OportunidadeCreate(OportunidadeBase):
    custo: float | None = None
    lucro: float | None = None
    data: datetime
    responsavel: str
    empresa_id: int
    contato_id: int

class OportunidadeUpdate(BaseModel):
    tipo_negocio: str | None = None
    custo: float | None = None
    lucro: float | None = None
    data: datetime | None = None
    responsavel: str | None = None

class OportunidadeResponse(OportunidadeCreate):
    id: int
    empresa_id: int
    contato_id: int

    model_config = ConfigDict(from_attributes=True)