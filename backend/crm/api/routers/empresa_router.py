from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crm.services.empresa_service import get_empresas, create_empresa, get_empresa, update_empresa, delete_empresa
from crm.db.session import get_db
from crm.schemas.empresa_schema import EmpresaCreate, EmpresaResponse, EmpresaUpdate

router = APIRouter(
    prefix="/empresa",
    tags=["empresa"]
)

@router.get("/", response_model=list[EmpresaResponse])
def read_empresas_router(db: Session = Depends(get_db)):
    return get_empresas(db)

@router.post("/", response_model=EmpresaResponse)
def create_empresa_router(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    nova_empresa = create_empresa(db, empresa.model_dump()) 
    return nova_empresa

@router.get("/{empresa_id}", response_model=EmpresaResponse)
def read_empresa_router(empresa_id: int, db: Session = Depends(get_db)):
    empresa = get_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@router.put("/{empresa_id}", response_model=EmpresaResponse)
def update_empresa_router(empresa_id: int, empresa: EmpresaUpdate, db: Session = Depends(get_db)):
    updated_empresa = update_empresa(db, empresa_id, empresa.model_dump())
    if not updated_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return updated_empresa

@router.delete("/{empresa_id}")
def delete_empresa_router(empresa_id: int, db: Session = Depends(get_db)):
    empresa = delete_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return {"message": f"Empresa {empresa_id} deletada com sucesso"}