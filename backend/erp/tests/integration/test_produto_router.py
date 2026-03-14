"""
Testes de integração para rotas de Produto
"""
import pytest
from fastapi.testclient import TestClient


class TestProdutoRouter:
    """Testes das rotas da API de Produto"""

    def test_create_produto_endpoint(self, client: TestClient):
        """Deve criar um produto via POST"""
        payload = {
            "nome": "Webcam HD",
            "descricao": "Webcam Full HD com microfone",
            "preco": 350.0,
            "estoque": 30,
        }
        
        response = client.post("/erp/v1/produto", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Webcam HD"
        assert data["preco"] == 350.0

    def test_list_produtos_endpoint(self, client: TestClient):
        """Deve listar todos os produtos"""
        for i in range(2):
            client.post("/erp/v1/produto", json={
                "nome": f"Produto ERP {i}",
                "descricao": f"Descrição do produto {i}",
                "preco": 200.0 + (i * 100),
            })
        
        response = client.get("/erp/v1/produto/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_produto_endpoint(self, client: TestClient):
        """Deve recuperar um produto por ID"""
        create_response = client.post("/erp/v1/produto", json={
            "nome": "SSD 1TB",
            "descricao": "SSD NVMe 1TB rápido",
            "preco": 800.0,
        })
        produto_id = create_response.json()["id"]
        
        response = client.get(f"/erp/v1/produto/{produto_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "SSD 1TB"

    def test_get_produto_not_found(self, client: TestClient):
        """Deve retornar 404 para produto inexistente"""
        response = client.get("/erp/v1/produto/9999")
        
        assert response.status_code == 404

    def test_update_produto_endpoint(self, client: TestClient):
        """Deve atualizar um produto via PUT"""
        create_response = client.post("/erp/v1/produto", json={
            "nome": "Fone Bluetooth",
            "descricao": "Fone com rastreamento por GPS",
            "preco": 250.0,
        })
        produto_id = create_response.json()["id"]
        
        update_payload = {
            "nome": "Fone Bluetooth",
            "descricao": "Fone Bluetooth com bateria de 20h",
            "preco": 300.0,
        }
        response = client.put(f"/erp/v1/produto/{produto_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["preco"] == 300.0

    def test_delete_produto_endpoint(self, client: TestClient):
        """Deve deletar um produto"""
        create_response = client.post("/erp/v1/produto", json={
            "nome": "Hub USB",
            "descricao": "Hub USB 3.0 com 7 portas",
            "preco": 120.0,
        })
        produto_id = create_response.json()["id"]
        
        response = client.delete(f"/erp/v1/produto/{produto_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/erp/v1/produto/{produto_id}")
        assert get_response.status_code == 404
