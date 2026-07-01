from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserOut(UserBase):
    id: str
    created_at: datetime


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    target_role: str | None = None
    experience_level: str | None = None
    company_target: str | None = None
