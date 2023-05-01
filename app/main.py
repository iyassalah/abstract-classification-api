"""Entry point for the app, run this using uvicorn"""
from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import batch, interactive
from fastapi.middleware.cors import CORSMiddleware

load_dotenv('../.env.dev')

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)

#just to be able to send the request in the same machine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """TODO: add things here"""
    return {"message": "hi"}
