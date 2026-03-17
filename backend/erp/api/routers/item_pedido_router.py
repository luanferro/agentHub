from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from erp.db.session import get_db
from erp.services.item_pedido_service import get_all_itens_pedidos, get_item_pedido, create_item_pedido, update_item_pedido, delete_item_pedido
from erp.schemas.item_pedido_schema import ItemPedidoResponse, ItemPedidoCreate, ItemPedidoUpdate

router = APIRouter(
    prefix="/item",
    tags=["item"]
)

@router.get("/", response_model=list[ItemPedidoResponse])
def read_all_itens_router(db: Session = Depends(get_db)):
    return get_all_itens_pedidos(db)

@router.get("/{item_pedido_id}", response_model=ItemPedidoResponse)
def read_item_router(item_pedido_id: int, db: Session = Depends(get_db)):
    item = get_item_pedido(db, item_pedido_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.post("/", response_model=ItemPedidoResponse)
def create_item_router(item: ItemPedidoCreate, db: Session = Depends(get_db)):
    novo_item = create_item_pedido(db, item.model_dump())
    if not novo_item:
        raise HTTPException(status_code=400, detail="Erro ao criar item. Verifique os dados fornecidos")
    return novo_item

@router.put("/{item_pedido_id}", response_model=ItemPedidoResponse)
def update_item_router(item_pedido_id: int, item: ItemPedidoUpdate, db: Session = Depends(get_db)):
    updated_item = update_item_pedido(db, item_pedido_id, item.model_dump())
    if not updated_item:
        raise HTTPException(status_code=404, detail="item não encontrado")
    return updated_item

@router.delete("/{item_pedido_id}")
def delete_item_router(item_pedido_id: int, db: Session = Depends(get_db)):
    item = delete_item_pedido(db, item_pedido_id)
    if not item:
        raise HTTPException(status_code=404, detail="item não encontrado")
    return {"message": f"item {item_pedido_id} deletado com sucesso"}
