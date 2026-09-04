# Lamaris API

FastAPI backend for the Lamaris Real Estate & Construction platform.

## Architecture

`React/Vite frontend → FastAPI REST API → SQLAlchemy → PostgreSQL`

Property media is stored in **Cloudinary**. The database stores the Cloudinary secure URL and public ID for each gallery image.

The database schema is managed with **Alembic**. The API does not create or alter tables during application startup.

## Local setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `DATABASE_URL`, generate a strong `JWT_SECRET`, and configure the three Cloudinary environment variables.

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
- `20260904_0004` — Cloudinary public ID storage for property images

## Property persistence

Core PostgreSQL tables:

- `users` — authenticated admin accounts, roles and JWT token versions
- `properties` — durable listings, lifecycle status, pricing/details and timestamps
- `property_images` — ordered galleries linked to properties with Cloudinary storage metadata
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
- `POST /api/properties/{id}/images/upload` — admin upload and persist an image to Cloudinary
- `POST /api/properties/{id}/images/reorder` — admin reorder gallery
- `DELETE /api/properties/images/{image_id}` — admin remove an image from Cloudinary and PostgreSQL

Direct external image URL attachment is intentionally disabled so property galleries remain under application-controlled Cloudinary storage.

Validation includes non-blank required fields, normalized lowercase slugs, supported status values, non-negative bedroom/room counts, image MIME/signature checks, a 10 MB image limit and a 30-image-per-property limit.

## Image storage

Cloudinary is the production and application storage provider. Property images use the namespace `lamaris/properties/{property_id}/{generated_id}`. Each upload uses a unique public ID, `overwrite=false`, and stores the returned secure URL and public ID in PostgreSQL.

The API validates image type and signature before upload. Uploads write to Cloudinary before the database record is committed; if the database write fails, the uploaded Cloudinary asset is deleted. Image deletion keeps the database transaction pending until the Cloudinary deletion succeeds, so a storage failure rolls the DB deletion back.

Cloudinary credentials are server-side only and must never be exposed to the frontend.

## Production rule

Do not put production database credentials, JWT secrets or Cloudinary credentials in Git. Configure them through deployment environment variables or a secrets manager.
