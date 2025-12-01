# 🚀 Benefits Service — Sistema de Benefícios com FastAPI, RabbitMQ e PostgreSQL

Um sistema completo de benefícios corporativos utilizando:

* **FastAPI (serviço web / API REST)**
* **RabbitMQ (fila assíncrona para cargas pesadas)**
* **Worker (processamento assíncrono)**
* **PostgreSQL (banco relacional)**
* **Docker + Docker Compose (orquestração)**

---

# 📂 Estrutura do Projeto

```
benefits_service/
│   ├── .env                      # Variáveis de ambiente
│   ├── docker-compose.yml        # Orquestração completa
│   ├── requirements.txt          # Dependências Python
│   ├── README.md                 # Documento atual
│
├───app/                          # Serviço Web (FastAPI)
│   ├── main.py                   # Inicialização da API
│   ├── config.py                 # Configurações (env)
│   ├── db.py                     # Conexão com PostgreSQL (pool)
│   └── routes/                   # Rotas HTTP (rest API)
│       ├── benefits.py
│       ├── companies.py
│       ├── employees.py
│       └── loads.py
│
├───worker/                       # Worker assíncrono (RabbitMQ)
│   ├── consumer.py               # Consumidor de mensagens
│   └── config.py                 # Configurações do worker
│
├───web/
│   └── Dockerfile                # Dockerfile do serviço Web
│
└───worker/
    └── Dockerfile                # Dockerfile do Worker
```

---

# ⚙️ Pré-requisitos

Antes de rodar o projeto você precisa ter instalado:

* **Docker**
* **Docker Compose**
* (Opcional) Python 3.11+ para desenvolvimento local

---

# 🔧 Configuração — `.env`

Crie um arquivo `.env` na raiz com:

```env
POSTGRES_USER=benefits
POSTGRES_PASSWORD=benefits_pass
POSTGRES_DB=benefits_db

WEB_PORT=8000

RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
```

> **Dica:** você também pode usar o `.env.example` como base.
> **Observação:** por se tratar de um projeto apenas para fins educativos, disponibilizei o env de acesso utilizado.

---

# ▶️ Como Rodar Tudo

Na raiz do projeto:

```bash
docker compose up --build
```

Isso irá iniciar automaticamente:

* **PostgreSQL**
* **RabbitMQ**
* **API (FastAPI)**
* **Worker (processamento assíncrono)**

---

# 🌐 Endpoints Principais

Com tudo rodando, acesse:

### ▶️ Swagger UI (documentação automática)

📌 `http://localhost:8000/docs`

### ▶️ Health check

```
GET /health
```

---

# 📌 Rotas Disponíveis

## 🏢 Empresas

```
POST /companies
GET  /companies
```

## 👥 Funcionários

```
POST /employees
GET  /employees
```

## 🎁 Benefícios

```
POST /benefits
GET  /benefits
```

## 📤 Cargas (assíncrono via RabbitMQ)

```
POST /load
```

Quando o endpoint `/load` é chamado:

1. O FastAPI valida a entrada
2. Envia uma mensagem para a fila `benefits_queue`
3. O **Worker** consome e processa no background
4. O banco é atualizado após o processamento

---

# 🧠 Arquitetura

A arquitetura é dividida em microserviços simples:

### **1. FastAPI (Web)**

* Recebe requisições HTTP
* Executa operações rápidas no banco
* Para tarefas pesadas → envia mensagem ao RabbitMQ

---

### **2. RabbitMQ**

Fila usada para:

* Processamento de cargas de funcionários
* Integrações com sistemas externos
* Garantir que a API nunca trave

---

### **3. Worker**

Processo separado que:

* Escuta a fila `benefits_queue`
* Processa dados sem bloquear a API
* Grava no banco

---

### **4. PostgreSQL**

Onde ficam:

* empresas
* funcionários
* benefícios
* histórico de cargas

---

# 🧪 Exemplos de Requisição (via cURL)

## Criar empresa

```bash
curl -X POST http://localhost:8000/companies \
  -H "Content-Type: application/json" \
  -d '{"name": "Empresa XPTO"}'
```

## Criar funcionário

```bash
curl -X POST http://localhost:8000/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Paulo", "company_id": 1}'
```

## Criar benefício

```bash
curl -X POST http://localhost:8000/benefits \
  -H "Content-Type: application/json" \
  -d '{"name": "Vale Alimentação"}'
```

## Enviar carga (vai para o RabbitMQ)

```bash
curl -X POST http://localhost:8000/load \
  -H "Content-Type: application/json" \
  -d '{"file_path": "dados.csv"}'
```

---

# 🛠 Tecnologias Utilizadas

* **FastAPI**
* **PostgreSQL**
* **RabbitMQ**
* **Psycopg2**
* **Pika**
* **Docker**
* **Docker Compose**
* **Python 3.11**

---

# 📘 Objetivo do Projeto

Este projeto foi criado para demonstrar:

✔ Arquitetura moderna usando fila
✔ Worker assíncrono para operações pesadas
✔ API limpa e bem estruturada
✔ SQL puro (sem ORM)
✔ Conexão robusta com Postgres
✔ Comunicação entre serviços via Docker


---

# 🙋 Autor

**Paulo**
Desenvolvedor Python / FastAPI
Focado em backend, integrações e sistemas distribuídos.

