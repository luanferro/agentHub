"""
Configuração de fixtures de teste para E2E
"""
import pytest
import os
import sys

# Adiciona backend ao path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Define variáveis de ambiente padrão para testes
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")

# Importa apps
from crm.main import app as crm_app
from crm.db.base import Base as CRM_Base
from crm.db.session import get_db as crm_get_db

from erp.main import app as erp_app
from erp.db.base import Base as ERP_Base
from erp.db.session import get_db as erp_get_db

from rh.main import app as rh_app
from rh.db.base import Base as RH_Base
from rh.db.session import get_db as rh_get_db

# Importa models para registrar
import crm.models
import erp.models
import rh.models


@pytest.fixture(scope="session")
def test_engine():
    """
    Cria uma engine SQLite em memória única para toda a sessão de testes
    """
    test_engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    
    # Cria todas as tabelas para todos os serviços
    CRM_Base.metadata.create_all(bind=test_engine)
    ERP_Base.metadata.create_all(bind=test_engine)
    RH_Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    CRM_Base.metadata.drop_all(bind=test_engine)
    ERP_Base.metadata.drop_all(bind=test_engine)
    RH_Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def crm_client(test_engine):
    """Cliente de teste para CRM"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    crm_app.dependency_overrides[crm_get_db] = override_get_db
    
    client = TestClient(crm_app)
    yield client
    
    crm_app.dependency_overrides.clear()


@pytest.fixture
def erp_client(test_engine):
    """Cliente de teste para ERP"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    erp_app.dependency_overrides[erp_get_db] = override_get_db
    
    client = TestClient(erp_app)
    yield client
    
    erp_app.dependency_overrides.clear()


@pytest.fixture
def rh_client(test_engine):
    """Cliente de teste para RH"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    rh_app.dependency_overrides[rh_get_db] = override_get_db
    
    client = TestClient(rh_app)
    yield client
    
    rh_app.dependency_overrides.clear()
