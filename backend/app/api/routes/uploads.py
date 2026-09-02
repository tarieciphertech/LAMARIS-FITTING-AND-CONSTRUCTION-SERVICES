from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.core.security import get_current_user
from app.db.models import User

router = APIRouter(prefix="/uploads", tags=["uploads"])
settings = get_settings()
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024


@router.post("/image")
async def upload_image(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG and WebP images are allowed")

    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller")

    extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[file.content_type]
    directory = Path(settings.upload_dir)
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    path = directory / filename
    path.write_bytes(data)

    return {"url": f"/uploads/{filename}", "filename": filename}
