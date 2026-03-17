from fastapi import APIRouter
from gateway.schemas.chat_schema import ChatRequest, ChatResponse
from gateway.guardrails.pii_filter import filter_pii
from gateway.guardrails.token_counter import count_tokens
from gateway.config import MODELS, openai_api_key, anthropic_api_key
from openai import OpenAI
from anthropic import Anthropic

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat(request: ChatRequest):
   
    # Escolhe o modelo com base no modo selecionado
    model_info = MODELS.get(request.mode, MODELS["fast"])
    provider = model_info["provider"]
    model_name = model_info["model"]

    # Filtra informações pessoais do prompt
    filtered_prompt = filter_pii(request.prompt)

    # Conta tokens de entrada
    tokens_input = count_tokens(filtered_prompt, model_name)

    if provider == "openai":
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": filtered_prompt}]
        )
        response_text = response.choices[0].message.content
        tokens_output = response.usage.total_tokens - tokens_input

    elif provider == "anthropic":
        client = Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": filtered_prompt}]
        )
        response_text = response.content[0].text
        tokens_output = len(response_text) // 4  # Estimativa de tokens para Claude

    return ChatResponse(
        response=response_text,
        model_used=model_name,
        tokens_input=tokens_input,
        tokens_output=tokens_output
    )
