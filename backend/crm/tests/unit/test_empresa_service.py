"""
Testes unitários para o serviço de Empresa
"""
import pytest
from sqlalchemy.orm import Session

from crm.models.empresa import Empresa
from crm.services.empresa_service import (
    get_empresas,
    create_empresa,
    get_empresa,
    update_empresa,
    delete_empresa,
)


class TestEmpresaService:
    """Testes da camada de serviço de Empresa"""

    def test_create_empresa(self, db_session: Session):
        """Deve criar uma empresa com dados válidos"""
        empresa_data = {
            "nome": "Acme Corporation",
            "cnpj": "12.345.678/0001-99",
            "razao_social": "Acme Corp Brasil",
            "ramo": "Tecnologia",
            "endereco": "São Paulo, SP",
        }
        
        empresa = create_empresa(db_session, empresa_data)
        
        assert empresa.id is not None
        assert empresa.nome == "Acme Corporation"
        assert empresa.cnpj == "12.345.678/0001-99"

    def test_get_empresa_by_id(self, db_session: Session):
        """Deve recuperar uma empresa pelo ID"""
        empresa_data = {
            "nome": "Tech Solutions",
            "cnpj": "98.765.432/0001-11",
            "razao_social": "Tech Solutions LTDA",
        }
        
        empresa = create_empresa(db_session, empresa_data)
        retrieved = get_empresa(db_session, empresa.id)
        
        assert retrieved is not None
        assert retrieved.id == empresa.id
        assert retrieved.nome == "Tech Solutions"

    def test_get_empresa_not_found(self, db_session: Session):
        """Deve retornar None quando empresa não existe"""
        result = get_empresa(db_session, 999)
        assert result is None

    def test_get_all_empresas(self, db_session: Session):
        """Deve retornar todas as empresas"""
        for i in range(3):
            create_empresa(
                db_session,
                {
                    "nome": f"Empresa {i}",
                    "cnpj": f"00.000.00{i}/0001-00",
                }
            )
        
        empresas = get_empresas(db_session)
        assert len(empresas) == 3

    def test_update_empresa(self, db_session: Session):
        """Deve atualizar dados de uma empresa"""
        empresa_data = {
            "nome": "Old Name",
            "cnpj": "11.111.111/0001-11",
        }
        
        empresa = create_empresa(db_session, empresa_data)
        updated_data = {"nome": "New Name", "ramo": "Financeiro"}
        updated = update_empresa(db_session, empresa.id, updated_data)
        
        assert updated.nome == "New Name"
        assert updated.ramo == "Financeiro"

    def test_delete_empresa(self, db_session: Session):
        """Deve deletar uma empresa"""
        empresa_data = {
            "nome": "To Delete",
            "cnpj": "22.222.222/0001-22",
        }
        
        empresa = create_empresa(db_session, empresa_data)
        deleted = delete_empresa(db_session, empresa.id)
        
        assert deleted.id == empresa.id
        assert get_empresa(db_session, empresa.id) is None

    def test_delete_nonexistent_empresa(self, db_session: Session):
        """Deve retornar None ao deletar empresa inexistente"""
        result = delete_empresa(db_session, 999)
        assert result is None
