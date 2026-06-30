# NL2SQL BankBot

A production-quality AI chatbot whose knowledge is stored in a structured PostgreSQL database. Instead of retrieving answers from documents, the chatbot answers questions by converting natural language into structured queries and searching relational data directly.

---

## How It Works

```
User Question
      │
      ▼
FastAPI (REST API)
      │
      ▼
Groq LLM — converts question to structured JSON
      │
      ▼
{"entity": "bank", "fact": "home_loan", "attribute": "interest_rate"}
      │
      ▼
SQLAlchemy + PostgreSQL — retrieves the value
      │
      ▼
Groq LLM — converts value to natural language
      │
      ▼
"The home loan interest rate is 8.5%."
```

---

## Technology Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| uv | Fast dependency management |
| FastAPI | REST API framework |
| Groq API (Llama 3.3) | Natural language understanding and response generation |
| PostgreSQL 16 | Structured knowledge database |
| PostgreSQL LTREE | Hierarchical path queries |
| SQLAlchemy 2.0 | ORM and database sessions |
| Alembic | Database migration and version control |
| psycopg 3 | PostgreSQL driver |
| Pydantic v2 | Request/response validation |
| Docker + Docker Compose | Containerized infrastructure |
| pytest | Automated testing |

---

## Project Structure

```
nl2sql-bankbot/
├── app/
│   ├── main.py                        # FastAPI entry point
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py                # POST /chat endpoint
│   │       └── health.py              # GET /health endpoint
│   ├── core/
│   │   └── config.py                  # Centralized settings via pydantic-settings
│   ├── db/
│   │   ├── database.py                # Engine + session management
│   │   ├── migrations/                # Alembic migration files
│   │   ├── models/
│   │   │   ├── base.py                # SQLAlchemy DeclarativeBase
│   │   │   └── entity.py              # Entity, Attribute, EntityValue ORM models
│   │   └── repositories/
│   │       └── entity_repository.py   # All database query functions
│   ├── schemas/
│   │   └── chat.py                    # Pydantic request/response schemas
│   └── services/
│       ├── llm_service.py             # Groq API client
│       ├── query_service.py           # Natural language → structured JSON
│       ├── search_service.py          # JSON → PostgreSQL search
│       └── response_service.py        # DB result → natural language
├── docker/
│   └── Dockerfile                     # FastAPI production image
├── sql/
│   ├── schema/
│   │   ├── 00_init.sql                # LTREE extension setup
│   │   └── 01_create_tables.sql       # EAV table definitions
│   └── seed/
│       └── 01_seed_data.sql           # Sample bank data
├── tests/
│   ├── conftest.py                    # Shared pytest fixtures
│   ├── unit/
│   │   ├── test_database.py           # Database connection and ORM tests
│   │   ├── test_repository.py         # Repository function tests
│   │   └── test_services.py           # Service layer tests
│   └── integration/
│       └── test_api.py                # Full API endpoint tests
├── chat.py                            # Terminal chat interface
├── docker-compose.yml                 # Orchestrates postgres + api services
├── pyproject.toml                     # Project dependencies
├── uv.lock                            # Locked dependency versions
├── .env.example                       # Environment variable template
└── alembic.ini                        # Alembic configuration
```

---

## Database Design (EAV Model)

The chatbot uses an **Entity-Attribute-Value (EAV)** pattern with three tables and LTREE for hierarchical path queries.

### entity
Stores entities and their facts.

| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| entity_name | VARCHAR(100) | e.g. `bank` |
| fact | VARCHAR(100) | e.g. `home_loan` |
| created_at | TIMESTAMPTZ | Auto-set on insert |

### attribute
Stores attribute types.

| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| label | VARCHAR(100) | e.g. `interest_rate` |
| created_at | TIMESTAMPTZ | Auto-set on insert |

### entity_value
Links entity + attribute + value with an LTREE path.

| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| entity_id | INTEGER | Foreign key → entity |
| attribute_id | INTEGER | Foreign key → attribute |
| path_name | LTREE | e.g. `bank.home_loan.interest_rate` |
| value | TEXT | e.g. `8.5` |
| type | VARCHAR(20) | `string`, `numeric`, `boolean`, `date` |
| created_at | TIMESTAMPTZ | Auto-set on insert |

### Sample Data

The database includes these bank facts:

| Fact | Attributes |
|---|---|
| central_bank | address, email, phone, website, manager |
| home_loan | interest_rate, loan_amount, tenure, processing_fee, collateral |
| main_branch | address, email, phone, manager, website |
| saving_account | interest_rate, minimum_balance, maximum_balance |
| fixed_deposit | interest_rate, minimum_balance, tenure |
| sub_branch | address, email, phone, manager |
| personal_loan | interest_rate, loan_amount, tenure, processing_fee, collateral, loan_type |
| vehicle_loan | interest_rate, loan_amount, tenure, processing_fee, collateral, loan_type |

---

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- A Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone and Configure

```bash
git clone <your-repo-url>
cd nl2sql-bankbot
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 2. Install Dependencies

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Start PostgreSQL

```bash
docker compose up -d postgres
```

> PostgreSQL is exposed on **host port 5433** (mapped to container port 5432) to avoid conflicts with any local PostgreSQL installation. Make sure `POSTGRES_PORT=5433` in your `.env`.

### 4. Run Database Migrations and Seed Data

```bash
# Apply schema
docker exec -i chatbot_postgres psql -U chatbot_user -d chatbot_db \
  < sql/schema/00_init.sql

