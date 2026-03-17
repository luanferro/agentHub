"""
Configuração compartilhada de fixtures para testes do RH
"""
import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Define variáveis de ambiente padrão para testes
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")

from rh.main import app
from rh.db.base import Base
from rh.db.session import get_db

# Importa todos os models para que SQLAlchemy registre as tabelas
import rh.models


@pytest.fixture
def engine():
    """
    Cria uma única engine SQLite em memória compartilhada entre fixtures
    """
    test_engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def test_db(engine):
    """
    Sessão de testes que compartilha a mesma engine do client
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(engine):
    """
    Cliente de teste FastAPI com banco de dados compartilhado (mesmo engine)
    """
    # Cria nova SessionLocal com a mesma engine do test_db
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Sobrescreve a dependência de DB da app com o DB de teste
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    test_client = TestClient(app)
    yield test_client
    
    # Limpa overrides após teste
    app.dependency_overrides.clear()


@pytest.fixture
def db_session(test_db):
    """
    Fixture que retorna a sessão de BD para testes unitários
    """
    return test_db
