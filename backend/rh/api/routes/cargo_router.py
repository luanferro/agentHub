from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from rh.services.cargo_service import get_cargos, get_cargo, create_cargo, update_cargo, delete_cargo
from rh.db.session import get_db
from rh.schemas.cargo_schema import CargoCreate, CargoResponse, CargoUpdate

router = APIRouter(
    prefix="/cargos",
    tags=["cargos"]
)

@router.get("/", response_model=list[CargoResponse])
def read_cargos_router(db: Session = Depends(get_db)):
    return get_cargos(db)

@router.get("/{cargo_id}", response_model=CargoResponse)
def read_cargo_router(cargo_id: int, db: Session = Depends(get_db)):
    cargo = get_cargo(db, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return cargo

@router.post("/", response_model=CargoResponse)
def create_cargo_router(cargo: CargoCreate, db: Session = Depends(get_db)):
    novo_cargo = create_cargo(db, cargo.model_dump())
    if not novo_cargo:
        raise HTTPException(status_code=400, detail="Erro ao criar cargo. Verifique os dados fornecidos.")
    return novo_cargo

@router.put("/{cargo_id}", response_model=CargoResponse)
def update_cargo_router(cargo_id: int, cargo: CargoUpdate, db: Session = Depends(get_db)):
    updated_cargo = update_cargo(db, cargo_id, cargo.model_dump())
    if not updated_cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return updated_cargo

@router.delete("/{cargo_id}")
def delete_cargo_router(cargo_id: int, db: Session = Depends(get_db)):
    cargo = delete_cargo(db, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return {"message": f"Cargo {cargo_id} deletado com sucesso"}