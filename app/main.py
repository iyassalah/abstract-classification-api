from fastapi import FastAPI

from .routers import batch, interactive

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)


@app.get("/")
async def root():
    return {"message": "hi"}
