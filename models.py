import re

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class Dish(Document):
    name: str
    price: Indexed(float)
    category: str

    class Settings:
        name = "dishes"


class DishUpdateRequest(BaseModel):
    old_value: str | float
    new_value: str | float
    field: str  # "name", "price", "category"


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
