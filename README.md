# my-hobby

개인 취미 프로젝트 — Python FastAPI 웹 서비스

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLAlchemy (async) + Alembic for migrations
- **Validation**: Pydantic v2

## Project Structure

```
my-hobby/
├── app/
│   ├── main.py            # FastAPI app entrypoint
│   ├── config.py           # Settings and environment config
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic request/response schemas
│   ├── routers/            # API route handlers
│   ├── services/           # Business logic layer
│   ├── repositories/       # Database access layer
│   └── dependencies.py     # Dependency injection (DB session, auth, etc.)
├── alembic/                # Database migration files
├── tests/                  # Test files mirroring app/ structure
├── alembic.ini
├── requirements.txt
└── .env
```

## Build & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# Run all tests
pytest

# Run a single test file
pytest tests/test_example.py

# Run a specific test
pytest tests/test_example.py::test_function_name -v

# Database migrations
alembic upgrade head          # Apply all migrations
alembic revision --autogenerate -m "description"  # Create new migration
alembic downgrade -1          # Rollback last migration

# Linting
ruff check .
ruff format .
```

## API Docs

When the dev server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

- **Routers** handle HTTP concerns (request parsing, response formatting, status codes)
- **Services** contain business logic and orchestrate between repositories
- **Repositories** handle all database queries via SQLAlchemy
- **Schemas** define API contracts using Pydantic models, separate from ORM models
- Dependencies are injected via FastAPI's `Depends()` mechanism
