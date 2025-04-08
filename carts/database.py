from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from pydantic import EmailStr

from carts.models import Cart


async def add_cart_item(cart: Cart):
    try:
        return await cart.save()
    except Exception as e:
        raise HTTPException(400, str(e))


async def show_cart(user_email: EmailStr):
    try:
        return await Cart.find(Cart.user_email == user_email).to_list()
    except Exception as e:
        raise HTTPException(400, str(e))


async def cart_delete(user_email: EmailStr, dish_name: str, quantity: float):
    try:
        client_cart = Cart.find(Cart.user_email == user_email, Cart.dish_name == dish_name)
        if not client_cart:
            raise HTTPException(400, "No items in cart")
        for i in range(int(quantity)):
            await client_cart.delete()
    except Exception as e:
        raise HTTPException(404, str(e))


async def cart_clear(user_email: EmailStr):
    try:
        client_cart = Cart.find(Cart.user_email == user_email)
        if not client_cart:
            raise HTTPException(400, "No items in cart")
        await client_cart.delete_many()
    except Exception as e:
        raise HTTPException(400, str(e))


async def cart_update(user_email: EmailStr, dish_name, quantity: float):
    try:
        client_cart = await Cart.find_one(Cart.user_email == user_email, Cart.dish_name == dish_name)
        if not client_cart:
            raise HTTPException(400, "No items in cart")
        client_cart.quantity += quantity
        await client_cart.save()
        return {"status_code": 200, "detail": "Number changed successfully"}

    except Exception as e:
        raise HTTPException(404, str(e))