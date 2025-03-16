from fastapi import FastAPI, HTTPException
from database import (get_dish, get_dishes, connect, add_dish, delete_dish,
                      change_name_dish, change_price_dish, change_category_dish)
from models import Dish
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/dishes")
async def get_dishes_api():
    results = await get_dishes()
    return results


@app.get("/dish/{category}")
async def get_dish_api(category: str):
    results = await get_dish(category)
    return results


@app.post("/add-dish/{name}/{price}/{category}")
async def add_dish_api(name: str, price: float, category: str):
    dish = Dish(name=name, price=price, category=category)
    await add_dish(dish)


@app.delete("/delete-dish/{name}")
async def delete_dish_api(name: str):
    await delete_dish(name)


@app.post("/change-dish/name/{old_name}/{name}")
async def change_dish_api(old_name: str, name: str):
    await change_name_dish(old_name=old_name, name=name)


@app.post("/change-dish/price/{old_price}/{price}")
async def change_dish_api(old_price: float, price: float):
    await change_price_dish(old_price=old_price, price=price)


@app.post("/change-dish/category/{old_category}/{category}")
async def change_dish_api(old_category: str, category: str):
    await change_category_dish(old_category=old_category, category=category)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8080)
