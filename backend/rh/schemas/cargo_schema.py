from pydantic import BaseModel, ConfigDict

class CargoBase(BaseModel):
    nome: str
    salario_base: float

class CargoCreate(CargoBase):
    descricao: str | None = None
    departamento_id: int | None = None

class CargoUpdate(CargoBase):
    nome: str | None = None
    descricao: str | None = None
    departamento_id: int | None = None
    salario_base: float | None = None

class CargoResponse(CargoCreate):
    id: int
    departamento_id: int

    model_config = ConfigDict(from_attributes=True)