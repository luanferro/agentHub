import httpx
from server import mcp
from config import RH_API_URL

@mcp.tool()
async def listar_funcionarios() -> str:
    """Lista todos os funcionários cadastrados no RH."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RH_API_URL}/api/v1/funcionario/")
        return response.text

@mcp.tool()
async def buscar_funcionario(funcionario_id: str) -> str:
    """Lista um funcionário cadastrado no RH a partir do ID do funcionário"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RH_API_URL}/api/v1/funcionario/{funcionario_id}")
        return response.text
    
@mcp.tool()
async def criar_funcionario(nome: str, email: str, cpf: str, data_admissao: str, cargo: str, salario: float) -> str:
    """Cria um novo funcionário no RH."""
    async with httpx.AsyncClient() as client:
        payload = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "data_admissao": data_admissao,
            "cargo": cargo,
            "salario": salario
        }
        response = await client.post(f"{RH_API_URL}/api/v1/funcionario/", json=payload)
        return response.text    

@mcp.tool()
async def listar_departamentos() -> str:
    """Lista todos os departamentos cadastrados no RH."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RH_API_URL}/api/v1/departamento/")
        return response.text
    
@mcp.tool()
async def buscar_departamento(departamento_id: str) -> str:
    """Lista um departamento cadastrado no RH a partir do ID do departamento"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RH_API_URL}/api/v1/departamento/{departamento_id}")
        return response.text

@mcp.tool()
async def criar_departamento(nome: str, descricao: str) -> str:
    """Cria um novo departamento no RH."""
    async with httpx.AsyncClient() as client:
        payload = {
            "nome": nome,
            "descricao": descricao
        }
        response = await client.post(f"{RH_API_URL}/api/v1/departamento/", json=payload)
        return response.text