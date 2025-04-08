from fastapi import HTTPException
from pydantic import EmailStr

from carts.models import Cart


async def add_cart_item(cart: Cart):
    try:
        user_item = await Cart.find_one(Cart.user_email == cart.user_email, Cart.dish_name == cart.dish_name)
        if user_item:
            user_item.quantity += cart.quantity
            await user_item.save()
            return {"status": 200, "detail": "Items updated"}
        await cart.save()
        return {"status": 200, "detail": "New items added"}
    except Exception as e:
        raise HTTPException(400, str(e))


async def show_cart(user_email: EmailStr):
    try:
        cart_items = await Cart.find(Cart.user_email == user_email).to_list()
        if not cart_items:
            raise HTTPException(404, "No items in cart")
        total_price = sum(item.price * item.quantity for item in cart_items)
        return {"status": "OK", "items": cart_items, "total_price": total_price}
    except Exception as e:
        raise HTTPException(400, str(e))


async def cart_delete(user_email: EmailStr, dish_name: str, quantity: float):
    try:
        client_cart = await Cart.find(Cart.user_email == user_email, Cart.dish_name == dish_name).to_list()
        if not client_cart:
            raise HTTPException(400, "No such item in cart")

        for _ in range(min(int(quantity), len(client_cart))):
            await client_cart.pop(0).delete()
    except Exception as e:
        raise HTTPException(404, str(e))


async def cart_clear(user_email: EmailStr):
    try:
        client_cart = await Cart.find(Cart.user_email == user_email).count()
        if client_cart == 0:
            raise HTTPException(400, "No items in cart")
        await Cart.delete_many(Cart.user_email == user_email)
    except Exception as e:
        raise HTTPException(400, str(e))


async def cart_update(user_email: EmailStr, dish_name, quantity: float):
    try:
        client_cart = await Cart.find_one(Cart.user_email == user_email, Cart.dish_name == dish_name)
        if not client_cart:
            raise HTTPException(400, "No such item in cart")
        if client_cart.quantity + quantity <= 0:
            await client_cart.delete()
            return {"status": 200, "detail": "Item successfully removed from cart"}
        client_cart.quantity += quantity
        await client_cart.save_changes()

    except Exception as e:
        raise HTTPException(404, str(e))