from fastapi import APIRouter, HTTPException
from users.database import login_user, register_user
from models import User, UserCreate

router = APIRouter()


@router.get("/user/login/{email}/{password}")
async def login_user_api(email: str, password: str):
    user = await login_user(email, password)
    if user is None:
        return HTTPException(status_code=400, detail="Invalid password or email")
    return {"status": 200}


@router.post("/user/register/")
async def register_user_api(user: UserCreate):
    user = await register_user(user)
    return user
