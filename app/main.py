"""Entry point for the app, run this using uvicorn"""
from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import batch, interactive

load_dotenv('../.env.dev')

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)


@app.get("/")
async def root():
    """TODO: add things here"""
    return {"message": "hi"}
