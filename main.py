from fastapi import FastAPI
from database import get_dish, get_dishes, connect
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


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8080)
