import datetime

from fastapi import Query, Depends, Body
from fastapi.routing import APIRouter
from users.auth import get_current_user
from carts.models import Cart, CartIn
from carts.database import (add_cart_item, show_cart, cart_clear, cart_delete,
                            cart_update)
import logging
from logging.config import dictConfig
import sys


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ"
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        }
    },
    "handlers": {
        "console": {
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "orders.log",
            "maxBytes": 10485760,
            "backupCount": 3
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger("app")

router = APIRouter()


@router.post('/api/cart/add', status_code=200)
async def add_cart_item_api(cart_in: CartIn = Body(...),
                            user=Depends(get_current_user)):
    cart = Cart(
        user_email=user.email,
        dish_name=cart_in.dish_name,
        price=cart_in.price,
        category=cart_in.category,
        quantity=cart_in.quantity
    )
    await add_cart_item(cart)
    return {"status": "OK", "message": "Item added to cart"}


@router.get('/api/cart/', status_code=200)
async def get_cart_items_api(user=Depends(get_current_user)):
    return await show_cart(user.email)


@router.delete('/api/cart/clear/', status_code=200)
async def clear_cart_items_api(user=Depends(get_current_user)):
    await cart_clear(user.email)
    return {"status": "OK", "message": "Cart was cleared"}


@router.delete('/api/cart/remove/{dish_name}/', status_code=200)
async def remove_cart_item_api(
        dish_name: str,
        quantity: float = Query(1.0, gt=0, description="Quantity to remove"),
        user=Depends(get_current_user)
):
    await cart_delete(user.email, dish_name, quantity)
    return {"status": "OK", "message": "Item removed from the cart"}


@router.put('/api/cart/update/{dish_name}/', status_code=200)
async def update_cart_item_api(
        dish_name: str,
        quantity: float = Query(1.0, description="Quantity to update(negatives are allowed)"),
        user=Depends(get_current_user)
):
    await cart_update(user.email, dish_name, quantity)
    return {"status": "OK", "message": f"{dish_name}`s quantity changed by {quantity}"}


@router.post('/api/orders/create', status_code=200)
async def create_order_api(user=Depends(get_current_user)):
    logger.info(f"Order creation started for {user.email}")

    try:
        cart_items = await show_cart(user.email)
        logger.debug(f"Raw cart data: {cart_items}")

        items = cart_items.get("items")

        order_data = {
            "user_email": user.email,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "items": [
                {
                    "dish_name": item.dish_name,
                    "quantity": item.quantity,
                    "price": item.price
                } for item in items
            ],
            "total_price": cart_items.get("total_price")
        }

        logger.info({
            "order": {
                "user": user.email,
                "total_price": order_data["total_price"],
                "item_count": len(order_data["items"]),
                "dishes": [item["dish_name"] for item in order_data["items"]]
            }
        })

        return {"status": "OK", "message": "Заказ успешно создан"}

    except Exception as e:
        logger.error(f"Order failed: {str(e)}", exc_info=True)
        return {"status": "error", "message": "Internal server error"}
