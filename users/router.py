from fastapi import APIRouter, HTTPException, Body, Depends
from users.database import login_user, register_user
from models import User, UserCreate
from users.auth import create_access_token, get_current_user

router = APIRouter()


@router.post("/login/")
async def login_user_api(user_data: dict = Body(...)):
    email = user_data.get('email')
    password = user_data.get('password')
    user = await login_user(email, password)
    if user is None:
        return HTTPException(status_code=400, detail="Invalid password or email")

    authentication_token = create_access_token({"sub": user.get('email')})
    return {"status": 200, "access_token": authentication_token, "token_type": "bearer"}


@router.post("/register/")
async def register_user_api(user: UserCreate):
    user = await register_user(user)
    return user


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

