"""
Testes unitários para o serviço de Pedido
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from erp.models.pedido import Pedido
from erp.services.pedido_service import (
    get_all_pedidos,
    create_pedido,
    get_pedido,
    update_pedido,
    delete_pedido,
)


class TestPedidoService:
    """Testes da camada de serviço de Pedido"""

    def test_create_pedido(self, db_session: Session):
        """Deve criar um pedido com dados válidos"""
        pedido_data = {
            "data": datetime.now(),
            "status": True,
            "valor_total": 5000.0,
            "client_nome": "Cliente ABC",
        }
        
        pedido = create_pedido(db_session, pedido_data)
        
        assert pedido.id is not None
        assert pedido.client_nome == "Cliente ABC"
        assert pedido.valor_total == 5000.0

    def test_get_pedido_by_id(self, db_session: Session):
        """Deve recuperar um pedido pelo ID"""
        pedido_data = {
            "data": datetime.now(),
            "status": False,
            "valor_total": 3000.0,
            "client_nome": "Cliente XYZ",
        }
        
        pedido = create_pedido(db_session, pedido_data)
        retrieved = get_pedido(db_session, pedido.id)
        
        assert retrieved is not None
        assert retrieved.id == pedido.id
        assert retrieved.client_nome == "Cliente XYZ"

    def test_get_pedido_not_found(self, db_session: Session):
        """Deve retornar None quando pedido não existe"""
        result = get_pedido(db_session, 999)
        assert result is None

    def test_get_all_pedidos(self, db_session: Session):
        """Deve retornar todos os pedidos"""
        for i in range(3):
            create_pedido(
                db_session,
                {
                    "data": datetime.now(),
                    "status": i % 2 == 0,
                    "valor_total": 1000.0 * (i + 1),
                    "client_nome": f"Cliente {i}",
                }
            )
        
        pedidos = get_all_pedidos(db_session)
        assert len(pedidos) >= 3

    def test_update_pedido(self, db_session: Session):
        """Deve atualizar dados de um pedido"""
        pedido_data = {
            "data": datetime.now(),
            "status": False,
            "valor_total": 2000.0,
            "client_nome": "Cliente Teste",
        }
        
        pedido = create_pedido(db_session, pedido_data)
        updated_data = {
            "status": True,
            "valor_total": 2500.0,
        }
        updated = update_pedido(db_session, pedido.id, updated_data)
        
        assert updated.status == True
        assert updated.valor_total == 2500.0

    def test_delete_pedido(self, db_session: Session):
        """Deve deletar um pedido"""
        pedido_data = {
            "data": datetime.now(),
            "status": True,
            "valor_total": 1500.0,
            "client_nome": "Cliente para Deletar",
        }
        
        pedido = create_pedido(db_session, pedido_data)
        deleted = delete_pedido(db_session, pedido.id)
        
        assert deleted.id == pedido.id
        assert get_pedido(db_session, pedido.id) is None
