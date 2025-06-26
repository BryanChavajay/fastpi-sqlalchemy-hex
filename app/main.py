from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hola_mundo():
    return {"Hola": "Mundo"}
