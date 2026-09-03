from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_current_user
from app.db.models import Property, PropertyImage, PropertyStatus, User
from app.db.session import get_db
from app.schemas import PropertyCreate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


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
        if status not in {item.value for item in PropertyStatus}:
            raise HTTPException(status_code=422, detail="Invalid property status")
        query = query.where(Property.status == status)
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


# Static image routes must be declared before /{property_id} so "images" is not parsed as an integer.
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
    try:
        status_value = PropertyStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid property status")
    item = Property(**payload.model_dump(exclude={"status"}), status=status_value)
    db.add(item)
    db.commit()
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
    try:
        status_value = PropertyStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid property status")
    for key, value in payload.model_dump(exclude={"status"}).items():
        setattr(item, key, value)
    item.status = status_value
    if status_value == PropertyStatus.archived:
        item.featured = False
    db.commit()
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
    next_order = max((image.sort_order for image in item.images), default=-1) + 1
    db.add(PropertyImage(property_id=property_id, url=url, alt_text=alt_text, sort_order=next_order))
    db.commit()
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
