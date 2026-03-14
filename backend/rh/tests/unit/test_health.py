"""
Testes básicos de exemplo para RH
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthCheck:
    """Testes básicos de saúde da API"""

    def test_root_endpoint(self, client: TestClient):
        """Deve retornar mensagem de boas-vindas"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "Welcome" in response.json()["message"]
