# 🚀 agentHub

> **Enterprise API Agent Platform** - Arquitetura de microserviços integrada para gestão de CRM, ERP e RH com APIs REST modulares e testes abrangentes.

[![Tests](https://github.com/seu-usuario/agentHub/workflows/Tests/badge.svg)](https://github.com/seu-usuario/agentHub/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Como Rodar](#como-rodar)
- [Testes](#testes)
- [Documentação API](#documentação-api)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## 🎯 Visão Geral

**agentHub** é uma plataforma de APIs para gestão empresarial integrada, composta por três microserviços independentes:

### **CRM (Customer Relationship Management)**
Gerencia relacionamento com clientes: empresas, contatos e oportunidades de negócio.
- 📊 Cadastro de empresas (CNPJ, nome, descrição)
- 👥 Gestão de contatos (nome, email, telefone)
- 💼 Rastreamento de oportunidades (stage, valor, probabilidade)

### **ERP (Enterprise Resource Planning)**
Controla operações comerciais e inventário.
- 📦 Gestão de produtos (nome, preço, estoque)
- 🛒 Gestão de pedidos (status, valor total, itens)
- 📈 Relatórios de movimentação

### **RH (Human Resources)**
Administra recursos humanos da empresa.
- 👔 Cadastro de funcionários (nome, CPF, data admissão, salário)
- 🏢 Gestão de departamentos (estrutura organizacional)
- 📋 Cargo e hierarquias

---

## 🏗️ Arquitetura

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────┐
│              Gateway API (opcional)              │
│         (Roteamento/Agregação de reqs)         │
└────┬─────────┬─────────┬─────────────────────┘
     │         │         │
  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
  │ CRM │  │ ERP │  │ RH  │
  └──┬──┘  └──┬──┘  └──┬──┘
     │        │        │
  ┌──▼──────▼──────▼──┐
  │   PostgreSQL DB    │
  │  (Produção)        │
  └───────────────────┘

Durante TESTES → SQLite in-memory (StaticPool)
```

### Stack Técnico por Serviço

```
CRM, ERP, RH:
├── FastAPI 0.115+ (Web framework)
├── SQLAlchemy 2.0+ (ORM)
├── Pydantic (Validação de schemas)
├── Alembic (Migrations)
└── Docker (Containerização)

Testing:
├── pytest 7.4+ (Framework de testes)
├── pytest-asyncio (Async support)
├── pytest-cov (Coverage reports)
└── SQLite (In-memory para testes)

CI/CD:
├── GitHub Actions
├── Codecov (Coverage tracking)
└── Docker Compose
```

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Propósito |
|------------|--------|----------|
| **Python** | 3.11+ | Runtime |
| **FastAPI** | 0.115+ | Web framework |
| **SQLAlchemy** | 2.0+ | ORM |
| **PostgreSQL** | 15+ | Database (prod) |
| **SQLite** | Latest | Database (tests) |
| **Docker** | Latest | Containerização |
| **pytest** | 7.4+ | Testes |
| **Alembic** | Latest | Migrations |

---

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Docker & Docker Compose (opcional, para banco de dados)
- Git

### 1. Clonar Repositório

```bash
git clone https://github.com/seu-usuario/agentHub.git
cd agentHub
```

### 2. Configurar Ambiente Virtual

```bash
# Criar venv
python -m venv .venv

# Ativar venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
# Instalar todos os requirements
pip install -r backend/crm/requirements.txt
pip install -r backend/erp/requirements.txt
pip install -r backend/rh/requirements.txt

# (Opcional) Ferramentas de desenvolvimento
pip install pytest pytest-asyncio pytest-cov pytest-xdist black isort flake8
```

### 4. Configurar Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```bash
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_aqui
POSTGRES_DB=agentHub
DB_HOST=localhost
DB_PORT=5432

# FastAPI
DEBUG=True

# MCP Server (opcional)
MCP_SERVER_PORT=8001
```

### 5. Executar Banco de Dados

**Opção A: Docker Compose** (recomendado)
```bash
docker-compose up -d
```

**Opção B: PostgreSQL Local**
```bash
# Criar database
createdb agentHub

# Executar migrations
cd backend/crm && alembic upgrade head
cd ../erp && alembic upgrade head
cd ../rh && alembic upgrade head
```

---

## 🚀 Como Rodar

### Executar um Serviço Individual

```bash
# CRM
cd backend/crm
python main.py
# Acessa em: http://localhost:8000/docs

# ERP
cd backend/erp
python main.py
# Acessa em: http://localhost:8001/docs

# RH
cd backend/rh
python main.py
# Acessa em: http://localhost:8002/docs
```

### Executar Todos os Serviços Simultaneamente

**Terminal 1 - CRM:**
```bash
cd backend/crm && python main.py
```

**Terminal 2 - ERP:**
```bash
cd backend/erp && python main.py
```

**Terminal 3 - RH:**
```bash
cd backend/rh && python main.py
```

### Executar via Docker Compose

```bash
# Inicia todos os serviços
docker-compose up

# Em detached mode
docker-compose up -d

# Ver logs
docker-compose logs -f crm
docker-compose logs -f erp
docker-compose logs -f rh

# Parar serviços
docker-compose down
```

---

## 🧪 Testes

### Executar Testes Localmente

```bash
# Todos os testes
pytest backend/crm/tests backend/erp/tests backend/rh/tests -v

# Por serviço
pytest backend/crm/tests -v
pytest backend/erp/tests -v
pytest backend/rh/tests -v

# Por tipo
pytest backend/crm/tests/unit/ -v          # Testes unitários
pytest backend/crm/tests/integration/ -v   # Testes integração

# Teste específico
pytest backend/crm/tests/unit/test_empresa_service.py::TestEmpresaService::test_create_empresa -v
```

### Gerar Coverage Report

```bash
# HTML report
pytest backend/crm/tests --cov=. --cov-report=html
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux

# Terminal report
pytest backend/crm/tests --cov=. --cov-report=term-missing
```

### Estatísticas de Testes

| Serviço | Testes | Status |
|---------|--------|--------|
| CRM | 42 | ✅ 40 passing, 2 skipped |
| ERP | 24 | ✅ 24 passing |
| RH | 25 | ✅ 24 passing, 1 skipped |
| **TOTAL** | **91** | **✅ 87 passing, 3 skipped** |

Para mais detalhes, ver [TESTING.md](TESTING.md)

---

## 📚 Documentação API

Cada serviço fornece documentação interativa Swagger:

### Acessar Swagger UI

- **CRM:** http://localhost:8000/docs
- **ERP:** http://localhost:8001/docs
- **RH:** http://localhost:8002/docs

### Exemplo de Request (CRM)

```bash
# Criar empresa
curl -X POST "http://localhost:8000/crm/v1/empresa" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Tech Solutions S.A.",
    "cnpj": "12.345.678/0001-90"
  }'

# Listar empresas
curl -X GET "http://localhost:8000/crm/v1/empresa/"

# Buscar por ID
curl -X GET "http://localhost:8000/crm/v1/empresa/1"

# Atualizar
curl -X PUT "http://localhost:8000/crm/v1/empresa/1" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Nova Tech Solutions"}'

# Deletar
curl -X DELETE "http://localhost:8000/crm/v1/empresa/1"
```

### Schema de Resposta

Todas as APIs retornam JSON estruturado:

```json
{
  "id": 1,
  "nome": "Tech Solutions S.A.",
  "cnpj": "12.345.678/0001-90",
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}
```

---

## 📁 Estrutura de Diretórios

```
agentHub/
├── backend/
│   ├── crm/
│   │   ├── main.py                 # Entry point
│   │   ├── requirements.txt
│   │   ├── alembic.ini              # Migrations config
│   │   ├── dockerfile
│   │   ├── api/
│   │   │   └── routers/             # HTTP endpoints
│   │   │       ├── empresa_router.py
│   │   │       ├── contato_router.py
│   │   │       └── oportunidade_router.py
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── empresa.py
│   │   │   ├── contato.py
│   │   │   └── oportunidade.py
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   └── *_schema.py
│   │   ├── services/                # Business logic
│   │   │   └── *_service.py
│   │   ├── db/
│   │   │   ├── base.py              # SQLAlchemy base
│   │   │   ├── session.py           # DB session
│   │   │   └── config.py
│   │   ├── migrations/              # Alembic migrations
│   │   └── tests/
│   │       ├── conftest.py          # Pytest fixtures
│   │       ├── unit/                # Unit tests
│   │       └── integration/         # Integration tests
│   ├── erp/                         # [mesma estrutura]
│   └── rh/                          # [mesma estrutura]
│
├── tests/
│   ├── conftest.py                  # E2E fixtures
│   └── e2e_workflow.py              # End-to-end tests
│
├── .github/
│   └── workflows/
│       └── tests.yml                # CI/CD pipeline
│
├── docker-compose.yml               # Compose config
├── TESTING.md                       # Testing guide
├── TESTS_SUMMARY.md                 # Test results
├── TEST_COMMANDS.sh                 # Useful commands
└── README.md                        # Este arquivo
```

---

## 🔄 CI/CD Pipeline

GitHub Actions executam automaticamente:

1. **Testes** - Em Python 3.11 com PostgreSQL
   ```bash
   pytest backend/crm/tests backend/erp/tests backend/rh/tests --cov
   ```

2. **Coverage** - Upload para Codecov
   ```bash
   codecov upload
   ```

3. **Linting** - Code style checks
   ```bash
   black --check backend/
   isort --check backend/
   flake8 backend/
   ```

**Status:** [![Tests](https://github.com/seu-usuario/agentHub/workflows/Tests/badge.svg)](https://github.com/seu-usuario/agentHub/actions)

---

## 🤝 Contribuindo

### Passo 1: Fork & Clone

```bash
git clone https://github.com/seu-usuario/agentHub.git
cd agentHub
```

### Passo 2: Criar Branch Feature

```bash
git checkout -b feature/sua-feature
```

### Passo 3: Fazer Alterações

```bash
# Desenvolver feature
# Adicionar testes correspondentes
```

### Passo 4: Rodar Testes Localmente

```bash
# Verificar testes
pytest backend/crm/tests backend/erp/tests backend/rh/tests -v

# Verificar qualidade de código
black backend/
isort backend/
flake8 backend/
```

### Passo 5: Commit & Push

```bash
git add .
git commit -m "feat: descrição clara da feature"
git push origin feature/sua-feature
```

### Passo 6: Abrir Pull Request

1. Vá para [GitHub](https://github.com/seu-usuario/agentHub)
2. Clique em "New Pull Request"
3. Descreva suas mudanças
4. Aguarde review

### Convenções de Commit

```
feat:   Quando adiciona uma nova feature
fix:    Quando corrige um bug
test:   Quando adiciona ou modifica testes
docs:   Quando modifica documentação
style:  Quando muda formatação (sem afetar lógica)
refactor: Quando refactora código
chore:  Quando atualiza dependências
```

---

## 📊 Roadmap

### ✅ Completado (v1.0)
- [x] Microserviços CRM, ERP, RH
- [x] APIs REST com FastAPI
- [x] Testes unitários e integração (87 testes)
- [x] CI/CD com GitHub Actions
- [x] Docker Compose setup
- [x] Documentação completa

### 🔄 Em Progresso
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Caching com Redis
- [ ] Message queue (Celery/RabbitMQ)
- [ ] Logging centralizado

### 📝 Planejado
- [ ] API Gateway (Kong/Nginx)
- [ ] GraphQL endpoint
- [ ] Mobile app
- [ ] Admin dashboard
- [ ] Webhooks

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'crm'"

```bash
# Adicionar backend ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
python main.py
```

### Erro: "connection refused" ao banco

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Reiniciar serviços
docker-compose down
docker-compose up -d
```

### Testes falhando

```bash
# Verificar fixtures
pytest --fixtures | grep seu_fixture

# Ver logs detalhados
pytest backend/crm/tests -vv --tb=long
```

Para mais soluções, ver [TESTING.md](TESTING.md#troubleshooting)

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Desenvolvimento** - Sua Equipe
- **Testes** - Implementação completa com 87+ testes
- **Documentação** - README, TESTING.md, guides

---

## 📞 Suporte

- 📧 Email: suporte@agentHub.com
- 💬 Issues: [GitHub Issues](https://github.com/seu-usuario/agentHub/issues)
- 📖 Documentação: [docs/](docs/)

---

## 🙏 Agradecimentos

Obrigado por usar **agentHub**! Se encontrar problemas ou tiver sugestões, abra uma [issue](https://github.com/seu-usuario/agentHub/issues).

---

<div align="center">

**Feito com ❤️ para gestão empresarial moderna**

⭐ Considere dar uma estrela se este projeto foi útil!

</div>
