from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.models import Enquiry, Property, User
from app.db.session import get_db
from app.schemas import EnquiryCreate, EnquiryOut

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


@router.post("", response_model=EnquiryOut, status_code=201)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    if payload.property_id and not db.get(Property, payload.property_id):
        raise HTTPException(status_code=404, detail="Property not found")
    item = Enquiry(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[EnquiryOut])
def list_enquiries(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list(db.scalars(select(Enquiry).order_by(Enquiry.created_at.desc())).all())


@router.patch("/{enquiry_id}/status", response_model=EnquiryOut)
def update_enquiry_status(enquiry_id: int, status: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.get(Enquiry, enquiry_id)
    if not item:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    item.status = status
    db.commit()
    db.refresh(item)
    return item
