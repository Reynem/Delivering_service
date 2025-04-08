from fastapi.routing import APIRouter
from pydantic import EmailStr

from carts.models import Cart
from carts.database import (add_cart_item, show_cart, cart_clear, cart_delete)


router = APIRouter()


@router.post('/api/cart/add')
async def add_cart_item_api(cart: Cart):
    await add_cart_item(cart)


@router.get('/api/cart/{user_email}')
async def get_cart_items_api(user_email: EmailStr):
    await show_cart(user_email)


@router.delete('/api/cart/clear/{user_email}')
async def clear_cart_items_api(user_email: EmailStr):
    await cart_clear(user_email)


@router.post('/api/cart/remove/{user_email}/{dish_name}/{quantity}')
async def remove_cart_item_api(user_email: EmailStr, dish_name: str, quantity: float):
    await cart_delete(user_email, dish_name, quantity)


