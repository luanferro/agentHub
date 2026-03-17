from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from erp.db.session import get_db
from erp.services.produto_service import get_all_produtos, get_produto, update_produto, create_produto, delete_produto
from erp.schemas.produto_schema import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(
    prefix="/produto",
    tags=["produto"]
)

@router.get("/", response_model=list[ProdutoResponse])
def read_all_produtos_router(db: Session = Depends(get_db)):
    return get_all_produtos(db)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def read_produto_router(produto_id: int, db: Session = Depends(get_db)):
    produto = get_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoResponse)
def create_produto_router(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = create_produto(db, produto.model_dump())
    if not novo_produto:
        raise HTTPException(status_code=400, detail="Erro ao criar produto. Verifique os dados fornecidos")
    return novo_produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
def update_produto_router(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    updated_produto = update_produto(db, produto_id, produto.model_dump())
    if not updated_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_produto

@router.delete("/{produto_id}")
def delete_produto_router(produto_id: int, db: Session = Depends(get_db)):
    produto = delete_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": f"Produto {produto_id} deletado com sucesso"}