docker exec -i chatbot_postgres psql -U chatbot_user -d chatbot_db \
  < sql/schema/01_create_tables.sql

# Insert sample data
docker exec -i chatbot_postgres psql -U chatbot_user -d chatbot_db \
  < sql/seed/01_seed_data.sql

# Apply Alembic migrations
uv run alembic upgrade head
```

### 5. Start the API

```bash
uv run uvicorn app.main:app --reload --port 8001
```

Visit:
- **http://localhost:8001/health** — health check
- **http://localhost:8001/docs** — interactive Swagger UI

---

## Running with Docker (Full Stack)

Run everything in Docker with a single command:

```bash
docker compose up --build
```

This starts:
- `chatbot_postgres` — PostgreSQL on port 5433
- `chatbot_api` — FastAPI on port 8000

Check status:

```bash
docker compose ps
```

Stop everything:

```bash
docker compose down
```

---

## API Endpoints

### `GET /health`

Returns the health status of the app and database.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "app": "NL2SQL BankBot",
  "env": "production",
  "database": "connected"
}
```

### `POST /chat`

Accepts a natural language question and returns a natural language answer.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the home loan interest rate?"}'
```

Response:
```json
{
  "question": "What is the home loan interest rate?",
  "answer": "The home loan interest rate is 8.5%.",
  "success": true,
  "query": {
    "entity": "bank",
    "fact": "home_loan",
    "attribute": "interest_rate"
  },
  "data": {
    "value": "8.5",
    "type": "numeric",
    "path_name": "bank.home_loan.interest_rate",
    "formatted_value": "8.5%"
  }
}
```

---

## Terminal Chat Interface

For quick testing without curl, use the interactive terminal chat:

```bash
uv run python chat.py
```

> SQL query logging is disabled (`echo=False` in `database.py`) so the terminal output stays clean — only the conversation is shown.

```
==================================================
   NL2SQL BankBot — Terminal Chat
==================================================
Ask me anything about the bank!
Type 'exit' or 'quit' to stop.
==================================================

You: What is the home loan interest rate?
Bot: The home loan interest rate is 8.5%.

You: Who is the manager of the main branch?
Bot: The manager is Ram Prasad Sharma.

You: exit
Bot: Goodbye! Have a great day.
```

---

## Database Queries

Connect to the database:

```bash
docker exec -it chatbot_postgres psql -U chatbot_user -d chatbot_db
```

> This connects from inside the Docker network, so the container's internal port 5432 is used directly — no need to reference the host-mapped port 5433 here.

View individual tables directly:

```bash
docker exec -it chatbot_postgres psql -U chatbot_user -d chatbot_db
```

```sql
SELECT * FROM entity;
SELECT * FROM attribute;
SELECT * FROM entity_value;
```

View all data with human-readable names:

```sql
SELECT
    e.entity_name,
    e.fact,
    a.label AS attribute,
    ev.value,
    ev.type,
    ev.path_name
FROM entity_value ev
JOIN entity e ON e.id = ev.entity_id
JOIN attribute a ON a.id = ev.attribute_id
ORDER BY e.fact, a.label;
```

Search by LTREE path:

```sql
SELECT path_name, value, type
FROM entity_value
WHERE path_name <@ 'bank.home_loan';
```

---

## Running Tests

```bash
uv run pytest tests/ -v
```

The test suite includes 33 tests covering:
- Database connection and ORM models
- Repository query functions
- Service layer logic (query parsing, value formatting)
- Full API endpoint integration tests

---

## Development Phases Completed

| Phase | Description | Status |
|---|---|---|
| 1 | Project initialization with uv | ✅ |
| 2 | Docker setup with PostgreSQL | ✅ |
| 3 | PostgreSQL + LTREE extension setup | ✅ |
| 4 | EAV database schema design | ✅ |
| 5 | Sample bank data seeding | ✅ |
| 6 | Alembic migration configuration | ✅ |
| 7 | SQLAlchemy ORM models | ✅ |
| 8 | Repository layer | ✅ |
| 9 | Groq LLM integration | ✅ |
| 10 | Query understanding (NL → JSON) | ✅ |
| 11 | Database search (JSON → PostgreSQL) | ✅ |
| 12 | Response generation (DB result → NL) | ✅ |
| 13 | FastAPI REST endpoints | ✅ |
| 14 | Automated testing (33 tests) | ✅ |
| 15 | Full Docker Compose deployment | ✅ |
| 16 | Final architecture review | ⏳ Pending |

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | Application name | `NL2SQL BankBot` |
| `APP_ENV` | Environment (development/production) | `development` |
| `DEBUG` | Enable FastAPI debug mode | `true` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5433` |
| `POSTGRES_DB` | Database name | `chatbot_db` |
| `POSTGRES_USER` | Database user | `chatbot_user` |
| `POSTGRES_PASSWORD` | Database password | `chatbot_pass` |
| `GROQ_API_KEY` | Groq API key (required) | — |
| `GROQ_MODEL` | Groq model to use | `llama-3.3-70b-versatile` |

