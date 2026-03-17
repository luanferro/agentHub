import os

MODELS = {
    "fast": {
        "provider": "openai",
        "model": "gpt-4o-mini"
    },
    "smart": {
        "provider": "anthropic", 
        "model": "claude-3-5-haiku-20241022"
    }
}

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")