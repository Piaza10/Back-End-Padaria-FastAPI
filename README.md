# 🍞 Padaria API

API REST para gestão completa de padarias, desenvolvida com **FastAPI**, **PostgreSQL** e **Docker**. Inclui autenticação JWT, controle de acesso por função (RBAC) e interface visual com pgAdmin.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) — framework web moderno e de alta performance
- [PostgreSQL 16](https://www.postgresql.org/) — banco de dados relacional
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para Python
- [Alembic](https://alembic.sqlalchemy.org/) — migrations de banco de dados
- [Pydantic v2](https://docs.pydantic.dev/) — validação de dados
- [Poetry](https://python-poetry.org/) — gerenciamento de dependências
- [Docker + Docker Compose](https://www.docker.com/) — containerização
- [pgAdmin 4](https://www.pgadmin.org/) — interface visual para o banco
- [python-jose](https://github.com/mpdavis/python-jose) — geração e validação de tokens JWT
- [passlib + bcrypt](https://passlib.readthedocs.io/) — hash seguro de senhas

---

## 📦 Funcionalidades

- ✅ Gestão de **ingredientes** com controle de estoque
- ✅ Gestão de **clientes**
- ✅ Gestão de **produtos** com vínculo de ingredientes e quantidade por receita
- ✅ Gestão de **pedidos** com cálculo automático do total
- ✅ **Autenticação JWT** com login e expiração de token
- ✅ **RBAC** — controle de acesso por função (`admin`, `caixa`, `estoquista`)
- ✅ **Migrations** automáticas com Alembic na inicialização
- ✅ **pgAdmin** incluído no ambiente Docker

---

## 🗂️ Estrutura do Projeto

```
padaria/
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── .dockerignore
├── pyproject.toml
├── poetry.lock
├── main.py
├── database.py
│
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── auth/
│   ├── hashing.py
│   ├── jwt.py
│   └── dependencies.py
│
├── models/
│   ├── usuario.py
│   ├── cliente.py
│   ├── ingrediente.py
│   ├── produto.py
│   └── pedido.py
│
├── schemas/
│   ├── usuario.py
│   ├── cliente.py
│   ├── ingrediente.py
│   ├── produto.py
│   └── pedido.py
│
└── routers/
    ├── auth.py
    ├── clientes.py
    ├── ingredientes.py
    ├── produtos.py
    └── pedidos.py
```

---

## ⚙️ Como rodar o projeto

### Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/padaria-api.git
cd padaria-api
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
# PostgreSQL
POSTGRES_USER=padaria_user
POSTGRES_PASSWORD=sua_senha_aqui
POSTGRES_DB=padaria_db

# Conexão interna usada pela aplicação
DATABASE_URL=postgresql://padaria_user:sua_senha_aqui@db:5432/padaria_db

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@padaria.com
PGADMIN_DEFAULT_PASSWORD=sua_senha_pgadmin

# JWT
SECRET_KEY=gere_uma_chave_segura_com_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Para gerar uma `SECRET_KEY` segura:
> ```bash
> openssl rand -hex 32
> ```

### 3. Suba os containers

```bash
docker-compose up --build
```

As migrations são aplicadas automaticamente na inicialização.

---

## 🌐 Acessos

| Serviço | URL |
|---------|-----|
| API | http://localhost:8000 |
| Documentação Swagger | http://localhost:8000/docs |
| Documentação ReDoc | http://localhost:8000/redoc |
| pgAdmin | http://localhost:5050 |

### Conectar o pgAdmin ao banco

Após acessar o pgAdmin, clique em **Add New Server** e preencha:

| Campo | Valor |
|-------|-------|
| Name | Padaria |
| Host | `db` |
| Port | `5432` |
| Database | `padaria_db` |
| Username | `padaria_user` |
| Password | *(valor do .env)* |

---

## 🔐 Autenticação

### 1. Crie um usuário admin

```http
POST /auth/registrar
Content-Type: application/json

{
  "nome": "Administrador",
  "email": "admin@padaria.com",
  "senha": "suasenha",
  "role": "admin"
}
```

### 2. Faça login e obtenha o token

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@padaria.com&password=suasenha
```

### 3. Use o token nas requisições

```http
Authorization: Bearer <token>
```

No Swagger (`/docs`), clique em **Authorize** e cole o token.

---

## 👥 Funções e permissões

| Endpoint | admin | caixa | estoquista |
|----------|:-----:|:-----:|:----------:|
| Ingredientes — listar/buscar | ✅ | ❌ | ✅ |
| Ingredientes — criar/editar | ✅ | ❌ | ✅ |
| Ingredientes — deletar | ✅ | ❌ | ❌ |
| Clientes — listar/buscar/criar/editar | ✅ | ✅ | ❌ |
| Clientes — deletar | ✅ | ❌ | ❌ |
| Produtos — listar/buscar | ✅ | ✅ | ✅ |
| Produtos — criar/editar | ✅ | ❌ | ✅ |
| Produtos — deletar | ✅ | ❌ | ❌ |
| Pedidos — listar/buscar/criar/editar | ✅ | ✅ | ❌ |
| Pedidos — deletar | ✅ | ❌ | ❌ |

---

## 🛠️ Comandos úteis

```bash
# Subir em background
docker-compose up --build -d

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f app

# Derrubar os containers
docker-compose down

# Derrubar e apagar volumes (dados do banco)
docker-compose down -v

# Gerar uma nova migration após alterar um model
docker-compose exec app alembic revision --autogenerate -m "descricao"

# Aplicar migrations manualmente
docker-compose exec app alembic upgrade head

# Reverter a última migration
docker-compose exec app alembic downgrade -1
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
