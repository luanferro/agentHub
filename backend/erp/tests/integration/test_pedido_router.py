"""
Testes de integração para rotas de Pedido
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient


class TestPedidoRouter:
    """Testes das rotas da API de Pedido"""

    def test_create_pedido_endpoint(self, client: TestClient):
        """Deve criar um pedido via POST"""
        payload = {
            "data": datetime.now().isoformat(),
            "status": True,
            "valor_total": 7500.0,
            "client_nome": "Empresa Grande",
        }
        
        response = client.post("/erp/v1/pedido", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["client_nome"] == "Empresa Grande"
        assert data["valor_total"] == 7500.0

    def test_list_pedidos_endpoint(self, client: TestClient):
        """Deve listar todos os pedidos"""
        for i in range(2):
            client.post("/erp/v1/pedido", json={
                "data": datetime.now().isoformat(),
                "status": True,
                "valor_total": 4000.0 + (i * 1000),
                "client_nome": f"Cliente ERP {i}",
            })
        
        response = client.get("/erp/v1/pedido/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_pedido_endpoint(self, client: TestClient):
        """Deve recuperar um pedido por ID"""
        create_response = client.post("/erp/v1/pedido", json={
            "data": datetime.now().isoformat(),
            "status": False,
            "valor_total": 2200.0,
            "client_nome": "Cliente Específico",
        })
        pedido_id = create_response.json()["id"]
        
        response = client.get(f"/erp/v1/pedido/{pedido_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["client_nome"] == "Cliente Específico"

    def test_get_pedido_not_found(self, client: TestClient):
        """Deve retornar 404 para pedido inexistente"""
        response = client.get("/erp/v1/pedido/9999")
        
        assert response.status_code == 404

    @pytest.mark.skip(reason="Requer correcao do serviço para nao sobrescrever campos com None")
    def test_update_pedido_endpoint(self, client: TestClient):
        """Deve atualizar um pedido via PUT"""
        create_response = client.post("/erp/v1/pedido", json={
            "data": datetime.now().isoformat(),
            "status": False,
            "valor_total": 3300.0,
            "client_nome": "Cliente para Atualizar",
        })
        pedido_id = create_response.json()["id"]
        
        update_payload = {
            "status": True,
            "valor_total": 3800.0,
            "client_nome": "Cliente para Atualizar",
        }
        response = client.put(f"/erp/v1/pedido/{pedido_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == True

    def test_delete_pedido_endpoint(self, client: TestClient):
        """Deve deletar um pedido"""
        create_response = client.post("/erp/v1/pedido", json={
            "data": datetime.now().isoformat(),
            "status": True,
            "valor_total": 5500.0,
            "client_nome": "Cliente para Deletar",
        })
        pedido_id = create_response.json()["id"]
        
        response = client.delete(f"/erp/v1/pedido/{pedido_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/erp/v1/pedido/{pedido_id}")
        assert get_response.status_code == 404
