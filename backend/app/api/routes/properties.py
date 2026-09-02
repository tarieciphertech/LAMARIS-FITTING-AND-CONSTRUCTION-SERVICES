from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_current_user
from app.db.models import Property, PropertyImage, PropertyStatus, User
from app.db.session import get_db
from app.schemas import PropertyCreate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", response_model=list[PropertyOut])
def list_properties(
    property_type: str | None = None,
    location: str | None = None,
    status: str = "available",
    featured: bool | None = None,
    db: Session = Depends(get_db),
):
    query = select(Property).options(selectinload(Property.images)).order_by(Property.created_at.desc())
    if status:
        query = query.where(Property.status == status)
    if property_type:
        query = query.where(Property.property_type.ilike(f"%{property_type}%"))
    if location:
        query = query.where(Property.location.ilike(f"%{location}%"))
    if featured is not None:
        query = query.where(Property.featured == featured)
    return list(db.scalars(query).unique().all())


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
    item = db.get(Property, property_id)
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    try:
        status_value = PropertyStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid property status")
    for key, value in payload.model_dump(exclude={"status"}).items():
        setattr(item, key, value)
    item.status = status_value
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
def attach_image(property_id: int, url: str, alt_text: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.scalar(select(Property).options(selectinload(Property.images)).where(Property.id == property_id))
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    next_order = max((image.sort_order for image in item.images), default=-1) + 1
    db.add(PropertyImage(property_id=property_id, url=url, alt_text=alt_text, sort_order=next_order))
    db.commit()
    db.refresh(item)
    return item
