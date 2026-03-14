"""
Testes de integração para rotas de Funcionário
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestFuncionarioRouter:
    """Testes das rotas da API de Funcionário"""

    @pytest.fixture
    def departamento(self, test_db: Session):
        """Cria um departamento para testes"""
        from rh.models.departamento import Departamento
        depto = Departamento(
            nome="Vendas",
            descricao="Departamento de Vendas"
        )
        test_db.add(depto)
        test_db.commit()
        test_db.refresh(depto)
        return depto

    def test_create_funcionario_endpoint(self, client: TestClient, test_db: Session, departamento):
        """Deve criar um funcionário via POST"""
        payload = {
            "nome": "Carlos Ferreira",
            "email": "carlos@company.com",
            "cpf": "111.333.555-66",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Vendedor",
            "salario": 3500.0,
            "departamento_id": departamento.id,
        }
        
        response = client.post("/rh/v1/funcionarios", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Carlos Ferreira"

    def test_list_funcionarios_endpoint(self, client: TestClient, test_db: Session, departamento):
        """Deve listar todos os funcionários"""
        for i in range(2):
            client.post("/rh/v1/funcionarios", json={
                "nome": f"Func RH {i}",
                "email": f"frh{i}@company.com",
                "cpf": f"222.333.444-{i:02d}",
                "data_admissao": datetime.now().isoformat(),
                "cargo": f"Cargo {i}",
                "salario": 4000.0,
                "departamento_id": departamento.id,
            })
        
        response = client.get("/rh/v1/funcionarios/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_funcionario_endpoint(self, client: TestClient, test_db: Session, departamento):
        """Deve recuperar um funcionário por ID"""
        create_response = client.post("/rh/v1/funcionarios", json={
            "nome": "Luciana Rocha",
            "email": "luciana@company.com",
            "cpf": "333.444.555-66",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Gerente de Vendas",
            "salario": 6000.0,
            "departamento_id": departamento.id,
        })
        func_id = create_response.json()["id"]
        
        response = client.get(f"/rh/v1/funcionarios/{func_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Luciana Rocha"

    def test_get_funcionario_not_found(self, client: TestClient):
        """Deve retornar 404 para funcionário inexistente"""
        response = client.get("/rh/v1/funcionarios/9999")
        
        assert response.status_code == 404

    def test_update_funcionario_endpoint(self, client: TestClient, test_db: Session, departamento):
        """Deve atualizar um funcionário via PUT"""
        create_response = client.post("/rh/v1/funcionarios", json={
            "nome": "Rafael Gomes",
            "email": "rafael@company.com",
            "cpf": "444.555.666-77",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Trainee",
            "salario": 2500.0,
            "departamento_id": departamento.id,
        })
        func_id = create_response.json()["id"]
        
        update_payload = {
            "nome": "Rafael Gomes Silva",
            "email": "rafael@company.com",
            "cpf": "444.555.666-77",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Vendedor Júnior",
            "salario": 3500.0,
            "departamento_id": departamento.id,
        }
        response = client.put(f"/rh/v1/funcionarios/{func_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["cargo"] == "Vendedor Júnior"

    def test_delete_funcionario_endpoint(self, client: TestClient, test_db: Session, departamento):
        """Deve deletar um funcionário"""
        create_response = client.post("/rh/v1/funcionarios", json={
            "nome": "Mariana Dias",
            "email": "mariana@company.com",
            "cpf": "555.666.777-88",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Analista",
            "salario": 5500.0,
            "departamento_id": departamento.id,
        })
        func_id = create_response.json()["id"]
        
        response = client.delete(f"/rh/v1/funcionarios/{func_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/rh/v1/funcionarios/{func_id}")
        assert get_response.status_code == 404
