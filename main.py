from fastapi import FastAPI

import dishes.router
from database import connect
import uvicorn
from contextlib import asynccontextmanager
from metadata import tags_metadata
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield


app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=dishes.router.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8000)
