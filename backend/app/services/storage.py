from __future__ import annotations

from pathlib import Path

import httpx

from app.core.config import get_settings

settings = get_settings()


class StorageError(RuntimeError):
    pass


def _object_url(path: str) -> str:
    return f"{settings.supabase_storage_public_base_url}/{path}"


async def upload_image(path: str, data: bytes, content_type: str) -> str:
    """Upload an image to Supabase Storage, or fall back to local storage in dev."""
    if not settings.supabase_storage_enabled:
        local_path = Path(settings.upload_dir) / path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(data)
        return f"/uploads/{path}"

    url = f"{settings.supabase_url.rstrip('/')}/storage/v1/object/{settings.supabase_storage_bucket}/{path}"
    headers = {
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
        "apikey": settings.supabase_service_role_key,
        "Content-Type": content_type,
        "x-upsert": "false",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, content=data, headers=headers)
    if response.status_code not in (200, 201):
        raise StorageError(f"Supabase Storage upload failed ({response.status_code})")
    return _object_url(path)


async def delete_image(url: str) -> None:
    """Delete a stored image. Remote objects are removed from Supabase."""
    if settings.supabase_storage_enabled and url.startswith(settings.supabase_storage_public_base_url + "/"):
        path = url.removeprefix(settings.supabase_storage_public_base_url + "/")
        endpoint = f"{settings.supabase_url.rstrip('/')}/storage/v1/object/{settings.supabase_storage_bucket}"
        headers = {
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
            "apikey": settings.supabase_service_role_key,
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(endpoint, headers=headers, json={"prefixes": [path]})
        if response.status_code not in (200, 204):
            raise StorageError(f"Supabase Storage delete failed ({response.status_code})")
        return

    prefix = "/uploads/"
    if url.startswith(prefix):
        root = Path(settings.upload_dir).resolve()
        candidate = (root / url.removeprefix(prefix)).resolve()
        if candidate.is_file() and root in candidate.parents:
            candidate.unlink()
