from fastapi import APIRouter

from dishes.database import (get_dish, get_dishes, add_dish, delete_dish,
                             change_dish)
from dishes.models import Dish
from dishes.models import DishUpdateRequest

router = APIRouter()


@router.get("/dishes/", tags=["dishes"], summary="Get all dishes")
async def get_dishes_api():
    results = await get_dishes()
    return results


@router.get("api/dish/{category}", tags=["dishes"], summary="Get dish by category")
async def get_dish_api(category: str):
    results = await get_dish(category)
    return results


@router.post("/api/add-dish", tags=["dishes"], summary="Add a new dish")
async def add_dish_api(dish: Dish):
    await add_dish(dish)


@router.delete("/api/delete-dish/{name}", tags=["dishes"], summary="Delete a dish by name")
async def delete_dish_api(name: str):
    await delete_dish(name)


@router.post("/change-dish/", tags=["dishes"], summary="Change dish details")
async def change_dish_api(request: DishUpdateRequest):
    try:
        await change_dish(request.old_value, request.new_value, request.field)
    except Exception as e:
        raise ValueError(str(e))
