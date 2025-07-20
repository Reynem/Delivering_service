from fastapi import HTTPException
from pydantic import EmailStr

from carts.models import Cart, CartIn
from dishes.models import Dish


async def add_cart_item(cart_in: CartIn, user_email: EmailStr):
    try:
        dish = await Dish.find_one(Dish.name == cart_in.dish_name)
        if not dish:
            raise HTTPException(400, "Dish not found")

        user_item = await Cart.find_one(Cart.user_email == user_email, Cart.dish_id == dish.id)

        if user_item:
            user_item.quantity += cart_in.quantity
            await user_item.save_changes()
            return {"status": 200, "detail": "Items updated"}

        new_cart_item = Cart(user_email=user_email, dish_id=dish.id, quantity=cart_in.quantity)
        await new_cart_item.save()
        return {"status": 200, "detail": "New items added"}
    except Exception as e:
        raise HTTPException(400, str(e))


async def show_cart(user_email: EmailStr):
    try:
        cart_items_db = await Cart.find(Cart.user_email == user_email).to_list()

        if not cart_items_db:
            return {"status": "OK", "items": [], "total_price": 0}

        populated_cart_items = []
        total_price = 0.0

        for item_in_cart in cart_items_db:
            dish = await Dish.find_one(Dish.id == item_in_cart.dish_id)
            if dish:
                populated_cart_items.append({
                    "dish_id": str(item_in_cart.dish_id),
                    "dish_name": dish.name,
                    "price": dish.price,
                    "category": dish.category,
                    "quantity": item_in_cart.quantity
                })
                total_price += dish.price * item_in_cart.quantity
            else:
                print(f"Warning: Dish with ID {item_in_cart.dish_id} not found for user {user_email}'s cart.")

        return {"status": "OK", "items": populated_cart_items, "total_price": total_price}
    except Exception as e:
        print(f"Error in show_cart: {e}")
        raise HTTPException(500, "Failed to retrieve cart")


async def cart_delete(user_email: EmailStr, dish_name: str, quantity: int):
    try:
        dish = await Dish.find_one(Dish.name == dish_name)
        if not dish:
            raise HTTPException(400, "Dish not found")

        client_item = await Cart.find_one(Cart.user_email == user_email, Cart.dish_id == dish.id)

        if not client_item:
            raise HTTPException(400, "No such item in cart")

        upd_quantity = client_item.quantity - quantity

        if upd_quantity > 0:
            client_item.quantity = upd_quantity
            await client_item.save_changes()
        else:
            await client_item.delete()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"An error occurred: {str(e)}")


async def cart_clear(user_email: EmailStr):
    try:
        result = await Cart.find(Cart.user_email == user_email).delete()

        if result.deleted_count == 0:
            raise HTTPException(400, "No items in cart to clear")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Failed to clear cart: {str(e)}")


async def cart_update(user_email: EmailStr, dish_name: str, quantity: int):
    try:
        dish = await Dish.find_one(Dish.name == dish_name)
        if not dish:
            raise HTTPException(400, "Dish not found")

        client_cart_item = await Cart.find_one(Cart.user_email == user_email, Cart.dish_id == dish.id)
        if not client_cart_item:
            raise HTTPException(400, "No such item in cart")

        if client_cart_item.quantity + quantity <= 0:
            await client_cart_item.delete()
            return {"status": 200, "detail": "Item successfully removed from cart"}

        client_cart_item.quantity += quantity
        await client_cart_item.save_changes()
        return {"status": 200, "detail": "Item quantity updated"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Failed to update cart item: {str(e)}")
