from fastapi import FastAPI
from crm.api.routers.empresa_router import router as empresa_router
from crm.api.routers.oportunidade_router import router as oportunidade_router  
from crm.api.routers.contato_router import router as contato_router

app = FastAPI(title="CRM API", version="1.0")

app.include_router(empresa_router, prefix="/crm/v1")
app.include_router(oportunidade_router, prefix="/crm/v1")
app.include_router(contato_router, prefix="/crm/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRM API"}