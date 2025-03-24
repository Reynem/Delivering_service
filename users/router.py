from fastapi import APIRouter, HTTPException, Body
from users.database import login_user, register_user
from models import User, UserCreate

router = APIRouter()


@router.post("/login/")
async def login_user_api(user_data: dict = Body(...)):
    email = user_data.get('email')
    password = user_data.get('password')
    user = await login_user(email, password)
    if user is None:
        return HTTPException(status_code=400, detail="Invalid password or email")
    return {"status": 200}


@router.post("/register/")
async def register_user_api(user: UserCreate):
    user = await register_user(user)
    return user
