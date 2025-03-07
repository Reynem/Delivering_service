from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import Document, Indexed, init_beanie
from models import Dish


async def connect():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    await init_beanie(database=client["dishesDB"], document_models=[Dish])


async def get_dishes():
    result = await Dish.find({}).to_list()
    print(result)
    return result


async def get_dish(category: str):
    result = await Dish.find({"category": category}).to_list()
    return result


if __name__ == "__main__":
    asyncio.run(connect())
