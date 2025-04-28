import os
from typing import Dict, Any
from string import digits, ascii_letters, punctuation
from secrets import choice
from fastapi import HTTPException
import httpx

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


async def verify_google_token(id_token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": id_token}
            )
            if response.status_code != 200:
                raise HTTPException(400, "Invalid ID token")
            id_info: Dict[str, Any] = response.json()
            if id_info["aud"] != GOOGLE_CLIENT_ID:
                raise HTTPException(400, "Invalid audience")
            return id_info

    except Exception as e:
        return HTTPException(200, str(e))


def generate_secure_password(length: int = 16) -> str:
    if length < 8:  # For unpredictable issues
        raise ValueError("Too short password!")

    characters = ascii_letters + digits + punctuation
    password = ''.join(choice(characters) for _ in range(length))
    return password
