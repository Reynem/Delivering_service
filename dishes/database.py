from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from models import Dish


async def connect():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    return client["dishesDB"]


async def get_dishes():
    result = await Dish.find({}).to_list()
    return result


async def get_dish(category: str):
    result = await Dish.find({"category": category}).to_list()
    return result


async def add_dish(dish: Dish):
    await dish.create()


async def delete_dish(name: str):
    await Dish.find_one(Dish.name == name).delete()


async def change_name_dish(old_name: str, name: str):
    dish = await Dish.find_one(Dish.name == old_name)
    if not dish:
        raise ValueError(f"Dish with name '{old_name}' not found")

    await dish.update({"$set": {"name": name}})


async def change_price_dish(old_price: float, price: float):
    dish = await Dish.find_one(Dish.price == old_price)
    if not dish:
        raise ValueError(f"Dish with price '{old_price}' not found")

    await dish.update({"$set": {"price": price}})


async def change_category_dish(old_category: str, category: str):
    dish = await Dish.find_one(Dish.category == old_category)
    if not dish:
        raise ValueError(f"Dish with category '{old_category}' not found")

    await dish.update({"$set": {"category": category}})


if __name__ == "__main__":
    asyncio.run(connect())
