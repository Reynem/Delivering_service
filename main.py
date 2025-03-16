from fastapi import FastAPI, HTTPException

from database import (get_dish, get_dishes, connect, add_dish, delete_dish,
                      change_name_dish, change_price_dish, change_category_dish)
from models import Dish
import uvicorn
from contextlib import asynccontextmanager
from models import DishUpdateRequest
from metadata import tags_metadata
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield


app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/dishes", tags=["dishes"], summary="Get all dishes")
async def get_dishes_api():
    results = await get_dishes()
    return results


@app.get("/dish/{category}", tags=["dishes"], summary="Get dish by category")
async def get_dish_api(category: str):
    results = await get_dish(category)
    return results


@app.post("/add-dish/{name}/{price}/{category}", tags=["dishes"], summary="Add a new dish")
async def add_dish_api(name: str, price: float, category: str):
    dish = Dish(name=name, price=price, category=category)
    await add_dish(dish)


@app.delete("/delete-dish/{name}", tags=["dishes"], summary="Delete a dish by name")
async def delete_dish_api(name: str):
    await delete_dish(name)


@app.post("/change-dish/", tags=["dishes"], summary="Change dish details")
async def change_dish_api(request: DishUpdateRequest):
    if request.field == "name":
        await change_name_dish(request.old_value, request.new_value)
    elif request.field == "price":
        await change_price_dish(float(request.old_value), float(request.new_value))
    elif request.field == "category":
        await change_category_dish(request.old_value, request.new_value)
    else:
        raise ValueError("Invalid field")


# Legacy methods:


@app.post("/change-dish/name/{old_name}/{name}", tags=["legacy"])
async def change_dish_api(old_name: str, name: str):
    await change_name_dish(old_name=old_name, name=name)


@app.post("/change-dish/price/{old_price}/{price}", tags=["legacy"])
async def change_dish_api(old_price: float, price: float):
    await change_price_dish(old_price=old_price, price=price)


@app.post("/change-dish/category/{old_category}/{category}", tags=["legacy"])
async def change_dish_api(old_category: str, category: str):
    await change_category_dish(old_category=old_category, category=category)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8080)
