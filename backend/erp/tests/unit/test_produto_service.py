"""
Testes unitários para o serviço de Produto
"""
import pytest
from sqlalchemy.orm import Session

from erp.models.produto import Produto
from erp.services.produto_service import (
    get_all_produtos,
    create_produto,
    get_produto,
    update_produto,
    delete_produto,
)


class TestProdutoService:
    """Testes da camada de serviço de Produto"""

    def test_create_produto(self, db_session: Session):
        """Deve criar um produto com dados válidos"""
        produto_data = {
            "nome": "Notebook Dell",
            "descricao": "Notebook com processador Intel i7",
            "preco": 5000.0,
            "estoque": 15,
        }
        
        produto = create_produto(db_session, produto_data)
        
        assert produto.id is not None
        assert produto.nome == "Notebook Dell"
        assert produto.preco == 5000.0

    def test_get_produto_by_id(self, db_session: Session):
        """Deve recuperar um produto pelo ID"""
        produto_data = {
            "nome": "Mouse Logitech",
            "descricao": "Mouse sem fio com bateria de longa duração",
            "preco": 150.0,
            "estoque": 50,
        }
        
        produto = create_produto(db_session, produto_data)
        retrieved = get_produto(db_session, produto.id)
        
        assert retrieved is not None
        assert retrieved.id == produto.id
        assert retrieved.nome == "Mouse Logitech"

    def test_get_produto_not_found(self, db_session: Session):
        """Deve retornar None quando produto não existe"""
        result = get_produto(db_session, 999)
        assert result is None

    def test_get_all_produtos(self, db_session: Session):
        """Deve retornar todos os produtos"""
        for i in range(3):
            create_produto(
                db_session,
                {
                    "nome": f"Produto {i}",
                    "descricao": f"Descrição do produto {i}",
                    "preco": 100.0 * (i + 1),
                    "estoque": 10 * (i + 1),
                }
            )
        
        produtos = get_all_produtos(db_session)
        assert len(produtos) >= 3

    def test_update_produto(self, db_session: Session):
        """Deve atualizar dados de um produto"""
        produto_data = {
            "nome": "Teclado Mecanico",
            "descricao": "Teclado simples",
            "preco": 450.0,
            "estoque": 20,
        }
        
        produto = create_produto(db_session, produto_data)
        updated_data = {
            "descricao": "Teclado RGB com switches mecânicos",
            "preco": 500.0,
        }
        updated = update_produto(db_session, produto.id, updated_data)
        
        assert updated.descricao == "Teclado RGB com switches mecânicos"
        assert updated.preco == 500.0

    def test_delete_produto(self, db_session: Session):
        """Deve deletar um produto"""
        produto_data = {
            "nome": "Monitor 27 polegadas",
            "descricao": "Monitor Full HD com excelente qualidade",
            "preco": 1200.0,
        }
        
        produto = create_produto(db_session, produto_data)
        deleted = delete_produto(db_session, produto.id)
        
        assert deleted.id == produto.id
        assert get_produto(db_session, produto.id) is None
