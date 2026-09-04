from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.security import get_current_admin
from app.db.models import User
from app.services.storage import StorageError, upload_image

router = APIRouter(prefix="/uploads", tags=["uploads"])
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp": ".webp"}
MAX_BYTES = 10 * 1024 * 1024


def validate_image(content_type: str | None, data: bytes) -> None:
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG and WebP images are allowed")
    if content_type == "image/jpeg" and not data.startswith(b"\xff\xd8\xff"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid JPEG")
    if content_type == "image/png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid PNG")
    if content_type == "image/webp" and not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid WebP")


@router.post("/image")
async def upload_image_endpoint(file: UploadFile = File(...), _: User = Depends(get_current_admin)):
    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller")

    validate_image(file.content_type, data)
    public_id = f"lamaris/uploads/{uuid4().hex}"
    try:
        url, storage_key = await upload_image(public_id, data, file.content_type or "application/octet-stream")
    except StorageError as exc:
        raise HTTPException(status_code=502, detail="Image could not be uploaded to Cloudinary") from exc

    return {"url": url, "public_id": storage_key}
