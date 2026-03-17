from fastapi import FastAPI
from gateway.routers.chat import router as chat_router

app = FastAPI(title="AI Gateway", version="1.0")

app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Gateway"}