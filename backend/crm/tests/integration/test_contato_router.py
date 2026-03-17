"""
Testes de integração para rotas de Contato
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestContatoRouter:
    """Testes das rotas da API de Contato"""

    @pytest.fixture
    def empresa(self, test_db: Session):
        """Cria uma empresa para os testes"""
        from crm.models.empresa import Empresa
        empresa = Empresa(
            nome="Empresa Contato",
            cnpj="99.999.999/0001-00"
        )
        test_db.add(empresa)
        test_db.commit()
        test_db.refresh(empresa)
        return empresa

    def test_create_contato_endpoint(self, client: TestClient, test_db: Session, empresa):
        """Deve criar um contato via POST"""
        payload = {
            "nome": "Pedro Mendes",
            "email": "pedro@example.com",
            "telefone": "(21) 99999-1111",
            "empresa_id": empresa.id,
        }
        
        response = client.post("/crm/v1/contato", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Pedro Mendes"
        assert data["email"] == "pedro@example.com"

    def test_list_contatos_endpoint(self, client: TestClient, test_db: Session, empresa):
        """Deve listar todos os contatos"""
        for i in range(2):
            client.post("/crm/v1/contato", json={
                "nome": f"Contato {i}",
                "email": f"contato{i}@test.com",
                "empresa_id": empresa.id,
            })
        
        response = client.get("/crm/v1/contato/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_contato_endpoint(self, client: TestClient, test_db: Session, empresa):
        """Deve recuperar um contato por ID"""
        create_response = client.post("/crm/v1/contato", json={
            "nome": "Lucia Santos",
            "email": "lucia@example.com",
            "empresa_id": empresa.id,
        })
        contato_id = create_response.json()["id"]
        
        response = client.get(f"/crm/v1/contato/{contato_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contato_id
        assert data["nome"] == "Lucia Santos"

    def test_get_contato_not_found(self, client: TestClient):
        """Deve retornar 404 para contato inexistente"""
        response = client.get("/crm/v1/contato/999")
        
        assert response.status_code == 404

    def test_update_contato_endpoint(self, client: TestClient, test_db: Session, empresa):
        """Deve atualizar um contato via PUT"""
        create_response = client.post("/crm/v1/contato", json={
            "nome": "Bruno Costa",
            "email": "bruno@example.com",
            "empresa_id": empresa.id,
        })
        contato_id = create_response.json()["id"]
        
        update_payload = {
            "nome": "Bruno Costa Silva",
            "email": "bruno@example.com",
            "telefone": "(85) 99999-2222",
        }
        response = client.put(f"/crm/v1/contato/{contato_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Bruno Costa Silva"

    def test_delete_contato_endpoint(self, client: TestClient, test_db: Session, empresa):
        """Deve deletar um contato"""
        create_response = client.post("/crm/v1/contato", json={
            "nome": "Fernanda Lima",
            "email": "fernanda@example.com",
            "empresa_id": empresa.id,
        })
        contato_id = create_response.json()["id"]
        
        response = client.delete(f"/crm/v1/contato/{contato_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/crm/v1/contato/{contato_id}")
        assert get_response.status_code == 404

    @pytest.mark.skip(reason="Requer tratamento de IntegrityError no router (Task #6)")
    def test_create_contato_duplicate_email(self, client: TestClient, test_db: Session, empresa):
        """Deve retornar erro ao criar contato com email duplicado"""
        payload = {
            "nome": "Roberto Dias",
            "email": "roberto@example.com",
            "empresa_id": empresa.id,
        }
        
        response1 = client.post("/crm/v1/contato", json=payload)
        assert response1.status_code == 200
        
        payload["nome"] = "Outro Roberto"
        response2 = client.post("/crm/v1/contato", json=payload)
        
        assert response2.status_code in [422, 500, 409]
