from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PedidoBase(BaseModel):
    data: datetime
    status: bool
    valor_total: float
    client_nome: str

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    data: str | None = None
    status: bool | None = None
    valor_total: float | None = None
    client_nome: str | None = None

class PedidoResponse(PedidoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)