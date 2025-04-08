from fastapi import Query, Depends
from fastapi.routing import APIRouter
from pydantic import EmailStr
from users.auth import get_current_user
from carts.models import Cart
from carts.database import (add_cart_item, show_cart, cart_clear, cart_delete,
                            cart_update)


router = APIRouter()


@router.post('/api/cart/add', status_code=200)
async def add_cart_item_api(cart: Cart):
    await add_cart_item(cart)
    return {"status": "OK", "message": "Item added to cart"}


@router.get('/api/cart/', status_code=200)
async def get_cart_items_api(user=Depends(get_current_user)):
    await show_cart(user.email)
    return {"status": "OK", "message": "Cart items were shown"}


@router.delete('/api/cart/clear/', status_code=200)
async def clear_cart_items_api(user=Depends(get_current_user)):
    await cart_clear(user.email)
    return {"status": "OK", "message": "Cart was cleared"}


@router.delete('/api/cart/remove/{dish_name}/{quantity}', status_code=200)
async def remove_cart_item_api(
        dish_name: str,
        quantity: float = Query(1.0, gt=0, description="Quantity to remove"),
        user=Depends(get_current_user)
):
    await cart_delete(user.email, dish_name, quantity)
    return {"status": "OK", "message": "Item removed from the cart"}


@router.put('/api/cart/update/{dish_name}/{quantity}', status_code=200)
async def update_cart_item_api(
        dish_name: str,
        quantity: float = Query(1.0, description="Quantity to update(negatives are allowed)"),
        user=Depends(get_current_user)
):
    await cart_update(user.email, dish_name, quantity)
    return {"status": "OK", "message": f"{dish_name}`s quantity changed by {quantity}"}
