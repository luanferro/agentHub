from pydantic import BaseModel, ConfigDict

class ItemPedidoBase(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoUpdate(ItemPedidoBase):
    pedido_id: int | None = None
    produto_id: int | None = None
    quantidade: int | None = None
    preco_unitario: float | None = None

class ItemPedidoResponse(ItemPedidoCreate):
    id: int
    pedido_id: int
    produto_id: int

    model_config = ConfigDict(from_attributes=True)