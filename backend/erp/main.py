from fastapi import FastAPI
from erp.api.routers.pedido_router import router as pedido_router
from erp.api.routers.produto_router import router as produto_router  
from erp.api.routers.item_pedido_router import router as item_router

app = FastAPI(title="ERP API", version="1.0")

app.include_router(pedido_router, prefix="/erp/v1")
app.include_router(produto_router, prefix="/erp/v1")
app.include_router(item_router, prefix="/erp/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the ERP API"}