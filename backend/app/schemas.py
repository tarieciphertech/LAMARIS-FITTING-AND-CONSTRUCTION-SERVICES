from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
