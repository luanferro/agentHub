"""
Testes unitários para o serviço de Contato
"""
import pytest
from sqlalchemy.orm import Session

from crm.models.empresa import Empresa
from crm.models.contato import Contato
from crm.services.contato_service import (
    get_contatos,
    create_contato,
    get_contato,
    update_contato,
    delete_contato,
)


class TestContatoService:
    """Testes da camada de serviço de Contato"""

    @pytest.fixture
    def empresa(self, db_session: Session):
        """Cria uma empresa para os testes de contato"""
        empresa = Empresa(
            nome="Empresa Teste",
            cnpj="12.345.678/0001-99"
        )
        db_session.add(empresa)
        db_session.commit()
        db_session.refresh(empresa)
        return empresa

    def test_create_contato(self, db_session: Session, empresa):
        """Deve criar um contato com dados válidos"""
        contato_data = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "telefone": "(11) 99999-9999",
            "empresa_id": empresa.id,
        }
        
        contato = create_contato(db_session, contato_data)
        
        assert contato.id is not None
        assert contato.nome == "João Silva"
        assert contato.email == "joao@example.com"

    def test_get_contato_by_id(self, db_session: Session, empresa):
        """Deve recuperar um contato pelo ID"""
        contato_data = {
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "empresa_id": empresa.id,
        }
        
        contato = create_contato(db_session, contato_data)
        retrieved = get_contato(db_session, contato.id)
        
        assert retrieved is not None
        assert retrieved.id == contato.id
        assert retrieved.nome == "Maria Santos"

    def test_get_contato_not_found(self, db_session: Session):
        """Deve retornar None quando contato não existe"""
        result = get_contato(db_session, 999)
        assert result is None

    def test_get_all_contatos(self, db_session: Session, empresa):
        """Deve retornar todos os contatos"""
        for i in range(3):
            create_contato(
                db_session,
                {
                    "nome": f"Contato {i}",
                    "email": f"contato{i}@example.com",
                    "empresa_id": empresa.id,
                }
            )
        
        contatos = get_contatos(db_session)
        assert len(contatos) == 3

    def test_update_contato(self, db_session: Session, empresa):
        """Deve atualizar dados de um contato"""
        contato_data = {
            "nome": "Carlos Oliveira",
            "email": "carlos@example.com",
            "empresa_id": empresa.id,
        }
        
        contato = create_contato(db_session, contato_data)
        updated_data = {
            "nome": "Carlos Oliveira Silva",
            "telefone": "(11) 99999-8888",
        }
        updated = update_contato(db_session, contato.id, updated_data)
        
        assert updated.nome == "Carlos Oliveira Silva"
        assert updated.telefone == "(11) 99999-8888"

    def test_delete_contato(self, db_session: Session, empresa):
        """Deve deletar um contato"""
        contato_data = {
            "nome": "Ana Costa",
            "email": "ana@example.com",
            "empresa_id": empresa.id,
        }
        
        contato = create_contato(db_session, contato_data)
        deleted = delete_contato(db_session, contato.id)
        
        assert deleted.id == contato.id
        assert get_contato(db_session, contato.id) is None
