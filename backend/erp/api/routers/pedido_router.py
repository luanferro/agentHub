from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from erp.db.session import get_db
from erp.services.pedido_service import get_all_pedidos, get_pedido, create_pedido, update_pedido, delete_pedido
from erp.schemas.pedido_schema import PedidoCreate, PedidoResponse, PedidoUpdate

router = APIRouter(
    prefix="/pedido",
    tags=["pedido"]
)

@router.get("/", response_model=list[PedidoResponse])
def read_all_pedidos_router(db: Session = Depends(get_db)):
    return get_all_pedidos(db)

@router.get("/{pedido_id}", response_model=PedidoResponse)
def read_pedido_router(pedido_id: int, db: Session = Depends(get_db)):
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/", response_model=PedidoResponse)
def create_pedido_router(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = create_pedido(db, pedido.model_dump())
    if not novo_pedido:
        raise HTTPException(status_code=400, detail="Erro ao criar pedido. Verifique os dados fornecidos")
    return novo_pedido

@router.put("/{pedido_id}", response_model=PedidoResponse)
def update_pedido_router(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    updated_pedido = update_pedido(db, pedido_id, pedido.model_dump())
    if not updated_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return updated_pedido

@router.delete("/{pedido_id}")
def delete_pedido_router(pedido_id: int, db: Session = Depends(get_db)):
    pedido = delete_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": f"Pedido {pedido_id} deletado com sucesso"}
