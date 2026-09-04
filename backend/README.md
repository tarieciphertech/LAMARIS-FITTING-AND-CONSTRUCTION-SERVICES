# Lamaris API

FastAPI backend for the Lamaris Real Estate & Construction platform.

## Architecture

`React/Vite frontend → FastAPI REST API → SQLAlchemy → PostgreSQL`

The database schema is managed with **Alembic**. The API does not create or alter tables during application startup.

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

Run the automated backend suite:

```bash
python -m pytest -q
```

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

Current migrations:

- `20260903_0001` — safe baseline for existing MVP databases
- `20260903_0002` — property/image integrity constraints and indexes
- `20260903_0003` — explicit user roles for admin authorization

## Property persistence

Core PostgreSQL tables:

- `users` — authenticated admin accounts, roles and JWT token versions
- `properties` — durable listings, lifecycle status, pricing/details and timestamps
- `property_images` — ordered galleries linked to properties with cascading deletes
- `enquiries` — website/property enquiries

Property lifecycle:

`draft → available → sold / archived`

Property management endpoints are admin-only. Public reads expose available listings by default.

### Property API

- `GET /api/properties` — public listing/search/filter
- `GET /api/properties/{id}` — public property detail
- `POST /api/properties` — admin create
- `PATCH /api/properties/{id}` — admin update
- `DELETE /api/properties/{id}` — admin archive (non-destructive)
- `POST /api/properties/{id}/images` — admin attach an existing URL
- `POST /api/properties/{id}/images/upload` — admin upload and persist an image
- `POST /api/properties/{id}/images/reorder` — admin reorder gallery
- `DELETE /api/properties/images/{image_id}` — admin remove an image

Validation includes non-blank required fields, normalized lowercase slugs, supported status values, non-negative bedroom/room counts, image MIME/signature checks, a 10 MB image limit and a 30-image-per-property limit.

## Image storage

Development uses the configured `UPLOAD_DIR` filesystem. Production uses the `property-images` Supabase Storage bucket through the server-only service-role key. Property objects use the `properties/{property_id}/{generated_filename}` namespace.

The database stores the public object URL and gallery order. Uploads write to Storage before the database record is committed; if the database write fails, the uploaded object is cleaned up. Image deletion keeps the database transaction pending until the Storage deletion succeeds, so a Storage failure rolls the DB deletion back.

The production configuration deliberately fails fast when `ENVIRONMENT=production` but `DATABASE_URL`, `JWT_SECRET`, `SUPABASE_URL`, or `SUPABASE_SERVICE_ROLE_KEY` is missing.

## Production rule

Do not put production database credentials, JWT secrets or storage credentials in Git. Configure them through deployment environment variables or a secrets manager.
