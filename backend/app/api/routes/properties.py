from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.core.security import get_current_user
from app.db.models import Property, PropertyImage, PropertyStatus, User
from app.db.session import get_db
from app.schemas import PropertyCreate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])
settings = get_settings()
ALLOWED_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGES_PER_PROPERTY = 30


def _validate_image_bytes(content_type: str | None, data: bytes) -> str:
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG and WebP images are allowed")
    if content_type == "image/jpeg" and not data.startswith(b"\xff\xd8\xff"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid JPEG")
    if content_type == "image/png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid PNG")
    if content_type == "image/webp" and not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid WebP")
    return ALLOWED_TYPES[content_type]


@router.get("", response_model=list[PropertyOut])
def list_properties(
    q: str | None = Query(default=None, max_length=255),
    property_type: str | None = Query(default=None, max_length=100),
    location: str | None = Query(default=None, max_length=255),
    status: str | None = Query(default="available"),
    featured: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = select(Property).options(selectinload(Property.images)).order_by(Property.created_at.desc(), Property.id.desc())

    if status:
        try:
            status_value = PropertyStatus(status.strip().lower())
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid property status")
        query = query.where(Property.status == status_value)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.where(or_(
            Property.title.ilike(term),
            Property.location.ilike(term),
            Property.property_type.ilike(term),
            Property.description.ilike(term),
        ))
    if property_type and property_type.strip():
        query = query.where(Property.property_type.ilike(f"%{property_type.strip()}%"))
    if location and location.strip():
        query = query.where(Property.location.ilike(f"%{location.strip()}%"))
    if featured is not None:
        query = query.where(Property.featured == featured)

    query = query.offset(skip).limit(limit)
    return list(db.scalars(query).unique().all())


@router.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    image = db.get(PropertyImage, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Property image not found")
    db.delete(image)
    db.commit()


@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(Property).options(selectinload(Property.images)).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    return item


@router.post("", response_model=PropertyOut, status_code=201)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if db.scalar(select(Property).where(Property.slug == payload.slug)):
        raise HTTPException(status_code=409, detail="Slug already exists")
    status_value = PropertyStatus(payload.status)
    item = Property(**payload.model_dump(exclude={"status"}), status=status_value)
    if status_value == PropertyStatus.archived:
        item.featured = False
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Property could not be created because a unique value already exists")
    db.refresh(item)
    return item


@router.patch("/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, payload: PropertyCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.scalar(select(Property).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    duplicate = db.scalar(select(Property).where(Property.slug == payload.slug, Property.id != property_id))
    if duplicate:
        raise HTTPException(status_code=409, detail="Slug already exists")
    status_value = PropertyStatus(payload.status)
    for key, value in payload.model_dump(exclude={"status"}).items():
        setattr(item, key, value)
    item.status = status_value
    if status_value == PropertyStatus.archived:
        item.featured = False
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Property could not be updated because a unique value already exists")
    db.refresh(item)
    return item


@router.delete("/{property_id}", status_code=204)
def archive_property(property_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.get(Property, property_id)
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    item.status = PropertyStatus.archived
    item.featured = False
    db.commit()


@router.post("/{property_id}/images", response_model=PropertyOut)
def attach_image(
    property_id: int,
    url: str = Query(min_length=1, max_length=1000),
    alt_text: str | None = Query(default=None, max_length=255),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.scalar(select(Property).options(selectinload(Property.images)).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    if len(item.images) >= MAX_IMAGES_PER_PROPERTY:
        raise HTTPException(status_code=422, detail=f"A property can have at most {MAX_IMAGES_PER_PROPERTY} images")
    next_order = max((image.sort_order for image in item.images), default=-1) + 1
    db.add(PropertyImage(property_id=property_id, url=url.strip(), alt_text=alt_text.strip() if alt_text else None, sort_order=next_order))
    db.commit()
    db.refresh(item)
    return item


@router.post("/{property_id}/images/upload", response_model=PropertyOut)
async def upload_property_image(
    property_id: int,
    file: UploadFile = File(...),
    alt_text: str | None = Query(default=None, max_length=255),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.scalar(select(Property).options(selectinload(Property.images)).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    if len(item.images) >= MAX_IMAGES_PER_PROPERTY:
        raise HTTPException(status_code=422, detail=f"A property can have at most {MAX_IMAGES_PER_PROPERTY} images")

    data = await file.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller")
    extension = _validate_image_bytes(file.content_type, data)

    from pathlib import Path
    from uuid import uuid4

    directory = Path(settings.upload_dir) / "properties" / str(property_id)
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    path = directory / filename
    path.write_bytes(data)

    next_order = max((image.sort_order for image in item.images), default=-1) + 1
    image = PropertyImage(
        property_id=property_id,
        url=f"/uploads/properties/{property_id}/{filename}",
        alt_text=alt_text.strip() if alt_text else item.title,
        sort_order=next_order,
    )
    db.add(image)
    try:
        db.commit()
    except Exception:
        db.rollback()
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Image could not be saved")
    db.refresh(item)
    return item


@router.post("/{property_id}/images/reorder", response_model=PropertyOut)
def reorder_images(property_id: int, image_ids: list[int], db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.scalar(select(Property).options(selectinload(Property.images)).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    existing_ids = {image.id for image in item.images}
    if set(image_ids) != existing_ids or len(image_ids) != len(existing_ids):
        raise HTTPException(status_code=422, detail="image_ids must contain every image exactly once")
    images_by_id = {image.id: image for image in item.images}
    for order, image_id in enumerate(image_ids):
        images_by_id[image_id].sort_order = order
    db.commit()
    db.refresh(item)
    return item
