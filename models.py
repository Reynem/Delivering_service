
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Admin(Document):
    username: str
    password: str
    is_active: bool = True
    created_at: datetime = Field(datetime.now())
    updated_at: Optional[datetime] = None

    class Settings:
        name = "admins"


# Users:


class User(Document):
    name: Optional[str] = None
    password_hash: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    telegram_id: Optional[int] = None
    twofa_code: Optional[str] = None
    code_expires: Optional[datetime] = None

    class Settings:
        name = "Users"


class UserCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
