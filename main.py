import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from carts.models import Cart
from users.api.telegram_bot import TelegramBot
import dishes.router
import users.router
import carts.router
from database import connect
import uvicorn
from contextlib import asynccontextmanager
from metadata import tags_metadata
from fastapi.middleware.cors import CORSMiddleware
from models import User
from dishes.models import Dish
from beanie import init_beanie
import dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot
    dotenv.load_dotenv()
    telegram_id = os.getenv("TELEGRAM_BOT_ID")
    bot = TelegramBot(telegram_id)
    await asyncio.create_task(bot.run())
    database = await connect()
    await init_beanie(database=database, document_models=[Dish, User, Cart])
    yield


app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
bot = None

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=dishes.router.router)
app.include_router(router=users.router.router)
app.include_router(router=carts.router.router)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/login", response_class=HTMLResponse)
async def read_root():
    with open("static/login.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/register", response_class=HTMLResponse)
async def read_root():
    with open("static/register.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/cabinet", response_class=HTMLResponse)
async def read_cabinet():
    with open("static/cabinet.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8000)
