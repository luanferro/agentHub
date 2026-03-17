from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from rh.services.funcionario_service import get_funcionarios, get_funcionario, create_funcionario, update_funcionario, delete_funcionario
from rh.db.session import get_db
from rh.schemas.funcionario_schema import FuncionarioCreate, FuncionarioResponse, FuncionarioUpdate

router = APIRouter(
    prefix="/funcionarios",
    tags=["funcionarios"]
)

@router.get("/", response_model=list[FuncionarioResponse])
def read_funcionarios_router(db: Session = Depends(get_db)):
    return get_funcionarios(db)
    
@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
def read_funcionario_router(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = get_funcionario(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.post("/", response_model=FuncionarioResponse)
def create_funcionario_router(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    novo_funcionario = create_funcionario(db, funcionario.model_dump())
    if not novo_funcionario:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário. Verifique os dados fornecidos.")
    return novo_funcionario

@router.put("/{funcionario_id}", response_model=FuncionarioResponse)
def update_funcionario_router(funcionario_id: int, funcionario: FuncionarioUpdate, db: Session = Depends(get_db)):
    updated_funcionario = update_funcionario(db, funcionario_id, funcionario.model_dump())
    if not updated_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return updated_funcionario

@router.delete("/{funcionario_id}")
def delete_funcionario_router(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = delete_funcionario(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"message": f"Funcionário {funcionario_id} deletado com sucesso"}