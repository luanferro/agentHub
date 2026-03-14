import httpx
from mcp.server.fastmcp import FastMCP
from config import ERP_API_URL
from datetime import datetime

mcp = FastMCP("AgentHub")

@mcp.tool()
async def listar_produtos() -> str:
    """Lista todos os produtos cadastrados no ERP."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ERP_API_URL}/api/v1/produto/")
        return response.text
    
@mcp.tool()
async def buscar_produto(produto_id: str) -> str:
    """Lista um produto cadastrado no ERP a partir do ID do produto"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ERP_API_URL}/api/v1/produto/{produto_id}")
        return response.text
    
@mcp.tool()
async def criar_produto(nome: str, descricao: str, preco: float, estoque: int) -> str:
    """Cria um novo produto no ERP."""
    async with httpx.AsyncClient() as client:
        payload = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque
        }
        response = await client.post(f"{ERP_API_URL}/api/v1/produto/", json=payload)
        return response.text

@mcp.tool()
async def listar_pedidos() -> str:
    """Lista todos os pedidos cadastrados no ERP."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ERP_API_URL}/api/v1/pedido/")
        return response.text

@mcp.tool()
async def buscar_pedido(pedido_id: str) -> str:
    """Lista um pedido cadastrado no ERP a partir do ID do pedido"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ERP_API_URL}/api/v1/pedido/{pedido_id}")
        return response.text
    
@mcp.tool()
async def criar_pedido(data: datetime, status: bool, valor_total: float, client_nome: str) -> str:
    """Cria um novo pedido no ERP."""
    async with httpx.AsyncClient() as client:
        payload = {
            "data": data,
            "status": status,
            "valor_total": valor_total,
            "client_nome": client_nome
        }
        response = await client.post(f"{ERP_API_URL}/api/v1/pedido/", json=payload)
        return response.text    

    