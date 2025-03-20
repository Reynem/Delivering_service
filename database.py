from motor.motor_asyncio import AsyncIOMotorClient
import asyncio


async def connect():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    return client["dishesDB"]


if __name__ == "__main__":
    asyncio.run(connect())
