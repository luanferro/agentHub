"""
Testes de integração para rotas de Departamento
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestDepartamentoRouter:
    """Testes das rotas da API de Departamento"""

    def test_create_departamento_endpoint(self, client: TestClient):
        """Deve criar um departamento via POST"""
        payload = {
            "nome": "Marketing",
            "descricao": "Departamento de Marketing Digital",
        }
        
        response = client.post("/rh/v1/departamentos", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Marketing"

    def test_list_departamentos_endpoint(self, client: TestClient):
        """Deve listar todos os departamentos"""
        for i in range(2):
            client.post("/rh/v1/departamentos", json={
                "nome": f"Depto {i}",
                "descricao": f"Descrição {i}",
            })
        
        response = client.get("/rh/v1/departamentos/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_departamento_endpoint(self, client: TestClient):
        """Deve recuperar um departamento por ID"""
        create_response = client.post("/rh/v1/departamentos", json={
            "nome": "Operações",
            "descricao": "Departamento de Operações",
        })
        depto_id = create_response.json()["id"]
        
        response = client.get(f"/rh/v1/departamentos/{depto_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Operações"

    def test_get_departamento_not_found(self, client: TestClient):
        """Deve retornar 404 para departamento inexistente"""
        response = client.get("/rh/v1/departamentos/9999")
        
        assert response.status_code == 404

    def test_update_departamento_endpoint(self, client: TestClient, test_db: Session):
        """Deve atualizar um departamento via PUT"""
        create_response = client.post("/rh/v1/departamentos", json={
            "nome": "Logística",
            "descricao": "Departamento de Logística",
        })
        depto_id = create_response.json()["id"]
        
        update_payload = {
            "nome": "Logística",
            "descricao": "Departamento de Logística e Supply Chain",
        }
        response = client.put(f"/rh/v1/departamentos/{depto_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "Supply Chain" in data["descricao"]

    def test_delete_departamento_endpoint(self, client: TestClient):
        """Deve deletar um departamento"""
        create_response = client.post("/rh/v1/departamentos", json={
            "nome": "Qualidade",
            "descricao": "Departamento de Qualidade",
        })
        depto_id = create_response.json()["id"]
        
        response = client.delete(f"/rh/v1/departamentos/{depto_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/rh/v1/departamentos/{depto_id}")
        assert get_response.status_code == 404
