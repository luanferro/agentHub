from fastapi import FastAPI

from rh.api.routes.cargo_router import router as cargo_router
from rh.api.routes.departamento_router import router as departamento_router
from rh.api.routes.funcionario_router import router as funcionario_router

app = FastAPI(title="RH API", version="1.0")

app.include_router(cargo_router, prefix="/rh/v1")
app.include_router(departamento_router, prefix="/rh/v1")
app.include_router(funcionario_router, prefix="/rh/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RH API"}