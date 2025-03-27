import datetime
import uuid
from fastapi import APIRouter, HTTPException, Body, Depends, Request
from users.database import login_user, register_user
from models import User, UserCreate, UserUpdate
from users.auth import create_access_token, get_current_user
import dotenv
import os


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
    special_characters = set("!@#$%^&*()_+=-`~[]\\{}|;':\",./<>?")

    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Make password longer!"
        )
    elif user.password.islower() or user.password.isupper():
        raise HTTPException(
            status_code=400,
            detail="Add the capital or lowercase letters !"
        )
    elif not any(char.isdigit() for char in user.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain numbers"
        )

    elif not any(char in special_characters for char in user.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special symbol"
        )

    user = await register_user(user)
    return user


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/user/profile/")
async def edit_user_profile(user_changes: UserUpdate, current_user: User = Depends(get_current_user)):
    try:
        update_user = user_changes.model_dump(exclude_unset=True)
        for field, value in update_user.items():
            setattr(current_user, field, value)
        await current_user.save()
        return {"status_code": 200, "detail": "Profile changed successfully"}

    except Exception as e:
        print("Internal server error " + str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server exception"
        )


@router.post("/user/request-reset-password")
async def reset_user_password(email: str, request: Request):
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User is not found"
        )

    code = str(uuid.uuid4())[:6]
    user.twofa_code = code
    user.code_expires = datetime.datetime.now() + datetime.timedelta(minutes=10)
    await user.save()


