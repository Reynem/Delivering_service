import datetime
import uuid
from fastapi import APIRouter, HTTPException, Body, Depends, Request
from users.database import login_user, register_user
from models import User, UserCreate, UserUpdate
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


@router.post("/user/telegram/request-link")
async def request_telegram_link(request: Request, current_user: User = Depends(get_current_user)):
    code = str(uuid.uuid4())[:8]
    current_user.twofa_code = code
    current_user.code_expires = datetime.datetime.now() + datetime.timedelta(minutes=15)
    await current_user.save()
    return {"temp_token": code}


@router.post("/user/telegram/link")
async def reset_password_api(data: dict = Body(...)):
    temp_token = data.get("temp_token")
    chat_id = data.get("chat_id")
    if not temp_token or not chat_id:
        print("token or id is missing")
        raise HTTPException(404, "Token or id is missing")

    user = await User.find_one(User.twofa_code == temp_token)
    if not user:
        print("inappropriate token")
        raise HTTPException(404, "Inappropriate token")
    if datetime.datetime.now() > user.code_expires:
        raise HTTPException(400, "The token has expired")

    user.telegram_id = chat_id
    user.twofa_code = None
    user.code_expires = None
    await user.save()

    return {"status": "Telegram account linked successfully"}


@router.get("/users/me/telegram")
async def get_user_telegram_status(current_user: User = Depends(get_current_user)):
    return {"telegram_id": current_user.telegram_id}
