from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from dishes.models import Dish


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


async def change_dish(old_value: str | float, new_value: str | float, category: str):
    dish = await Dish.find_one(Dish.category == old_value)
    if not dish:
        raise ValueError(f"Dish with '{category}' {old_value} not found")

    await dish.update({"$set": {category: new_value}})


if __name__ == "__main__":
    asyncio.run(connect())
