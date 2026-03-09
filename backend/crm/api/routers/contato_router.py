from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crm.services.contato_service import get_contatos, create_contato, get_contato, update_contato, delete_contato
from crm.db.session import get_db
from crm.schemas.contato_schema import ContatoCreate, ContatoResponse, ContatoUpdate


router = APIRouter(
    prefix="/contato",
    tags=["contato"]
)

@router.get("/", response_model=list[ContatoResponse])
def read_contatos_router(db: Session = Depends(get_db)):
    return get_contatos(db)

@router.get("/{contato_id}", response_model=ContatoResponse)
def read_contato_router(contato_id: int, db: Session = Depends(get_db)):
    contato = get_contato(db, contato_id)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato

@router.post("/", response_model=ContatoResponse)
def create_contato_router(contato: ContatoCreate, db: Session = Depends(get_db)):
    novo_contato = create_contato(db, contato.model_dump())
    if not novo_contato:
        raise HTTPException(status_code=400, detail="Erro ao criar contato. Verifique os dados fornecidos.")
    return novo_contato

@router.put("/{contato_id}", response_model=ContatoResponse)
def update_contato_router(contato_id: int, contato: ContatoUpdate, db: Session = Depends(get_db)):
    updated_contato = update_contato(db, contato_id, contato.model_dump())
    if not updated_contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return updated_contato

@router.delete("/{contato_id}")
def delete_contato_router(contato_id: int, db: Session = Depends(get_db)):
    contato = delete_contato(db, contato_id)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return {"message": f"Contato {contato_id} deletado com sucesso"}