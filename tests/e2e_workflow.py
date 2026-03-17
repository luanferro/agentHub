"""
Testes E2E (End-to-End) que validam fluxos entre múltiplos serviços
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient


class TestCRMtoERPWorkflow:
    """Testes de workflow entre CRM e ERP"""

    def test_criar_empresa_e_pedido(self, crm_client: TestClient, erp_client: TestClient):
        """
        Fluxo E2E:
        1. Criar uma empresa no CRM
        2. Criar um contato no CRM
        3. Criar um pedido no ERP relacionado à empresa do CRM
        4. Validar que os dados foram persistidos corretamente
        """

        # STEP 1: Criar empresa no CRM
        empresa_response = crm_client.post("/crm/v1/empresa", json={
            "nome": "Tech Solutions S.A.",
            "cnpj": "11.222.333/0001-44",
        })
        assert empresa_response.status_code == 200
        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]
        assert empresa_data["nome"] == "Tech Solutions S.A."

        # STEP 2: Criar contato no CRM
        contato_response = crm_client.post("/crm/v1/contato", json={
            "nome": "Carlos E2E",
            "email": "carlos.e2e@example.com",
            "empresa_id": empresa_id,
        })
        assert contato_response.status_code == 200
        contato_data = contato_response.json()
        assert contato_data["nome"] == "Carlos E2E"

        # STEP 3: Criar pedido no ERP
        pedido_response = erp_client.post("/erp/v1/pedido", json={
            "data": datetime.now().isoformat(),
            "status": True,
            "valor_total": 15000.0,
            "client_nome": "Tech Solutions S.A.",  # Referência à empresa do CRM
        })
        assert pedido_response.status_code == 200
        pedido_data = pedido_response.json()
        assert pedido_data["client_nome"] == "Tech Solutions S.A."
        assert pedido_data["valor_total"] == 15000.0

        # STEP 4: Validar que os dados propagaram corretamente
        # Listar empresas no CRM - deve conter a criada
        empresas_response = crm_client.get("/crm/v1/empresa/")
        assert empresas_response.status_code == 200
        empresas = empresas_response.json()
        assert len(empresas) > 0
        assert any(e["nome"] == "Tech Solutions S.A." for e in empresas)

        # Listar pedidos no ERP - deve conter o criado
        pedidos_response = erp_client.get("/erp/v1/pedido/")
        assert pedidos_response.status_code == 200
        pedidos = pedidos_response.json()
        assert len(pedidos) > 0
        assert any(p["client_nome"] == "Tech Solutions S.A." for p in pedidos)

    def test_oportunidade_vinculada_ao_pedido(self, crm_client: TestClient, erp_client: TestClient):
        """
        Fluxo E2E:
        1. Criar empresa no CRM
        2. Criar contato no CRM
        3. Criar oportunidade no CRM vinculada à empresa e contato
        4. Criar pedido no ERP com valor similar ao da oportunidade
        5. Validar coerência dos dados entre sistemas
        """

        # STEP 1-2: Criar empresa e contato
        empresa = crm_client.post("/crm/v1/empresa", json={
            "nome": "Empresa Grande",
            "cnpj": "99.999.999/0001-99",
        }).json()

        contato = crm_client.post("/crm/v1/contato", json={
            "nome": "João Manager",
            "email": "joao@empresa-grande.com",
            "empresa_id": empresa["id"],
        }).json()

        # STEP 3: Criar oportunidade
        oportunidade = crm_client.post("/crm/v1/oportunidade", json={
            "tipo_negocio": "Consultoria Estratégica",
            "data": datetime.now().isoformat(),
            "responsavel": "Ana Sales",
            "empresa_id": empresa["id"],
            "contato_id": contato["id"],
            "custo": 5000.0,
            "lucro": 8000.0,
        }).json()
        assert oportunidade["tipo_negocio"] == "Consultoria Estratégica"

        # STEP 4: Criar pedido no ERP com valor próximo ao lucro da oportunidade
        pedido = erp_client.post("/erp/v1/pedido", json={
            "data": datetime.now().isoformat(),
            "status": True,
            "valor_total": 8000.0,  # Mesmo que o lucro da oportunidade
            "client_nome": "Empresa Grande",
        }).json()
        assert pedido["valor_total"] == 8000.0

        # STEP 5: Validar coerência
        # Recuperar oportunidade e validar
        oportunidade_get = crm_client.get(f"/crm/v1/oportunidade/{oportunidade['id']}").json()
        assert oportunidade_get["lucro"] == 8000.0

        # Recuperar pedido e validar
        pedido_get = erp_client.get(f"/erp/v1/pedido/{pedido['id']}").json()
        assert pedido_get["valor_total"] == 8000.0
        assert pedido_get["client_nome"] == "Empresa Grande"


class TestCRMtoRHWorkflow:
    """Testes de workflow entre CRM e RH"""

    def test_criar_empresa_e_funcionario(self, crm_client: TestClient, rh_client: TestClient):
        """
        Fluxo E2E:
        1. Criar empresa no CRM
        2. Criar contato do responsável da empresa no CRM
        3. Criar departamento no RH
        4. Criar funcionário no RH com mesmos dados do contato CRM
        5. Validar dados coerentes entre sistemas
        """

        # STEP 1: Criar empresa no CRM
        empresa = crm_client.post("/crm/v1/empresa", json={
            "nome": "Recursos Humanos Inc.",
            "cnpj": "12.345.678/0001-99",
        }).json()

        # STEP 2: Criar contato (representante da empresa)
        contato = crm_client.post("/crm/v1/contato", json={
            "nome": "Patricia RH",
            "email": "patricia@rh-inc.com",
            "empresa_id": empresa["id"],
        }).json()

        # STEP 3: Criar departamento no RH
        departamento = rh_client.post("/rh/v1/departamentos", json={
            "nome": "Recursos Humanos",
            "descricao": "Departamento de RH",
        }).json()

        # STEP 4: Criar funcionário no RH
        funcionario = rh_client.post("/rh/v1/funcionarios", json={
            "nome": "Patricia RH",
            "email": "patricia@rh-inc.com",
            "cpf": "123.456.789-00",
            "data_admissao": datetime.now().isoformat(),
            "cargo": "Gerente de RH",
            "salario": 8000.0,
            "departamento_id": departamento["id"],
        }).json()

        # STEP 5: Validar que ambos os sistemas têm dados coerentes
        # CRM tem contato com mesmo nome e email
        contato_get = crm_client.get(f"/crm/v1/contato/{contato['id']}").json()
        assert contato_get["email"] == "patricia@rh-inc.com"
        assert contato_get["nome"] == "Patricia RH"

        # RH tem funcionário com mesmo nome e email
        funcionario_get = rh_client.get(f"/rh/v1/funcionarios/{funcionario['id']}").json()
        assert funcionario_get["email"] == "patricia@rh-inc.com"
        assert funcionario_get["nome"] == "Patricia RH"
