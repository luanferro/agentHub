"""
Testes de integração para rotas de Oportunidade
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestOportunidadeRouter:
    """Testes das rotas da API de Oportunidade"""

    @pytest.fixture
    def setup_data(self, test_db: Session):
        """Cria empresa e contato para testes"""
        from crm.models.empresa import Empresa
        from crm.models.contato import Contato
        
        empresa = Empresa(
            nome="Empresa Oport",
            cnpj="88.888.888/0001-88"
        )
        test_db.add(empresa)
        test_db.commit()
        
        contato = Contato(
            nome="Contato Oport",
            email="oport@test.com",
            empresa_id=empresa.id
        )
        test_db.add(contato)
        test_db.commit()
        test_db.refresh(contato)
        
        return empresa, contato

    def test_create_oportunidade_endpoint(self, client: TestClient, test_db: Session, setup_data):
        """Deve criar uma oportunidade via POST"""
        empresa, contato = setup_data
        
        payload = {
            "tipo_negocio": "Venda Grande",
            "custo": 10000.0,
            "lucro": 30000.0,
            "data": datetime.now().isoformat(),
            "responsavel": "Vendedor Top",
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        }
        
        response = client.post("/crm/v1/oportunidade", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["tipo_negocio"] == "Venda Grande"

    def test_list_oportunidades_endpoint(self, client: TestClient, test_db: Session, setup_data):
        """Deve listar todas as oportunidades"""
        empresa, contato = setup_data
        
        for i in range(2):
            client.post("/crm/v1/oportunidade", json={
                "tipo_negocio": f"Oportunidade {i}",
                "responsavel": f"Responsável {i}",
                "data": datetime.now().isoformat(),
                "empresa_id": empresa.id,
                "contato_id": contato.id,
            })
        
        response = client.get("/crm/v1/oportunidade/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_oportunidade_endpoint(self, client: TestClient, test_db: Session, setup_data):
        """Deve recuperar uma oportunidade por ID"""
        empresa, contato = setup_data
        
        create_response = client.post("/crm/v1/oportunidade", json={
            "tipo_negocio": "Projeto Web",
            "responsavel": "Dev Lead",
            "data": datetime.now().isoformat(),
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        })
        oportunidade_id = create_response.json()["id"]
        
        response = client.get(f"/crm/v1/oportunidade/{oportunidade_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["tipo_negocio"] == "Projeto Web"

    def test_delete_oportunidade_endpoint(self, client: TestClient, test_db: Session, setup_data):
        """Deve deletar uma oportunidade"""
        empresa, contato = setup_data
        
        create_response = client.post("/crm/v1/oportunidade", json={
            "tipo_negocio": "Partnership",
            "responsavel": "Biz Dev",
            "data": datetime.now().isoformat(),
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        })
        oportunidade_id = create_response.json()["id"]
        
        response = client.delete(f"/crm/v1/oportunidade/{oportunidade_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/crm/v1/oportunidade/{oportunidade_id}")
        assert get_response.status_code == 404
