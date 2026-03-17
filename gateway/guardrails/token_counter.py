import tiktoken
from anthropic import Anthropic

def count_tokens(text: str, model: str) -> int:
    """Conta o número de tokens em um texto para um modelo específico."""
    
    if model == "gpt-4o-mini":
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)
        return len(tokens)
    elif model == "claude-3-5-haiku-20241022":
        return len(text) // 4

