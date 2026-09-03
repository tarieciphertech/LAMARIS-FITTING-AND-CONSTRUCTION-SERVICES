# Lamaris API

FastAPI backend for the Lamaris Real Estate & Construction platform.

## Architecture

`React/Vite frontend → FastAPI REST API → SQLAlchemy → PostgreSQL`

The database schema is managed with **Alembic**. The API no longer creates or alters tables during application startup.

## Local setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `DATABASE_URL` to a PostgreSQL database and generate a strong `JWT_SECRET`.

Apply the schema:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/api/health`

## Database workflow

Create a migration after changing ORM models:

```bash
alembic revision --autogenerate -m "describe the schema change"
```

Review the generated migration before applying it:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

## Current core tables

- `users` — admin accounts and JWT token versions
- `properties` — property listings and status
- `property_images` — ordered property galleries
- `enquiries` — website/property enquiries

Property lifecycle:

`draft → available → sold / archived`

The public API should expose available listings by default. Admin operations require authenticated JWT access.

## Production rule

Do not put production database credentials or JWT secrets in Git. Configure them through the deployment environment/secrets manager.
