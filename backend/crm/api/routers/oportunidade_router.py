from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crm.services.oportunidade_service import get_oportunidades, create_oportunidade, get_oportunidade, update_oportunidade, delete_oportunidade
from crm.db.session import get_db
from crm.schemas.oportunidade_schema import OportunidadeCreate, OportunidadeResponse, OportunidadeUpdate

router = APIRouter(
    prefix="/oportunidade",
    tags=["oportunidade"]
)

@router.get("/", response_model=list[OportunidadeResponse])
def read_oportunidades_router(db: Session = Depends(get_db)):
    return get_oportunidades(db)

@router.get("/{oportunidade_id}", response_model=OportunidadeResponse)
def read_oportunidade_router(oportunidade_id: int, db: Session = Depends(get_db)):
    oportunidade = get_oportunidade(db, oportunidade_id)
    if not oportunidade:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return oportunidade

@router.post("/", response_model=OportunidadeResponse)
def create_oportunidade_router(oportunidade: OportunidadeCreate, db: Session = Depends(get_db)):
    nova_oportunidade = create_oportunidade(db, oportunidade.model_dump())
    if not nova_oportunidade:
        raise HTTPException(status_code=400, detail="Erro ao criar oportunidade. Verifique os dados fornecidos.")
    return nova_oportunidade

@router.put("/{oportunidade_id}", response_model=OportunidadeResponse)
def update_oportunidade_router(oportunidade_id: int, oportunidade: OportunidadeUpdate, db: Session = Depends(get_db)):
    updated_oportunidade = update_oportunidade(db, oportunidade_id, oportunidade.model_dump())
    if not updated_oportunidade:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return updated_oportunidade

@router.delete("/{oportunidade_id}")
def delete_oportunidade_router(oportunidade_id: int, db: Session = Depends(get_db)):
    oportunidade = delete_oportunidade(db, oportunidade_id)
    if not oportunidade:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return {"message": f"Oportunidade {oportunidade_id} deletada com sucesso"}