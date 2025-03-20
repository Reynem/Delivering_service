from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from models import Dish


async def connect():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    await init_beanie(database=client["dishesDB"], document_models=[Dish])


if __name__ == "__main__":
    asyncio.run(connect())
