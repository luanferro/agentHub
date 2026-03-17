"""
Testes unitários para o serviço de Oportunidade
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from crm.models.empresa import Empresa
from crm.models.contato import Contato
from crm.models.oportunidade import Oportunidade
from crm.services.oportunidade_service import (
    get_oportunidades,
    create_oportunidade,
    get_oportunidade,
    update_oportunidade,
    delete_oportunidade,
)


class TestOportunidadeService:
    """Testes da camada de serviço de Oportunidade"""

    @pytest.fixture
    def setup_data(self, db_session: Session):
        """Cria empresa e contato para testes de oportunidade"""
        empresa = Empresa(
            nome="Empresa Oportunidade",
            cnpj="11.111.111/0001-11"
        )
        db_session.add(empresa)
        db_session.commit()
        
        contato = Contato(
            nome="Contato Teste",
            email="contato@test.com",
            empresa_id=empresa.id
        )
        db_session.add(contato)
        db_session.commit()
        db_session.refresh(contato)
        
        return empresa, contato

    def test_create_oportunidade(self, db_session: Session, setup_data):
        """Deve criar uma oportunidade com dados válidos"""
        empresa, contato = setup_data
        
        oportunidade_data = {
            "tipo_negocio": "Venda Software",
            "custo": 5000.0,
            "lucro": 15000.0,
            "data": datetime.now(),
            "responsavel": "João Vendedor",
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        }
        
        oportunidade = create_oportunidade(db_session, oportunidade_data)
        
        assert oportunidade.id is not None
        assert oportunidade.tipo_negocio == "Venda Software"
        assert oportunidade.responsavel == "João Vendedor"

    def test_get_oportunidade_by_id(self, db_session: Session, setup_data):
        """Deve recuperar uma oportunidade pelo ID"""
        empresa, contato = setup_data
        
        oportunidade_data = {
            "tipo_negocio": "Consultoria",
            "responsavel": "Maria Coach",
            "data": datetime.now(),
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        }
        
        oportunidade = create_oportunidade(db_session, oportunidade_data)
        retrieved = get_oportunidade(db_session, oportunidade.id)
        
        assert retrieved is not None
        assert retrieved.id == oportunidade.id
        assert retrieved.tipo_negocio == "Consultoria"

    def test_get_oportunidade_not_found(self, db_session: Session):
        """Deve retornar None quando oportunidade não existe"""
        result = get_oportunidade(db_session, 999)
        assert result is None

    def test_get_all_oportunidades(self, db_session: Session, setup_data):
        """Deve retornar todas as oportunidades"""
        empresa, contato = setup_data
        
        for i in range(3):
            create_oportunidade(
                db_session,
                {
                    "tipo_negocio": f"Negócio {i}",
                    "responsavel": f"Responsável {i}",
                    "data": datetime.now(),
                    "empresa_id": empresa.id,
                    "contato_id": contato.id,
                }
            )
        
        oportunidades = get_oportunidades(db_session)
        assert len(oportunidades) == 3

    def test_update_oportunidade(self, db_session: Session, setup_data):
        """Deve atualizar dados de uma oportunidade"""
        empresa, contato = setup_data
        
        oportunidade_data = {
            "tipo_negocio": "Venda Serviço",
            "responsavel": "Pedro Sales",
            "data": datetime.now(),
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        }
        
        oportunidade = create_oportunidade(db_session, oportunidade_data)
        updated_data = {
            "tipo_negocio": "Venda Premium",
            "lucro": 50000.0,
        }
        updated = update_oportunidade(db_session, oportunidade.id, updated_data)
        
        assert updated.tipo_negocio == "Venda Premium"
        assert updated.lucro == 50000.0

    def test_delete_oportunidade(self, db_session: Session, setup_data):
        """Deve deletar uma oportunidade"""
        empresa, contato = setup_data
        
        oportunidade_data = {
            "tipo_negocio": "Licitação",
            "responsavel": "Ana Bid",
            "data": datetime.now(),
            "empresa_id": empresa.id,
            "contato_id": contato.id,
        }
        
        oportunidade = create_oportunidade(db_session, oportunidade_data)
        deleted = delete_oportunidade(db_session, oportunidade.id)
        
        assert deleted.id == oportunidade.id
        assert get_oportunidade(db_session, oportunidade.id) is None
