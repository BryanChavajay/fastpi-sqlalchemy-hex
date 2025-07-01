from fastapi import FastAPI

from app.routers.main import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
def hola_mundo():
    return {"Hola": "Mundo"}
