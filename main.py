from fastapi import FastAPI
import uvicorn

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8080)