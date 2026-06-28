cat > README.md << 'EOF'
# AI Chatbot

A production-quality AI chatbot powered by:
- **FastAPI** — REST API layer
- **Groq LLM** — Natural language understanding
- **PostgreSQL** — Structured knowledge base (EAV model)
- **SQLAlchemy + Alembic** — ORM and database migrations
- **Docker** — Containerized infrastructure
- **uv** — Fast Python dependency management

## Quick Start

```bash
cp .env.example .env
# Edit .env with your credentials
uv sync
uv run uvicorn app.main:app --reload
```

## Project Structure

See docs for full architecture diagram.
EOF