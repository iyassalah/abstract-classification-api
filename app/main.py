"""Entry point for the app, run this using uvicorn"""
from fastapi import FastAPI

from .routers import batch, interactive

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)


@app.get("/")
async def root():
    """TODO: add things here

    Returns:
        _type_: _description_
    """
    return {"message": "hi"}
