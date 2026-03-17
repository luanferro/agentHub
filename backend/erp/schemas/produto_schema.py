from pydantic import BaseModel, ConfigDict

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float

class ProdutoCreate(ProdutoBase):
    estoque: int | None = None

class ProdutoUpdate(ProdutoBase):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    estoque: int | None = None

class ProdutoResponse(ProdutoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

