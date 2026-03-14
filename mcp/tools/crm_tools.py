import httpx
from server import mcp

from config import CRM_API_URL

@mcp.tool()
async def listar_empresas() -> str:
    """Lista todas as empresas cadastradas no CRM."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CRM_API_URL}/api/v1/empresa/")
        return response.text
    
@mcp.tool()
async def buscar_empresa(empresa_id: str) -> str:
    """Lista uma empresa cadastrada no CRM a partir do ID da empresa"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CRM_API_URL}/api/v1/empresa/{empresa_id}")
        return response.text
    
@mcp.tool()
async def criar_empresa(nome: str, cnpj: str, endereco: str, ramo: str, razao_social: str) -> str:
    """Cria uma nova empresa no CRM."""
    async with httpx.AsyncClient() as client:
        payload = {
            "nome": nome,
            "cnpj": cnpj,
            "endereco": endereco,
            "ramo": ramo,
            "razao_social": razao_social
        }
        response = await client.post(f"{CRM_API_URL}/api/v1/empresa/", json=payload)
        return response.text
    
@mcp.tool()
async def listar_contatos() -> str:
    """Lista todos os contatos cadastrados no CRM."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CRM_API_URL}/api/v1/contato/")
        return response.text
    
@mcp.tool()
async def buscar_contato(contato_id: str) -> str:
    """Lista um contato cadastrado no CRM a partir do ID do contato"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CRM_API_URL}/api/v1/contato/{contato_id}")
        return response.text
    
@mcp.tool()
async def criar_contato(nome: str, email: str, telefone: str, empresa_id: int) -> str:
    """Cria um novo contato no CRM."""
    async with httpx.AsyncClient() as client:
        payload = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "empresa_id": empresa_id
        }
        response = await client.post(f"{CRM_API_URL}/api/v1/contato/", json=payload)
        return response.text