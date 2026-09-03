from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.core.security import get_current_admin
from app.db.models import User

router = APIRouter(prefix="/uploads", tags=["uploads"])
settings = get_settings()
ALLOWED_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_BYTES = 10 * 1024 * 1024


def validate_image(content_type: str | None, data: bytes) -> str:
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG and WebP images are allowed")
    if content_type == "image/jpeg" and not data.startswith(b"\xff\xd8\xff"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid JPEG")
    if content_type == "image/png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid PNG")
    if content_type == "image/webp" and not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid WebP")
    return ALLOWED_TYPES[content_type]


@router.post("/image")
async def upload_image(file: UploadFile = File(...), _: User = Depends(get_current_admin)):
    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller")

    extension = validate_image(file.content_type, data)
    directory = Path(settings.upload_dir)
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    path = directory / filename
    path.write_bytes(data)

    return {"url": f"/uploads/{filename}", "filename": filename}
