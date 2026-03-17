from pydantic import BaseModel

class ChatRequest(BaseModel):
    mode: str = "fast"  # default to "fast" model   
    prompt: str

class ChatResponse(BaseModel):
    response: str
    model_used: str
    tokens_input: int
    tokens_output: int