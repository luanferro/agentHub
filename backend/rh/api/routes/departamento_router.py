from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from rh.services.departamento_service import get_departamentos, get_departamento, create_departamento, update_departamento, delete_departamento
from rh.db.session import get_db
from rh.schemas.departamento_schema import DepartamentoCreate, DepartamentoResponse, DepartamentoUpdate

router = APIRouter(
    prefix="/departamentos",
    tags=["departamentos"]
)

@router.get("/", response_model=list[DepartamentoResponse])
def read_departamentos_router(db: Session = Depends(get_db)):
    return get_departamentos(db)

@router.get("/{departamento_id}", response_model=DepartamentoResponse)
def read_departamento_router(departamento_id: int, db: Session = Depends(get_db)):
    departamento = get_departamento(db, departamento_id)
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return departamento

@router.post("/", response_model=DepartamentoResponse)
def create_departamento_router(departamento: DepartamentoCreate, db: Session = Depends(get_db)):
    novo_departamento = create_departamento(db, departamento.model_dump())
    if not novo_departamento:
        raise HTTPException(status_code=400, detail="Erro ao criar departamento. Verifique os dados fornecidos.")
    return novo_departamento

@router.put("/{departamento_id}", response_model=DepartamentoResponse)
def update_departamento_router(departamento_id: int, departamento: DepartamentoUpdate, db: Session = Depends(get_db)):
    updated_departamento = update_departamento(db, departamento_id, departamento.model_dump())
    if not updated_departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return updated_departamento

@router.delete("/{departamento_id}")
def delete_departamento_router(departamento_id: int, db: Session = Depends(get_db)):
    departamento = delete_departamento(db, departamento_id)
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return {"message": f"Departamento {departamento_id} deletado com sucesso"}