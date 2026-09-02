from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PropertyImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    alt_text: str | None = None
    sort_order: int


class PropertyCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255)
    property_type: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=255)
    price: str | None = None
    bedrooms: int | None = Field(default=None, ge=0)
    rooms: int | None = Field(default=None, ge=0)
    stand_size: str | None = None
    description: str | None = None
    features: str | None = None
    paperwork_status: str | None = None
    status: str = "draft"
    featured: bool = False


class PropertyOut(PropertyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    images: list[PropertyImageOut] = []


class EnquiryCreate(BaseModel):
    property_id: int | None = None
    name: str = Field(min_length=2, max_length=255)
    phone: str = Field(min_length=5, max_length=50)
    email: str | None = None
    message: str = Field(min_length=2)


class EnquiryOut(EnquiryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    must_change_password: bool
