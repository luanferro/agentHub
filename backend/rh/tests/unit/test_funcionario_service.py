"""
Testes unitários para o serviço de Funcionário
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from rh.models.funcionario import Funcionario
from rh.models.departamento import Departamento
from rh.services.funcionario_service import (
    get_funcionarios,
    create_funcionario,
    get_funcionario,
    update_funcionario,
    delete_funcionario,
)


class TestFuncionarioService:
    """Testes da camada de serviço de Funcionário"""

    @pytest.fixture
    def departamento(self, db_session: Session):
        """Cria um departamento para os testes"""
        depto = Departamento(
            nome="TI",
            descricao="Departamento de Tecnologia da Informação"
        )
        db_session.add(depto)
        db_session.commit()
        db_session.refresh(depto)
        return depto

    def test_create_funcionario(self, db_session: Session, departamento):
        """Deve criar um funcionário com dados válidos"""
        func_data = {
            "nome": "João Silva",
            "email": "joao@company.com",
            "cpf": "123.456.789-00",
            "data_admissao": datetime.now(),
            "cargo": "Desenvolvedor Senior",
            "salario": 8000.0,
            "departamento_id": departamento.id,
        }
        
        funcionario = create_funcionario(db_session, func_data)
        
        assert funcionario.id is not None
        assert funcionario.nome == "João Silva"
        assert funcionario.cpf == "123.456.789-00"

    def test_get_funcionario_by_id(self, db_session: Session, departamento):
        """Deve recuperar um funcionário pelo ID"""
        func_data = {
            "nome": "Maria Santos",
            "email": "maria@company.com",
            "cpf": "987.654.321-00",
            "data_admissao": datetime.now(),
            "cargo": "Analista",
            "salario": 5000.0,
            "departamento_id": departamento.id,
        }
        
        funcionario = create_funcionario(db_session, func_data)
        retrieved = get_funcionario(db_session, funcionario.id)
        
        assert retrieved is not None
        assert retrieved.id == funcionario.id
        assert retrieved.nome == "Maria Santos"

    def test_get_funcionario_not_found(self, db_session: Session):
        """Deve retornar None quando funcionário não existe"""
        result = get_funcionario(db_session, 999)
        assert result is None

    def test_get_all_funcionarios(self, db_session: Session, departamento):
        """Deve retornar todos os funcionários"""
        for i in range(3):
            create_funcionario(
                db_session,
                {
                    "nome": f"Funcionário {i}",
                    "email": f"func{i}@company.com",
                    "cpf": f"111.222.333-{i:02d}",
                    "data_admissao": datetime.now(),
                    "cargo": f"Cargo {i}",
                    "salario": 3000.0 + (1000.0 * i),
                    "departamento_id": departamento.id,
                }
            )
        
        funcionarios = get_funcionarios(db_session)
        assert len(funcionarios) >= 3

    def test_update_funcionario(self, db_session: Session, departamento):
        """Deve atualizar dados de um funcionário"""
        func_data = {
            "nome": "Pedro Costa",
            "email": "pedro@company.com",
            "cpf": "555.666.777-00",
            "data_admissao": datetime.now(),
            "cargo": "Estagiário",
            "salario": 2000.0,
            "departamento_id": departamento.id,
        }
        
        funcionario = create_funcionario(db_session, func_data)
        updated_data = {
            "cargo": "Desenvolvedor Junior",
            "salario": 4000.0,
        }
        updated = update_funcionario(db_session, funcionario.id, updated_data)
        
        assert updated.cargo == "Desenvolvedor Junior"
        assert updated.salario == 4000.0

    def test_delete_funcionario(self, db_session: Session, departamento):
        """Deve deletar um funcionário"""
        func_data = {
            "nome": "Ana Lima",
            "email": "ana@company.com",
            "cpf": "999.888.777-00",
            "data_admissao": datetime.now(),
            "cargo": "Gerente",
            "salario": 10000.0,
            "departamento_id": departamento.id,
        }
        
        funcionario = create_funcionario(db_session, func_data)
        deleted = delete_funcionario(db_session, funcionario.id)
        
        assert deleted.id == funcionario.id
        assert get_funcionario(db_session, funcionario.id) is None
