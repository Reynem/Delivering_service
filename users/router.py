from fastapi import APIRouter, HTTPException, Body, Depends
from users.database import login_user, register_user
from models import User, UserCreate
from users.auth import create_access_token, get_current_user

router = APIRouter()


@router.post("/login/")
async def login_user_api(user_data: dict = Body(...)):
    try:
        email = user_data.get('email')
        password = user_data.get('password')
        user = await login_user(email, password)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid password or email")
        if not hasattr(user, 'email'):
            raise HTTPException(status_code=500, detail="User object is invalid")
        authentication_token = create_access_token({"sub": user.email})
        print(f"[DEBUG] Generated token for {user.email}: {authentication_token}")

        return {
            "access_token": authentication_token,
            "token_type": "bearer"
        }

    except Exception as e:
        print(f"[ERROR] Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register/")
async def register_user_api(user: UserCreate):
    user = await register_user(user)
    return user


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

