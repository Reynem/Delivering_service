from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from models import User, UserCreate
from fastapi import HTTPException
from users.encryption import hash_password, verify_password


async def connect():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    return client["dishesDB"]


async def login_user(email: str, password: str):
    user = await User.find_one(User.email == email)
    if user and verify_password(password, user.password_hash):
        return user
    return None


async def register_user(user: UserCreate):
    try:
        db_user = await User.find_one(User.email == user.email)
        password_hash = hash_password(user.password)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=password_hash,
            address=user.address,
            phone=user.phone
        )
        await new_user.create()
        return {"message": "User registered successfully", "user_id": str(new_user.id)}
    except Exception as e:
        print("Registration error: " + str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal Server error"
        )


if __name__ == "__main__":
    asyncio.run(connect())
