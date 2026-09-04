import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROPERTY_STATUSES = {"draft", "available", "sold", "archived"}


class PropertyImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    storage_key: str | None = None
    alt_text: str | None = None
    sort_order: int


class PropertyCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255)
    property_type: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=255)
    price: str | None = Field(default=None, max_length=100)
    bedrooms: int | None = Field(default=None, ge=0)
    rooms: int | None = Field(default=None, ge=0)
    stand_size: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=10000)
    features: str | None = Field(default=None, max_length=10000)
    paperwork_status: str | None = Field(default=None, max_length=255)
    status: str = "draft"
    featured: bool = False

    @field_validator("title", "property_type", "location", mode="before")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Value must not be blank")
        return value.strip()

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        value = value.strip().lower()
        if not SLUG_RE.fullmatch(value):
            raise ValueError("Slug must contain only lowercase letters, numbers and single hyphens")
        return value

    @field_validator("price", "stand_size", "description", "features", "paperwork_status", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in PROPERTY_STATUSES:
            raise ValueError("Invalid property status")
        return value

    @field_validator("featured")
    @classmethod
    def validate_featured(cls, value: bool) -> bool:
        return bool(value)


class PropertyOut(PropertyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    images: list[PropertyImageOut] = Field(default_factory=list)


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


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=12, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if value.strip() != value:
            raise ValueError("Password must not start or end with whitespace")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain a lowercase letter")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain an uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain a number")
        return value
