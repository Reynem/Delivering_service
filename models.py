from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from typing import Optional


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
    name: str
    password_hash: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

    class Settings:
        name = "Users"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None
