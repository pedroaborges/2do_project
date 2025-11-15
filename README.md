## 📝 Projeto: Fullstack To-Do List com Django

Este projeto é uma aplicação **To-Do List** completa (full-stack) desenvolvida usando o framework **Django** e implementando diversas tecnologias modernas para gerenciamento de tarefas e infraestrutura.

-----

### ✨ Tecnologias e Recursos

  * [cite\_start]**Backend:** Django (5.2.7) [cite: 1]
  * [cite\_start]**Banco de Dados:** PostgreSQL (via `psycopg2-binary`) [cite: 1]
  * [cite\_start]**Filas de Tarefas/Agendamento:** Celery (5.5.3) [cite: 1] [cite\_start]com `django-celery-beat` (2.8.1) [cite: 1]
  * [cite\_start]**Servidor de Aplicação:** Gunicorn (23.0.0) [cite: 1]
  * [cite\_start]**Outras Dependências:** Gerenciamento de arquivos de ambiente (`django-environ`), manipulação de fuso horário (`django-timezone-field`, `tzdata`), e mais (conforme listado em `requirements.txt`). [cite: 1]
  * **Infraestrutura:** Docker e Docker Compose (para rodar a aplicação, PostgreSQL e Celery).

-----

### ⚙️ Pré-requisitos

Para rodar o projeto localmente, você precisa ter instalado:

1.  **Docker** e **Docker Compose:** Essenciais para orquestrar a aplicação, banco de dados (PostgreSQL) e o Celery.
2.  **Git:** Para clonar o repositório.

-----

### 🚀 Configuração e Execução

Siga os passos abaixo para configurar e iniciar a aplicação:

#### 1\. Clonar o Repositório

Abra seu terminal e clone o projeto:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome-do-diretorio-do-projeto>
```

#### 2\. Configurar Variáveis de Ambiente

O projeto requer um arquivo `.env` para armazenar configurações sensíveis, como segredos do Django e credenciais do banco de dados/Celery.

1.  Crie um arquivo chamado `.env` na raiz do projeto.
2.  Preencha-o com as variáveis necessárias. Um exemplo básico pode incluir:

<!-- end list -->

```env
# Configurações do Django
SECRET_KEY=<SUA_CHAVE_SECRETA_DO_DJANGO>
DEBUG=True

# Configurações do Banco de Dados PostgreSQL (Docker)
POSTGRES_DB=todolistdb
POSTGRES_USER=todolistuser
POSTGRES_PASSWORD=todolistpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

# URL do Banco de Dados para Django
DATABASE_URL=postgres://todolistuser:todolistpassword@db:5432/todolistdb

# Configurações do Broker do Celery (RabbitMQ ou Redis - ajuste o Docker Compose conforme necessário)
CELERY_BROKER_URL=redis://redis:6379/0 # Exemplo com Redis
```

> **Nota:** Certifique-se de que as configurações do banco de dados no `.env` correspondam aos volumes e nomes de serviço definidos no seu arquivo `docker-compose.yml`.

#### 3\. Iniciar os Serviços com Docker Compose

Use o Docker Compose para construir as imagens e iniciar todos os contêineres necessários (aplicação Django, PostgreSQL e Celery Worker/Beat).

```bash
docker-compose up --build
```

Este comando fará o seguinte:

  * Construirá a imagem Docker da aplicação Django.
  * Iniciará o contêiner do **PostgreSQL** (`db`).
  * Iniciará o contêiner do **Celery Worker** (para executar tarefas assíncronas).
  * Iniciará o contêiner do **Celery Beat** (para agendamento de tarefas recorrentes).
  * Iniciará o contêiner da aplicação Django (usando Gunicorn) no porto configurado (geralmente **8000**).

#### 4\. Acessar a Aplicação

Após o Docker Compose iniciar todos os serviços, a aplicação estará acessível em seu navegador:

🔗 **URL:** `http://localhost:8000`

-----

### 🛑 Parar a Aplicação

Para parar todos os contêineres e liberar os recursos, execute:

```bash
docker-compose down
```

-----

Posso te ajudar a gerar um arquivo `docker-compose.yml` de exemplo, se você precisar?
