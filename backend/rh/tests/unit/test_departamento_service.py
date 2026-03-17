"""
Testes unitários para o serviço de Departamento
"""
import pytest
from sqlalchemy.orm import Session

from rh.models.departamento import Departamento
from rh.services.departamento_service import (
    get_departamentos,
    create_departamento,
    get_departamento,
    update_departamento,
    delete_departamento,
)


class TestDepartamentoService:
    """Testes da camada de serviço de Departamento"""

    def test_create_departamento(self, db_session: Session):
        """Deve criar um departamento com dados válidos"""
        depto_data = {
            "nome": "Tecnologia",
            "descricao": "Departamento de Desenvolvimento e Infraestrutura",
        }
        
        departamento = create_departamento(db_session, depto_data)
        
        assert departamento.id is not None
        assert departamento.nome == "Tecnologia"

    def test_get_departamento_by_id(self, db_session: Session):
        """Deve recuperar um departamento pelo ID"""
        depto_data = {
            "nome": "Recursos Humanos",
            "descricao": "RH e Gestão de Pessoas",
        }
        
        departamento = create_departamento(db_session, depto_data)
        retrieved = get_departamento(db_session, departamento.id)
        
        assert retrieved is not None
        assert retrieved.id == departamento.id
        assert retrieved.nome == "Recursos Humanos"

    def test_get_departamento_not_found(self, db_session: Session):
        """Deve retornar None quando departamento não existe"""
        result = get_departamento(db_session, 999)
        assert result is None

    def test_get_all_departamentos(self, db_session: Session):
        """Deve retornar todos os departamentos"""
        for i in range(3):
            create_departamento(
                db_session,
                {
                    "nome": f"Departamento {i}",
                    "descricao": f"Descrição do departamento {i}",
                }
            )
        
        departamentos = get_departamentos(db_session)
        assert len(departamentos) >= 3

    def test_update_departamento(self, db_session: Session):
        """Deve atualizar dados de um departamento"""
        depto_data = {
            "nome": "Vendas",
            "descricao": "Departamento de Vendas",
        }
        
        departamento = create_departamento(db_session, depto_data)
        updated_data = {
            "descricao": "Departamento de Vendas e Relacionamento com Clientes",
        }
        updated = update_departamento(db_session, departamento.id, updated_data)
        
        assert "Relacionamento" in updated.descricao

    def test_delete_departamento(self, db_session: Session):
        """Deve deletar um departamento"""
        depto_data = {
            "nome": "Financeiro",
            "descricao": "Departamento Financeiro",
        }
        
        departamento = create_departamento(db_session, depto_data)
        deleted = delete_departamento(db_session, departamento.id)
        
        assert deleted.id == departamento.id
        assert get_departamento(db_session, departamento.id) is None
