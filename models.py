from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, UTC


class Admin(Document):
    username: str
    password: str
    is_active: bool = True
    created_at: datetime = Field(datetime.now())
    updated_at: Optional[datetime] = None

    class Settings:
        name = "admins"

    @classmethod
    async def get_admin(cls, username: str) -> Optional["Admin"]:
        return await cls.find_one({"username": username, "is_active": True})

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(tz=UTC)
        await super().save(*args, **kwargs)
        

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
