import re

def filter_pii(text: str) -> str:
    """Remove informações de identificação pessoal (PII) do texto."""
    
    cpf_regex = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}' 
    cpf_regex_alt = r'\d{11}'  # Formato sem pontuação
    telefone_regex = r'(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})-?\d{4}'
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    text = re.sub(email_regex, '[EMAIL]', text)
    text = re.sub(cpf_regex, '[CPF]', text)
    text = re.sub(cpf_regex_alt, '[CPF]', text)
    text = re.sub(telefone_regex, '[PHONE]', text)

    return text