from __future__ import annotations

import asyncio
from io import BytesIO

import cloudinary
from cloudinary import uploader

from app.core.config import get_settings

settings = get_settings()


class StorageError(RuntimeError):
    pass


def _configure() -> None:
    if not settings.cloudinary_enabled:
        raise StorageError("Cloudinary storage is not configured")
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


def _validate_public_id(public_id: str) -> str:
    public_id = public_id.strip().strip("/")
    if not public_id:
        raise StorageError("Invalid Cloudinary public ID")
    if ".." in public_id.split("/"):
        raise StorageError("Invalid Cloudinary public ID")
    if not public_id.startswith("lamaris/"):
        raise StorageError("Invalid Cloudinary public ID")
    return public_id


def _upload_sync(public_id: str, data: bytes, content_type: str) -> tuple[str, str]:
    _configure()
    result = uploader.upload(
        BytesIO(data),
        public_id=public_id,
        asset_folder="/".join(public_id.split("/")[:-1]),
        resource_type="image",
        overwrite=False,
        unique_filename=False,
        use_filename=False,
        invalidate=True,
    )
    secure_url = result.get("secure_url")
    returned_public_id = result.get("public_id")
    if not secure_url or not returned_public_id:
        raise StorageError("Cloudinary upload returned an incomplete response")
    return secure_url, returned_public_id


async def upload_image(public_id: str, data: bytes, content_type: str) -> tuple[str, str]:
    """Upload an image to Cloudinary and return (secure_url, public_id)."""
    public_id = _validate_public_id(public_id)
    try:
        return await asyncio.to_thread(_upload_sync, public_id, data, content_type)
    except StorageError:
        raise
    except Exception as exc:
        raise StorageError("Cloudinary upload failed") from exc


def _delete_sync(public_id: str) -> None:
    _configure()
    result = uploader.destroy(
        public_id,
        resource_type="image",
        type="upload",
        invalidate=True,
    )
    if result.get("result") not in {"ok", "not found"}:
        raise StorageError(f"Cloudinary delete failed: {result.get('result', 'unknown error')}")


async def delete_image(public_id: str) -> None:
    """Delete one image from Cloudinary by its stored public ID."""
    public_id = _validate_public_id(public_id)
    try:
        await asyncio.to_thread(_delete_sync, public_id)
    except StorageError:
        raise
    except Exception as exc:
        raise StorageError("Cloudinary delete failed") from exc
